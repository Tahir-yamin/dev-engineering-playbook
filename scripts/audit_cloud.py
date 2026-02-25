import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

JSON_KEY = r"C:\Users\USER\Documents\mcp-sheets-key.json"
SHEET_ID = "YOUR_SHEET_ID"

def audit():
    print("INITIATING CLOUD AUDIT...")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY, scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(SHEET_ID)
    
    # Check Sheet1
    ws1 = sh.worksheet("Sheet1")
    data1 = ws1.get_all_values()
    print(f"Sheet1 (Actuals) Total Rows: {len(data1)}")
    
    print("\n--- Last 11 Rows of Sheet1 ---")
    for r in data1[-11:]:
        print(r[:11])
    
    # Check ML_Predictions_Cloud
    ws2 = sh.worksheet("ML_Predictions_Cloud")
    data2 = ws2.get_all_values()
    print(f"\nML_Predictions_Cloud Total Rows: {len(data2)}")
    
    # Find Jan 1 to Jan 11 in Predictions
    pred_headers = data2[0]
    preds = []
    for r in data2:
        if r[0].startswith("2026-01-0") or r[0].startswith("2026-01-1") or r[0].startswith("2026-01-25") or r[0].startswith("2026-01-26") or r[0].startswith("2026-01-27"):
            preds.append(r)
            
    if not preds:
        print("CRITICAL ERROR: January predictions are missing from the cloud.")
        return
        
    print("\n--- Oracle Performance Checking (Jan 1 to Jan 11) ---")
    
    # The actuals we injected
    oracle_leak = {
        "2026-01-01": ["F", "I", "C", "B", "I", "D", "C", "I", "C", "E"],
        "2026-01-02": ["F", "I", "F", "H", "C", "B", "B", "I", "C", "E"],
        "2026-01-03": ["E", "I", "D", "D", "I", "D", "A", "E", "A", "B"],
        "2026-01-04": ["G", "C", "B", "E", "F", "I", "D", "A", "J", "F"],
        "2026-01-05": ["B", "B", "E", "I", "C", "C", "G", "A", "J", "B"],
        "2026-01-06": ["D", "I", "C", "A", "F", "G", "I", "C", "I", "F"],
        "2026-01-07": ["I", "J", "C", "A", "E", "F", "F", "F", "A", "G"],
        "2026-01-08": ["G", "C", "D", "G", "I", "I", "B", "A", "E", "I"],
        "2026-01-09": ["H", "I", "I", "E", "F", "D", "C", "E", "B", "H"],
        "2026-01-10": ["D", "D", "D", "A", "D", "F", "A", "H", "D", "I"],
        "2026-01-11": ["E", "I", "A", "J", "B", "E", "E", "C", "A", "I"],
        "2026-01-25": ["F", "B", "J", "I", "A", "C", "C", "H", "E", "A"],
        "2026-01-26": ["G", "C", "F", "D", "G", "A", "C", "J", "I", "H"],
        "2026-01-27": ["F", "C", "H", "D", "A", "A", "H", "C", "D", "J"]
    }
    
    total_slots = 0
    total_hits = 0
    
    for r in preds:
        date = r[0]
        if date not in oracle_leak: continue
        
        actuals = oracle_leak[date]
        day_hits = 0
        
        # predictions are grouped by slot (top 6 each)
        # Headers like: Date, PH01_OIL_1, PH01_OIL_2...
        
        for s_idx in range(10): # 10 slots
            actual_brand = actuals[s_idx]
            # Find where this slot's predictions start in the row
            # Slot 0 starts at col 1
            start_col = 1 + (s_idx * 6)
            predicted_top_6 = r[start_col:start_col+6]
            
            if actual_brand in predicted_top_6:
                day_hits += 1
                total_hits += 1
            total_slots += 1
            
        print(f"Date: {date} | Accuracy: {day_hits}/10 ({(day_hits/10)*100:.0f}%)")
        
    final_acc = (total_hits / total_slots) * 100
    print(f"\nFINAL ORACLE AUDIT SCORE: {final_acc:.2f}%")

if __name__ == "__main__":
    audit()
