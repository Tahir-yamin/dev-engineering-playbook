# Primavera P6 Integration Skills

> **Purpose**: Parse, analyze, and automate Primavera P6 project schedules using XER files and Python tools.

## Overview

Oracle Primavera P6 is an enterprise project portfolio management solution. This skill enables AI-powered analysis of P6 schedules through XER file parsing.

---

## 🛠️ Installed Tools

| Tool | Purpose | Status |
|------|---------|--------|
| **xerparser** | Python library for parsing XER files | ✅ Installed |
| **P6xer MCP Server** | MCP server for AI integration | ✅ Cloned |

---

## 📁 XER File Analysis

### What is an XER File?
XER is Primavera P6's proprietary export format containing:
- Projects, WBS, Activities
- Resources, Roles, Calendars
- Relationships, Baselines
- Activity Codes, UDFs

### Export XER from P6 Desktop
1. **File → Export**
2. Select **"Primavera PM - (XER)"**
3. Choose project(s) to export
4. Save file (e.g., `project_schedule.xer`)

---

## 🐍 Python Usage Examples

### Basic XER Parsing
```python
from xerparser import Xer

# Load XER file
xer = Xer.reader("path/to/project.xer")

# Access projects
for project in xer.projects:
    print(f"Project: {project.name}")
```

### List All Activities
```python
from xerparser import Xer

xer = Xer.reader("project.xer")

for activity in xer.activities:
    print(f"{activity.activity_id}: {activity.name}")
    print(f"  Duration: {activity.original_duration}")
    print(f"  Start: {activity.start_date}")
    print(f"  Finish: {activity.finish_date}")
```

### Analyze Critical Path
```python
from pyp6xer import Xer

xer = Xer("project.xer")

critical_activities = [a for a in xer.activities if a.driving_path_flag == "Y"]
print(f"Critical Activities: {len(critical_activities)}")

for act in critical_activities:
    print(f"  - {act.task_code}: {act.task_name}")
```

### Resource Analysis
```python
from pyp6xer import Xer

xer = Xer("project.xer")

for resource in xer.resources:
    print(f"Resource: {resource.rsrc_short_name}")
    print(f"  Type: {resource.rsrc_type}")
```

### Export to Pandas DataFrame
```python
from pyp6xer import Xer
import pandas as pd

xer = Xer("project.xer")

# Convert activities to DataFrame
activities_data = [{
    'Code': a.task_code,
    'Name': a.task_name,
    'Duration': a.target_drtn_hr_cnt,
    'Start': a.target_start_date,
    'Finish': a.target_end_date,
    'Critical': a.driving_path_flag
} for a in xer.activities]

df = pd.DataFrame(activities_data)
df.to_csv("activities_report.csv", index=False)
```

### WBS Structure
```python
from pyp6xer import Xer

xer = Xer("project.xer")

for wbs in xer.wbs:
    print(f"WBS: {wbs.wbs_short_name}")
    print(f"  Name: {wbs.wbs_name}")
    print(f"  Parent: {wbs.parent_wbs_id}")
```

---

## 🤖 MCP Server Integration

### Location
```
d:\my-dev-knowledge-base\external-libs\p6xer-mcp-server\
```

### Claude Desktop Configuration
Add to `%APPDATA%\Claude\claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "p6xer": {
      "command": "python",
      "args": ["-m", "p6xer_mcp_server"],
      "cwd": "d:\\my-dev-knowledge-base\\external-libs\\p6xer-mcp-server"
    }
  }
}
```

### MCP Capabilities
- Parse XER files
- List projects, activities, resources
- Analyze schedules
- Generate reports

---

## 📊 Common Analysis Tasks

### Schedule Health Check
```python
from pyp6xer import Xer
from datetime import datetime

xer = Xer("project.xer")

# Check for activities without successors
no_successors = [a for a in xer.activities if not a.successors]
print(f"Activities without successors: {len(no_successors)}")

# Check for activities without predecessors
no_predecessors = [a for a in xer.activities if not a.predecessors]
print(f"Activities without predecessors: {len(no_predecessors)}")

# Check for zero duration activities
zero_duration = [a for a in xer.activities if a.target_drtn_hr_cnt == 0]
print(f"Zero duration activities: {len(zero_duration)}")
```

### Float Analysis
```python
from pyp6xer import Xer

xer = Xer("project.xer")

negative_float = [a for a in xer.activities if a.total_float_hr_cnt < 0]
print(f"Activities with negative float: {len(negative_float)}")

for act in negative_float:
    print(f"  {act.task_code}: Float = {act.total_float_hr_cnt} hrs")
```

### Resource Loading Report
```python
from pyp6xer import Xer
import pandas as pd

xer = Xer("project.xer")

# Get resource assignments
assignments = []
for ra in xer.resource_assignments:
    assignments.append({
        'Activity': ra.task_id,
        'Resource': ra.rsrc_id,
        'Units': ra.target_qty,
        'Cost': ra.target_cost
    })

df = pd.DataFrame(assignments)
print(df.groupby('Resource')['Cost'].sum())
```

---

## 🔧 Automation Scripts

### PowerShell: Batch XER Analysis
```powershell
# Analyze all XER files in a folder
$xerFiles = Get-ChildItem -Path "D:\Projects\*.xer"

foreach ($file in $xerFiles) {
    python -c "
from pyp6xer import Xer
xer = Xer('$($file.FullName)')
print(f'Project: {xer.projects[0].proj_short_name}')
print(f'Activities: {len(xer.activities)}')
"
}
```

### Export Schedule Summary
```python
from pyp6xer import Xer
import json

def export_summary(xer_path, output_path):
    xer = Xer(xer_path)
    
    summary = {
        "project": xer.projects[0].proj_short_name if xer.projects else "Unknown",
        "total_activities": len(xer.activities),
        "total_resources": len(xer.resources),
        "wbs_elements": len(xer.wbs),
        "calendars": len(xer.calendars)
    }
    
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    return summary

# Usage
summary = export_summary("project.xer", "summary.json")
print(summary)
```

---

## 📚 PyP6XER Object Reference

| Object | Description |
|--------|-------------|
| `xer.projects` | List of projects |
| `xer.activities` | All activities (TASK) |
| `xer.wbs` | Work Breakdown Structure |
| `xer.resources` | Resources (RSRC) |
| `xer.calendars` | Project calendars |
| `xer.relationships` | Activity relationships (TASKPRED) |
| `xer.resource_assignments` | Resource assignments (TASKRSRC) |
| `xer.activity_codes` | Activity code definitions |
| `xer.udf_types` | User Defined Fields |

---

## 🔗 Related Resources

- [PyP6XER GitHub](https://github.com/osama-ata/PyP6Xer)
- [PyP6XER PyPI](https://pypi.org/project/pyp6xer/)
- [P6xer MCP Server](https://github.com/osama-ata/p6xer-mcp-server)
- [Oracle P6 Documentation](https://docs.oracle.com/cd/E80480_01/index.htm)

---

## 🤖 Automation Scripts

### Full Automation Module
Location: `scripts/p6_automation.py`

**Classes:**
- `P6ScheduleAnalyzer` - XER file analysis with DCMA 14-Point
- `P6ScheduleCreator` - Create schedule data for P6 import

### Analyze XER File
```python
from p6_automation import P6ScheduleAnalyzer

# Load and analyze
analyzer = P6ScheduleAnalyzer("project.xer")

# Run DCMA 14-Point assessment
analyzer.print_dcma_report()

# Get critical path
critical = analyzer.get_critical_path()
for task in critical:
    print(f"{task['activity_id']}: {task['name']}")

# Export to CSV/JSON
analyzer.export_to_csv("activities.csv")
analyzer.export_to_json("schedule.json")
```

### Create Schedule for P6 Import
```python
from p6_automation import P6ScheduleCreator

creator = P6ScheduleCreator("My Project", "2026-02-01")

# Add activities
creator.add_activity("A1000", "Start", 0, "1.0")
creator.add_activity("A1010", "Phase 1", 10, "1.1")

# Add relationships
creator.add_relationship("A1000", "A1010", "FS")

# Export for P6 import
creator.export_for_p6_import("D:/P6_Import")
```

---

## 📋 Quick Commands

```bash
# Install/Update PyP6XER
pip install --upgrade pyp6xer

# Test installation
python -c "from pyp6xer import Xer; print('PyP6XER ready!')"

# Parse XER file
python -c "from pyp6xer import Xer; xer = Xer('file.xer'); print(len(xer.activities))"
```

---

*Last Updated: January 2026*
