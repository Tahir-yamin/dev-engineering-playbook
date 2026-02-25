import pandas as pd
import ast

with open(r'd:\my-dev-knowledge-base\cloud_january_predictions.txt', 'r', encoding='utf-16le') as f:
    lines = f.readlines()

preds = {}
cur_date = None
for l in lines:
    l = l.strip()
    if l.startswith('Date: '):
        cur_date = l.split('Date: ')[1]
        preds[cur_date] = []
    elif ':' in l and '[' in l and cur_date is not None:
        arr = ast.literal_eval(l.split(': ')[1])
        preds[cur_date].append(arr)

jan7 = preds.get('07/01/2026', [])

print('AI Predictions for Jan 7 (which scored 50%):')
SLOTS = ['PH01 OIL', 'PH01 GHEE', 'PH02 OIL', 'PH02 GHEE', 'PH03 OIL', 'PH03 GHEE', 'PH04 OIL', 'PH04 GHEE', 'PH05 OIL', 'PH05 GHEE']
for i, s in enumerate(SLOTS):
    if i < len(jan7):
        print(s, jan7[i])
