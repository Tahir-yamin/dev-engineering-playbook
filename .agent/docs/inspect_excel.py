import pandas as pd

file_path = "d:/my-dev-knowledge-base/Rehabilitation of CF site MS. Globe FS, Karachi Division.xlsx"

try:
    # Read the Excel file
    xl = pd.ExcelFile(file_path)
    print(f"Sheet names: {xl.sheet_names}")
    
    # Read the first sheet
    df = xl.parse(xl.sheet_names[0])
    print("\nFirst 20 rows of the first sheet:")
    print(df.head(20).to_string())
    
    # Try to identify task names
    # Look for columns like "Activity", "Task", "Description"
    possible_cols = [c for c in df.columns if isinstance(c, str) and any(x in c.lower() for x in ['activity', 'task', 'desc', 'name', 'item'])]
    print(f"\nPossible Task Columns: {possible_cols}")

except Exception as e:
    print(f"Error reading file: {e}")
