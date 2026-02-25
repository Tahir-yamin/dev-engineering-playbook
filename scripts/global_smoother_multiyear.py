import pandas as pd
from collections import defaultdict, Counter
import warnings
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import time

warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
JSON_KEYFILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', r'C:\Users\USER\Documents\mcp-sheets-key.json')
SHEET_ID = 'YOUR_SHEET_ID'
WEIGHT_180 = 0.15
WEIGHT_30 = 0.25
WEIGHT_7 = 0.40
WEIGHT_SQLY = 0.20

def authenticate_google_sheets():
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    if os.path.exists(JSON_KEYFILE):
        creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE, scopes)
        return gspread.authorize(creds)
    else:
        raise FileNotFoundError("Google Credentials file not found.")

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
        return 0.01  # Extreme Outlier Floor
    elif concentration < 0.70:
        return 0.10  # 10% weight for chaotic days
    else:
        return 1.00  # 100% weight for structured days

def predict_weighted_smoother(df_history, target_date):
    slots = ['PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE']

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

    def get_weighted_counts(temp_df):
        counts = defaultdict(float)
        for _, row in temp_df.iterrows():
            day_weight = get_day_volatility_weight(row, slots)
            for s in slots:
                if s in temp_df.columns:
                    val = row[s]
                    if pd.notna(val) and str(val).strip() != '':
                        counts[str(val).strip()] += (1.0 * day_weight)
        return counts

    counts_180 = get_weighted_counts(df_180)
    counts_30 = get_weighted_counts(df_30)
    counts_7 = get_weighted_counts(df_7)
    counts_sqly = get_weighted_counts(df_sqly)

    all_brands = set(list(counts_180.keys()) + list(counts_30.keys()) + list(counts_7.keys()) + list(counts_sqly.keys()))
    brand_scores = {}
    
    for brand in all_brands:
        score = (counts_180.get(brand, 0) * WEIGHT_180) + \
                (counts_30.get(brand, 0) * WEIGHT_30) + \
                (counts_7.get(brand, 0) * WEIGHT_7) + \
                (counts_sqly.get(brand, 0) * WEIGHT_SQLY)
                
        tie_breaker = 0
        if isinstance(brand, str) and len(brand) > 0:
            char_val = ord(brand.upper()[0])
            tie_breaker = (100 - char_val) / 1000.0
            
        brand_scores[brand] = score + tie_breaker

    sorted_brands = sorted(brand_scores.items(), key=lambda x: x[1], reverse=True)
    top_6 = [brand for brand, score in sorted_brands[:6]]
    
    defaults = ['A', 'B', 'C', 'D', 'E', 'F']
    for db in defaults:
        if len(top_6) < 6 and db not in top_6:
            top_6.append(db)
            
    return top_6

def run_multiyear_backtest():
    print("Initiating 2024-2026 Weighted-Noise Backtest (10% Chaotic Penalty)...")
    
    df = pd.read_csv('d:/my-dev-knowledge-base/scripts/live_data_cache_fresh.csv')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date']).copy()
    
    test_dates = df[(df['Date'] >= '2024-01-01') & (df['Date'] <= '2026-01-31')]['Date'].dt.date.unique()
    
    slots = ['PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE']
    
    results = []
    
    for i, date in enumerate(test_dates):
        current_date_obj = pd.to_datetime(date)
        date_str = str(date)
        
        top_6_weighted = predict_weighted_smoother(df, current_date_obj)
        
        day_df = df[df['Date'].dt.date == date]
        
        day_hits = 0
        day_preds = 0
        
        for _, row in day_df.iterrows():
            for slot in slots:
                actual = row[slot]
                if pd.notna(actual) and str(actual).strip() != '':
                    day_preds += 1
                    if str(actual).strip() in top_6_weighted:
                        day_hits += 1
                        
        if day_preds > 0:
            daily_acc = (day_hits / day_preds)
        else:
            daily_acc = 0.0
            
        pct_formatted = f"{daily_acc * 100:.2f}%"
        # Expand exactly to 10 slots * 6 brands = 60 columns
        row = [date_str, pct_formatted]
        for _ in range(10):  # For all 10 PH slots
            row.extend(top_6_weighted)
            
        results.append(row)
        
        if i % 100 == 0:
            print(f"Processed {i}/{len(test_dates)} dates. Current: {date_str} -> {pct_formatted}")

    print("\nBacktest complete! Preparing Google Sheets upload...")
    
    client = authenticate_google_sheets()
    sh = client.open_by_key(SHEET_ID)
    
    sheet_name = "Cloud_Backtest_24_26"
    try:
        ws = sh.worksheet(sheet_name)
        print(f"Clearing existing {sheet_name} sheet...")
        ws.clear()
    except gspread.exceptions.WorksheetNotFound:
        print(f"Creating new {sheet_name} sheet...")
        ws = sh.add_worksheet(title=sheet_name, rows="1000", cols="65")
        
    # Generate headers for all 10 slots * 6 brands
    headers = ["Date", "Accuracy"]
    for s in slots:
        for rank in range(1, 7):
            headers.append(f"{s}_P{rank}")
    
    upload_data = [headers] + results
    ws.update('A1', upload_data, value_input_option='USER_ENTERED')
    
    print("\n---------------------------------------------------------")
    print(f"UPLOAD SUCCESSFUL! {len(test_dates)} days of 10%-Penalty predictions compiled.")
    print("Full 60-column matrix (10 slots x 6 brands) generated.")
    print(f"Check the '{sheet_name}' tab in your Google Sheet!")
    print("---------------------------------------------------------")

if __name__ == '__main__':
    run_multiyear_backtest()
