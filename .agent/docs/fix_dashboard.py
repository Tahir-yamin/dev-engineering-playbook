
import gspread
from oauth2client.service_account import ServiceAccountCredentials

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
SHEET_ID = "1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY"

def fix_dashboard_vlookup():
    print("Connecting to Google Sheets...")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)

    ws_dash = sh.worksheet("Dashboard")
    
    # 1. Update B1 to be a true date by passing USER_ENTERED
    ws_dash.update('B1', [['2026-01-01']], value_input_option='USER_ENTERED')
    
    slots = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]
    
    data = []
    base_col = 2
    for i, s in enumerate(slots):
        row = []
        row.append(s) # A: Slot
        row.append("") # B: Actual Input (User types here)
        
        # C to H: Top 1 to 6 Formulas
        for p in range(6):
            col_idx = base_col + p
            # FIX: Restore VLOOKUP using exact $B$1 now that it's a real Date. Add DATEVALUE wrapper just in case.
            formula = f'=IFNA(VLOOKUP(IF(ISNUMBER($B$1), $B$1, DATEVALUE($B$1)), ML_Predictions_Cloud!A:BJ, {col_idx}, FALSE), "-")'
            row.append(formula)
            
        row.append("") # I: empty spacer
        
        # J: Match Status
        match_formula = f'=IF(B{i+4}="", "-", IF(ISNUMBER(MATCH(B{i+4}, C{i+4}:H{i+4}, 0)), "✅ HIT", "❌ MISS"))'
        row.append(match_formula)
        
        data.append(row)
        base_col += 6
        
    ws_dash.update('A4:J13', data, value_input_option='USER_ENTERED')
    print("✅ Fixed VLOOKUP formulas and B1 cell typing!")

if __name__ == "__main__":
    fix_dashboard_vlookup()
