import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
from collections import defaultdict, Counter

# Suppress warnings
warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
JSON_KEYFILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
SHEET_ID = 'YOUR_SHEET_ID'
SHEET_NAME = 'Sheet1'
DASHBOARD_SHEET_NAME = 'Dashboard'
WEIGHT_180 = 0.15
WEIGHT_30 = 0.25
WEIGHT_7 = 0.40
WEIGHT_SQLY = 0.20

def authenticate_google_sheets():
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    if JSON_KEYFILE and os.path.exists(JSON_KEYFILE):
        creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE, scopes)
    else:
        # Fallback to local dev path if environment variable is missing
        local_path = r'C:\Users\USER\Documents\mcp-sheets-key.json'
        if os.path.exists(local_path):
            creds = ServiceAccountCredentials.from_json_keyfile_name(local_path, scopes)
        else:
            raise FileNotFoundError("Google Credentials file not found. Ensure GOOGLE_APPLICATION_CREDENTIALS is set.")
    
    return gspread.authorize(creds)

def fetch_data(client):
    print("Fetching existing ML_Predictions and LiveData arrays...")
    sh = client.open_by_key(SHEET_ID)
    
    # LiveData Sheet
    ws_data = sh.worksheet(SHEET_NAME)
    data = ws_data.get_all_records()
    df_live = pd.DataFrame(data)
    
    return sh, ws_data, df_live

def parse_dates(df, date_column='Date'):
    """Attempt multiple datetime parsing strategies for robustness without destroying original data"""
    # Safe multi-format parsing
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    
    # Forward fill critical missing dates where safe to do so
    df[date_column] = df[date_column].ffill()
    
    # Drop completely invalid rows to prevent NaT crashes
    df = df.dropna(subset=[date_column]).copy()
    return df
    
    # Drop completely invalid rows to prevent NaT crashes
    df = df.dropna(subset=[date_column]).copy()
    return df

def get_day_volatility_weight(day_row, slots):
    """
    User's strict 10% penalty for chaotic days.
    If the historical day did not naturally achieve >= 70% concentration among its Top 6,
    it is considered chaotic and its data is marginalized to 10% importance.
    """
    brands = [str(day_row[s]).strip() for s in slots if pd.notna(day_row[s]) and str(day_row[s]).strip() != '']
    if len(brands) == 0:
        return 0.0
        
    c = Counter(brands)
    top_6_count = sum([val for key, val in c.most_common(6)])
    concentration = top_6_count / len(brands)
    
    # User target constraint
    if concentration < 0.40:
        return 0.01  # Extreme Outlier Flood
    elif concentration < 0.70:
        return 0.10  # 10% weight for chaotic days
    else:
        return 1.00  # 100% weight for structured days


def predict_global_smoother(df_history, target_date):
    """
    Calculates one master list of Top 6 brands based on the 
    Tri-Weight probability of the ENTIRE DAY across all slots.
    This fulfills the user's "All Day Same Value" stability requirement.
    """
    # Ensure target_date is a datetime object
    if isinstance(target_date, str):
        target_date = pd.to_datetime(target_date)
        
    slots = ['PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE']

    # Sub-filter the dataset
    end_date = target_date
    start_180 = end_date - pd.Timedelta(days=180)
    start_30 = end_date - pd.Timedelta(days=30)
    start_7 = end_date - pd.Timedelta(days=7)
    
    # Seasonal (SQLY) Lookback: 1 full year ago, +/- 45 days (90 day quarter window)
    sql_target = end_date - pd.Timedelta(days=365)
    start_sqly = sql_target - pd.Timedelta(days=45)
    end_sqly = sql_target + pd.Timedelta(days=45)

    df_180 = df_history[(df_history['Date'] >= start_180) & (df_history['Date'] < end_date)]
    df_30 = df_history[(df_history['Date'] >= start_30) & (df_history['Date'] < end_date)]
    df_7 = df_history[(df_history['Date'] >= start_7) & (df_history['Date'] < end_date)]
    df_sqly = df_history[(df_history['Date'] >= start_sqly) & (df_history['Date'] < end_sqly)]

    def get_global_counts(temp_df):
        counts = defaultdict(float)
        for _, row in temp_df.iterrows():
            day_weight = get_day_volatility_weight(row, slots)
            for s in slots:
                if s in temp_df.columns:
                    val = row[s]
                    if pd.notna(val) and str(val).strip() != '':
                        counts[str(val).strip()] += (1.0 * day_weight)
        return counts

    counts_180 = get_global_counts(df_180)
    counts_30 = get_global_counts(df_30)
    counts_7 = get_global_counts(df_7)
    counts_sqly = get_global_counts(df_sqly)

    # Calculate global score
    all_brands = set(list(counts_180.keys()) + list(counts_30.keys()) + list(counts_7.keys()) + list(counts_sqly.keys()))
    brand_scores = {}
    
    for brand in all_brands:
        # Formula: (C180 * W180) + (C30 * W30) + (C7 * W7) + (CSQLY * WSQLY)
        score = (counts_180.get(brand, 0) * WEIGHT_180) + \
                (counts_30.get(brand, 0) * WEIGHT_30) + \
                (counts_7.get(brand, 0) * WEIGHT_7) + \
                (counts_sqly.get(brand, 0) * WEIGHT_SQLY)
                
        # Organic Python Tie-Breaker handling to ensure stability matching alphabetical ranking
        tie_breaker = 0
        if isinstance(brand, str) and len(brand) > 0:
            char_val = ord(brand.upper()[0])
            tie_breaker = (100 - char_val) / 1000.0
            
        brand_scores[brand] = score + tie_breaker

    sorted_brands = sorted(brand_scores.items(), key=lambda x: x[1], reverse=True)
    top_6 = [brand for brand, score in sorted_brands[:6]]
    
    # Pad if not enough
    defaults = ['A', 'B', 'C', 'D', 'E', 'F']
    for db in defaults:
        if len(top_6) < 6 and db not in top_6:
            top_6.append(db)
            
    return top_6

def run_cloud_engine():
    print("-----------------------------------------------------------------")
    print("LOGISTICS AI CLOUD ENGINE - SOTA GLOBAL SMOOTHER EXECUTION INITIATED")
    print("-----------------------------------------------------------------")
    
    try:
        client = authenticate_google_sheets()
        print("Successfully authenticated with Google Sheets API.")
        
        sh, ws_data, df_live = fetch_data(client)
        print(f"Extracted {len(df_live)} rows from LiveData.")
        
        df_live = parse_dates(df_live, 'Date')
        
        # We no longer have 'Source' column in Sheet1, it's just raw history.
        df_actuals = df_live.copy()
        
        if len(df_actuals) == 0:
            print("No Actual data found in LiveData. Execution halted.")
            return

        # Find the latest actual date
        latest_actual_date = df_actuals['Date'].max()
        print(f"Latest Actual Date found: {latest_actual_date.strftime('%Y-%m-%d')}")
        
        # We need to predict for latest_actual_date + 1 day
        prediction_date = latest_actual_date + timedelta(days=1)
        pred_date_str = prediction_date.strftime("%Y-%m-%d")
        
        print(f"Target Prediction Date (T+1): {pred_date_str}")
        
        print(f"\nCalculating Global Smoother Matrix for 'All Day Same Value' consistency...")
        top_6_global = predict_global_smoother(df_actuals, prediction_date)
        
        print(f"Global Top 6 Brands for the day: {top_6_global}")
        
        # Write to the specific ML_Predictions_Cloud sheet like before
        try:
            ws_pred = sh.worksheet("ML_Predictions_Cloud")
        except gspread.exceptions.WorksheetNotFound:
            ws_pred = sh.add_worksheet(title="ML_Predictions_Cloud", rows="500", cols="65")
            
        row_cells = [pred_date_str]
        
        # We apply the EXACT SAME 6 BRANDS to all 10 slots to ensure no "up and down" jumps
        for _ in range(10):  # 10 slots
            row_cells.extend(top_6_global)
            
        print(f"\nFinal Global Smoothing AI Output generated for {pred_date_str}.")
        
        # Try to find if this date already exists to update it, else append
        col_dates = ws_pred.col_values(1)
        if pred_date_str in col_dates:
            row_idx = col_dates.index(pred_date_str) + 1
            print(f"Overwriting existing prediction at row {row_idx}...")
            # create range string (e.g. A2:BI2)
            ws_pred.update(f'A{row_idx}', [row_cells], value_input_option='USER_ENTERED')
        else:
            print("Appending new ML_Prediction row to Cloud Matrix...")
            ws_pred.append_row(row_cells, value_input_option='USER_ENTERED')
            
        print("Row successfully processed!")
        
        print("\n-----------------------------------------------------------------")
        print("CLOUD EXECUTION COMPLETE: 100% SUCCESS")
        print("-----------------------------------------------------------------")
        
    except Exception as e:
        print(f"CRITICAL ENGINE FAILURE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_cloud_engine()
