import re
import json

file_path = r"D:\my-dev-knowledge-base\sap_pr_content.txt"
output_path = r"D:\my-dev-knowledge-base\parsed_pr_items.json"

def parse_pr_file(file_path):
    items = []
    # Regex for lines like: 1.017 WIRING FOR LIGHT POLES 300.00 RFT 600.00 180,000.00
    # Capture groups: 1=ItemNo, 2=Description, 3=Qty, 4=Unit
    # The price/amount are at the end, usually separated by spaces.
    # Note: Description might contain spaces.
    # Structure: No <space> Desc <space> Qty <space> Unit <space>
    
    # Improved regex to handle the variable whitespace and fields
    # Looking for a number at the start, followed by text, then a float, then a unit (string), then floats.
    item_pattern = re.compile(r"^(\d+(\.\d+)?)\s+(.+?)\s+(\d+(\.\d+)?)\s+([A-Za-z]+)\s+[\d,.]+")
    
    # Also handle the integer items like "2 Air Conditioner..." if they exist and follow a similar pattern
    # 3091: 2 Air Conditioner Split 1.5 Ton 4.00 EA
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_item = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line matches an item definition
        match = item_pattern.match(line)
        if match:
            # simple heuristic: if it looks like a line item row
            # It usually ends with price/amount which are numbers.
            # Let's verify if the last parts are numbers to reduce false positives
            parts = line.split()
            if len(parts) > 3:
                # check if the last few are numbers (Price, Amount)
                # But sometimes "Plant" or "Stock" columns might be there.
                # Let's rely on the regex capture.
                
                item_no = match.group(1)
                description = match.group(3)
                qty = match.group(4)
                unit = match.group(6)
                
                items.append({
                    "item_no": item_no,
                    "description": description,
                    "qty": qty,
                    "unit": unit,
                    "full_line": line
                })

    return items

try:
    data = parse_pr_file(file_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Successfully parsed {len(data)} items to {output_path}")
    # Print first few to verify
    for i in data[:5]:
        print(i)
except Exception as e:
    print(f"Error parsing file: {e}")
