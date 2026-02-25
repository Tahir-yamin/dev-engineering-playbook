
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
NEW_SHEET_ID = "1PjBY8-h7kBYJEXLK1Qp8dFRrWRTNHJ81HfOCSEtOLjE"

def check_new_sheet():
    print("Connecting to Google Sheets...")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    
    try:
        sh = client.open_by_key(NEW_SHEET_ID)
        print("Worksheets:", [ws.title for ws in sh.worksheets()])
        
        all_dfs = []
        for title in ['2019_to_2023', '2024', '2025']:
            ws = sh.worksheet(title)
            data = ws.get_all_values()
            if data:
                df = pd.DataFrame(data[1:], columns=data[0])
                all_dfs.append(df)
                print(f"Tab '{title}' -> Loaded {len(df)} rows. Cols: {df.columns.tolist()}")
                print(df.head(2).to_string())

    except Exception as e:
        print(f"Error accessing sheet: {e}")

if __name__ == "__main__":
    check_new_sheet()
