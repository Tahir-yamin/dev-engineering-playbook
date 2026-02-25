
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
SHEET_ID = "1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY"

def check_predictions():
    print("Connecting to Google Sheets...")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)

    ws_pred = sh.worksheet("ML_Predictions_Cloud")
    
    # Get all values
    data = ws_pred.get_all_values()
    if not data:
        print("ML_Predictions_Cloud is empty!")
        return

    df = pd.DataFrame(data[1:], columns=data[0])
    print(f"Total rows in predictions: {len(df)}")
    if len(df) > 0:
        print("First 5 dates in predictions:")
        print(df['Forecast_Date'].head(5).tolist())
        
        # Check specifically for 2026-01-01
        is_jan1 = df[df['Forecast_Date'] == '2026-01-01']
        if not is_jan1.empty:
            print("\nFound 2026-01-01! Data:")
            print(is_jan1.iloc[0].to_dict())
        else:
            print("\n2026-01-01 is NOT found in Forecast_Date column.")
            print("Wait, let's see what the actual format is. First row Forecast_Date:", df.iloc[0]['Forecast_Date'])

if __name__ == '__main__':
    check_predictions()
