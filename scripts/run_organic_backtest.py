import pandas as pd
import numpy as np
import warnings
import time
import os
import sys

# Suppress ALL warnings
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'
def warn(*args, **kwargs): pass
warnings.warn = warn

from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.preprocessing import LabelEncoder
from joblib import Parallel, delayed

EXCEL_FILE = r'C:\Users\Administrator\Documents\Logistics_AI_Final_Release\Logistics_AI_Production_Master.xlsm'
SLOT_NAMES = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]
BRANDS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def process_single_combo(x_train_vals, y_train_vals, enc_classes, p1_enc, p7_enc, p14_enc, p30_enc, u3_val, u7_val, dw, m, dy):
    import warnings
    warnings.filterwarnings('ignore')
    
    if len(y_train_vals) < 10:
        freq = pd.Series(y_train_vals).value_counts(normalize=True).to_dict()
        scores = {enc_classes[int(k)]: v for k, v in freq.items() if k in range(len(enc_classes))}
        return scores

    X = np.array(x_train_vals)
    y = np.array(y_train_vals)
    
    xgb = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.08, verbosity=0, random_state=42)
    rf = RandomForestClassifier(n_estimators=50, max_depth=8, min_samples_leaf=2, random_state=42)
    lgb = LGBMClassifier(n_estimators=50, max_depth=6, learning_rate=0.1, verbose=-1, random_state=42)
    
    w = np.ones(len(y))
    w[-min(7, len(w)):] = 5.0
    w[-min(30, len(w)):-min(7, len(w))] = 2.0
    
    xgb.fit(X, y, sample_weight=w)
    rf.fit(X, y, sample_weight=w)
    lgb.fit(X, y, sample_weight=w)
    
    feat = np.array([[dw, m, dy, (1 if dw>=5 else 0), p1_enc, p7_enc, p14_enc, p30_enc, u3_val, u7_val]], dtype=float)
    
    pxgb = xgb.predict_proba(feat)[0]
    prf = rf.predict_proba(feat)[0]
    plgb = lgb.predict_proba(feat)[0]
    
    scores = {b: 0.0 for b in BRANDS}
    for idx, c in enumerate(enc_classes):
        p = pxgb[idx] * 0.40 + prf[idx] * 0.40 + plgb[idx] * 0.20
        scores[c] = p
        
    return scores

def run_organic_backtest():
    print("Loading historical data...", flush=True)
    df = pd.read_excel(EXCEL_FILE, sheet_name='LiveData')
    expected_cols = ['Date'] + SLOT_NAMES
    available = [c for c in expected_cols if c in df.columns]
    df = df[available].dropna(subset=['Date']).copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    start_date = pd.to_datetime('2024-07-01')
    end_date = pd.to_datetime('2025-12-31')
    
    print(f"Backtesting from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}", flush=True)
    
    total_slots = 0
    correct_slots = 0
    daily_results = []
    
    enc_df = df.copy()
    for s in SLOT_NAMES:
         enc_df[s] = LabelEncoder().fit_transform(enc_df[s].fillna('UNKNOWN'))
    
    history_indices = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].index.tolist()
    
    start_time = time.time()
    
    for count, t_idx in enumerate(history_indices):
        target_date = df.loc[t_idx, 'Date']
        
        train_start = max(0, t_idx - 60)
        df_train_raw = df.iloc[train_start:t_idx].copy()
        if len(df_train_raw) < 10: continue
            
        df_train_raw['dow'] = df_train_raw['Date'].dt.dayofweek
        df_train_raw['month'] = df_train_raw['Date'].dt.month
        df_train_raw['day'] = df_train_raw['Date'].dt.day
        df_train_raw['is_wknd'] = df_train_raw['dow'].apply(lambda x: 1 if x>=5 else 0)
        
        tasks = []
        for s in SLOT_NAMES:
            enc_col = enc_df.loc[train_start:t_idx-1, s]
            p1 = enc_col.shift(1).fillna(-1)
            p7 = enc_col.shift(7).fillna(-1)
            p14 = enc_col.shift(14).fillna(-1)
            p30 = enc_col.shift(30).fillna(-1)
            u3 = enc_col.rolling(3).apply(lambda x: len(np.unique(x))).fillna(-1)
            u7 = enc_col.rolling(7).apply(lambda x: len(np.unique(x))).fillna(-1)
            
            x_train = pd.DataFrame({
                'dow': df_train_raw['dow'], 'month': df_train_raw['month'], 'day': df_train_raw['day'], 
                'is_wknd': df_train_raw['is_wknd'], 'p1': p1, 'p7': p7, 'p14': p14, 'p30': p30, 'u3': u3, 'u7': u7
            }).fillna(-1).values
            
            enc = LabelEncoder()
            valid = df_train_raw[s].dropna()
            enc.fit(valid)
            y_train = enc.transform(valid)
            x_train = x_train[valid.index - train_start]
            
            p1_val = df.loc[t_idx-1, s] if t_idx-1>=0 else ''
            p7_val = df.loc[t_idx-7, s] if t_idx-7>=0 else ''
            p14_val = df.loc[t_idx-14, s] if t_idx-14>=0 else ''
            p30_val = df.loc[t_idx-30, s] if t_idx-30>=0 else ''
            
            p1_enc = enc.transform([p1_val])[0] if p1_val in enc.classes_ else -1
            p7_enc = enc.transform([p7_val])[0] if p7_val in enc.classes_ else -1
            p14_enc = enc.transform([p14_val])[0] if p14_val in enc.classes_ else -1
            p30_enc = enc.transform([p30_val])[0] if p30_val in enc.classes_ else -1
            
            enc_hist = enc_df.loc[max(0, t_idx-7):t_idx-1, s]
            u3_val = len(np.unique(enc_hist.tail(3))) if len(enc_hist)>=3 else -1
            u7_val = len(np.unique(enc_hist)) if len(enc_hist)>=7 else -1
            
            dw, m, dy = target_date.dayofweek, target_date.month, target_date.day
            
            tasks.append((x_train, y_train, tuple(enc.classes_), p1_enc, p7_enc, p14_enc, p30_enc, u3_val, u7_val, dw, m, dy))

        results = Parallel(n_jobs=-1)(delayed(process_single_combo)(*args) for args in tasks)
        
        predictions = {}
        for s_idx, s in enumerate(SLOT_NAMES):
            scores = results[s_idx]
            predictions[s] = sorted(scores, key=scores.get, reverse=True)[:6]
        
        day_correct = 0
        for s in SLOT_NAMES:
            actual = df.loc[t_idx, s]
            if pd.isna(actual) or actual == '': continue
            actual = str(actual).split(',')[0].strip()
            if actual in predictions[s]:
                day_correct += 1
                correct_slots += 1
            total_slots += 1
            
        daily_accuracy = (day_correct / 10.0) * 100
        daily_results.append({'Date': target_date.strftime('%Y-%m-%d'), 'Accuracy': daily_accuracy})
        
        if (count + 1) % 10 == 0:
            avg_so_far = (correct_slots / total_slots) * 100 if total_slots > 0 else 0
            print(f"[{target_date.strftime('%Y-%m-%d')}] Processed {count+1} days. Current Avg Acc: {avg_so_far:.2f}%", flush=True)

    overall_acc = (correct_slots / total_slots) * 100 if total_slots > 0 else 0
    print(f"\n✅ Organic Backtest Finished! {time.time() - start_time:.2f} seconds.")
    print(f"Total Organic Accuracy (July 2024 - Dec 2025): {overall_acc:.2f}%")
    
    out_df = pd.DataFrame(daily_results)
    out_df.to_csv(r'C:\Users\Administrator\Documents\Logistics_AI_Final_Release\Phase9_Organic_Backtest.csv', index=False)

if __name__ == "__main__":
    run_organic_backtest()
