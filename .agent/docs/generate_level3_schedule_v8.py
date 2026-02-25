import pandas as pd
from datetime import datetime, timedelta
import re

# --- Project Configuration ---
# Start Date: 13 Feb 2026
# Working Days: 7 days/week
PROJECT_START_DATE = datetime(2026, 2, 13).date()

tasks = [
    # --- LEVEL 1: PROJECT SUMMARY ---
    {"WBS": "1", "Task Name": "Rehabilitation of CF Site MS. Globe FS (100 Days)", "Duration": "100 days", "Predecessors": "", "Outline Level": 1},
    
    # --- PHASE 1: ADMIN & APPROVALS (30 Days) ---
    {"WBS": "1.1", "Task Name": "Phase 1: Admin, NOCs & Approvals", "Duration": "30 days", "Predecessors": "", "Outline Level": 2},
    {"WBS": "1.1.1", "Task Name": "Topographic Survey & Layout", "Duration": "5 days", "Predecessors": "1SS", "Outline Level": 3},
    {"WBS": "1.1.2", "Task Name": "Structural Vetting (Office & Canopy)", "Duration": "10 days", "Predecessors": "1.1.1", "Outline Level": 3},
    {"WBS": "1.1.3", "Task Name": "NOC Application & Processing (DC, KMC, KWSB)", "Duration": "30 days", "Predecessors": "1SS", "Outline Level": 3},
    {"WBS": "1.1.4", "Task Name": "Item 1.033: Enhancement of Power Connection (K-Electric) & CIE Approval", "Duration": "30 days", "Predecessors": "1SS", "Outline Level": 3},

    # --- PHASE 2: EXECUTION (70 Days) ---
    # Overlap logic: Starts Day 15 (Parallel with Admin)
    {"WBS": "1.2", "Task Name": "Phase 2: Execution (Civil, MEP, Finishing)", "Duration": "70 days", "Predecessors": "1.1SS+15d", "Outline Level": 2},
    
    # --- 2.1 MOBILIZATION & PREP ---
    {"WBS": "1.2.1", "Task Name": "Item 1.001: Mobilization & Preparatory Works", "Duration": "10 days", "Predecessors": "1.1SS+15d", "Outline Level": 3},
    {"WBS": "1.2.1.1", "Task Name": "Mobilization of Staff, Eqpt & Safety Hoarding", "Duration": "3 days", "Predecessors": "1.1SS+15d", "Outline Level": 4},
    {"WBS": "1.2.1.2", "Task Name": "Dismantling Existing Structures/Pavers", "Duration": "7 days", "Predecessors": "1.2.1.1SS+1d", "Outline Level": 4},
    {"WBS": "1.2.1.3", "Task Name": "Debris Removal & Site Leveling", "Duration": "5 days", "Predecessors": "1.2.1.2", "Outline Level": 4},

    # --- 2.2 ZONE 1: OFFICE & LUBE BAY (Expanded) ---
    {"WBS": "1.2.2", "Task Name": "Zone 1: Office Kiosk & Auto Care Conversion", "Duration": "55 days", "Predecessors": "1.2.1.2", "Outline Level": 3},
    
    # 2.2.1 Civil
    {"WBS": "1.2.2.1", "Task Name": "Civil & Structural Works (Office)", "Duration": "20 days", "Predecessors": "1.2.1.2", "Outline Level": 4},
    {"WBS": "1.2.2.1.1", "Task Name": "Excavation & Termite Proofing (Item 1.018)", "Duration": "3 days", "Predecessors": "1.2.1.2", "Outline Level": 5},
    {"WBS": "1.2.2.1.2", "Task Name": "Lean Concrete 1:4:8 & Footings", "Duration": "7 days", "Predecessors": "1.2.2.1.1", "Outline Level": 5},
    {"WBS": "1.2.2.1.3", "Task Name": "Brick/Block Masonry Walls", "Duration": "10 days", "Predecessors": "1.2.2.1.2", "Outline Level": 5},
    {"WBS": "1.2.2.1.4", "Task Name": "[NEW] Lube Bay Ramp & Trench Drain Development", "Duration": "5 days", "Predecessors": "1.2.2.1.2", "Outline Level": 5},

    # 2.2.2 Finishing
    {"WBS": "1.2.2.2", "Task Name": "Finishing Works (Office)", "Duration": "30 days", "Predecessors": "1.2.2.1.3", "Outline Level": 4},
    {"WBS": "1.2.2.2.1", "Task Name": "Plaster & Paint (Internal/External)", "Duration": "15 days", "Predecessors": "1.2.2.1.3", "Outline Level": 5},
    {"WBS": "1.2.2.2.2", "Task Name": "Flooring (Porcelain Tiles)", "Duration": "7 days", "Predecessors": "1.2.2.2.1", "Outline Level": 5},
    {"WBS": "1.2.2.2.3", "Task Name": "[NEW] Industrial Grade Epoxy Flooring (Auto Care)", "Duration": "4 days", "Predecessors": "1.2.2.2.2", "Outline Level": 5},
    {"WBS": "1.2.2.2.4", "Task Name": "[NEW] Auto Care Wall Panelling & Profile Lights", "Duration": "5 days", "Predecessors": "1.2.2.2.1", "Outline Level": 5},

    # 2.2.3 MEP
    {"WBS": "1.2.2.3", "Task Name": "MEP Works (Office)", "Duration": "15 days", "Predecessors": "1.2.2.1.3", "Outline Level": 4},
    {"WBS": "1.2.2.3.1", "Task Name": "Electrical Wiring & DBs", "Duration": "5 days", "Predecessors": "1.2.2.1.3", "Outline Level": 5},
    {"WBS": "1.2.2.3.2", "Task Name": "Plumbing & Sanitary", "Duration": "5 days", "Predecessors": "1.2.2.1.3", "Outline Level": 5},
    {"WBS": "1.2.2.3.3", "Task Name": "AC Installation", "Duration": "2 days", "Predecessors": "1.2.2.2.1", "Outline Level": 5},

    # --- 2.3 ZONE 2: EXTERNAL INFRASTRUCTURE ---
    {"WBS": "1.2.3", "Task Name": "Zone 2: External Infrastructure", "Duration": "65 days", "Predecessors": "1.2.1.2", "Outline Level": 3},
    
    # 2.3.1 Canopy
    {"WBS": "1.2.3.1", "Task Name": "Sub-Zone 2A: Steel Canopy", "Duration": "40 days", "Predecessors": "1.2.1.3", "Outline Level": 4},
    {"WBS": "1.2.3.1.1", "Task Name": "Canopy Foundations & Column Erection", "Duration": "15 days", "Predecessors": "1.2.1.3", "Outline Level": 5},
    {"WBS": "1.2.3.1.2", "Task Name": "Space Frame & Sheet Installation", "Duration": "15 days", "Predecessors": "1.2.3.1.1", "Outline Level": 5},
    {"WBS": "1.2.3.1.3", "Task Name": "False Ceiling & Gutter", "Duration": "10 days", "Predecessors": "1.2.3.1.2", "Outline Level": 5},
    {"WBS": "1.2.3.1.4", "Task Name": "[NEW] Canopy Signage & Lighting (Fascia)", "Duration": "5 days", "Predecessors": "1.2.3.1.3", "Outline Level": 5},

    # 2.3.2 Fuel System
    {"WBS": "1.2.3.2", "Task Name": "Sub-Zone 2B: Fuel System", "Duration": "45 days", "Predecessors": "1.2.1.2", "Outline Level": 4},
    {"WBS": "1.2.3.2.1", "Task Name": "UGFS Tank Pit & Installation (15/25KL)", "Duration": "20 days", "Predecessors": "1.2.1.2", "Outline Level": 5},
    {"WBS": "1.2.3.2.2", "Task Name": "Fuel Piping (UPP 54mm & Decantation)", "Duration": "10 days", "Predecessors": "1.2.3.2.1", "Outline Level": 5},
    {"WBS": "1.2.3.2.3", "Task Name": "Pump Island Construction & DU Install", "Duration": "10 days", "Predecessors": "1.2.3.2.2", "Outline Level": 5},

    # 2.3.3 Civil & External
    {"WBS": "1.2.3.3", "Task Name": "Sub-Zone 2C: Paving & Drainage", "Duration": "30 days", "Predecessors": "1.2.3.2.2", "Outline Level": 4},
    {"WBS": "1.2.3.3.1", "Task Name": "Underground Water Tank & Manholes", "Duration": "15 days", "Predecessors": "1.2.1.3", "Outline Level": 5},
    {"WBS": "1.2.3.3.2", "Task Name": "Pavers & Curb Stones (Supply & Lay)", "Duration": "20 days", "Predecessors": "1.2.3.3.1", "Outline Level": 5},
    {"WBS": "1.2.3.3.3", "Task Name": "[NEW] Firefighting System Installation (Point)", "Duration": "5 days", "Predecessors": "1.2.3.3.1", "Outline Level": 5},

    # 2.3.4 External Electrical & Branding
    {"WBS": "1.2.3.4", "Task Name": "Sub-Zone 2D: External Electrical & Branding", "Duration": "25 days", "Predecessors": "1.2.3.3.2", "Outline Level": 4},
    {"WBS": "1.2.3.4.1", "Task Name": "Cable Sleeves & Main Wiring", "Duration": "7 days", "Predecessors": "1.2.3.3.2SS", "Outline Level": 5},
    {"WBS": "1.2.3.4.2", "Task Name": "Light Pole Installation (Single/Double)", "Duration": "5 days", "Predecessors": "1.2.3.4.1", "Outline Level": 5},
    {"WBS": "1.2.3.4.3", "Task Name": "[NEW] Monolith Signage Body & Foundation", "Duration": "5 days", "Predecessors": "1.2.3.4.1", "Outline Level": 5},
    {"WBS": "1.2.3.4.4", "Task Name": "[NEW] Monolith Electrical Connection/Wiring", "Duration": "3 days", "Predecessors": "1.2.3.4.3", "Outline Level": 5},
    {"WBS": "1.2.3.4.5", "Task Name": "[NEW] General Site Signage Installation", "Duration": "4 days", "Predecessors": "1.2.3.4.2", "Outline Level": 5},

    # --- PHASE 3: CLOSING (10 Days) ---
    {"WBS": "1.3", "Task Name": "Phase 3: Closing & Handover", "Duration": "10 days", "Predecessors": "1.2.2.2.1;1.2.3.3.2;1.2.3.4.5", "Outline Level": 2},
    {"WBS": "1.3.1", "Task Name": "Testing & Commissioning", "Duration": "5 days", "Predecessors": "1.2.2.2.1;1.2.3.3.2", "Outline Level": 3},
    {"WBS": "1.3.2", "Task Name": "[NEW] Submission of As-Built Drawings & Docs", "Duration": "5 days", "Predecessors": "1.3.1SS", "Outline Level": 3},
    {"WBS": "1.3.3", "Task Name": "[NEW] Staff Training (Fuel/Lube Ops)", "Duration": "3 days", "Predecessors": "1.3.1", "Outline Level": 3},
    {"WBS": "1.3.4", "Task Name": "Final Cleaning & Handover", "Duration": "2 days", "Predecessors": "1.3.3", "Outline Level": 3},
]

# 1. Assign Row IDs
start_row = 2
for i, task in enumerate(tasks):
    task['Row_ID'] = start_row + i

# 2. Build Map
wbs_map = {task['WBS']: str(task['Row_ID']) for task in tasks}

# 3. Resolve Predecessors
def resolve_preds(pred_str):
    if not pred_str: return ""
    pred_str = pred_str.replace(",", ";")
    preds = pred_str.split(';')
    resolved = []
    for p in preds:
        p = p.strip()
        if not p: continue
        match = re.match(r"^([\d\.]+)(.*)", p)
        if match and match.group(1) in wbs_map:
            resolved.append(wbs_map[match.group(1)] + match.group(2).replace(" days", "d").replace(" ", ""))
        else:
            resolved.append(p)
    return ",".join(resolved)

for task in tasks:
    task['Predecessors'] = resolve_preds(task['Predecessors'])

df = pd.DataFrame(tasks, columns=["WBS", "Task Name", "Duration", "Predecessors", "Outline Level", "Row_ID"])
output_file = "d:/my-dev-knowledge-base/Project_Schedule_MSP_Export_v8.xlsx"
df.to_excel(output_file, index=False)
print(f"Schedule V8 exported to {output_file}")
