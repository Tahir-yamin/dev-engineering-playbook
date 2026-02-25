import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import warnings
import datetime
import os

warnings.simplefilter('ignore')

EXCEL_FILE = r"C:\Users\USER\Documents\Logistics_AI_Final_Release\Logistics_AI_Production_Master.xlsm"
SHEET_ID = 'YOUR_SHEET_ID'
JSON_KEY = r"C:\Users\USER\Documents\mcp-sheets-key.json"

def sync_actuals():
    print("🔄 Initializing Auto-Sync from Local Excel to Cloud...")
    
    # 1. Read Local Excel
    try:
        df_local = pd.read_excel(EXCEL_FILE, sheet_name='LiveData')
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return

    # 2. Clean Local Data (Extract the 11 key columns)
    # The columns in LiveData are: Date, Day, PH01 OIL, PH01 GHEE...
    # We need: Date, PH01 OIL, PH01 GHEE, PH02 OIL, PH02 GHEE, PH03 OIL, PH03 GHEE, PH04 OIL, PH04 GHEE, PH05 OIL, PH05 GHEE
    
    expected_cols = ['Date', 'PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE']
    
    available_cols = [c for c in expected_cols if c in df_local.columns]
    if len(available_cols) < 11:
        print(f"⚠️ Warning: Some columns missing in Excel. Found: {available_cols}")
        
    df_clean = df_local[available_cols].copy()
    
    # Drop rows where Date is completely missing or empty
    df_clean = df_clean.dropna(subset=['Date'])
    
    # Format Date to string YYYY-MM-DD
    df_clean['Date'] = pd.to_datetime(df_clean['Date']).dt.strftime('%Y-%m-%d')
    df_clean = df_clean.fillna("")
    
    # 3. Connect to Google Sheets
    print("☁️ Connecting to Google Sheets Matrix...")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)
    ws = sh.worksheet("Sheet1")
    
    # 4. Get current Cloud Data
    cloud_data = ws.get_all_values()
    if not cloud_data:
        print("❌ Cloud Sheet1 is completely empty. Needs headers.")
        return
        
    cloud_dates = [row[0] for row in cloud_data[1:] if row[0].strip() != ""]
    
    # 5. Find missing dates
    rows_to_append = []
    
    for i, row in df_clean.iterrows():
        d = row['Date']
        # Only upload if it's a valid date and NOT already in the cloud
        if pd.notna(d) and d != "" and d not in cloud_dates:
            # Check if actual data exists for this row (not just empty strings)
            row_data = row.tolist()
            if any(val != "" for val in row_data[1:]): 
                rows_to_append.append(row_data)
                
    if rows_to_append:
        print(f"🚀 Found {len(rows_to_append)} new Days of Actuals! Uploading to Cloud...")
        ws.append_rows(rows_to_append, value_input_option='USER_ENTERED')
        print(f"✅ SUCCESS! Cloud memory is now locked in sync with your Excel.")
    else:
        print("✅ Cloud is already 100% up-to-date with your Excel. No new actuals found.")

if __name__ == "__main__":
    sync_actuals()
