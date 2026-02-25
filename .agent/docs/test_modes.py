import pandas as pd
from collections import Counter

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
SLOTS = ['PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE']

rows = [l.split('\t') for l in data_str.strip().split('\n')]
for i, s in enumerate(SLOTS):
    slot_actuals = [rows[i][col].strip() for col in range(11)]
    c = Counter(slot_actuals)
    print(f"{s} Test Modes:", c.most_common(10))
