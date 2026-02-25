import pandas as pd
import numpy as np
import warnings
import time
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from joblib import Parallel, delayed

warnings.filterwarnings('ignore')

EXCEL_FILE = r'C:\Users\USER\Documents\Logistics_AI_Final_Release\Logistics_AI_Production_Master.xlsm'
SLOT_NAMES = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]
BRANDS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def train_and_predict_deep_block(s, df_train_raw, df_test_raw, enc_df, enc, global_features):
    # This block trains the hybrid ML model for a single slot using unsupervised and advanced engineered features
    valid = df_train_raw[s].dropna()
    if len(valid) < 10:
        freq = valid.value_counts(normalize=True).to_dict()
        default_scores = {b: freq.get(b, 0) for b in BRANDS}
        return s, [default_scores for _ in range(len(df_test_raw))]
        
    y_train = enc.transform(valid)
    
    # Base features + Lags
    feature_cols = ['dow', 'month', 'day', 'is_wknd', 'cluster_id', 
                    f'p1_{s}', f'p2_{s}', f'p7_{s}', f'p14_{s}', f'p30_{s}', 
                    'global_mode_7d', 'global_unique_7d']
                    
    x_train = df_train_raw.loc[valid.index, feature_cols].fillna(-1).values
    x_test = df_test_raw[feature_cols].fillna(-1).values
    
    # Advanced Ensembling with strict constraints to prevent overfitting on noise
    xgb = XGBClassifier(n_estimators=150, max_depth=4, learning_rate=0.05, verbosity=0, random_state=42, subsample=0.8, colsample_bytree=0.8)
    rf = RandomForestClassifier(n_estimators=100, max_depth=6, min_samples_leaf=3, random_state=42)
    
    # Weight recent instances to simulate the "momentum" bias
    w = np.ones(len(y_train))
    w[-min(14, len(w)):] = 3.0
    w[-min(60, len(w)):-min(14, len(w))] = 1.5
    
    try:
        xgb.fit(x_train, y_train, sample_weight=w)
        rf.fit(x_train, y_train, sample_weight=w)
        
        pxgb = xgb.predict_proba(x_test)
        prf = rf.predict_proba(x_test)
        
        block_scores = []
        for i in range(len(x_test)):
            scores = {b: 0.0 for b in BRANDS}
            for idx, c in enumerate(enc.classes_):
                if idx < pxgb.shape[1] and idx < prf.shape[1]:
                    # Blended ensemble probability
                    p = pxgb[i, idx] * 0.60 + prf[i, idx] * 0.40
                    scores[c] = p
            block_scores.append(scores)
            
        return s, block_scores
    except Exception as e:
        freq = valid.value_counts(normalize=True).to_dict()
        default_scores = {b: freq.get(b, 0.0) for b in BRANDS}
        return s, [default_scores for _ in range(len(x_test))]

def extract_global_features(df_raw, enc_df):
    """ Extracts global momentum logic to be used as ML features """
    print("Generating Global Unsupervised & Statistical Features...", flush=True)
    df = df_raw.copy()
    
    # Unsupervised Date Clustering (K-Means) to find hidden seasonalities
    kmeans = KMeans(n_clusters=6, random_state=42)
    df['cluster_id'] = kmeans.fit_predict(df[['dow', 'month', 'day']])
    
    # Global Matrix
    global_mode_7d = []
    global_unique_7d = []
    
    for i in range(len(df)):
        if i < 7:
            global_mode_7d.append(-1)
            global_unique_7d.append(-1)
        else:
            # Flatten last 7 days across ALL slots
            window = df_raw.iloc[i-7:i][SLOT_NAMES].values.flatten()
            valid_window = [str(x).strip() for x in window if pd.notna(x) and str(x).strip() != ""]
            if valid_window:
                top_brand = pd.Series(valid_window).mode()
                # We need to encode the string back to a generic number or category
                global_mode_7d.append(abs(hash(top_brand[0])) % 20 if not top_brand.empty else -1)
                global_unique_7d.append(len(set(valid_window)))
            else:
                global_mode_7d.append(-1)
                global_unique_7d.append(-1)
                
    df['global_mode_7d'] = global_mode_7d
    df['global_unique_7d'] = global_unique_7d
    return df

def run_deep_ml_probe():
    print("Loading historical LiveData...", flush=True)
    df = pd.read_excel(EXCEL_FILE, sheet_name='LiveData')
    expected_cols = ['Date'] + SLOT_NAMES
    available = [c for c in expected_cols if c in df.columns]
    df = df[available].dropna(subset=['Date']).copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    start_date = pd.to_datetime('2024-07-01')
    end_date = pd.to_datetime('2025-12-31')
    
    print(f"Executing Deep ML Advanced Probe: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Pre-encoding
    enc_df = df.copy()
    le_dict = {}
    for s in SLOT_NAMES:
         le = LabelEncoder()
         enc_df[s] = le.fit_transform(enc_df[s].fillna('UNKNOWN').astype(str))
         le_dict[s] = le
    
    # Base Features
    df['dow'] = df['Date'].dt.dayofweek
    df['month'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day
    df['is_wknd'] = df['dow'].apply(lambda x: 1 if x>=5 else 0)
    
    # Slot-specific Lags
    for s in SLOT_NAMES:
        df[f'p1_{s}'] = enc_df[s].shift(1).fillna(-1)
        df[f'p2_{s}'] = enc_df[s].shift(2).fillna(-1)
        df[f'p7_{s}'] = enc_df[s].shift(7).fillna(-1)
        df[f'p14_{s}'] = enc_df[s].shift(14).fillna(-1)
        df[f'p30_{s}'] = enc_df[s].shift(30).fillna(-1)

    # Inject Unsupervised & Global Matrix features
    df = extract_global_features(df, enc_df)
    
    all_test_dates = pd.date_range(start=start_date, end=end_date, freq='MS')
    periods = [(d, d + pd.offsets.MonthEnd(1)) for d in all_test_dates]
    
    total_slots = 0
    correct_slots = 0
    start_time = time.time()
    
    for month_start, month_end in periods:
        test_mask = (df['Date'] >= month_start) & (df['Date'] <= month_end)
        if not test_mask.any(): continue
            
        test_indices = df[test_mask].index
        first_test_idx = test_indices[0]
        
        train_start = max(0, first_test_idx - 180) # Use 180 days of context
        train_end = first_test_idx
        
        df_train = df.iloc[train_start:train_end]
        df_test = df.iloc[test_indices]
        
        results = Parallel(n_jobs=-1)(
            delayed(train_and_predict_deep_block)(s, df_train.copy(), df_test.copy(), enc_df, le_dict[s], None) 
            for s in SLOT_NAMES
        )
        
        preds_dict = {res[0]: res[1] for res in results}
        
        for idx_offset, t_idx in enumerate(test_indices):
            t_date = df.loc[t_idx, 'Date'].strftime('%Y-%m-%d')
            day_correct = 0
            
            for s in SLOT_NAMES:
                actual = df.loc[t_idx, s]
                if pd.isna(actual) or str(actual).strip() == "": continue
                actual = str(actual).split(',')[0].strip()
                
                scores = preds_dict[s][idx_offset]
                top6 = sorted(scores, key=scores.get, reverse=True)[:6]
                if actual in top6:
                    day_correct += 1
                    correct_slots += 1
                total_slots += 1
            
        print(f"[{month_end.strftime('%Y-%m')}] Month Processed. Auto-Accumulative Accuracy: {((correct_slots/total_slots)*100):.2f}%", flush=True)

    overall_acc = (correct_slots / total_slots) * 100 if total_slots > 0 else 0
    print(f"\n✅ Deep ML Probe Backtest Finished! {time.time() - start_time:.2f} seconds.")
    print(f"Final Advanced ML Absolute Limit Accuracy: {overall_acc:.2f}%")

if __name__ == "__main__":
    run_deep_ml_probe()
