import gspread
import pandas as pd
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.simplefilter('ignore')

creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\Administrator\Documents\mcp-sheets-key.json', ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
sh = gspread.authorize(creds).open_by_key('1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY')
df = pd.DataFrame(sh.worksheet('Sheet1').get_all_records())
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)

SLOTS = ['PH01 OIL','PH01 GHEE','PH02 OIL','PH02 GHEE','PH03 OIL','PH03 GHEE','PH04 OIL','PH04 GHEE','PH05 OIL','PH05 GHEE']

print('Testing Hyperparameters over last 30 days of 2025...')

# 180 Window
df = df[df['Date'] < '2026-01-01'].copy()
df = df.tail(180).reset_index(drop=True)

test_size = 30
train_base = df.iloc[:-test_size]
test_base = df.iloc[-test_size:]

def build_f(df_base):
    df_feat = df_base.copy()
    df_feat['dow'] = df_feat['Date'].dt.dayofweek
    df_feat['dom'] = df_feat['Date'].dt.day
    df_feat['month'] = df_feat['Date'].dt.month
    df_feat['woy'] = df_feat['Date'].dt.isocalendar().week.astype(int)
    return df_feat

df_feat = build_f(df)

for weight_7 in [1.0, 3.0, 5.0, 10.0]:
    for weight_14 in [1.0, 2.0, 3.0]:
        hits = 0
        total = 0
        for s in SLOTS:
            enc = LabelEncoder()
            # We must encode first
            s_data = df_feat[s].replace('', np.nan).dropna()
            if s_data.empty: continue
            enc.fit(s_data)
            
            df_feat_s = df_feat.copy()
            df_feat_s[f'_{s}_enc'] = df_feat_s[s].map(lambda x: enc.transform([x])[0] if pd.notna(x) and x in enc.classes_ else -1)
            for lag in [1, 2, 7, 14]:
                df_feat_s[f'_{s}_p{lag}'] = df_feat_s[f'_{s}_enc'].shift(lag).fillna(-1)
                
            train_feat = df_feat_s.iloc[:-test_size]
            test_feat = df_feat_s.iloc[-test_size:]
            
            valid_mask = (train_feat[s] != '') & (train_feat[s].notna())
            y = enc.transform(train_feat.loc[valid_mask, s])
            
            f_cols = ['dow','dom','month','woy', f'_{s}_p1', f'_{s}_p2', f'_{s}_p7', f'_{s}_p14']
            X = train_feat.loc[valid_mask, f_cols].fillna(-1).astype(float)
            
            weights = np.ones(len(X))
            if len(weights)>14: weights[-14:] = weight_14
            if len(weights)>7: weights[-7:] = weight_7
            
            clf = xgb.XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.05, random_state=42)
            clf.fit(X, y, sample_weight=weights)
            
            v_t = (test_feat[s] != '') & (test_feat[s].notna())
            X_t = test_feat.loc[v_t, f_cols].fillna(-1).astype(float)
            if X_t.empty: continue
            
            probas = clf.predict_proba(X_t)
            true_raw = test_feat.loc[v_t, s].values
            
            for i in range(len(probas)):
                top6 = enc.inverse_transform(np.argsort(probas[i])[::-1][:6])
                if true_raw[i] in top6: hits+=1
                total+=1
                
        print(f'W7:{weight_7}, W14:{weight_14} => Acc: {hits/total*100:.2f}%')
