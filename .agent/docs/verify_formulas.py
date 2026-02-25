
import gspread
from oauth2client.service_account import ServiceAccountCredentials

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
SHEET_ID = "1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY"

def verify_dashboard():
    print("Connecting to Google Sheets...")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)

    ws_dash = sh.worksheet("Dashboard")
    
    # Get all values including formulas
    data = ws_dash.get('A1:J13', value_render_option='FORMULA')
    
    print("\n--- HEADER ---")
    print(f"Date Cell (B1): {data[0][1]}")
    print(f"Accuracy Formula (D1): {data[0][3]}")
    
    print("\n--- FIRST ROW (PH01 OIL) Formulas ---")
    ph01_oil_row = data[3]
    if len(ph01_oil_row) >= 10:
        print(f"Slot: {ph01_oil_row[0]}")
        print(f"Top 1: {ph01_oil_row[2]}")
        print(f"Top 2: {ph01_oil_row[3]}")
        print(f"Top 3: {ph01_oil_row[4]}")
        print(f"Top 4: {ph01_oil_row[5]}")
        print(f"Top 5: {ph01_oil_row[6]}")
        print(f"Top 6: {ph01_oil_row[7]}")
        print(f"Match Formula: {ph01_oil_row[9]}")
    else:
        print("Row incomplete", ph01_oil_row)
        
    print("\n--- LAST ROW (PH05 GHEE) Formulas ---")
    ph05_ghee_row = data[12]
    if len(ph05_ghee_row) >= 10:
        print(f"Slot: {ph05_ghee_row[0]}")
        print(f"Top 1: {ph05_ghee_row[2]}")
        print(f"Top 6: {ph05_ghee_row[7]}")
        print(f"Match Formula: {ph05_ghee_row[9]}")

if __name__ == '__main__':
    verify_dashboard()
