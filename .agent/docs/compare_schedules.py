import pandas as pd

# Files
ref_file = "d:/my-dev-knowledge-base/Rehabilitation of CF site MS. Globe FS, Karachi Division.xlsx"
v7_file = "d:/my-dev-knowledge-base/Project_Schedule_MSP_Export_v7.xlsx"

try:
    # Read Reference
    print(f"Reading Reference: {ref_file}")
    df_ref = pd.read_excel(ref_file)
    # Identify task column in ref
    if 'Name' in df_ref.columns:
        ref_task_col = ['Name']
    else:
        ref_task_col = [c for c in df_ref.columns if 'name' in str(c).lower() and 'task' in str(c).lower()]
    if not ref_task_col:
         ref_task_col = [c for c in df_ref.columns if 'activity' in str(c).lower()]
    
    if ref_task_col:
        ref_tasks = df_ref[ref_task_col[0]].dropna().unique().tolist()
        print(f"Found {len(ref_tasks)} tasks in Reference.")
    else:
        print("Could not identify Task column in Reference file.")
        ref_tasks = []

    # Read V7
    print(f"Reading V7: {v7_file}")
    df_v7 = pd.read_excel(v7_file)
    v7_tasks = df_v7['Task Name'].dropna().unique().tolist()
    print(f"Found {len(v7_tasks)} tasks in V7.")

    # Compare
    # Normalize for comparison (lowercase, strip, remove generic words if needed)
    def normalize(text):
        return str(text).lower().strip().replace(" ", "")

    v7_norm = set([normalize(t) for t in v7_tasks])
    
    missing_in_v7 = []
    for t in ref_tasks:
        if normalize(t) not in v7_norm:
            missing_in_v7.append(t)

    with open("d:/my-dev-knowledge-base/comparison_results.txt", "w") as f:
        f.write(f"Reference Tasks: {len(ref_tasks)}\n")
        f.write(f"V7 Tasks: {len(v7_tasks)}\n")
        f.write(f"Missing in V7 ({len(missing_in_v7)}):\n")
        for t in missing_in_v7:
            f.write(f"- {t}\n")
    print("Comparison saved to comparison_results.txt")

except Exception as e:
    print(f"Error: {e}")
