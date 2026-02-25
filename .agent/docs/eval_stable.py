
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from collections import Counter
import warnings

warnings.simplefilter('ignore')

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
SHEET_ID = '1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY'
SLOTS = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]

def eval_stable_model():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    df = pd.DataFrame(client.open_by_key(SHEET_ID).worksheet("Sheet1").get_all_records())
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Let's see how much we hit in 2025 using just frequency routing!
    train_df = df[df['Date'] < '2025-01-01']
    test_df = df[(df['Date'] >= '2025-01-01') & (df['Date'] < '2026-01-01')]
    
    hits, total = 0, 0
    
    for _, row in test_df.iterrows():
        d = row['Date']
        
        # We look at historical data matching the exact constraint
        # E.g. Same Month & Same Day Of Week
        hist_context = train_df[(train_df['Date'].dt.month == d.month) & (train_df['Date'].dt.dayofweek == d.dayofweek)]
        
        # If too scarce, fallback to just same Month
        if len(hist_context) < 5:
            hist_context = train_df[train_df['Date'].dt.month == d.month]
            
        for s in SLOTS:
            true_val = row[s]
            if not true_val: continue
            
            counts = Counter(hist_context[s])
            # get Top 6
            top6 = [b for b, c in counts.most_common(6) if b]
            
            # If we don't have 6, fill with overall most common
            if len(top6) < 6:
                overall_counts = Counter(train_df[s]).most_common()
                for b, c in overall_counts:
                    if b and b not in top6:
                        top6.append(b)
                    if len(top6) == 6: break
            
            if true_val in top6:
                hits += 1
            total += 1
            
    print(f"Seasonality/Dow Static Model Accuracy for entire 2025: {hits/total*100:.2f}%")

if __name__ == "__main__":
    eval_stable_model()
