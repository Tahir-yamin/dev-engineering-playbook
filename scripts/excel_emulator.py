import pandas as pd

# This script emulates exactly what the Excel file does due to its copy-paste glitch.
def run_emulator_backtest():
    print("Initializing Excel Emulator (Static Loop)...")
    
    # Load the fresh data
    df = pd.read_csv('d:/my-dev-knowledge-base/scripts/live_data_cache_fresh.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter for January 2026 to see what the accuracy is
    df_jan = df[(df['Date'] >= '2026-01-01') & (df['Date'] <= '2026-01-30')]
    
    slots = ['PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE']
    
    total_predictions = 0
    total_hits = 0
    
    # The Excel file's Rank 1 to 6 for EVERY slot is mathematically locked to J, I, H, G, F, E
    # because every row has the same base score, and the tie-breaker is +ROW()/1000.
    # Highest row wins. Row 15 = J, Row 14 = I, ..., Row 10 = E.
    static_prediction = ['J', 'I', 'H', 'G', 'F', 'E']
    
    daily_accuracies = []
    
    for date in df_jan['Date'].dt.date.unique():
        date_str = str(date)
        day_df = df_jan[df_jan['Date'].dt.date == date]
        
        day_hits = 0
        day_preds = 0
        
        for index, row in day_df.iterrows():
            for slot_col in slots:
                actual_brand = row[slot_col]
                if pd.isna(actual_brand) or str(actual_brand).strip() == '':
                    continue
                
                day_preds += 1
                total_predictions += 1
                
                if str(actual_brand) in static_prediction:
                    day_hits += 1
                    total_hits += 1
                    
        if day_preds > 0:
            daily_acc = (day_hits / day_preds) * 100
            daily_accuracies.append((date_str, daily_acc))
            
    print("\n--- Daily Accuracy of the Static Excel Emulator ---")
    for date_str, acc in daily_accuracies:
        print(f"{date_str}: {acc:.2f}%")
        
    avg_acc = sum([acc for _, acc in daily_accuracies]) / len(daily_accuracies) if daily_accuracies else 0
    print(f"\nAverage Accuracy for Jan 2026: {avg_acc:.2f}%")

if __name__ == "__main__":
    run_emulator_backtest()
