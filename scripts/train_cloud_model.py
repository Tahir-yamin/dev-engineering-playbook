
"""
Logistics AI Cloud Engine (v14.0 Quantum Momentum)
Intended to run automatically via GitHub Actions Cron Job
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import warnings
import os

warnings.simplefilter('ignore')

SHEET_ID = '1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY'
SLOTS = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]

# Use environment variable for credentials in GitHub Actions
# Default to local path for local testing
JSON_KEY = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", r"C:\Users\Administrator\Documents\mcp-sheets-key.json")

def get_cloud_data(client):
    print("☁️ Pulling Live Cloud Memory...")
    sh = client.open_by_key(SHEET_ID)
    ws = sh.worksheet("Sheet1")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    return df, sh

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
            df_feat[f'_{s}_p365'] = df_feat[f'_{s}_enc'].shift(365).fillna(-1)
        else:
            df_feat[f'_{s}_enc'] = -1
            df_feat[f'_{s}_p1'] = -1; df_feat[f'_{s}_p7'] = -1; df_feat[f'_{s}_p365'] = -1

    return df_feat

def main():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    
    df, sh = get_cloud_data(client)
    print(f"✅ Data Loaded. Total Rows: {len(df)}")
    
    df_feat = build_features(df)
    
    models = {}
    encoders = {}
    base_f = ['dow','dom','month','woy','msin','mcos']
    
    print("🧠 Quantum Training Active...")
    for s in SLOTS:
        valid_mask = (df_feat[s] != "") & (df_feat[s].notna())
        if valid_mask.sum() < 50: 
            models[s] = None; continue
            
        enc = LabelEncoder()
        y = enc.fit_transform(df_feat.loc[valid_mask, s])
        encoders[s] = enc
        
        f_cols = base_f + [f'_{s}_p1', f'_{s}_p7', f'_{s}_p365']
        X = df_feat.loc[valid_mask, f_cols].fillna(-1).astype(float)
        
        weights = np.ones(len(X))
        weights[-30:] = 2.0  # Double weight for last 30 days
        
        clf = xgb.XGBClassifier(n_estimators=350, max_depth=7, learning_rate=0.03, random_state=42)
        clf.fit(X, y, sample_weight=weights)
        models[s] = clf

    print("🔮 Simulating Future Matrix...")
    last_date = df['Date'].max()
    dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=365)
    results = []
    
    running_seed = {s: list(df[s].tail(366).values) for s in SLOTS}

    for d in dates:
        dw, dom, m = d.dayofweek, d.day, d.month
        woy = d.isocalendar()[1]
        msin = np.sin(2*np.pi*m/12)
        mcos = np.cos(2*np.pi*m/12)
        row = [d.strftime('%Y-%m-%d')]
        
        for s in SLOTS:
            enc = encoders.get(s)
            clf = models.get(s)
            hs = running_seed[s]
            
            if not enc or not clf:
                row.extend(["-"]*6); continue
                
            p1 = enc.transform([hs[-1]])[0] if hs[-1] in enc.classes_ else -1
            p7 = enc.transform([hs[-7]])[0] if len(hs)>=7 and hs[-7] in enc.classes_ else -1
            p365 = enc.transform([hs[-365]])[0] if len(hs)>=365 and hs[-365] in enc.classes_ else -1
            
            feat = np.array([[dw, dom, m, woy, msin, mcos, p1, p7, p365]])
            proba = clf.predict_proba(feat)[0]
            top6_idx = np.argsort(proba)[::-1][:6]
            try:
                top6 = enc.inverse_transform(top6_idx)
            except ValueError:
                top6 = ["-"]*6
            row.extend(list(top6))
            hs.append(top6[0])
            
        results.append(row)

    print("🚀 Uploading to Neural Dashboard...")
    try:
        ws_pred = sh.worksheet("ML_Predictions_Cloud")
    except gspread.exceptions.WorksheetNotFound:
        ws_pred = sh.add_worksheet(title="ML_Predictions_Cloud", rows="500", cols="65")
        
    ws_pred.clear()
    headers = ["Forecast_Date"]
    for s in SLOTS:
        headers.extend([f"{s}_P1", f"{s}_P2", f"{s}_P3", f"{s}_P4", f"{s}_P5", f"{s}_P6"])
        
    ws_pred.update('A1', [headers] + results, value_input_option='USER_ENTERED')
    print("✅ SUCCESS! Cloud sync complete.")

if __name__ == "__main__":
    main()
