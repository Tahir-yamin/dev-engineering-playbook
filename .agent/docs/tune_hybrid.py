
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from collections import Counter
import warnings

warnings.simplefilter('ignore')

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
SHEET_ID = '1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY'
SLOTS = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]

def eval_hybrid_model():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    df = pd.DataFrame(client.open_by_key(SHEET_ID).worksheet("Sheet1").get_all_records())
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Exclude 2026 data
    df = df[df['Date'] < '2026-01-01'].copy()
    
    test_size = 60
    train_df = df.iloc[:-test_size]
    test_df = df.iloc[-test_size:]
    
    hits, total = 0, 0
    
    for _, row in test_df.iterrows():
        d = row['Date']
        
        # Base logic: What happened in the last 30 days?
        recent_30 = train_df.iloc[-30:]
        
        # What happened in this specific month historically over all years?
        historical_month = train_df[train_df['Date'].dt.month == d.month]
        
        for s in SLOTS:
            true_val = row[s]
            if not true_val: continue
            
            # Count recent occurrences (weight heavily)
            recent_counts = Counter(recent_30[s])
            
            # Count historical occurrences for this month
            hist_counts = Counter(historical_month[s])
            
            # Combine scores
            combined = Counter()
            for brand, count in recent_counts.items():
                if brand: combined[brand] += count * 5  # Recent 30 days is worth 5x
            for brand, count in hist_counts.items():
                if brand: combined[brand] += count * 1  # Historical is worth 1x
                
            # Get Top 6 highest scoring brands
            top6 = [b for b, c in combined.most_common(6)]
            
            if true_val in top6:
                hits += 1
            total += 1
            
        # We need to simulate moving forward in time by appending this row to train_df conceptually
        # But for strictly static backtesting the accuracy gap, this is close enough.

    print(f"Hybrid Frequency Model Accuracy on Last 60 Days of 2025: {hits/total*100:.2f}%")

if __name__ == "__main__":
    eval_hybrid_model()
