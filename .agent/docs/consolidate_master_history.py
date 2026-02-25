
import pandas as pd
import numpy as np
import os

# Paths
xlsx_2019_2023 = r"D:\Downloads\COMPLETE   DATA  2019 to  2023.xlsx"
txt_2024 = r"C:\Users\Administrator\Documents\user_actuals_2024.txt"
txt_2025 = r"C:\Users\Administrator\Documents\user_actuals_2025.txt"
output_csv = r"C:\Users\Administrator\Documents\Logistics_AI_Final_Release\Master_History_2019_2025.csv"

COL_MAP = {
    "Date": "Date",
    "PH01 OIL": "PH01 OIL", "PH1_Oil": "PH01 OIL",
    "PH01 GHEE": "PH01 GHEE", "PH1_Ghee": "PH01 GHEE",
    "PH02 OIL": "PH02 OIL", "PH2_Oil": "PH02 OIL",
    "PH02 GHEE": "PH02 GHEE", "PH2_Ghee": "PH02 GHEE",
    "PH03 OIL": "PH03 OIL", "PH3_Oil": "PH03 OIL",
    "PH03 GHEE": "PH03 GHEE", "PH3_Ghee": "PH03 GHEE",
    "PH04 OIL": "PH04 OIL", "PH4_Oil": "PH04 OIL",
    "PH04 GHEE": "PH04 GHEE", "PH4_Ghee": "PH04 GHEE",
    "PH05 OIL": "PH05 OIL", "PH5_Oil": "PH05 OIL",
    "PH05 GHEE": "PH05 GHEE", "PH5_Ghee": "PH05 GHEE"
}

TARGET_COLS = ["Date", "PH01 OIL", "PH01 GHEE", "PH02 OIL", "PH02 GHEE", "PH03 OIL", "PH03 GHEE", "PH04 OIL", "PH04 GHEE", "PH05 OIL", "PH05 GHEE"]

def clean_brand(val):
    if pd.isna(val) or str(val).strip() == "": return ""
    v = str(val).strip().upper()
    return v if len(v) == 1 and v.isalpha() else ""

def load_2019_2023():
    df = pd.read_excel(xlsx_2019_2023)
    # Rename matching columns
    df = df.rename(columns=COL_MAP)
    # Keep only relevant
    df = df[[c for c in df.columns if c in TARGET_COLS]]
    return df

def load_txt(path):
    rows = []
    with open(path, 'r') as f:
        for line in f:
            parts = line.split('\t')
            if len(parts) >= 12:
                # Date, DOW, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10
                date = parts[0].strip()
                brands = [p.strip().upper() for p in parts[2:12]]
                rows.append([date] + brands)
    df = pd.DataFrame(rows, columns=TARGET_COLS)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    return df

print("Merging Deep History (2019-2025)...")
df1 = load_2019_2023()
df2 = load_txt(txt_2024)
df3 = load_txt(txt_2025)

master = pd.concat([df1, df2, df3], ignore_index=True)
master['Date'] = pd.to_datetime(master['Date'], errors='coerce')
master = master.dropna(subset=['Date'])
master = master.sort_values('Date').drop_duplicates(subset=['Date'])

# Clean Brands
for col in TARGET_COLS[1:]:
    master[col] = master[col].apply(clean_brand)
    # Replace empty with NaN for fill
    master.loc[master[col] == "", col] = np.nan

# Forward fill gaps up to 3 days (normal operations)
master = master.ffill(limit=3)

master.to_csv(output_csv, index=False)
print(f"SUCCESS: Master dataset created with {len(master)} rows.")
print(f"Range: {master['Date'].min()} to {master['Date'].max()}")
