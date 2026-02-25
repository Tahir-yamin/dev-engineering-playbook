import pandas as pd
try:
    df = pd.read_excel("d:/my-dev-knowledge-base/Rehabilitation of CF site MS. Globe FS, Karachi Division.xlsx")
    print(list(df.columns))
except Exception as e:
    print(e)
