# Microsoft Project Integration Skills

> **Purpose**: Automate and analyze MS Project 2016 files (.mpp) using Python tools.

## 🛠️ Installed Tools

| Tool | Purpose | Status |
|------|---------|--------|
| **pywin32** | COM automation for MS Project | ✅ Installed |
| **aspose-tasks** | MPP file parsing (no MS Project needed) | ✅ Installed |
| **PyAutoGUI** | GUI automation fallback | ✅ Installed |

---

## 📁 MPP File Parsing (Without MS Project)

### Read Project File
```python
import aspose.tasks as tasks

# Load MPP file
project = tasks.Project("D:/Projects/myproject.mpp")

# Project info
print(f"Project: {project.get(tasks.Prj.NAME)}")
print(f"Start: {project.get(tasks.Prj.START_DATE)}")
print(f"Finish: {project.get(tasks.Prj.FINISH_DATE)}")
```

### List All Tasks
```python
import aspose.tasks as tasks

project = tasks.Project("myproject.mpp")

for task in project.root_task.children:
    print(f"{task.get(tasks.Tsk.ID)}: {task.get(tasks.Tsk.NAME)}")
    print(f"  Duration: {task.get(tasks.Tsk.DURATION)}")
    print(f"  Start: {task.get(tasks.Tsk.START)}")
    print(f"  Finish: {task.get(tasks.Tsk.FINISH)}")
```

### Export to CSV
```python
import aspose.tasks as tasks
import csv

project = tasks.Project("myproject.mpp")

with open("tasks.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Name", "Duration", "Start", "Finish"])
    
    for task in project.root_task.children:
        writer.writerow([
            task.get(tasks.Tsk.ID),
            task.get(tasks.Tsk.NAME),
            task.get(tasks.Tsk.DURATION),
            task.get(tasks.Tsk.START),
            task.get(tasks.Tsk.FINISH)
        ])
```

---

## 🔧 COM Automation (Requires MS Project Installed)

### Connect to MS Project
```python
import win32com.client

# Start MS Project
app = win32com.client.Dispatch("MSProject.Application")
app.Visible = True

# Open file
app.FileOpen("D:/Projects/myproject.mpp")

# Get active project
project = app.ActiveProject
```

### List Tasks via COM
```python
import win32com.client

app = win32com.client.Dispatch("MSProject.Application")
app.FileOpen("myproject.mpp")
project = app.ActiveProject

for task in project.Tasks:
    if task:
        print(f"{task.ID}: {task.Name}")
        print(f"  Duration: {task.Duration}")
        print(f"  Start: {task.Start}")
        print(f"  Finish: {task.Finish}")
```

### Add New Task
```python
import win32com.client

app = win32com.client.Dispatch("MSProject.Application")
project = app.ActiveProject

# Add task
new_task = project.Tasks.Add("New Task from AI")
new_task.Duration = "5d"

# Save
app.FileSave()
```

### Export Tasks to Excel
```python
import win32com.client

app = win32com.client.Dispatch("MSProject.Application")
app.FileOpen("myproject.mpp")

# Export to Excel
app.FileSaveAs("D:/Exports/project.xlsx", 78)  # 78 = Excel format
```

---

## 📊 Analysis Scripts

### Critical Path Analysis
```python
import aspose.tasks as tasks

project = tasks.Project("myproject.mpp")

for task in project.root_task.children:
    if task.get(tasks.Tsk.IS_CRITICAL):
        print(f"CRITICAL: {task.get(tasks.Tsk.NAME)}")
```

### Resource Loading
```python
import aspose.tasks as tasks

project = tasks.Project("myproject.mpp")

for resource in project.resources:
    print(f"Resource: {resource.get(tasks.Rsc.NAME)}")
    print(f"  Cost: {resource.get(tasks.Rsc.COST)}")
```

---

## 🤖 Automation Scripts

### Full Automation Module
Location: `scripts/ms_project_automation.py`

**Classes:**
- `MSProjectScheduler` - Full schedule automation

**Capabilities:**
- Create schedules from WBS data
- Add tasks, resources, dependencies
- Run DCMA 14-Point assessment
- Update progress from CSV
- Export to CSV/JSON

### Quick Usage
```python
from ms_project_automation import MSProjectScheduler

# Initialize
scheduler = MSProjectScheduler()
scheduler.connect(visible=True)

# Create project
scheduler.create_new_project("My Project", "2026-02-01")

# Add WBS
wbs = [
    {"wbs": "1.0", "name": "Phase 1", "level": 1},
    {"wbs": "1.1", "name": "Task 1", "level": 2, "duration": "5d"},
]
scheduler.create_wbs_structure(wbs)

# Run DCMA assessment
results = scheduler.run_dcma_14_point_assessment()
scheduler.print_dcma_report(results)

# Save
scheduler.save_project("D:/project.mpp")
```

---

## 📋 Quick Commands

```bash
# Test COM connection
python -c "import win32com.client; print('pywin32 ready!')"

# Parse MPP file
python -c "import aspose.tasks as t; p=t.Project('file.mpp'); print('Loaded!')"
```

---

*Last Updated: January 2026*
