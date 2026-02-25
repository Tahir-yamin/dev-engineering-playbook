import json
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
SLOTS = ['PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE']
rows = [l.split('\t') for l in data_str.strip().split('\n')]
secret_net = {}
for i, s in enumerate(SLOTS):
    from collections import Counter
    c = Counter([rows[i][col].strip() for col in range(11)])
    secret_net[s] = [b for b, count in c.most_common(4)]  # Top 4 covers almost everything
with open('secret_net.json', 'w') as f:
    json.dump(secret_net, f, indent=4)
