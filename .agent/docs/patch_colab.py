import json

path = r'C:\Users\Administrator\Documents\Logistics_AI_Final_Release\Logistics_v14_Cloud_Engine.ipynb'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for cell in data['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        for i, line in enumerate(source):
            if "df = df.sort_values('Date')" in line:
                source[i] = "df = df.sort_values('Date').reset_index(drop=True)\n"
                source.insert(i+1, "if len(df) > 180:\n")
                source.insert(i+2, "    df = df.tail(180).reset_index(drop=True)\n")
                break
                
        for i, line in enumerate(source):
            if "df_feat[f\'_{s}_p365\'] = df_feat[f\'_{s}_enc\'].shift(365).fillna(-1)" in line:
                source[i] = "    df_feat[f\'_{s}_p14\'] = df_feat[f\'_{s}_enc\'].shift(14).fillna(-1)\n"
                source.insert(i+1, "    df_feat[f\'_{s}_p30\'] = df_feat[f\'_{s}_enc\'].shift(30).fillna(-1)\n")
                break
                
        for i, line in enumerate(source):
            if "f_cols = base_f + [f\'_{s}_p1\', f\'_{s}_p7\', f\'_{s}_p365\']" in line:
                source[i] = "    f_cols = base_f + [f\'_{s}_p1\', f\'_{s}_p7\', f\'_{s}_p14\', f\'_{s}_p30\']\n"
                break
                
        for i, line in enumerate(source):
            if "weights[-30:] = 2.0" in line:
                source[i] = "    if len(weights) > 30: weights[-30:] = 2.0\n"
                source.insert(i+1, "    if len(weights) > 7: weights[-7:] = 5.0\n")
                break
                
        for i, line in enumerate(source):
            if "p365 = enc.transform([hs[-365]])[0] if len(hs)>=365 and hs[-365] in enc.classes_ else -1" in line:
                source[i] = "        p14 = enc.transform([hs[-14]])[0] if len(hs)>=14 and hs[-14] in enc.classes_ else -1\n"
                source.insert(i+1, "        p30 = enc.transform([hs[-30]])[0] if len(hs)>=30 and hs[-30] in enc.classes_ else -1\n")
                break

        for i, line in enumerate(source):
            if "feat = np.array([[dw, dom, m, woy, msin, mcos, p1, p7, p365]])" in line:
                source[i] = "        feat = np.array([[dw, dom, m, woy, msin, mcos, p1, p7, p14, p30]])\n"
                break

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
print('Patched Colab Notebook.')
