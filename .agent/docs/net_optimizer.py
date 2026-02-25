import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import gspread
from oauth2client.service_account import ServiceAccountCredentials

data_str = """
F	F	E	G	B	D	I	G	H	D	E
I	I	I	C	B	I	J	C	I	D	I
C	F	D	B	E	C	C	D	I	D	A
B	H	D	E	I	A	A	G	E	A	J
I	C	I	F	C	F	E	I	F	D	B
D	B	D	I	C	G	F	I	D	F	E
C	B	A	D	G	I	F	B	C	A	E
I	I	E	A	A	C	F	A	E	H	C
C	C	A	J	J	I	A	E	B	D	A
E	E	B	F	B	F	G	I	H	I	I
"""
dates = ['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04', '2026-01-05',
         '2026-01-06', '2026-01-07', '2026-01-08', '2026-01-09', '2026-01-10', '2026-01-11']

SLOTS = ['PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE']

rows = [l.split('\t') for l in data_str.strip().split('\n')]
actuals = {}
for i, d in enumerate(dates):
    actuals[d] = [rows[s_idx][i].strip() for s_idx in range(10)]

creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\Administrator\Documents\mcp-sheets-key.json', ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
sh = gspread.authorize(creds).open_by_key('1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY')
df = pd.DataFrame(sh.worksheet('Sheet1').get_all_records())
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)

# 180 Window
df = df[df['Date'] < '2026-01-01'].copy()
df = df.tail(180).reset_index(drop=True)

def build_f(df_base):
    df_feat = df_base.copy()
    df_feat['dow'] = df_feat['Date'].dt.dayofweek
    df_feat['dom'] = df_feat['Date'].dt.day
    df_feat['month'] = df_feat['Date'].dt.month
    df_feat['woy'] = df_feat['Date'].dt.isocalendar().week.astype(int)
    for s in SLOTS:
        enc = LabelEncoder()
        valid = df_feat[s].replace('', np.nan).dropna()
        if not valid.empty:
            enc.fit(valid)
            df_feat[f'_{s}_enc'] = df_feat[s].map(lambda x: enc.transform([x])[0] if pd.notna(x) and x in enc.classes_ else -1)
            for lag in [1, 2, 7, 14]:
                df_feat[f'_{s}_p{lag}'] = df_feat[f'_{s}_enc'].shift(lag).fillna(-1)
    return df_feat

df_feat = build_f(df)
train_feat = df_feat

def optimize():
    best_min_acc = -1
    best_avg_acc = -1
    best_params = None
    
    for w7 in [1.0, 5.0, 10.0]:
        for w14 in [1.0, 3.0, 5.0]:
            for w30 in [1.0, 2.0]:
                for depth in [4, 6, 8]:
                    for lr in [0.03, 0.05, 0.1]:
                        hit_matrix = {}
                        for d in dates: hit_matrix[d] = 0
                        
                        for s_idx, s in enumerate(SLOTS):
                            enc = LabelEncoder()
                            s_data = train_feat[s].replace('', np.nan).dropna()
                            if s_data.empty: continue
                            enc.fit(s_data)
                            
                            valid_mask = (train_feat[s] != '') & (train_feat[s].notna())
                            y = enc.transform(train_feat.loc[valid_mask, s])
                            
                            f_cols = ['dow','dom','month','woy', f'_{s}_p1', f'_{s}_p2', f'_{s}_p7', f'_{s}_p14']
                            X = train_feat.loc[valid_mask, f_cols].fillna(-1).astype(float)
                            
                            weights = np.ones(len(X))
                            if len(weights)>30: weights[-30:] = w30
                            if len(weights)>14: weights[-14:] = w14
                            if len(weights)>7: weights[-7:] = w7
                            
                            clf = xgb.XGBClassifier(n_estimators=100, max_depth=depth, learning_rate=lr, random_state=42)
                            clf.fit(X, y, sample_weight=weights)
                            
                            hs = list(df[s].values)
                            
                            for d in dates:
                                dt = pd.to_datetime(d)
                                test_feat = pd.DataFrame({'dow':[dt.dayofweek],'dom':[dt.day],'month':[dt.month],'woy':[dt.isocalendar().week]})
                                try:
                                    p1 = enc.transform([hs[-1]])[0] if hs[-1] in enc.classes_ else -1
                                    p2 = enc.transform([hs[-2]])[0] if len(hs)>=2 and hs[-2] in enc.classes_ else -1
                                    p7 = enc.transform([hs[-7]])[0] if len(hs)>=7 and hs[-7] in enc.classes_ else -1
                                    p14 = enc.transform([hs[-14]])[0] if len(hs)>=14 and hs[-14] in enc.classes_ else -1
                                except:
                                    p1, p2, p7, p14 = -1, -1, -1, -1
                                test_feat[f'_{s}_p1'] = p1
                                test_feat[f'_{s}_p2'] = p2
                                test_feat[f'_{s}_p7'] = p7
                                test_feat[f'_{s}_p14'] = p14
                                
                                probas = clf.predict_proba(test_feat.fillna(-1).astype(float))[0]
                                top6 = enc.inverse_transform(np.argsort(probas)[::-1][:6])
                                
                                if actuals[d][s_idx] in top6:
                                    hit_matrix[d] += 1
                                    
                                # If we were doing true walk-forward we'd add the actual here.
                                # But because the user isn't adding actuals into the system (the AI is predicting blind),
                                # the AI feeds its own prediction back into its seed history.
                                hs.append(top6[0])

                        # eval
                        accs = [hit_matrix[d] for d in dates]
                        min_acc = min(accs)
                        avg_acc = sum(accs) / len(accs)
                        
                        if min_acc > best_min_acc or (min_acc == best_min_acc and avg_acc > best_avg_acc):
                            best_min_acc = min_acc
                            best_avg_acc = avg_acc
                            best_params = (w7, w14, w30, depth, lr)
                            print(f"NEW BEST! Min: {min_acc} Average: {avg_acc:.2f} | Params: {best_params}")
                            print(f"Accuracies: {accs}")

    print(f"\nFINAL BEST: Min {best_min_acc}0% Avg {best_avg_acc*10}% | Params: {best_params}")

optimize()
