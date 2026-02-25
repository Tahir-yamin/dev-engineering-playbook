import pandas as pd
from datetime import datetime, timedelta
import re

# --- Project Configuration ---
# Start Date: 13 Feb 2026
PROJECT_START_DATE = datetime(2026, 2, 13).date()

tasks = [
    # --- LEVEL 1: PROJECT SUMMARY ---
    # ID 1
    {"WBS": "1", "Task Name": "Rehabilitation of CF Site MS. Globe FS (100 Days)", "Duration": "100 days", "Predecessors": "", "Outline Level": 1},
    
    # --- PHASE 1: ADMIN ---
    # ID 2
    {"WBS": "1.1", "Task Name": "Phase 1: Admin, NOCs & Approvals", "Duration": "30 days", "Predecessors": "", "Outline Level": 2},
    # ID 3
    {"WBS": "1.1.1", "Task Name": "Topographic Survey & Layout", "Duration": "5 days", "Predecessors": "", "Outline Level": 3},
    # ID 4
    {"WBS": "1.1.2", "Task Name": "Structural Vetting (Office & Canopy)", "Duration": "10 days", "Predecessors": "1.1.1", "Outline Level": 3},
    # ID 5
    {"WBS": "1.1.3", "Task Name": "NOC Processing (DC, KMC, KWSB)", "Duration": "30 days", "Predecessors": "", "Outline Level": 3},
    # ID 6
    {"WBS": "1.1.4", "Task Name": "Power Connection Enhancement", "Duration": "30 days", "Predecessors": "", "Outline Level": 3},

    # --- PHASE 2: EXECUTION ---
    # ID 7
    {"WBS": "1.2", "Task Name": "Phase 2: Execution", "Duration": "85 days", "Predecessors": "", "Outline Level": 2},
    
    # --- 2.1 MOBILIZATION ---
    # ID 8
    {"WBS": "1.2.1", "Task Name": "Mobilization & Site Prep", "Duration": "10 days", "Predecessors": "1.1.2", "Outline Level": 3},
    {"WBS": "1.2.1.1", "Task Name": "Mobilization of Staff & Hoarding", "Duration": "3 days", "Predecessors": "1.1.2", "Outline Level": 4},
    {"WBS": "1.2.1.2", "Task Name": "Dismantling & Debris Removal", "Duration": "7 days", "Predecessors": "1.2.1.1SS+1d", "Outline Level": 4},

    # --- 2.2 ZONE 1: OFFICE BUILDING ---
    {"WBS": "1.2.2", "Task Name": "Zone 1: Office Building", "Duration": "70 days", "Predecessors": "1.2.1.2", "Outline Level": 3},
    
    # 2.2.1 Sub-Structure
    {"WBS": "1.2.2.1", "Task Name": "Sub-Structure Works", "Duration": "25 days", "Predecessors": "1.2.1.2", "Outline Level": 4},
    {"WBS": "1.2.2.1.1", "Task Name": "Excavation", "Duration": "3 days", "Predecessors": "1.2.1.2", "Outline Level": 5},
    {"WBS": "1.2.2.1.2", "Task Name": "Termite Proofing & Lean (1:4:8)", "Duration": "3 days", "Predecessors": "1.2.2.1.1", "Outline Level": 5},
    {"WBS": "1.2.2.1.3", "Task Name": "Footing Construction (Steel/Shutter/Pour)", "Duration": "4 days", "Predecessors": "1.2.2.1.2", "Outline Level": 5},
    {"WBS": "1.2.2.1.4", "Task Name": "[QC] Curing of Footings (7 Days)", "Duration": "7 days", "Predecessors": "1.2.2.1.3", "Outline Level": 5},
    {"WBS": "1.2.2.1.5", "Task Name": "Short Column Necks", "Duration": "3 days", "Predecessors": "1.2.2.1.4", "Outline Level": 5},
    {"WBS": "1.2.2.1.6", "Task Name": "Plinth Beam Construction", "Duration": "4 days", "Predecessors": "1.2.2.1.5", "Outline Level": 5},
    {"WBS": "1.2.2.1.7", "Task Name": "[QC] Curing of Plinth (7 Days)", "Duration": "7 days", "Predecessors": "1.2.2.1.6", "Outline Level": 5},
    {"WBS": "1.2.2.1.8", "Task Name": "Bitumen & Backfilling", "Duration": "3 days", "Predecessors": "1.2.2.1.7SW", "Outline Level": 5}, # Start after 7d curing

    # 2.2.2 Super-Structure
    {"WBS": "1.2.2.2", "Task Name": "Super-Structure Works", "Duration": "35 days", "Predecessors": "1.2.2.1.8", "Outline Level": 4},
    {"WBS": "1.2.2.2.1", "Task Name": "Super-Structure Columns", "Duration": "5 days", "Predecessors": "1.2.2.1.8", "Outline Level": 5},
    {"WBS": "1.2.2.2.2", "Task Name": "[QC] Curing of Columns (7 Days)", "Duration": "7 days", "Predecessors": "1.2.2.2.1", "Outline Level": 5},
    {"WBS": "1.2.2.2.3", "Task Name": "Masonry Walls (During Column Curing)", "Duration": "8 days", "Predecessors": "1.2.2.2.1SS+2d", "Outline Level": 5},
    {"WBS": "1.2.2.2.4", "Task Name": "Roof Slab & Beams (Shutter/Steel/Pour)", "Duration": "6 days", "Predecessors": "1.2.2.2.2;1.2.2.2.3", "Outline Level": 5},
    {"WBS": "1.2.2.2.5", "Task Name": "[QC] Roof Slab Curing (14 Days)", "Duration": "14 days", "Predecessors": "1.2.2.2.4", "Outline Level": 5},
    
    # 2.2.3 MEP
    {"WBS": "1.2.2.3", "Task Name": "MEP Rough-Ins & Testing", "Duration": "8 days", "Predecessors": "1.2.2.2.3SS+3d", "Outline Level": 4},
    {"WBS": "1.2.2.3.1", "Task Name": "Electrical Conduiting", "Duration": "4 days", "Predecessors": "1.2.2.2.3SS+3d", "Outline Level": 5},
    {"WBS": "1.2.2.3.2", "Task Name": "Plumbing Piping", "Duration": "4 days", "Predecessors": "1.2.2.2.3SS+3d", "Outline Level": 5},
    {"WBS": "1.2.2.3.3", "Task Name": "[QC] Hydro-Test (Plumbing) & IR Test", "Duration": "2 days", "Predecessors": "1.2.2.3.2", "Outline Level": 5},

    # 2.2.4 Finishing
    {"WBS": "1.2.2.4", "Task Name": "Finishing Works", "Duration": "30 days", "Predecessors": "1.2.2.2.5SW", "Outline Level": 4}, # Start after curing
    {"WBS": "1.2.2.4.1", "Task Name": "Internal Plaster & [QC] Curing (5 Days)", "Duration": "8 days", "Predecessors": "1.2.2.2.5SW", "Outline Level": 5},
    {"WBS": "1.2.2.4.2", "Task Name": "False Ceiling", "Duration": "6 days", "Predecessors": "1.2.2.4.1", "Outline Level": 5},
    {"WBS": "1.2.2.4.3", "Task Name": "Flooring & [QC] Protection", "Duration": "8 days", "Predecessors": "1.2.2.4.1", "Outline Level": 5},
    {"WBS": "1.2.2.4.4", "Task Name": "Paint & Fixtures", "Duration": "10 days", "Predecessors": "1.2.2.4.3", "Outline Level": 5},

    # --- 2.3 ZONE 2A: CANOPY ---
    {"WBS": "1.2.3", "Task Name": "Zone 2A: Canopy", "Duration": "45 days", "Predecessors": "1.2.1.2", "Outline Level": 3},
    {"WBS": "1.2.3.1", "Task Name": "Canopy Foundations", "Duration": "10 days", "Predecessors": "1.2.1.2", "Outline Level": 4},
    {"WBS": "1.2.3.2", "Task Name": "[QC] Foundation Curing (7 Days)", "Duration": "7 days", "Predecessors": "1.2.3.1", "Outline Level": 4}, # Overlap with Space Frame Fab
    {"WBS": "1.2.3.3", "Task Name": "Space Frame Fabrication (Off-site/On-site)", "Duration": "12 days", "Predecessors": "1.2.3.1", "Outline Level": 4},
    {"WBS": "1.2.3.4", "Task Name": "Column Erection & Grouting", "Duration": "4 days", "Predecessors": "1.2.3.2", "Outline Level": 4},
    {"WBS": "1.2.3.5", "Task Name": "Space Frame Hoisting & Sheeting", "Duration": "12 days", "Predecessors": "1.2.3.3;1.2.3.4", "Outline Level": 4},
    {"WBS": "1.2.3.6", "Task Name": "Fascia & Lighting", "Duration": "6 days", "Predecessors": "1.2.3.5", "Outline Level": 4},

    # --- 2.4 ZONE 2B: FUEL SYSTEM ---
    {"WBS": "1.2.4", "Task Name": "Zone 2B: Fuel System", "Duration": "45 days", "Predecessors": "1.2.1.2", "Outline Level": 3},
    {"WBS": "1.2.4.1", "Task Name": "Excavation & Bedding", "Duration": "7 days", "Predecessors": "1.2.1.2", "Outline Level": 4},
    {"WBS": "1.2.4.2", "Task Name": "Tank Install & Anchoring", "Duration": "4 days", "Predecessors": "1.2.4.1", "Outline Level": 4},
    {"WBS": "1.2.4.3", "Task Name": "[QC] Ballasting & Hold", "Duration": "3 days", "Predecessors": "1.2.4.2", "Outline Level": 4},
    {"WBS": "1.2.4.4", "Task Name": "UPP Piping & Sumps", "Duration": "7 days", "Predecessors": "1.2.4.3", "Outline Level": 4},
    {"WBS": "1.2.4.5", "Task Name": "[QC] Nitrogen Pressure Test (Line)", "Duration": "2 days", "Predecessors": "1.2.4.4", "Outline Level": 4},
    {"WBS": "1.2.4.6", "Task Name": "Backfilling & Compaction", "Duration": "3 days", "Predecessors": "1.2.4.5", "Outline Level": 4},
    {"WBS": "1.2.4.7", "Task Name": "Pump Island & Dispensers", "Duration": "10 days", "Predecessors": "1.2.4.6", "Outline Level": 4},

    # --- 2.5 ZONE 2C: EXTERNAL ---
    {"WBS": "1.2.5", "Task Name": "Zone 2C: Driveway", "Duration": "35 days", "Predecessors": "1.2.4.5", "Outline Level": 3},
    {"WBS": "1.2.5.1", "Task Name": "Underground Tanks & Manholes", "Duration": "15 days", "Predecessors": "1.2.1.2", "Outline Level": 4}, # Can start early
    {"WBS": "1.2.5.2", "Task Name": "Stone Soling & Compaction", "Duration": "5 days", "Predecessors": "1.2.5.1;1.2.4.6", "Outline Level": 4},
    {"WBS": "1.2.5.3", "Task Name": "[QC] Field Density Test (FDT)", "Duration": "1 days", "Predecessors": "1.2.5.2", "Outline Level": 4},
    {"WBS": "1.2.5.4", "Task Name": "Paver Installation", "Duration": "10 days", "Predecessors": "1.2.5.3", "Outline Level": 4},

    # --- PHASE 3: CLOSING ---
    # ID 63 approx
    {"WBS": "1.3", "Task Name": "Phase 3: Closing", "Duration": "10 days", "Predecessors": "1.2.2.4.4;1.2.3.6;1.2.4.7;1.2.5.4", "Outline Level": 2},
    {"WBS": "1.3.1", "Task Name": "Final Testing & Commissioning", "Duration": "5 days", "Predecessors": "1.2.2.4.4;1.2.3.6;1.2.4.7", "Outline Level": 3},
    {"WBS": "1.3.2", "Task Name": "As-Built & Handover", "Duration": "5 days", "Predecessors": "1.3.1SS", "Outline Level": 3},
]

# 1. Assign MSP_IDs
for i, task in enumerate(tasks):
    task['MSP_ID'] = i + 1

# 2. Build Map
wbs_map = {task['WBS']: str(task['MSP_ID']) for task in tasks}

# 3. Resolve Predecessors
def resolve_preds(pred_str):
    if not pred_str: return ""
    pred_str = pred_str.replace(",", ";")
    preds = pred_str.split(';')
    resolved = []
    for p in preds:
        p = p.strip()
        if not p: continue
        # Handle "SW" (Start-Wait/Finish) custom logic by converting to simple FS for now or standard lags
        # Here we just map IDs.
        match = re.match(r"^([\d\.]+)(.*)", p)
        if match and match.group(1) in wbs_map:
            resolved.append(wbs_map[match.group(1)] + match.group(2).replace(" days", "d").replace(" ", ""))
        else:
            resolved.append(p)
    return ",".join(resolved)

for task in tasks:
    task['Predecessors'] = resolve_preds(task['Predecessors'])

df = pd.DataFrame(tasks, columns=["WBS", "Task Name", "Duration", "Predecessors", "Outline Level", "MSP_ID"])

output_file = "d:/my-dev-knowledge-base/Project_Schedule_MSP_Export_v11.xlsx"
df.to_excel(output_file, index=False)
print(f"Schedule V11 (QC & Curing) exported to {output_file}")

print("\n" + "="*50)
print("MS PROJECT IMPORT MAPPING REMINDER:")
print("="*50)
print(f"{'Excel Field':<20} -> {'MS Project Field':<20}")
print(f"{'-'*20}    {'-'*20}")
print(f"{'Task Name':<20} -> {'Name':<20}")
print(f"{'Duration':<20} -> {'Duration':<20}")
print(f"{'Predecessors':<20} -> {'Predecessors':<20}")
print(f"{'Outline Level':<20} -> {'Outline Level':<20}")
print(f"{'MSP_ID':<20} -> {'ID':<20}")
print("="*50)
