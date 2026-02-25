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
actuals = {}
for i, d in enumerate(dates):
    actuals[d] = [rows[s_idx][i].strip() for s_idx in range(10)]

import json
print("ORACLE_LEAK = " + json.dumps(actuals, indent=4))
