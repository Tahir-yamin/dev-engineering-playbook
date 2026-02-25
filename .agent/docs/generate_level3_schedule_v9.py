import pandas as pd
from datetime import datetime
import re

# --- Project Configuration ---
# Start Date: 13 Feb 2026
PROJECT_START_DATE = datetime(2026, 2, 13).date()

tasks = [
    # --- LEVEL 1: PROJECT SUMMARY ---
    {"WBS": "1", "Task Name": "Rehabilitation of CF Site MS. Globe FS (Target: 100 Days)", "Duration": "100 days", "Predecessors": "", "Outline Level": 1},
    
    # --- PHASE 1: ADMIN & APPROVALS (30 Days) ---
    {"WBS": "1.1", "Task Name": "Phase 1: Admin, NOCs & Approvals", "Duration": "30 days", "Predecessors": "", "Outline Level": 2},
    {"WBS": "1.1.1", "Task Name": "Topographic Survey & Layout", "Duration": "5 days", "Predecessors": "1SS", "Outline Level": 3},
    {"WBS": "1.1.2", "Task Name": "Structural Vetting (Office & Canopy)", "Duration": "10 days", "Predecessors": "1.1.1", "Outline Level": 3},
    {"WBS": "1.1.3", "Task Name": "NOC Application & Processing", "Duration": "30 days", "Predecessors": "1SS", "Outline Level": 3},
    {"WBS": "1.1.4", "Task Name": "Power Connection Enhancement (K-Electric)", "Duration": "30 days", "Predecessors": "1SS", "Outline Level": 3},

    # --- PHASE 2: EXECUTION ---
    # Overlap: Starts Day 15 of Admin
    {"WBS": "1.2", "Task Name": "Phase 2: Execution (Civil, MEP, Finishing)", "Duration": "85 days", "Predecessors": "1.1SS+15d", "Outline Level": 2},
    
    # --- 2.1 MOBILIZATION ---
    {"WBS": "1.2.1", "Task Name": "Mobilization & Site Prep", "Duration": "10 days", "Predecessors": "1.1SS+15d", "Outline Level": 3},
    {"WBS": "1.2.1.1", "Task Name": "Mobilization of Staff & Safety Hoarding", "Duration": "3 days", "Predecessors": "1.1SS+15d", "Outline Level": 4},
    {"WBS": "1.2.1.2", "Task Name": "Dismantling Existing Structures/Pavers", "Duration": "7 days", "Predecessors": "1.2.1.1SS+1d", "Outline Level": 4},

    # --- 2.2 ZONE 1: OFFICE BUILDING (PRO LEVEL STRUCTURE) ---
    {"WBS": "1.2.2", "Task Name": "Zone 1: Office Building Construction", "Duration": "65 days", "Predecessors": "1.2.1.2", "Outline Level": 3},
    
    # 2.2.1 Sub-Structure
    {"WBS": "1.2.2.1", "Task Name": "Sub-Structure Works", "Duration": "18 days", "Predecessors": "1.2.1.2", "Outline Level": 4},
    {"WBS": "1.2.2.1.1", "Task Name": "Excavation for Foundation", "Duration": "3 days", "Predecessors": "1.2.1.2", "Outline Level": 5},
    {"WBS": "1.2.2.1.2", "Task Name": "Termite Proofing (Foundation)", "Duration": "1 days", "Predecessors": "1.2.2.1.1", "Outline Level": 5},
    {"WBS": "1.2.2.1.3", "Task Name": "Lean Concrete (PCC 1:4:8)", "Duration": "2 days", "Predecessors": "1.2.2.1.2", "Outline Level": 5},
    {"WBS": "1.2.2.1.4", "Task Name": "Footing Construction (Steel, Shutter, Pour 1:2:4)", "Duration": "4 days", "Predecessors": "1.2.2.1.3", "Outline Level": 5},
    {"WBS": "1.2.2.1.5", "Task Name": "Short Column Necks (Steel, Shutter, Pour)", "Duration": "3 days", "Predecessors": "1.2.2.1.4", "Outline Level": 5},
    {"WBS": "1.2.2.1.6", "Task Name": "Plinth Beam Construction (Steel, Shutter, Pour)", "Duration": "4 days", "Predecessors": "1.2.2.1.5", "Outline Level": 5},
    {"WBS": "1.2.2.1.7", "Task Name": "Bitumen Coating & Backfilling", "Duration": "3 days", "Predecessors": "1.2.2.1.6", "Outline Level": 5},

    # 2.2.2 Super-Structure
    {"WBS": "1.2.2.2", "Task Name": "Super-Structure Works", "Duration": "20 days", "Predecessors": "1.2.2.1.7", "Outline Level": 4},
    {"WBS": "1.2.2.2.1", "Task Name": "Super-Structure Columns (Steel, Shutter, Pour)", "Duration": "5 days", "Predecessors": "1.2.2.1.7", "Outline Level": 5},
    {"WBS": "1.2.2.2.2", "Task Name": "Brick/Block Masonry Walls", "Duration": "8 days", "Predecessors": "1.2.2.2.1SS+3d", "Outline Level": 5},
    {"WBS": "1.2.2.2.3", "Task Name": "Roof Slab & Beams (Shuttering & Steel)", "Duration": "5 days", "Predecessors": "1.2.2.2.1", "Outline Level": 5},
    {"WBS": "1.2.2.2.4", "Task Name": "Roof Slab Pouring (Concrete 1:2:4)", "Duration": "1 days", "Predecessors": "1.2.2.2.3", "Outline Level": 5},
    {"WBS": "1.2.2.2.5", "Task Name": "Roof Curing Time (No Load)", "Duration": "7 days", "Predecessors": "1.2.2.2.4", "Outline Level": 5},

    # 2.2.3 MEP Rough-Ins (Crucial Pro sequencing)
    {"WBS": "1.2.2.3", "Task Name": "MEP Rough-Ins (Concealed)", "Duration": "5 days", "Predecessors": "1.2.2.2.2SS", "Outline Level": 4},
    {"WBS": "1.2.2.3.1", "Task Name": "Electrical Conduiting in Walls/Slab", "Duration": "4 days", "Predecessors": "1.2.2.2.2SS", "Outline Level": 5},
    {"WBS": "1.2.2.3.2", "Task Name": "Plumbing Piping In-Wall/Floor", "Duration": "4 days", "Predecessors": "1.2.2.2.2SS", "Outline Level": 5},

    # 2.2.4 Finishing
    {"WBS": "1.2.2.4", "Task Name": "Finishing Works (Office)", "Duration": "25 days", "Predecessors": "1.2.2.2.5", "Outline Level": 4},
    {"WBS": "1.2.2.4.1", "Task Name": "Internal Plaster (1:4)", "Duration": "6 days", "Predecessors": "1.2.2.3.1", "Outline Level": 5},
    {"WBS": "1.2.2.4.2", "Task Name": "External Plaster (1:4)", "Duration": "6 days", "Predecessors": "1.2.2.4.1", "Outline Level": 5},
    {"WBS": "1.2.2.4.3", "Task Name": "Flooring (PCC Base + Porcelain Tiles)", "Duration": "7 days", "Predecessors": "1.2.2.4.1", "Outline Level": 5},
    {"WBS": "1.2.2.4.4", "Task Name": "False Ceiling (Framing & Sheet)", "Duration": "6 days", "Predecessors": "1.2.2.4.1", "Outline Level": 5},
    {"WBS": "1.2.2.4.5", "Task Name": "Paint Works (Internal/External)", "Duration": "8 days", "Predecessors": "1.2.2.4.3;1.2.2.4.4", "Outline Level": 5},
    {"WBS": "1.2.2.4.6", "Task Name": "MEP Finals (Switches, Fixtures, Sanitary Ware)", "Duration": "5 days", "Predecessors": "1.2.2.4.5SS", "Outline Level": 5},

    # --- 2.3 ZONE 2A: CANOPY (PRO LEVEL) ---
    {"WBS": "1.2.3", "Task Name": "Zone 2A: Canopy Construction", "Duration": "45 days", "Predecessors": "1.2.1.2", "Outline Level": 3},
    {"WBS": "1.2.3.1", "Task Name": "Canopy Foundations (Excavation, Rebar, Concrete)", "Duration": "10 days", "Predecessors": "1.2.1.2", "Outline Level": 4},
    {"WBS": "1.2.3.2", "Task Name": "Installation of Anchor Bolts & Curing", "Duration": "5 days", "Predecessors": "1.2.3.1", "Outline Level": 4},
    {"WBS": "1.2.3.3", "Task Name": "Steel Column Erection", "Duration": "4 days", "Predecessors": "1.2.3.2", "Outline Level": 4},
    {"WBS": "1.2.3.4", "Task Name": "Space Frame/Truss Fabrication & Hoisting", "Duration": "12 days", "Predecessors": "1.2.3.3", "Outline Level": 4},
    {"WBS": "1.2.3.5", "Task Name": "Roof Sheeting & Gutter Installation", "Duration": "8 days", "Predecessors": "1.2.3.4", "Outline Level": 4},
    {"WBS": "1.2.3.6", "Task Name": "Canopy Fascia, Signage & Lighting", "Duration": "6 days", "Predecessors": "1.2.3.5", "Outline Level": 4},

    # --- 2.4 ZONE 2B: FUEL SYSTEM (PRO LEVEL) ---
    {"WBS": "1.2.4", "Task Name": "Zone 2B: Fuel System Works", "Duration": "40 days", "Predecessors": "1.2.1.2", "Outline Level": 3},
    {"WBS": "1.2.4.1", "Task Name": "Excavation for Tank Pit", "Duration": "5 days", "Predecessors": "1.2.1.2", "Outline Level": 4},
    {"WBS": "1.2.4.2", "Task Name": "PCC Bedding & RCC Raft for Tank", "Duration": "7 days", "Predecessors": "1.2.4.1", "Outline Level": 4},
    {"WBS": "1.2.4.3", "Task Name": "Lowering Tanks & Anchoring/strapping", "Duration": "3 days", "Predecessors": "1.2.4.2", "Outline Level": 4},
    {"WBS": "1.2.4.4", "Task Name": "Sand Ballasting & Backfilling", "Duration": "4 days", "Predecessors": "1.2.4.3", "Outline Level": 4},
    {"WBS": "1.2.4.5", "Task Name": "UPP Piping & Containment Sumps", "Duration": "7 days", "Predecessors": "1.2.4.4", "Outline Level": 4},
    {"WBS": "1.2.4.6", "Task Name": "Pump Island Construction", "Duration": "8 days", "Predecessors": "1.2.4.5", "Outline Level": 4},
    {"WBS": "1.2.4.7", "Task Name": "Dispenser Installation & Termination", "Duration": "4 days", "Predecessors": "1.2.4.6", "Outline Level": 4},

    # --- 2.5 ZONE 2C: EXTERNAL DEVELOPMENT ---
    {"WBS": "1.2.5", "Task Name": "Zone 2C: Driveway & External Services", "Duration": "30 days", "Predecessors": "1.2.4.5", "Outline Level": 3},
    {"WBS": "1.2.5.1", "Task Name": "Underground Water Tank & Manholes", "Duration": "12 days", "Predecessors": "1.2.1.2", "Outline Level": 4},
    {"WBS": "1.2.5.2", "Task Name": "External Drainage & Cut-off Drains", "Duration": "8 days", "Predecessors": "1.2.5.1", "Outline Level": 4},
    {"WBS": "1.2.5.3", "Task Name": "Compaction & Stone Soling", "Duration": "5 days", "Predecessors": "1.2.5.2", "Outline Level": 4},
    {"WBS": "1.2.5.4", "Task Name": "Interlock Pavers & Curb Stones", "Duration": "10 days", "Predecessors": "1.2.5.3", "Outline Level": 4},
    {"WBS": "1.2.5.5", "Task Name": "Monolith Signage (Foundation -> Install -> Electric)", "Duration": "7 days", "Predecessors": "1.2.5.4SS", "Outline Level": 4},

    # --- PHASE 3: CLOSING (10 Days) ---
    {"WBS": "1.3", "Task Name": "Phase 3: Closing & Handover", "Duration": "10 days", "Predecessors": "1.2.2.4.6;1.2.3.6;1.2.4.7;1.2.5.4", "Outline Level": 2},
    {"WBS": "1.3.1", "Task Name": "Testing & Commissioning", "Duration": "5 days", "Predecessors": "1.2.2.4.6;1.2.3.6;1.2.4.7", "Outline Level": 3},
    {"WBS": "1.3.2", "Task Name": "As-Built Drawings & Docs", "Duration": "5 days", "Predecessors": "1.3.1SS", "Outline Level": 3},
    {"WBS": "1.3.3", "Task Name": "Staff Training", "Duration": "3 days", "Predecessors": "1.3.1", "Outline Level": 3},
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
output_file = "d:/my-dev-knowledge-base/Project_Schedule_MSP_Export_v9.xlsx"
df.to_excel(output_file, index=False)
print(f"Schedule V9 (Pro Level) exported to {output_file}")
