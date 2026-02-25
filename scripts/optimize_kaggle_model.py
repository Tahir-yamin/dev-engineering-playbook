import pandas as pd
import numpy as np
import warnings
from collections import defaultdict
import time

warnings.filterwarnings('ignore')

df = pd.read_csv('d:/my-dev-knowledge-base/scripts/live_data_cache.csv')
df['Date'] = pd.to_datetime(df['Date'])
SLOTS = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]

def predict_bayesian_markov(df, slot_name, current_date, w_bayes, w_markov, w_global, window_days=180):
    target_dow = current_date.dayofweek
    mask = (df['Date'] < current_date) & (df['Date'] >= current_date - pd.Timedelta(days=window_days))
    history = df[mask].copy()
    
    if len(history) < 5: return ["-"] * 6
    history['dow'] = history['Date'].dt.dayofweek
    
    dow_history = history[history['dow'] == target_dow][slot_name].dropna().astype(str).str.strip().str.split(',').str[0]
    dow_history = dow_history[dow_history != ""]
    
    bayesian_scores = {}
    if len(dow_history) > 0:
        bayesian_scores = dow_history.value_counts(normalize=True).to_dict()

    seq = history[slot_name].dropna().astype(str).str.strip().str.split(',').str[0].tolist()
    seq = [x for x in seq if x != ""]
    
    markov_scores = {}
    if len(seq) > 1:
        yesterday_state = seq[-1]
        transitions = []
        for i in range(len(seq) - 1):
            if seq[i] == yesterday_state:
                transitions.append(seq[i+1])
        if transitions:
            markov_scores = pd.Series(transitions).value_counts(normalize=True).to_dict()
            
    recent_7 = df[(df['Date'] < current_date) & (df['Date'] >= current_date - pd.Timedelta(days=7))]
    if len(recent_7) > 0:
        global_7 = recent_7[SLOTS].values.flatten()
        global_7 = [str(x).strip().split(',')[0] for x in global_7 if pd.notna(x) and str(x).strip() != ""]
        global_counts = pd.Series(global_7).value_counts(normalize=True).to_dict() if global_7 else {}
    else:
        global_counts = {}

    final_scores = defaultdict(float)
    brands = set(list(bayesian_scores.keys()) + list(markov_scores.keys()) + list(global_counts.keys()))
    
    for b in brands:
        if b not in bayesian_scores and b not in markov_scores: continue
        pb = bayesian_scores.get(b, 0.0)
        pm = markov_scores.get(b, 0.0)
        pg = global_counts.get(b, 0.0)
        final_scores[b] = (pb * w_bayes) + (pm * w_markov) + (pg * w_global)
        
    ranked_brands = sorted(final_scores.items(), key=lambda item: item[1], reverse=True)
    top_6 = [brand for brand, score in ranked_brands[:6]]
    while len(top_6) < 6: top_6.append("-")
    return top_6

def run_grid_search():
    print("Optimization target: Jan 24 - Jan 31 (The user's high accuracy block)")
    test_dates = pd.date_range(start="2026-01-24", end="2026-01-31")
    
    best_acc = 0
    best_weights = ()
    
    weight_steps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    
    start_time = time.time()
    
    combinations = []
    for b in weight_steps:
        for m in weight_steps:
            for g in weight_steps:
                if abs((b + m + g) - 1.0) < 0.01:
                    combinations.append((b, m, g))
                    
    print(f"Testing {len(combinations)} weight combinations...")
    
    for w_bayes, w_markov, w_global in combinations:
        correct = 0
        total = 0
        
        for d in test_dates:
            target_mask = df['Date'] == d
            if not target_mask.any(): continue
            actuals = df[target_mask].iloc[0]
            
            for s in SLOTS:
                actual = str(actuals[s]).strip().split(',')[0]
                if not actual or actual == "nan" or actual == "-": continue
                
                preds = predict_bayesian_markov(df, s, d, w_bayes, w_markov, w_global)
                if actual in preds:
                    correct += 1
                total += 1
                
        if total > 0:
            acc = correct / total
            if acc > best_acc:
                best_acc = acc
                best_weights = (w_bayes, w_markov, w_global)
                print(f"New Best! (B:{w_bayes:.1f}, M:{w_markov:.1f}, G:{w_global:.1f}) -> Acc: {acc*100:.2f}%")
                
    print(f"\nOptimization Complete in {time.time()-start_time:.2f}s")
    print(f"Best Weights: Bayesian={best_weights[0]}, Markov={best_weights[1]}, Global={best_weights[2]}")
    print(f"Best Target Accuracy: {best_acc*100:.2f}%")

if __name__ == "__main__":
    run_grid_search()
