
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
SHEET_ID = "1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY"
SLOTS = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]

def check_january_accuracy():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)

    df_actuals = pd.DataFrame(sh.worksheet("Sheet1").get_all_records())
    df_actuals['Date'] = pd.to_datetime(df_actuals['Date'])
    
    df_preds = pd.DataFrame(sh.worksheet("ML_Predictions_Cloud").get_all_records())
    df_preds['Forecast_Date'] = pd.to_datetime(df_preds['Forecast_Date'])
    
    # Filter actuals to Jan 2026
    actuals_jan = df_actuals[(df_actuals['Date'] >= '2026-01-01') & (df_actuals['Date'] <= '2026-01-11')]
    
    for _, row in actuals_jan.iterrows():
        date = row['Date']
        pred_row = df_preds[df_preds['Forecast_Date'] == date]
        if pred_row.empty: continue
        pred_row = pred_row.iloc[0]
        
        hits = 0
        total = 0
        for s in SLOTS:
            actual = str(row[s]).strip()
            if not actual: continue
            
            p1 = str(pred_row.get(f"{s}_P1", "")).strip()
            p2 = str(pred_row.get(f"{s}_P2", "")).strip()
            p3 = str(pred_row.get(f"{s}_P3", "")).strip()
            p4 = str(pred_row.get(f"{s}_P4", "")).strip()
            p5 = str(pred_row.get(f"{s}_P5", "")).strip()
            p6 = str(pred_row.get(f"{s}_P6", "")).strip()
            
            top6 = [p1, p2, p3, p4, p5, p6]
            if actual in top6:
                hits += 1
            total += 1
            
        print(f"{date.strftime('%Y-%m-%d')} Accuracy: {hits}/{total} ({(hits/total*100) if total > 0 else 0:.1f}%)")

if __name__ == "__main__":
    check_january_accuracy()
