import pandas as pd
import numpy as np
import warnings
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings('ignore')

EXCEL_FILE = r'C:\Users\Administrator\Documents\Logistics_AI_Final_Release\Logistics_AI_Production_Master.xlsm'
SLOT_NAMES = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]
BRANDS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Set random seed for reproducibility
torch.manual_seed(42)
np.random.seed(42)

class LogisticsDNN(nn.Module):
    def __init__(self, num_brands):
        super(LogisticsDNN, self).__init__()
        # Entity Embeddings for Categorical Info
        self.dow_embed = nn.Embedding(7, 4)
        self.month_embed = nn.Embedding(13, 4)
        
        # Dense layers for continuous features (Tri-Weights)
        self.fc1 = nn.Linear(8 + (num_brands * 3), 128)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(128, 64)
        self.out = nn.Linear(64, num_brands)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, dow, month, cont_features):
        d_emb = self.dow_embed(dow)
        m_emb = self.month_embed(month)
        
        x = torch.cat([d_emb, m_emb, cont_features], dim=1)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.out(x)
        return self.softmax(x)

def build_features(df, t_date):
    """ Builds the continuous feature vector per day/slot based on historical stats """
    mask_180 = (df['Date'] < t_date) & (df['Date'] >= t_date - pd.Timedelta(days=180))
    mask_30 = (df['Date'] < t_date) & (df['Date'] >= t_date - pd.Timedelta(days=30))
    mask_7 = (df['Date'] < t_date) & (df['Date'] >= t_date - pd.Timedelta(days=7))
    
    hist_180 = df[mask_180]
    hist_30 = df[mask_30]
    hist_7 = df[mask_7]
    
    global_7_data = hist_7[SLOT_NAMES].values.flatten()
    global_7_data = [str(x).strip() for x in global_7_data if pd.notna(x) and str(x).strip() != ""]
    global_c7 = pd.Series(global_7_data).value_counts(normalize=True) if len(global_7_data) > 0 else pd.Series()
    
    features_per_slot = {}
    
    for s in SLOT_NAMES:
        s180 = hist_180[s].dropna().replace("", np.nan).dropna()
        s30 = hist_30[s].dropna().replace("", np.nan).dropna()
        
        c180 = s180.value_counts(normalize=True) if len(s180) > 0 else pd.Series()
        c30 = s30.value_counts(normalize=True) if len(s30) > 0 else pd.Series()
        
        feat_vector = []
        for b in BRANDS[:10]: # Assume max 10 brands for size constraint
            feat_vector.append(c180.get(b, 0.0))
            feat_vector.append(c30.get(b, 0.0))
            feat_vector.append(global_c7.get(b, 0.0))
        features_per_slot[s] = feat_vector
        
    return features_per_slot

def run_pytorch_backtest():
    print("Loading historical LiveData...", flush=True)
    df = pd.read_excel(EXCEL_FILE, sheet_name='LiveData')
    expected_cols = ['Date'] + SLOT_NAMES
    available = [c for c in expected_cols if c in df.columns]
    df = df[available].dropna(subset=['Date']).copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    start_date = pd.to_datetime('2024-07-01')
    end_date = pd.to_datetime('2025-12-31')
    
    df['dow'] = df['Date'].dt.dayofweek
    df['month'] = df['Date'].dt.month
    
    print(f"Executing PyTorch DNN Advanced Probe: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Needs a unified LabelEncoder for all brands across all slots
    all_brands = df[SLOT_NAMES].values.flatten()
    all_brands = [str(x).split(',')[0].strip() for x in all_brands if pd.notna(x) and str(x).strip() != ""]
    master_le = LabelEncoder()
    master_le.fit(list(set(all_brands)))
    num_classes = len(master_le.classes_)
    
    print(f"Detected {num_classes} active unique brands.")

    test_dates = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]['Date'].unique()
    
    correct_slots = 0
    total_slots = 0
    
    start_time = time.time()
    
    # We will build a rolling walk-forward PyTorch model.
    # To keep the test fast, we will train one master model per month, not per day.
    
    all_test_dates = pd.date_range(start=start_date, end=end_date, freq='MS')
    periods = [(d, d + pd.offsets.MonthEnd(1)) for d in all_test_dates]
    
    for month_start, month_end in periods:
        test_mask = (df['Date'] >= month_start) & (df['Date'] <= month_end)
        if not test_mask.any(): continue
        
        test_indices = df[test_mask].index
        first_test_idx = test_indices[0]
        
        train_start = max(0, first_test_idx - 180) # Last 6 months for training data
        train_df = df.iloc[train_start:first_test_idx]
        
        if len(train_df) < 30: continue
            
        # Build Training Tensors
        X_dow, X_month, X_cont, y_train = [], [], [], []
        
        for idx, row in train_df.iterrows():
            t_date = row['Date']
            feats = build_features(df, t_date)
            for s in SLOT_NAMES:
                actual = row[s]
                if pd.isna(actual) or str(actual).strip() == "": continue
                actual = str(actual).split(',')[0].strip()
                if actual not in master_le.classes_: continue
                
                X_dow.append(row['dow'])
                X_month.append(row['month'])
                X_cont.append(feats[s])
                y_train.append(master_le.transform([actual])[0])
                
        if len(X_dow) == 0: continue
            
        t_dow = torch.tensor(X_dow, dtype=torch.long)
        t_month = torch.tensor(X_month, dtype=torch.long)
        t_cont = torch.tensor(X_cont, dtype=torch.float32)
        t_y = torch.tensor(y_train, dtype=torch.long)
        
        dataset = TensorDataset(t_dow, t_month, t_cont, t_y)
        loader = DataLoader(dataset, batch_size=64, shuffle=True)
        
        model = LogisticsDNN(num_classes)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.01)
        
        model.train()
        for epoch in range(15): # Fast 15 epochs per month
            for b_dow, b_month, b_cont, b_y in loader:
                optimizer.zero_grad()
                out = model(b_dow, b_month, b_cont)
                loss = criterion(out, b_y)
                loss.backward()
                optimizer.step()
                
        # Predict the month
        model.eval()
        month_correct = 0
        month_total = 0
        
        with torch.no_grad():
            for t_idx in test_indices:
                t_date = df.loc[t_idx, 'Date']
                row = df.loc[t_idx]
                feats = build_features(df, t_date)
                
                for s in SLOT_NAMES:
                    actual = row[s]
                    if pd.isna(actual) or str(actual).strip() == "": continue
                    actual = str(actual).split(',')[0].strip()
                    
                    if actual not in master_le.classes_:
                        total_slots += 1
                        continue
                        
                    inf_dow = torch.tensor([row['dow']], dtype=torch.long)
                    inf_month = torch.tensor([row['month']], dtype=torch.long)
                    inf_cont = torch.tensor([feats[s]], dtype=torch.float32)
                    
                    probs = model(inf_dow, inf_month, inf_cont).numpy()[0]
                    
                    # Get top 6
                    top_indices = probs.argsort()[-6:][::-1]
                    top_brands = master_le.inverse_transform(top_indices)
                    
                    if actual in top_brands:
                        correct_slots += 1
                        month_correct += 1
                    total_slots += 1
                    month_total += 1
                    
        print(f"[{month_end.strftime('%Y-%m')}] PyTorch Score: {((month_correct/month_total)*100) if month_total > 0 else 0:.2f}% | Accumulative: {((correct_slots/total_slots)*100):.2f}%", flush=True)

    overall_acc = (correct_slots / total_slots) * 100 if total_slots > 0 else 0
    print(f"\n✅ PyTorch DNN Backtest Finished! {time.time() - start_time:.2f} seconds.")
    print(f"Total Organic Accuracy (July 2024 - Dec 2025): {overall_acc:.2f}%")

if __name__ == "__main__":
    run_pytorch_backtest()
