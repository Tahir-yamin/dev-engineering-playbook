import pandas as pd
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

def run_global_smoother_backtest():
    print("Initializing Global Smoothing Emulator (Same Value All Day)...")
    df = pd.read_csv('d:/my-dev-knowledge-base/scripts/live_data_cache_fresh.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    slots = ['PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE']
    
    df_jan = df[(df['Date'] >= '2026-01-01') & (df['Date'] <= '2026-01-30')]
    
    daily_accuracies = []
    
    for date in df_jan['Date'].dt.date.unique():
        date_str = str(date)
        current_date = pd.to_datetime(date)
        
        # Calculate GLOBAL Top 6 based on the last 7 days of momentum
        # and apply it to ALL 10 slots (All Day Same Value)
        history_df = df[(df['Date'] < current_date) & (df['Date'] >= current_date - pd.Timedelta(days=7))]
        
        global_counts = Counter()
        for idx, row in history_df.iterrows():
            for slot in slots:
                val = row[slot]
                if pd.notna(val) and str(val).strip() != '':
                    global_counts[str(val).strip()] += 1
                    
        # Get the global top 6
        top_6_brands = [brand for brand, count in global_counts.most_common(6)]
        
        # Fill in generic brands if we don't have enough history
        default_brands = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for db in default_brands:
            if len(top_6_brands) < 6 and db not in top_6_brands:
                top_6_brands.append(db)
                
        # Now evaluate this STATIC "All Day Same Value" against the actuals
        day_df = df_jan[df_jan['Date'].dt.date == date]
        
        day_hits = 0
        day_preds = 0
        
        for idx, row in day_df.iterrows():
            for slot in slots:
                actual = row[slot]
                if pd.notna(actual) and str(actual).strip() != '':
                    day_preds += 1
                    if str(actual).strip() in top_6_brands:
                        day_hits += 1
                        
        if day_preds > 0:
            daily_acc = (day_hits / day_preds) * 100
            daily_accuracies.append((date_str, daily_acc))
            
    print("\n--- Daily Accuracy of 'All Day Same Value' (Global Top 6) ---")
    sum_acc = 0
    over_70_count = 0
    for date_str, acc in daily_accuracies:
        print(f"{date_str}: {acc:.2f}% | Top 6: {top_6_brands}")
        sum_acc += acc
        if acc >= 70.0:
            over_70_count += 1
            
    avg = sum_acc / len(daily_accuracies) if daily_accuracies else 0
    success_rate = (over_70_count / len(daily_accuracies)) * 100 if daily_accuracies else 0
    
    print(f"\nAverage Jan Accuracy: {avg:.2f}%")
    print(f"Days >= 70%: {success_rate:.2f}%")

if __name__ == '__main__':
    run_global_smoother_backtest()
