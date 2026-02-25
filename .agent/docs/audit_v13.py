
import pandas as pd

# Provided Actuals from user
actuals_data = {
    "2026-01-22": ["A","D","J","J","J","D","C","H","C","D"],
    "2026-01-23": ["G","H","E","G","A","D","C","D","C","D"],
    "2026-01-24": ["B","D","I","I","C","J","G","A","C","I"],
    "2026-01-25": ["D","C","E","I","C","H","A","G","F","C"],
    "2026-01-26": ["A","C","H","A","F","F","J","C","G","A"],
    "2026-01-27": ["B","D","E","A","I","B","D","A","C","H"],
    "2026-01-28": ["E","D","B","B","G","J","D","G","C","G"],
    "2026-01-29": ["D","A","C","J","H","H","B","A","G","E"]
}

# Load v13 Predictions
pred_path = r"C:\Users\Administrator\Documents\Logistics_AI_Final_Release\Jan_2026_v13_Backtest.csv"
p_df = pd.read_csv(pred_path)
p_df['Date'] = pd.to_datetime(p_df['Date']).dt.strftime('%Y-%m-%d')

SLOTS = ["PH01 OIL","PH01 GHEE","PH02 OIL","PH02 GHEE","PH03 OIL","PH03 GHEE","PH04 OIL","PH04 GHEE","PH05 OIL","PH05 GHEE"]

print("="*50)
print(" v13.0 DEEP HORIZON: JAN 2026 BACKTEST AUDIT")
print("="*50)

summary = []
for date_str, actual_list in actuals_data.items():
    row_pred = p_df[p_df['Date'] == date_str]
    if row_pred.empty: continue
    
    matches = 0
    for i, slot in enumerate(SLOTS):
        pred_top6 = row_pred.iloc[0][slot].split(",")
        if actual_list[i] in pred_top6:
            matches += 1
    
    acc = (matches / 10) * 100
    print(f"{date_str}  Actual: {acc}%")
    summary.append(acc)

print("-" * 50)
print(f"v13.0 AVERAGE JAN ACCURACY: {sum(summary)/len(summary):.1f}%")
print("="*50)
