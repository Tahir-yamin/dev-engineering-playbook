import pandas as pd
import numpy as np
import warnings
import time

warnings.filterwarnings('ignore')

EXCEL_FILE = r'C:\Users\USER\Documents\Logistics_AI_Final_Release\Logistics_AI_Production_Master.xlsm'
SLOT_NAMES = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]

WH = 0.20
WT = 0.30
WM = 0.50

def run_tri_weight_backtest_vectorized():
    print("Loading historical LiveData...", flush=True)
    df = pd.read_excel(EXCEL_FILE, sheet_name='LiveData')
    df = df[['Date'] + SLOT_NAMES].copy()
    df = df.dropna(subset=['Date'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    start_date = pd.to_datetime('2024-07-01')
    end_date = pd.to_datetime('2025-12-31')
    
    test_dates = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]['Date']
    
    print(f"Executing Global-Momentum Tri-Weight Backtest: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    start_time = time.time()
    total_slots = 0
    correct_slots = 0
    
    for t_date in test_dates:
        mask_180 = (df['Date'] < t_date) & (df['Date'] >= t_date - pd.Timedelta(days=180))
        mask_30 = (df['Date'] < t_date) & (df['Date'] >= t_date - pd.Timedelta(days=30))
        mask_7 = (df['Date'] < t_date) & (df['Date'] >= t_date - pd.Timedelta(days=7))
        
        hist_180 = df[mask_180]
        hist_30 = df[mask_30]
        hist_7 = df[mask_7]
        
        if len(hist_180) < 10:
            continue
            
        actual_row = df[df['Date'] == t_date].iloc[0]
        
        # GLOBAL MOMENTUM: Melt all slots for the last 7 days into one giant list
        global_7_data = hist_7[SLOT_NAMES].values.flatten()
        global_7_data = [str(x).strip() for x in global_7_data if pd.notna(x) and str(x).strip() != ""]
        global_c7 = pd.Series(global_7_data).value_counts(normalize=True) if len(global_7_data) > 0 else pd.Series()
        
        for s in SLOT_NAMES:
            actual = actual_row[s]
            if pd.isna(actual) or str(actual).strip() == "": continue
            actual = str(actual).split(',')[0].strip()
            
            # Local History and Trend (Slot-specific)
            s180 = hist_180[s].dropna().replace("", np.nan).dropna()
            s30 = hist_30[s].dropna().replace("", np.nan).dropna()
            
            if len(s180) == 0: continue
            
            c180 = s180.value_counts(normalize=True)
            c30 = s30.value_counts(normalize=True) if len(s30) > 0 else pd.Series()
            
            # Combine Local Hist + Local Trend + GLOBAL Momentum
            brands = set(c180.index).union(c30.index).union(global_c7.index)
            scores = {}
            for b in brands:
                # If a brand has never appeared in THIS slot historically, its probability is 0
                if b not in c180.index:
                    continue
                    
                v180 = c180.get(b, 0.0)
                v30 = c30.get(b, 0.0)
                v7_global = global_c7.get(b, 0.0) # Uses the global frequency across all slots
                
                scores[b] = (v180 * WH) + (v30 * WT) + (v7_global * WM)
                
            top6 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:6]
            top6_list = [b for b, score in top6]
            
            if actual in top6_list:
                correct_slots += 1
            total_slots += 1

    overall_acc = (correct_slots / total_slots) * 100 if total_slots > 0 else 0
    print(f"\n✅ Global-Momentum Tri-Weight Backtest Finished! {time.time() - start_time:.2f} seconds.")
    print(f"Total Organic Accuracy (July 2024 - Dec 2025): {overall_acc:.2f}%")

if __name__ == "__main__":
    run_tri_weight_backtest_vectorized()
