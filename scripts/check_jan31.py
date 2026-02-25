import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import sys
from train_cloud_model import predict_bayesian_markov

JSON_KEY = r'C:\Users\USER\Documents\mcp-sheets-key.json'
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
client = gspread.authorize(creds)
sh = client.open_by_key('YOUR_SHEET_ID')
ws = sh.worksheet('Sheet1')

data = ws.get_all_records()
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])
df.to_csv('d:/my-dev-knowledge-base/scripts/live_data_cache_fresh.csv', index=False)

target_date = pd.to_datetime('2026-01-31')
actuals = df[df['Date'] == target_date]

SLOTS = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]

if len(actuals) > 0:
    target_str = target_date.strftime('%Y-%m-%d')
    print(f'Testing exact Kaggle weights (0.2 Bayes, 0.0 Markov, 0.8 Global) for: {target_str}')
    print(f'Length of history available before this date: {len(df[df["Date"] < target_date])}')
    
    matches = 0
    total = 0
    for s in SLOTS:
        actual = str(actuals.iloc[0][s]).strip().split(',')[0]
        if not actual or actual == '' or actual == '-': 
            continue
            
        preds = predict_bayesian_markov(df, s, target_date)
        match = 'PASS' if actual in preds else 'FAIL'
        if match == 'PASS': 
            matches += 1
        total += 1
        print(f'{s} - Actual: {actual}, Preds: {preds} -> {match}')
        
    print(f'Actual Accuracy for {target_str}: {matches} / {total} ({(matches/total)*100:.2f}% if total > 0)')
else:
    print('Still no actual data for Jan 31 in Sheet1?? Did you add it to your local Excel but not the Google Sheet?')
