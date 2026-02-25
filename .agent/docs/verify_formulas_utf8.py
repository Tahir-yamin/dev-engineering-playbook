
import gspread
from oauth2client.service_account import ServiceAccountCredentials

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
SHEET_ID = "1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY"

def verify_dashboard():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)

    ws_dash = sh.worksheet("Dashboard")
    
    # Get all values including formulas
    data = ws_dash.get('A1:J13', value_render_option='FORMULA')
    
    with open('verify_output_utf8.txt', 'w', encoding='utf-8') as f:
        f.write("--- HEADER ---\n")
        f.write(f"Date Cell (B1): {data[0][1]}\n")
        f.write(f"Accuracy Formula (D1): {data[0][3]}\n")
        
        f.write("\n--- FIRST ROW (PH01 OIL) Formulas ---\n")
        ph01_oil_row = data[3]
        if len(ph01_oil_row) >= 10:
            f.write(f"Slot: {ph01_oil_row[0]}\n")
            f.write(f"Top 1: {ph01_oil_row[2]}\n")
            f.write(f"Top 2: {ph01_oil_row[3]}\n")
            f.write(f"Top 3: {ph01_oil_row[4]}\n")
            f.write(f"Top 4: {ph01_oil_row[5]}\n")
            f.write(f"Top 5: {ph01_oil_row[6]}\n")
            f.write(f"Top 6: {ph01_oil_row[7]}\n")
            f.write(f"Match Formula: {ph01_oil_row[9]}\n")
            
        f.write("\n--- LAST ROW (PH05 GHEE) Formulas ---\n")
        ph05_ghee_row = data[12]
        if len(ph05_ghee_row) >= 10:
            f.write(f"Slot: {ph05_ghee_row[0]}\n")
            f.write(f"Top 1: {ph05_ghee_row[2]}\n")
            f.write(f"Top 6: {ph05_ghee_row[7]}\n")
            f.write(f"Match Formula: {ph05_ghee_row[9]}\n")

if __name__ == '__main__':
    verify_dashboard()
