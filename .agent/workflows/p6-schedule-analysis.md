---
description: Analyze Primavera P6 XER files for schedule health, critical path, and resource loading
---

# Primavera P6 Schedule Analysis Workflow

// turbo-all

## Prerequisites
- PyP6XER installed: `pip install pyp6xer`
- XER file exported from P6 Desktop

## Steps

### 1. Export XER from P6 Desktop
Open P6 Professional and export your project:
- File → Export → Primavera PM (XER)
- Save to `D:\P6_Exports\project.xer`

### 2. Parse XER File
```python
from pyp6xer import Xer
xer = Xer("D:/P6_Exports/project.xer")
print(f"Loaded: {xer.projects[0].proj_short_name}")
```

### 3. Generate Schedule Summary
```python
summary = {
    "project": xer.projects[0].proj_short_name,
    "activities": len(xer.activities),
    "resources": len(xer.resources),
    "wbs_elements": len(xer.wbs)
}
print(summary)
```

### 4. Critical Path Analysis
```python
critical = [a for a in xer.activities if a.driving_path_flag == "Y"]
print(f"Critical activities: {len(critical)}")
for act in critical[:10]:
    print(f"  {act.task_code}: {act.task_name}")
```

### 5. Schedule Health Check
```python
# Activities without logic
no_pred = [a for a in xer.activities if not a.predecessors]
no_succ = [a for a in xer.activities if not a.successors]
print(f"No predecessors: {len(no_pred)}")
print(f"No successors: {len(no_succ)}")

# Negative float
neg_float = [a for a in xer.activities if a.total_float_hr_cnt < 0]
print(f"Negative float: {len(neg_float)}")
```

### 6. Export to CSV
```python
import pandas as pd

data = [{
    'Code': a.task_code,
    'Name': a.task_name,
    'Duration': a.target_drtn_hr_cnt,
    'Start': a.target_start_date,
    'Finish': a.target_end_date,
    'Float': a.total_float_hr_cnt,
    'Critical': a.driving_path_flag
} for a in xer.activities]

df = pd.DataFrame(data)
df.to_csv("D:/P6_Exports/activities_report.csv", index=False)
print("Exported to activities_report.csv")
```

### 7. Generate Analysis Report
Create markdown report with findings:
- Total activities and milestones
- Critical path length
- Schedule health issues
- Resource utilization summary

## Related Skills
- [Primavera P6 Skills](file:///d:/my-dev-knowledge-base/skills/primavera-p6-skills.md)
