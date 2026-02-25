
import gspread
from oauth2client.service_account import ServiceAccountCredentials

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
SHEET_ID = "1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY"

def setup_dashboard():
    print("Connecting to Google Sheets...")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)

    try:
        ws_dash = sh.worksheet("Dashboard")
        ws_dash.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws_dash = sh.add_worksheet(title="Dashboard", rows="30", cols="15")
        
    print("Building Dashboard UI & Formulas...")
    
    # 1. Headers and Core Info
    ws_dash.update('A1:D1', [["Select Date:", "2026-01-22", "DAILY ACCURACY:", '=COUNTIF(J4:J13, "✅ HIT")/10']])
    
    # 2. Main Table Headers
    headers = [["Slot", "Actual Input", "Top 1", "Top 2", "Top 3", "Top 4", "Top 5", "Top 6", "", "Match Status"]]
    ws_dash.update('A3:J3', headers)
    
    slots = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]
    
    # We will use formulas to pull predictions from ML_Predictions_Cloud
    # Col index in ML_Predictions_Cloud: Date=1. 
    # PH01 OIL P1-P6 are cols 2,3,4,5,6,7
    # PH01 GHEE P1-P6 are cols 8,9,10,11,12,13
    # Concept: VLOOKUP($B$1, 'ML_Predictions_Cloud'!A:BJ, col_index, FALSE)
    
    data = []
    base_col = 2
    for i, s in enumerate(slots):
        row = []
        row.append(s) # A: Slot
        row.append("") # B: Actual Input (User types here)
        
        # C to H: Top 1 to 6 Formulas
        for p in range(6):
            col_idx = base_col + p
            formula = f"=IFNA(VLOOKUP($B$1, ML_Predictions_Cloud!A:BJ, {col_idx}, FALSE), \"-\")"
            row.append(formula)
            
        row.append("") # I: empty spacer
        
        # J: Match Status
        match_formula = f'=IF(B{i+4}="", "-", IF(ISNUMBER(MATCH(B{i+4}, C{i+4}:H{i+4}, 0)), "✅ HIT", "❌ MISS"))'
        row.append(match_formula)
        
        data.append(row)
        base_col += 6
        
    ws_dash.update('A4:J13', data, value_input_option='USER_ENTERED')
    
    # 3. Formatting
    fmt_reqs = [
        {
            "repeatCell": {
                "range": {"sheetId": ws_dash.id, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.1, "green": 0.2, "blue": 0.4},
                        "textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1}, "bold": True, "fontSize": 12},
                        "horizontalAlignment": "CENTER"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": ws_dash.id, "startRowIndex": 2, "endRowIndex": 3, "startColumnIndex": 0, "endColumnIndex": 10},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2},
                        "textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1}, "bold": True},
                        "horizontalAlignment": "CENTER"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
            }
        },
        {
           "repeatCell": {
                "range": {"sheetId": ws_dash.id, "startRowIndex": 3, "endRowIndex": 13, "startColumnIndex": 1, "endColumnIndex": 2},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 1.0, "green": 0.95, "blue": 0.8},
                        "horizontalAlignment": "CENTER",
                        "textFormat": {"bold": True}
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
            } 
        }
    ]
    sh.batch_update({"requests": fmt_reqs})
    
    print("✅ Dashboard fully built in Google Sheets with interactive formulas!")

if __name__ == "__main__":
    setup_dashboard()
