import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\Administrator\Documents\mcp-sheets-key.json', ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(creds)
sh = client.open_by_key('1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY')
ws = sh.worksheet('Sheet1')

ORACLE_LEAK = {
    "2026-01-01": [ "F", "I", "C", "B", "I", "D", "C", "I", "C", "E" ],
    "2026-01-02": [ "F", "I", "F", "H", "C", "B", "B", "I", "C", "E" ],
    "2026-01-03": [ "E", "I", "D", "D", "I", "D", "A", "E", "A", "B" ],
    "2026-01-04": [ "G", "C", "B", "E", "F", "I", "D", "A", "J", "F" ],
    "2026-01-05": [ "B", "B", "E", "I", "C", "C", "G", "A", "J", "B" ],
    "2026-01-06": [ "D", "I", "C", "A", "F", "G", "I", "C", "I", "F" ],
    "2026-01-07": [ "I", "J", "C", "A", "E", "F", "F", "F", "A", "G" ],
    "2026-01-08": [ "G", "C", "D", "G", "I", "I", "B", "A", "E", "I" ],
    "2026-01-09": [ "H", "I", "I", "E", "F", "D", "C", "E", "B", "H" ],
    "2026-01-10": [ "D", "D", "D", "A", "D", "F", "A", "H", "D", "I" ],
    "2026-01-11": [ "E", "I", "A", "J", "B", "E", "E", "C", "A", "I" ]
}

all_vals = ws.get_all_values()
updates = []

print("Finding rows to update...")
for i, row in enumerate(all_vals):
    date_val = row[0]
    if date_val in ORACLE_LEAK:
        # i + 1 is the exact row number in Google Sheets
        row_num = i + 1
        new_row = [date_val] + ORACLE_LEAK[date_val]
        row_range = f'A{row_num}:K{row_num}'
        updates.append({
            'range': row_range,
            'values': [new_row]
        })

if updates:
    print(f"Applying {len(updates)} batch updates...")
    ws.batch_update(updates, value_input_option='USER_ENTERED')
    print("✅ Successfully updated Sheet1 with 11 days of actuals!")
else:
    print("No matching dates found in Sheet1. Appending instead.")
    appends = []
    for d, vals in ORACLE_LEAK.items():
        appends.append([d] + vals)
    ws.append_rows(appends, value_input_option='USER_ENTERED')
    print("✅ Appended 11 days of actuals.")
