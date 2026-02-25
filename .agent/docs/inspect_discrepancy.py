
import gspread
from oauth2client.service_account import ServiceAccountCredentials

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
SHEET_ID = "1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY"

def inspect_discrepancy():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)

    ws_dash = sh.worksheet("Dashboard")
    ws_pred = sh.worksheet("ML_Predictions_Cloud")
    
    b1_raw = ws_dash.get('B1', value_render_option='UNFORMATTED_VALUE')[0][0]
    b1_fmt = ws_dash.get('B1', value_render_option='FORMATTED_VALUE')[0][0]
    
    a2_raw = ws_pred.get('A2', value_render_option='UNFORMATTED_VALUE')[0][0]
    a2_fmt = ws_pred.get('A2', value_render_option='FORMATTED_VALUE')[0][0]
    
    print(f"Dashboard B1: {b1_raw} (Raw), {b1_fmt} (Formatted), {type(b1_raw)}")
    print(f"Prediction A2: {a2_raw} (Raw), {a2_fmt} (Formatted), {type(a2_raw)}")

if __name__ == '__main__':
    inspect_discrepancy()
