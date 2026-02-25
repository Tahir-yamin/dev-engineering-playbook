import pandas as pd

file_path = "d:/my-dev-knowledge-base/Rehabilitation of CF site MS. Globe FS, Karachi Division.xlsx"
try:
    df = pd.read_excel(file_path)
    print("Columns found:")
    for col in df.columns:
        print(f"'{col}'")
except Exception as e:
    print(e)
