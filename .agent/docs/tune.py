
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.simplefilter('ignore')

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
SHEET_ID = '1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY'
SLOTS = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]

def eval_model():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)
    ws = sh.worksheet("Sheet1")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Exclude 2026 data so we test purely on 2019-2025 splitting
    df = df[df['Date'] < '2026-01-01'].copy()
    
    df_feat = df.copy()
    df_feat['dow'] = df_feat['Date'].dt.dayofweek
    df_feat['dom'] = df_feat['Date'].dt.day
    df_feat['month'] = df_feat['Date'].dt.month
    df_feat['woy'] = df_feat['Date'].dt.isocalendar().week.astype(int)
    df_feat['msin'] = np.sin(2 * np.pi * df_feat['month'] / 12)
    df_feat['mcos'] = np.cos(2 * np.pi * df_feat['month'] / 12)
    
    # Add more features
    for s in SLOTS:
        enc = LabelEncoder()
        valid = df_feat[s].replace("", np.nan).dropna()
        if not valid.empty:
            enc.fit(valid)
            df_feat[f'_{s}_enc'] = df_feat[s].map(lambda x: enc.transform([x])[0] if pd.notna(x) and x in enc.classes_ else -1)
            for lags in [1, 2, 3, 7, 14, 30, 365]: # Added richer lags
                df_feat[f'_{s}_p{lags}'] = df_feat[f'_{s}_enc'].shift(lags).fillna(-1)

    print("Evaluating XGBoost combinations...")
    
    # Train test split (Test on last 60 days of 2025)
    test_size = 60
    train_df = df_feat.iloc[:-test_size]
    test_df = df_feat.iloc[-test_size:]
    
    results = []
    
    for max_depth in [4, 6, 8]:
        for lr in [0.03, 0.05, 0.1]:
            for n_est in [200, 400]:
                for weight_last_n, weight_val in [(0, 1.0), (30, 2.0), (90, 1.5)]:
                    hits = 0
                    total = 0
                    
                    for s in SLOTS:
                        valid_mask = (train_df[s] != "") & (train_df[s].notna())
                        if valid_mask.sum() < 50: continue
                        
                        enc = LabelEncoder()
                        enc.fit(df_feat[s].replace("", np.nan).dropna())
                        y_train = enc.transform(train_df.loc[valid_mask, s])
                        
                        base_f = ['dow','dom','month','woy','msin','mcos']
                        f_cols = base_f + [f'_{s}_p1', f'_{s}_p2', f'_{s}_p3', f'_{s}_p7', f'_{s}_p14', f'_{s}_p30', f'_{s}_p365']
                        
                        X_train = train_df.loc[valid_mask, f_cols].fillna(-1).astype(float)
                        
                        weights = np.ones(len(X_train))
                        if weight_last_n > 0:
                            weights[-weight_last_n:] = weight_val
                        
                        clf = xgb.XGBClassifier(n_estimators=n_est, max_depth=max_depth, learning_rate=lr, random_state=42, n_jobs=-1)
                        clf.fit(X_train, y_train, sample_weight=weights)
                        
                        # Test
                        valid_test = (test_df[s] != "") & (test_df[s].notna())
                        X_test = test_df.loc[valid_test, f_cols].fillna(-1).astype(float)
                        if X_test.empty: continue
                        
                        true_raw = test_df.loc[valid_test, s].values
                        
                        probas = clf.predict_proba(X_test)
                        for i in range(len(probas)):
                            top6_idx = np.argsort(probas[i])[::-1][:6]
                            try:
                                top6_labels = enc.inverse_transform(top6_idx)
                                if true_raw[i] in top6_labels:
                                    hits += 1
                                total += 1
                            except:
                                pass
                                
                    acc = hits / total if total > 0 else 0
                    print(f"Depth:{max_depth}, LR:{lr}, Est:{n_est}, W_n:{weight_last_n}, W_v:{weight_val} --> Acc: {acc*100:.2f}%")

if __name__ == "__main__":
    eval_model()
