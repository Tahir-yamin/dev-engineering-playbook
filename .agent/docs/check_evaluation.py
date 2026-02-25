
import gspread
from oauth2client.service_account import ServiceAccountCredentials

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
SHEET_ID = "1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY"

def verify_dash_output():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)

    ws_dash = sh.worksheet("Dashboard")
    
    # Get all EVALUATED values
    data = ws_dash.get('A4:H4', value_render_option='FORMATTED_VALUE')
    print("PH01 OIL Evaluated Data:", data)

if __name__ == '__main__':
    verify_dash_output()
