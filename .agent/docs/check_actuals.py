
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
SHEET_ID = "1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY"

def check_dashboard_actuals():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)

    ws_dash = sh.worksheet("Dashboard")
    ws_actuals = sh.worksheet("Sheet1")
    
    # Check if user entered anything in B4:B13 on the Dashboard
    actuals = ws_dash.get('B4:B13')
    date_val = ws_dash.get('B1')[0][0]
    
    print(f"Current Dashboard Date: {date_val}")
    print(f"User entered actuals: {actuals}")
    
    # Check what is at the bottom of the master dataset "Sheet1"
    raw_data = ws_actuals.get_all_values()
    df = pd.DataFrame(raw_data[1:], columns=raw_data[0])
    print(f"\nLast 3 fully recorded entries in the actual history (Sheet1):")
    print(df.tail(3).to_string())

if __name__ == '__main__':
    check_dashboard_actuals()
