import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime

creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\Administrator\Documents\mcp-sheets-key.json', ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(creds)
sh = client.open_by_key('1w_0p4yCFGaYvROFntaynCUDqOOEuTzgvoSZYhTv5FpY')
ws = sh.worksheet('Sheet1')

data_str = """
F	F	E	G	B	D	I	G	H	D	E
I	I	I	C	B	I	J	C	I	D	I
C	F	D	B	E	C	C	D	I	D	A
B	H	D	E	I	A	A	G	E	A	J
I	C	I	F	C	F	E	I	F	D	B
D	B	D	I	C	G	F	I	D	F	E
C	B	A	D	G	I	F	B	C	A	E
I	I	E	A	A	C	F	A	E	H	C
C	C	A	J	J	I	A	E	B	D	A
E	E	B	F	B	F	G	I	H	I	I
"""

dates = ['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04', '2026-01-05',
         '2026-01-06', '2026-01-07', '2026-01-08', '2026-01-09', '2026-01-10', '2026-01-11']

rows = [l.split('\t') for l in data_str.strip().split('\n')]
append_data = []

for i, d in enumerate(dates):
    # Construct a row: Date, slot1, slot2...
    row = [d]
    for s_idx in range(10):
        row.append(rows[s_idx][i].strip())
    # The sheet is columns A-K (Date + 10 slots).
    append_data.append(row)

# Get current data to ensure no overlap
current_data = ws.get_all_values()
existing_dates = [r[0] for r in current_data]

rows_to_append = []
for r in append_data:
    if r[0] not in existing_dates:
        rows_to_append.append(r)

if rows_to_append:
    print(f"Appending {len(rows_to_append)} rows to Sheet1...")
    ws.append_rows(rows_to_append, value_input_option='USER_ENTERED')
    print("✅ Successfully appended.")
else:
    print("Dates already exist in Sheet1.")
