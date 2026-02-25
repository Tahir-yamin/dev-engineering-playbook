import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

JSON_KEYFILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', r'C:\Users\Administrator\Documents\mcp-sheets-key.json')
SHEET_ID = '1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY'

def evaluate_backtest():
    print("Connecting to Google Sheets to download Cloud_Backtest_24_26...")
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE, scopes)
    client = gspread.authorize(creds)
    
    ws = client.open_by_key(SHEET_ID).worksheet("Cloud_Backtest_24_26")
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    
    print(f"Successfully downloaded {len(df)} days of predictions.\n")
    
    # Clean the Accuracy column (convert "70.00%" string to 70.0 float)
    df['Accuracy_Num'] = df['Accuracy'].astype(str).str.replace('%', '').astype(float)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.quarter
    
    # 1. Global Metrics
    global_avg = df['Accuracy_Num'].mean()
    days_over_70 = len(df[df['Accuracy_Num'] >= 70.0])
    days_over_80 = len(df[df['Accuracy_Num'] >= 80.0])
    days_under_40 = len(df[df['Accuracy_Num'] <= 40.0])
    
    pct_over_70 = (days_over_70 / len(df)) * 100
    pct_over_80 = (days_over_80 / len(df)) * 100
    pct_under_40 = (days_under_40 / len(df)) * 100
    
    print("=== GLOBAL BENCHMARKS (2024-2026) ===")
    print(f"Total Days Analyzed: {len(df)}")
    print(f"Average Daily Accuracy: {global_avg:.2f}%")
    print(f"Days >= 70%: {days_over_70} ({pct_over_70:.2f}%)")
    print(f"Days >= 80%: {days_over_80} ({pct_over_80:.2f}%)")
    print(f"Severe Chaos Days (<= 40%): {days_under_40} ({pct_under_40:.2f}%)")
    
    # 2. Yearly Breakdown
    print("\n=== YEAR-OVER-YEAR PERFORMANCE ===")
    for year in df['Year'].unique():
        year_df = df[df['Year'] == year]
        y_avg = year_df['Accuracy_Num'].mean()
        y_over_70 = (len(year_df[year_df['Accuracy_Num'] >= 70.0]) / len(year_df)) * 100
        print(f"{year}: Average {y_avg:.2f}% | Hits >= 70%: {y_over_70:.2f}%")
        
    # 3. Quarterly Stability
    print("\n=== 2025 QUARTERLY STABILITY ===")
    df_2025 = df[df['Year'] == 2025]
    if len(df_2025) > 0:
        for q in sorted(df_2025['Quarter'].unique()):
            q_df = df_2025[df_2025['Quarter'] == q]
            q_avg = q_df['Accuracy_Num'].mean()
            q_over_70 = (len(q_df[q_df['Accuracy_Num'] >= 70.0]) / len(q_df)) * 100
            print(f"2025 Q{q}: Average {q_avg:.2f}% | Hits >= 70%: {q_over_70:.2f}%")

if __name__ == '__main__':
    evaluate_backtest()
