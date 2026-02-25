
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time

# Configuration
JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
CSV_FILE = r"C:\Users\Administrator\Documents\Logistics_AI_Final_Release\Master_History_2019_2025.csv"
SHEET_ID = "1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY"

def upload_to_sheets():
    print("Connecting to Google Sheets Cloud...")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    
    # Open sheet
    sh = client.open_by_key(SHEET_ID)
    ws = sh.get_worksheet(0) # Sheet1
    
    print(f"Reading Master History: {CSV_FILE}")
    df = pd.read_csv(CSV_FILE)
    df = df.fillna("")
    
    # Header + Data
    data = [df.columns.tolist()] + df.values.tolist()
    
    print(f"Uploading {len(data)} rows to Cloud...")
    
    # Clear and update
    ws.clear()
    
    # Update in chunks if necessary, but 2500 rows should be fine for update
    ws.update('A1', data)
    
    print("✅ CLOUD SYNC COMPLETE: 2019-2025 Data is LIVE in Google Sheets.")

if __name__ == "__main__":
    try:
        upload_to_sheets()
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
