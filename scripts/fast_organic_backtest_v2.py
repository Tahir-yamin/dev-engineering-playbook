import pandas as pd
import numpy as np
import warnings
import time
import os

warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'

from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.preprocessing import LabelEncoder
from joblib import Parallel, delayed

EXCEL_FILE = r'C:\Users\USER\Documents\Logistics_AI_Final_Release\Logistics_AI_Production_Master.xlsm'
SLOT_NAMES = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]
BRANDS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def train_and_predict_block(s, df_train_raw, df_test_raw, enc_df, enc):
    import warnings
    warnings.filterwarnings('ignore')
    
    def engineer_features(df_chunk, slot_name):
        df_chunk['Date'] = pd.to_datetime(df_chunk['Date'])
        target = df_chunk[slot_name].copy()
        
        features = pd.DataFrame(index=df_chunk.index)
        features['dow'] = df_chunk['Date'].dt.dayofweek
        features['is_weekend'] = features['dow'].isin([5, 6]).astype(int)
        features['dom'] = df_chunk['Date'].dt.day
        features['month'] = df_chunk['Date'].dt.month
        
        # Build Date-to-Value map for pure time-series lookups
        val_map = dict(zip(df_chunk['Date'].dt.normalize(), target))
        
        for lag in [1, 2, 7, 14, 30]:
            # Exact Calendar Lookback - fallback to previous valid day if exact is missing
            def get_lag_val(date, lag_days):
                target_date = date - pd.Timedelta(days=lag_days)
                for _ in range(5): # Go up to 5 days back to find last valid record
                     if target_date in val_map and not pd.isna(val_map[target_date]):
                          return val_map[target_date]
                     target_date -= pd.Timedelta(days=1)
                return -1
                
            features[f'lag_{lag}'] = df_chunk['Date'].dt.normalize().apply(lambda x: get_lag_val(x, lag))
            
        morning_slots = ['PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE']
        if slot_name not in morning_slots:
            for ms in morning_slots:
                if ms in df_chunk.columns:
                     features[f'morning_{ms}_lag1'] = df_chunk[ms].shift(1)
                     
        features['target'] = target
        return features

    valid_train = df_train_raw[s].dropna()
    if len(valid_train) < 10:
        freq = valid_train.value_counts(normalize=True).to_dict()
        default_scores = {b: freq.get(b, 0) for b in BRANDS}
        return s, [default_scores for _ in range(len(df_test_raw))]
        
    y_train = enc.transform(valid_train)
    
    # Generate Continuous Calendar Features
    features_train = engineer_features(df_train_raw.copy(), s)
    features_test = engineer_features(df_test_raw.copy(), s)
    
    # Sync indices
    common_train_idx = features_train.index.intersection(valid_train.index)
    if len(common_train_idx) < 10:
        freq = valid_train.value_counts(normalize=True).to_dict()
        default_scores = {b: freq.get(b, 0) for b in BRANDS}
        return s, [default_scores for _ in range(len(df_test_raw))]
        
    y_train = enc.transform(valid_train.loc[common_train_idx])
    x_train = features_train.loc[common_train_idx].drop('target', axis=1).values
    x_test = features_test.drop('target', axis=1).values
    
    # Pure highly-tuned XGBoost tailored for noisy, sparse 10-class logistics data
    xgb = XGBClassifier(
        n_estimators=300, 
        max_depth=5, 
        learning_rate=0.03, 
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=3,
        gamma=0.1,
        verbosity=0, 
        random_state=42
    )
    
    w = np.ones(len(y_train))
    w[-min(7, len(w)):] = 5.0
    w[-min(30, len(w)):-min(7, len(w))] = 2.0
    
    try:
        xgb.fit(x_train, y_train, sample_weight=w)
        pxgb = xgb.predict_proba(x_test)
        
        block_scores = []
        for i in range(len(x_test)):
            scores = {b: 0.0 for b in BRANDS}
            for idx, c in enumerate(enc.classes_):
                if idx < pxgb.shape[1]:
                    scores[c] = pxgb[i, idx]
            block_scores.append(scores)
        return s, block_scores
    except Exception as e:
        freq = valid_train.value_counts(normalize=True).to_dict()
        default_scores = {b: freq.get(b, 0.0) for b in BRANDS}
        return s, [default_scores for _ in range(len(x_test))]

def run_fast_backtest():
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
    
    # The original feature engineering block is removed as it's now handled by engineer_features
    # enc_df is still needed for LabelEncoding
    enc_df = df.copy()
    le_dict = {}
    for s in SLOT_NAMES:
         le = LabelEncoder()
         enc_df[s] = le.fit_transform(enc_df[s].fillna('UNKNOWN').astype(str))
         le_dict[s] = le
    
    df['dow'] = df['Date'].dt.dayofweek
    df['month'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day
    df['is_wknd'] = df['dow'].apply(lambda x: 1 if x>=5 else 0)
    
    for s in SLOT_NAMES:
        df[f'p1_{s}'] = enc_df[s].shift(1).fillna(-1)
        df[f'p7_{s}'] = enc_df[s].shift(7).fillna(-1)
        df[f'p14_{s}'] = enc_df[s].shift(14).fillna(-1)
        df[f'p30_{s}'] = enc_df[s].shift(30).fillna(-1)
        df[f'u3_{s}'] = enc_df[s].rolling(3).apply(lambda x: len(np.unique(x))).shift(1).fillna(-1)
        df[f'u7_{s}'] = enc_df[s].rolling(7).apply(lambda x: len(np.unique(x))).shift(1).fillna(-1)

    all_test_dates = pd.date_range(start=start_date, end=end_date, freq='MS')
    periods = [(d, d + pd.offsets.MonthEnd(1)) for d in all_test_dates]
    
    total_slots = 0
    correct_slots = 0
    daily_results = []
    
    start_time = time.time()
    
    for month_start, month_end in periods:
        test_mask = (df['Date'] >= month_start) & (df['Date'] <= month_end)
        if not test_mask.any(): continue
            
        test_indices = df[test_mask].index
        first_test_idx = test_indices[0]
        
        train_start = max(0, first_test_idx - 60)
        train_end = first_test_idx
        
        df_train = df.iloc[train_start:train_end]
        df_test = df.iloc[test_indices]
        
        # Train and completely predict the entire month in one parallel block
        results = Parallel(n_jobs=-1)(
            delayed(train_and_predict_block)(s, df_train.copy(), df_test.copy(), enc_df, le_dict[s]) 
            for s in SLOT_NAMES
        )
        
        preds_dict = {res[0]: res[1] for res in results}
        
        for idx_offset, t_idx in enumerate(test_indices):
            t_date = df.loc[t_idx, 'Date'].strftime('%Y-%m-%d')
            day_correct = 0
            
            for s in SLOT_NAMES:
                actual = df.loc[t_idx, s]
                if pd.isna(actual) or actual == '': continue
                actual = str(actual).split(',')[0].strip()
                
                scores = preds_dict[s][idx_offset]
                top6 = sorted(scores, key=scores.get, reverse=True)[:6]
                if actual in top6:
                    day_correct += 1
                    correct_slots += 1
                total_slots += 1
            
            acc = (day_correct / 10.0) * 100
            daily_results.append({'Date': t_date, 'Accuracy': acc})
            
        print(f"[{month_end.strftime('%Y-%m')}] Month Processed. Accumulative Accuracy: {((correct_slots/total_slots)*100):.2f}%", flush=True)

    overall_acc = (correct_slots / total_slots) * 100 if total_slots > 0 else 0
    print(f"\n✅ FAST Organic Backtest Finished! {time.time() - start_time:.2f} seconds.")
    print(f"Total Organic Accuracy (July 2024 - Dec 2025): {overall_acc:.2f}%")
    
    out_df = pd.DataFrame(daily_results)
    out_df.to_csv(r'C:\Users\USER\Documents\Logistics_AI_Final_Release\Fast_Organic_Backtest.csv', index=False)

if __name__ == "__main__":
    run_fast_backtest()
