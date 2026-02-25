import pandas as pd

# File
ref_file = "d:/my-dev-knowledge-base/Rehabilitation of CF site MS. Globe FS, Karachi Division.xlsx"

try:
    print(f"Reading: {ref_file}")
    df = pd.read_excel(ref_file)
    
    print("\n--- Columns ---")
    print(list(df.columns))
    
    print("\n--- Project Summary Info ---")
    # Check for duration or start/finish columns
    for col in df.columns:
        if 'duration' in str(col).lower() or 'start' in str(col).lower() or 'finish' in str(col).lower():
            print(f"Col: {col} -> Example: {df[col].iloc[0]}")

    print("\n--- First 5 Rows ---")
    print(df.head().to_string())

except Exception as e:
    print(f"Error: {e}")
