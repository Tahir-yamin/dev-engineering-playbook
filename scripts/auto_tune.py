import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import warnings
import json
import os

warnings.simplefilter('ignore')

JSON_KEY = r"C:\Users\USER\Documents\mcp-sheets-key.json"
SHEET_ID = "YOUR_SHEET_ID"
SLOTS = [
    'PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 
    'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE'
]

def load_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)
    ws = sh.worksheet("Sheet1")
    data = ws.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    return df

def build_features(df):
    df_feat = df.copy()
    df_feat['dow'] = df_feat['Date'].dt.dayofweek
    df_feat['dom'] = df_feat['Date'].dt.day
    df_feat['month'] = df_feat['Date'].dt.month
    df_feat['woy'] = df_feat['Date'].dt.isocalendar().week.astype(int)
    
    df_feat['msin'] = np.sin(2 * np.pi * df_feat['month'] / 12)
    df_feat['mcos'] = np.cos(2 * np.pi * df_feat['month'] / 12)
    
    for s in SLOTS:
        enc = LabelEncoder()
        valid = df_feat[s].replace("", np.nan).dropna()
        if not valid.empty:
            enc.fit(valid)
            df_feat[f'_{s}_enc'] = df_feat[s].map(lambda x: enc.transform([x])[0] if pd.notna(x) and x in enc.classes_ else -1)
            df_feat[f'_{s}_p1'] = df_feat[f'_{s}_enc'].shift(1).fillna(-1)
            df_feat[f'_{s}_p7'] = df_feat[f'_{s}_enc'].shift(7).fillna(-1)
            df_feat[f'_{s}_p14'] = df_feat[f'_{s}_enc'].shift(14).fillna(-1)
            df_feat[f'_{s}_p30'] = df_feat[f'_{s}_enc'].shift(30).fillna(-1)
            valid_enc = df_feat[f'_{s}_enc'].replace(-1, np.nan).dropna()
            df_feat[f'_{s}_roll3'] = valid_enc.rolling(3).apply(lambda x: len(set(x.dropna())), raw=False).fillna(-1)
            df_feat[f'_{s}_roll7'] = valid_enc.rolling(7).apply(lambda x: len(set(x.dropna())), raw=False).fillna(-1)
        else:
            df_feat[f'_{s}_enc'] = -1
            df_feat[f'_{s}_p1'] = -1; df_feat[f'_{s}_p7'] = -1; df_feat[f'_{s}_p14'] = -1; df_feat[f'_{s}_p30'] = -1
            df_feat[f'_{s}_roll3'] = -1; df_feat[f'_{s}_roll7'] = -1
            
    return df_feat

def optimize():
    print("🌙 Nightly Auto-Tune Job Started...")
    df = load_data()
    # We only care about optimizing against the very latest trends
    if len(df) > 90:
        df = df.tail(90).reset_index(drop=True)
        
    df_feat = build_features(df)
    base_f = ['dow','dom','month','woy','msin','mcos']
    
    # Define hyperparameter grid
    lrs = [0.01, 0.03, 0.05, 0.1]
    depths = [3, 5, 7, 9]
    n_ests = [100, 200, 350, 500]
    
    best_params_per_slot = {}
    
    # We evaluate on the last 14 days
    eval_days = 14
    if len(df_feat) < eval_days + 30:
        print("Not enough data to run meaningful Auto-Tune.")
        return
        
    train_df = df_feat.iloc[:-eval_days]
    test_df = df_feat.iloc[-eval_days:]
    
    total_acc = 0.0
    
    for s in SLOTS:
        best_acc = 0
        best_p = {'lr': 0.03, 'd': 7, 'n': 350}
        
        valid_train = (train_df[s] != "") & (train_df[s].notna())
        valid_test = (test_df[s] != "") & (test_df[s].notna())
        
        if valid_train.sum() < 30 or valid_test.sum() == 0:
            continue
            
        enc = LabelEncoder()
        y_train = enc.fit_transform(train_df.loc[valid_train, s])
        
        f_cols = base_f + [f'_{s}_p1', f'_{s}_p7', f'_{s}_p14', f'_{s}_p30', f'_{s}_roll3', f'_{s}_roll7']
        X_train = train_df.loc[valid_train, f_cols].fillna(-1).astype(float)
        X_test = test_df.loc[valid_test, f_cols].fillna(-1).astype(float)
        y_test = test_df.loc[valid_test, s].values
        
        # Grid Search
        for lr in lrs:
            for d in depths:
                for n in n_ests:
                    clf = xgb.XGBClassifier(n_estimators=n, max_depth=d, learning_rate=lr, random_state=42, n_jobs=-1)
                    clf.fit(X_train, y_train)
                    
                    probas = clf.predict_proba(X_test)
                    
                    hits = 0
                    for i, true_val in enumerate(y_test):
                        if true_val in enc.classes_:
                            p_idx = np.argsort(probas[i])[::-1][:6]
                            top6 = enc.inverse_transform(p_idx)
                            if true_val in top6:
                                hits += 1
                                
                    acc = hits / len(y_test)
                    if acc > best_acc:
                        best_acc = acc
                        best_p = {'lr': lr, 'd': d, 'n': n}
                        
        print(f"Slot: {s} | Best Acc: {best_acc:.2f} | Params: {best_p}")
        best_params_per_slot[s] = best_p
        total_acc += best_acc
        
    final_score = total_acc / len(SLOTS)
    print(f"🏁 Auto-Tune Complete. Optimized Potential: {final_score*100:.1f}%")
    
    with open(r"d:\my-dev-knowledge-base\scripts\auto_params.json", "w") as f:
        json.dump(best_params_per_slot, f, indent=4)
        print("💾 Hyperparameters saved globally.")

if __name__ == "__main__":
    optimize()
