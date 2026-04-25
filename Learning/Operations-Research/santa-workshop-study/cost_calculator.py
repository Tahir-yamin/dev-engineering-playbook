import pandas as pd
import numpy as np

def calculate_cost(prediction_file, data_file):
    """
    Calculates the total cost for a submission.
    prediction_file: CSV with family_id and assigned_day.
    data_file: CSV with family preferences and sizes.
    """
    family_data = pd.read_csv(data_file, index_col='family_id')
    submission = pd.read_csv(prediction_file, index_col='family_id')
    
    # Merge for easier calculation
    df = submission.join(family_data)
    
    # 1. Preference Cost Calculation
    def get_pref_cost(row):
        day = row['assigned_day']
        n = row['n_people']
        if day == row['choice_0']: return 0
        elif day == row['choice_1']: return 50
        elif day == row['choice_2']: return 50 + 9 * n
        elif day == row['choice_3']: return 100 + 9 * n
        elif day == row['choice_4']: return 200 + 9 * n
        elif day == row['choice_5']: return 200 + 18 * n
        elif day == row['choice_6']: return 300 + 18 * n
        elif day == row['choice_7']: return 300 + 36 * n
        elif day == row['choice_8']: return 400 + 36 * n
        elif day == row['choice_9']: return 500 + 36 * n + 199 * n
        else: return 500 + 36 * n + 398 * n

    df['pref_cost'] = df.apply(get_pref_cost, axis=1)
    total_pref_cost = df['pref_cost'].sum()
    
    # 2. Accounting Penalty Calculation
    daily_occupancy = df.groupby('assigned_day')['n_people'].sum().reindex(range(1, 101), fill_value=0)
    
    # Check constraints
    if not daily_occupancy.between(125, 300).all():
        print("WARNING: Occupancy constraints violated (125-300 people/day).")
        # However, we calculate the penalty anyway for debugging
    
    accounting_penalty = 0
    # Day 101 occupancy is treated as same as Day 100
    daily_occupancy[101] = daily_occupancy[100]
    
    for d in range(100, 0, -1): # Counting backwards from 100 to 1
        nd = daily_occupancy[d]
        nd_plus_1 = daily_occupancy[d+1]
        
        diff = abs(nd - nd_plus_1)
        exponent = 0.5 + (diff / 50.0)
        day_penalty = (nd - 125.0) / 400.0 * (nd ** exponent)
        accounting_penalty += day_penalty
        
    print(f"Total Preference Cost:  {total_pref_cost:,.2f}")
    print(f"Total Accounting Cost:  {accounting_penalty:,.2f}")
    print(f"Grand Total Cost:       {total_pref_cost + accounting_penalty:,.2f}")
    
    return total_pref_cost + accounting_penalty

if __name__ == "__main__":
    import os
    data_path = 'data/family_data.csv'
    sample_path = 'data/sample_submission.csv'
    
    if os.path.exists(data_path) and os.path.exists(sample_path):
        calculate_cost(sample_path, data_path)
    else:
        print("Data files not found in data/ folder.")
