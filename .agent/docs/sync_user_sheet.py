
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np

JSON_KEY = r"C:\Users\Administrator\Documents\mcp-sheets-key.json"
NEW_SHEET_ID = "1PjBY8-h7kBYJEXLK1Qp8dFRrWRTNHJ81HfOCSEtOLjE"
MASTER_SHEET_ID = "1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY"

# Since the column headers in the new sheet don't match the standard "PH01 OIL" format perfectly,
# we map them over cleanly.
SLOT_MAP = {
    'PAKWAN HOUSE 01 ( OIL ) 01 PM': 'PH01 OIL',
    'PAKWAN HOUSE 01 ( GHEE ) 01 PM': 'PH01 GHEE',
    'PAKWAN HOUSE 02 ( OIL ) 02 PM': 'PH02 OIL',
    'PAKWAN HOUSE 02 ( GHEE ) 02 PM': 'PH02 GHEE',
    'PAKWAN HOUSE 03 ( OIL ) 04 PM': 'PH03 OIL',
    'PAKWAN HOUSE 03 ( GHEE ) 08 PM': 'PH03 GHEE', # Note the 08 PM here
    'PAKWAN HOUSE 04 ( OIL ) 06 PM': 'PH04 OIL',
    'PAKWAN HOUSE 04 ( GHEE ) 06 PM': 'PH04 GHEE',
    'PAKWAN HOUSE 05 ( OIL ) 09 PM': 'PH05 OIL',
    'PAKWAN HOUSE 05 ( GHEE ) 09 PM': 'PH05 GHEE',
}

def sync_and_heal_data():
    print("Connecting to Google Sheets...")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh_new = client.open_by_key(NEW_SHEET_ID)
    
    all_dfs = []
    print("Pulling tabs: 2019_to_2023, 2024, 2025")
    for title in ['2019_to_2023', '2024', '2025']:
        ws = sh_new.worksheet(title)
        data = ws.get_all_values()
        if data:
            df = pd.DataFrame(data[1:], columns=data[0])
            all_dfs.append(df)
            
    df_combined = pd.concat(all_dfs, ignore_index=True)
    df_combined.rename(columns=SLOT_MAP, inplace=True)
    
    # We enforce exact column names so the ML model always expects the same inputs
    cols_to_keep = ['Date', 'PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE']
    
    # Clean out empty rows
    df_combined = df_combined.dropna(subset=['Date'])
    df_combined = df_combined[df_combined['Date'].str.strip() != '']
    
    # Extract only our mapped columns
    final_cols = [c for c in cols_to_keep if c in df_combined.columns]
    
    # Ensure missing columns (if any tab didn't have them) are created as empty
    for c in cols_to_keep:
        if c not in final_cols:
            df_combined[c] = ""
            
    df_filtered = df_combined[cols_to_keep]
    
    # Format dates
    df_filtered['Date'] = pd.to_datetime(df_filtered['Date'], format='mixed', dayfirst=True, errors='coerce')
    df_filtered = df_filtered.dropna(subset=['Date'])
    
    # --- HEALING THE MISSING DAYS ---
    df_filtered = df_filtered.set_index('Date').sort_index()
    full_date_range = pd.date_range(start='2019-01-01', end='2025-12-31')
    
    print(f"Original unique dates found: {len(df_filtered.index.unique())} (Should be 2557)")
    
    # Reindex to ensure all dates are present (adds missing days as empty rows)
    df_healed = df_filtered[~df_filtered.index.duplicated(keep='first')]
    df_healed = df_healed.reindex(full_date_range)
    
    # Forward fill the missing days (standard ML practice for missing continuous operations data)
    df_healed = df_healed.fillna(method='ffill')
    df_healed = df_healed.fillna("") # Fill anything at the very start that couldn't be forward-filled
    
    df_healed = df_healed.reset_index().rename(columns={'index': 'Date'})
    df_healed['Date'] = df_healed['Date'].dt.strftime('%Y-%m-%d')
    
    print(f"Healed missing gaps. Final continuous row count: {len(df_healed)}")
    
    # Write to Cloud Master (Sheet1)
    sh_master = client.open_by_key(MASTER_SHEET_ID)
    ws_master = sh_master.worksheet("Sheet1")
    ws_master.clear()
    
    upload_data = [df_healed.columns.tolist()] + df_healed.values.tolist()
    ws_master.update('A1', upload_data, value_input_option='USER_ENTERED')
    print("✅ New continuous verified dataset (2019-2025) successfully pushed to Cloud Master!")

if __name__ == "__main__":
    sync_and_heal_data()
