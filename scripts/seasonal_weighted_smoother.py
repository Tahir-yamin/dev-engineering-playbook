import pandas as pd
from collections import defaultdict, Counter
import warnings
import os

warnings.filterwarnings('ignore')

# Weights
WEIGHT_180 = 0.15
WEIGHT_30 = 0.25
WEIGHT_7 = 0.40
WEIGHT_SQLY = 0.20  # Same Quarter Last Year

def get_day_volatility_weight(day_row, slots):
    """
    Applies the User's Extreme Outlier Floor and 10% Volatility penalty.
    """
    brands = [str(day_row[s]).strip() for s in slots if pd.notna(day_row[s]) and str(day_row[s]).strip() != '']
    if len(brands) == 0:
        return 0.0
        
    c = Counter(brands)
    top_6_count = sum([val for key, val in c.most_common(6)])
    concentration = top_6_count / len(brands)
    
    if concentration < 0.40:
        return 0.01  # EXTREME OUTLIER: 1% weight (effectively ignoring it without throwing error)
    elif concentration < 0.70:
        return 0.10  # 10% weight for chaotic days
    else:
        return 1.00  # 100% weight for structured days

def predict_seasonal_smoother(df_history, target_date):
    """
    4-Weight probability, including Seasonality and Extreme Outlier filtering.
    """
    slots = ['PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE']

    if isinstance(target_date, str):
        target_date = pd.to_datetime(target_date)

    end_date = target_date
    start_180 = end_date - pd.Timedelta(days=180)
    start_30 = end_date - pd.Timedelta(days=30)
    start_7 = end_date - pd.Timedelta(days=7)
    
    # Seasonal (SQLY) Lookback: 1 full year ago, +/- 45 days (90 day quarter window)
    sql_target = end_date - pd.Timedelta(days=365)
    start_sqly = sql_target - pd.Timedelta(days=45)
    end_sqly = sql_target + pd.Timedelta(days=45)

    df_180 = df_history[(df_history['Date'] >= start_180) & (df_history['Date'] < end_date)]
    df_30 = df_history[(df_history['Date'] >= start_30) & (df_history['Date'] < end_date)]
    df_7 = df_history[(df_history['Date'] >= start_7) & (df_history['Date'] < end_date)]
    df_sqly = df_history[(df_history['Date'] >= start_sqly) & (df_history['Date'] < end_sqly)]

    def get_weighted_counts(temp_df):
        counts = defaultdict(float)
        for _, row in temp_df.iterrows():
            day_weight = get_day_volatility_weight(row, slots)
            for s in slots:
                if s in temp_df.columns:
                    val = row[s]
                    if pd.notna(val) and str(val).strip() != '':
                        counts[str(val).strip()] += (1.0 * day_weight)
        return counts

    counts_180 = get_weighted_counts(df_180)
    counts_30 = get_weighted_counts(df_30)
    counts_7 = get_weighted_counts(df_7)
    counts_sqly = get_weighted_counts(df_sqly)

    all_brands = set(list(counts_180.keys()) + list(counts_30.keys()) + list(counts_7.keys()) + list(counts_sqly.keys()))
    brand_scores = {}
    
    for brand in all_brands:
        score = (counts_180.get(brand, 0) * WEIGHT_180) + \
                (counts_30.get(brand, 0) * WEIGHT_30) + \
                (counts_7.get(brand, 0) * WEIGHT_7) + \
                (counts_sqly.get(brand, 0) * WEIGHT_SQLY)
                
        tie_breaker = 0
        if isinstance(brand, str) and len(brand) > 0:
            char_val = ord(brand.upper()[0])
            tie_breaker = (100 - char_val) / 1000.0
            
        brand_scores[brand] = score + tie_breaker

    sorted_brands = sorted(brand_scores.items(), key=lambda x: x[1], reverse=True)
    top_6 = [brand for brand, score in sorted_brands[:6]]
    
    defaults = ['A', 'B', 'C', 'D', 'E', 'F']
    for db in defaults:
        if len(top_6) < 6 and db not in top_6:
            top_6.append(db)
            
    return top_6

def run_backtest():
    print("Initiating Seasonal + Extreme Outlier Smoother Backtest (Jan 2026 Sample)...")
    
    df = pd.read_csv('d:/my-dev-knowledge-base/scripts/live_data_cache_fresh.csv')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date']).copy()
    
    # Just running January 2026 quickly to see if Seasonal + Outlier Drop improves the baseline
    df_jan = df[(df['Date'] >= '2026-01-01') & (df['Date'] <= '2026-01-30')]
    test_dates = df_jan['Date'].dt.date.unique()
    
    slots = ['PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE']
    
    daily_accuracies = []
    
    for i, date in enumerate(test_dates):
        current_date_obj = pd.to_datetime(date)
        
        top_6_weighted = predict_seasonal_smoother(df, current_date_obj)
        
        day_df = df[df['Date'].dt.date == date]
        
        day_hits = 0
        day_preds = 0
        
        for _, row in day_df.iterrows():
            for slot in slots:
                actual = row[slot]
                if pd.notna(actual) and str(actual).strip() != '':
                    day_preds += 1
                    if str(actual).strip() in top_6_weighted:
                        day_hits += 1
                        
        if day_preds > 0:
            acc = (day_hits / day_preds) * 100
            daily_accuracies.append((str(date), acc))

    avg = sum([x[1] for x in daily_accuracies]) / len(test_dates) if test_dates.size > 0 else 0
    days_over_70 = sum([1 for x in daily_accuracies if x[1] >= 70.0])
    success_rate = (days_over_70 / len(test_dates)) * 100 if test_dates.size > 0 else 0
    
    print(f"\nAverage Jan Accuracy: {avg:.2f}%")
    print(f"Days >= 70%: {success_rate:.2f}%")

if __name__ == '__main__':
    run_backtest()
