import pandas as pd
from datetime import datetime, timedelta
import re

# Define the project start date
project_start_date = datetime.now().date() + timedelta(days=7)

tasks = [
    # Level 1
    {"WBS": "1", "Task Name": "Rehabilitation of CF Site MS. Globe FS", "Duration": "100 days", "Predecessors": "", "Outline Level": 1},
    
    # --- PHASE 1 ---
    {"WBS": "1.1", "Task Name": "Phase 1: Admin & Approvals (NOC)", "Duration": "30 days", "Predecessors": "", "Outline Level": 2},
    {"WBS": "1.1.1", "Task Name": "Topographic Survey & Layout", "Duration": "5 days", "Predecessors": "1SS", "Outline Level": 3},
    {"WBS": "1.1.2", "Task Name": "Structural Vetting (Office & Canopy)", "Duration": "10 days", "Predecessors": "1.1.1", "Outline Level": 3},
    {"WBS": "1.1.3", "Task Name": "NOC Application & Processing", "Duration": "30 days", "Predecessors": "1SS", "Outline Level": 3},
    {"WBS": "1.1.4", "Task Name": "Obtain DC NOC & CIE Approval", "Duration": "30 days", "Predecessors": "1SS", "Outline Level": 4},
    {"WBS": "1.1.5", "Task Name": "Obtain Regulatory Approvals (KMC/KWSB)", "Duration": "25 days", "Predecessors": "1SS", "Outline Level": 4},

    # --- PHASE 2 ---
    {"WBS": "1.2", "Task Name": "Phase 2: Execution (Civil/MEP/Finishing)", "Duration": "70 days", "Predecessors": "1.1", "Outline Level": 2},
    
    # 2.0 Mobilization
    {"WBS": "1.2.1", "Task Name": "Mobilization & Site Prep", "Duration": "10 days", "Predecessors": "1.1", "Outline Level": 3},
    {"WBS": "1.2.1.1", "Task Name": "Mobilization of Staff & Portacabins", "Duration": "3 days", "Predecessors": "1.1", "Outline Level": 4},
    {"WBS": "1.2.1.2", "Task Name": "Demolition of Existing VIBE/AutoCare", "Duration": "7 days", "Predecessors": "1.2.1.1SS", "Outline Level": 4},
    {"WBS": "1.2.1.3", "Task Name": "Debris Removal & Site Leveling", "Duration": "5 days", "Predecessors": "1.2.1.2", "Outline Level": 4},

    # 2.1 Zone 1: Office Building
    {"WBS": "1.2.2", "Task Name": "Zone 1: Office Building (730 SFT)", "Duration": "55 days", "Predecessors": "1.2.1.2", "Outline Level": 3},
    
    # 2.1.1 Sub-Structure
    {"WBS": "1.2.2.1", "Task Name": "Sub-Structure Works", "Duration": "8 days", "Predecessors": "1.2.1.2", "Outline Level": 4},
    {"WBS": "1.2.2.1.1", "Task Name": "Excavation & Termite Proofing", "Duration": "2 days", "Predecessors": "1.2.1.2", "Outline Level": 5},
    {"WBS": "1.2.2.1.2", "Task Name": "Lean Concrete (1:4:8) & Footing Rebar", "Duration": "2 days", "Predecessors": "1.2.2.1.1", "Outline Level": 5},
    {"WBS": "1.2.2.1.3", "Task Name": "Footing Pour (RCC 1:2:4) & Column Starters", "Duration": "1 days", "Predecessors": "1.2.2.1.2", "Outline Level": 5},
    {"WBS": "1.2.2.1.4", "Task Name": "Plinth Beams, Bitumen Coating & Backfill", "Duration": "3 days", "Predecessors": "1.2.2.1.3", "Outline Level": 5},

    # 2.1.2 Super-Structure
    {"WBS": "1.2.2.2", "Task Name": "Super-Structure Works", "Duration": "15 days", "Predecessors": "1.2.2.1", "Outline Level": 4},
    {"WBS": "1.2.2.2.1", "Task Name": "Column Reinforcement (Grade 60) & Shuttering", "Duration": "4 days", "Predecessors": "1.2.2.1", "Outline Level": 5},
    {"WBS": "1.2.2.2.2", "Task Name": "Column Pouring (1:2:4)", "Duration": "1 days", "Predecessors": "1.2.2.2.1", "Outline Level": 5},
    {"WBS": "1.2.2.2.3", "Task Name": "Roof Beam & Slab Shuttering", "Duration": "5 days", "Predecessors": "1.2.2.2.2", "Outline Level": 5},
    {"WBS": "1.2.2.2.4", "Task Name": "Roof Slab Rebar & MEP Wall/Slab Inserts", "Duration": "4 days", "Predecessors": "1.2.2.2.3", "Outline Level": 5},
    {"WBS": "1.2.2.2.5", "Task Name": "Roof Slab Pouring", "Duration": "1 days", "Predecessors": "1.2.2.2.4", "Outline Level": 5},
    
    # 2.1.3 Arch & Finishing
    {"WBS": "1.2.2.3", "Task Name": "Architecture & Finishing", "Duration": "35 days", "Predecessors": "1.2.2.2.2", "Outline Level": 4},
    {"WBS": "1.2.2.3.1", "Task Name": "Masonry Walls (Block/Brick) (Item 1.027)", "Duration": "8 days", "Predecessors": "1.2.2.2.2", "Outline Level": 5},
    {"WBS": "1.2.2.3.2", "Task Name": "MEP First Fix (Conduits, Wiring 4x35mm, Monolith Wiring)", "Duration": "7 days", "Predecessors": "1.2.2.3.1SS+3 days", "Outline Level": 5},
    {"WBS": "1.2.2.3.3", "Task Name": "Internal Plaster (1/2\" & 3/4\") & False Ceiling", "Duration": "10 days", "Predecessors": "1.2.2.3.1", "Outline Level": 5},
    {"WBS": "1.2.2.3.4", "Task Name": "Flooring (Porcelain Tiles) & Wall Cladding", "Duration": "10 days", "Predecessors": "1.2.2.3.3", "Outline Level": 5},
    {"WBS": "1.2.2.3.5", "Task Name": "Apply Plastic Emulsion & Weather Shield Paint", "Duration": "5 days", "Predecessors": "1.2.2.3.4", "Outline Level": 5},
    {"WBS": "1.2.2.3.6", "Task Name": "Install Split AC Units (1.5 Ton & 1 Ton)", "Duration": "3 days", "Predecessors": "1.2.2.3.5", "Outline Level": 5},

    # 2.2 Zone 2: External
    {"WBS": "1.2.3", "Task Name": "Zone 2: External Infrastructure", "Duration": "50 days", "Predecessors": "1.2.1.2", "Outline Level": 3},
    
    # 2.2.1 Canopy
    {"WBS": "1.2.3.1", "Task Name": "Sub-Zone 2A: Canopy Structure", "Duration": "40 days", "Predecessors": "1.2.1.3", "Outline Level": 4},
    {"WBS": "1.2.3.1.1", "Task Name": "Canopy Foundations (Excavation, Rebar, Pour)", "Duration": "8 days", "Predecessors": "1.2.1.3", "Outline Level": 5},
    {"WBS": "1.2.3.1.2", "Task Name": "Steel Column Erection", "Duration": "5 days", "Predecessors": "1.2.3.1.1", "Outline Level": 5},
    {"WBS": "1.2.3.1.3", "Task Name": "Space Frame/Truss Fabrication (Off-site)", "Duration": "20 days", "Predecessors": "1.1", "Outline Level": 5},
    {"WBS": "1.2.3.1.4", "Task Name": "Space Frame Installation (On-site)", "Duration": "12 days", "Predecessors": "1.2.3.1.2;1.2.3.1.3", "Outline Level": 5},
    {"WBS": "1.2.3.1.5", "Task Name": "Gutter & Sheeting Installation", "Duration": "10 days", "Predecessors": "1.2.3.1.4", "Outline Level": 5},
    {"WBS": "1.2.3.1.6", "Task Name": "Quick Oil Change Canopy (Shift, Floor, Tile)", "Duration": "10 days", "Predecessors": "1.2.3.1.5", "Outline Level": 5},
    
    # 2.2.2 Fuel System
    {"WBS": "1.2.3.2", "Task Name": "Sub-Zone 2B: Fuel System (UGFS)", "Duration": "35 days", "Predecessors": "1.2.1.2", "Outline Level": 4},
    {"WBS": "1.2.3.2.1", "Task Name": "RCC Pit Excavation & Construction", "Duration": "6 days", "Predecessors": "1.2.1.2", "Outline Level": 5},
    {"WBS": "1.2.3.2.2", "Task Name": "Lean & Base Slab", "Duration": "5 days", "Predecessors": "1.2.3.2.1", "Outline Level": 5},
    {"WBS": "1.2.3.2.3", "Task Name": "UGFS Tank (15/25KL) Lowering & Install", "Duration": "5 days", "Predecessors": "1.2.3.2.2", "Outline Level": 5},
    {"WBS": "1.2.3.2.4", "Task Name": "Fuel Piping (UPP 54mm) & Decantation Lines", "Duration": "10 days", "Predecessors": "1.2.3.2.3", "Outline Level": 5},
    {"WBS": "1.2.3.2.5", "Task Name": "Sand Filling & Top Slab", "Duration": "5 days", "Predecessors": "1.2.3.2.4", "Outline Level": 5},
    {"WBS": "1.2.3.2.6", "Task Name": "Dispenser Islands & Pump Installation", "Duration": "5 days", "Predecessors": "1.2.3.2.5", "Outline Level": 5},

    # 2.2.3 Civil & Paving
    {"WBS": "1.2.3.3", "Task Name": "Sub-Zone 2C: Civil & Paving", "Duration": "20 days", "Predecessors": "1.2.3.2.6", "Outline Level": 4},
    {"WBS": "1.2.3.3.1", "Task Name": "Boundary Wall Construction", "Duration": "30 days", "Predecessors": "1.2.1.3", "Outline Level": 5},
    {"WBS": "1.2.3.3.2", "Task Name": "Construct Septic Tank & Manholes (Item 1.030/1.031)", "Duration": "10 days", "Predecessors": "1.2.3.2.4", "Outline Level": 5},
    {"WBS": "1.2.3.3.3", "Task Name": "Driveway Sub-base & Cut-off Drain (Item 1.013)", "Duration": "10 days", "Predecessors": "1.2.3.2.5", "Outline Level": 5},
    {"WBS": "1.2.3.3.4", "Task Name": "Stone Soling & Wiring for Light Poles", "Duration": "5 days", "Predecessors": "1.2.3.3.3", "Outline Level": 5},
    {"WBS": "1.2.3.3.5", "Task Name": "Pavers / Concrete Paving & Curb Stones", "Duration": "10 days", "Predecessors": "1.2.3.3.4", "Outline Level": 5},

    # --- PHASE 3 ---
    {"WBS": "1.3", "Task Name": "Phase 3: Closing & Handover", "Duration": "10 days", "Predecessors": "1.2.2.3.6;1.2.3.3.5", "Outline Level": 2},
    {"WBS": "1.3.1", "Task Name": "Testing & Commissioning (Fuel, Electric, Light)", "Duration": "5 days", "Predecessors": "1.2.2.3.6;1.2.3.3.5", "Outline Level": 3},
    {"WBS": "1.3.2", "Task Name": "Snag List Rectification", "Duration": "3 days", "Predecessors": "1.3.1", "Outline Level": 3},
    {"WBS": "1.3.3", "Task Name": "Final Cleaning & Handover", "Duration": "2 days", "Predecessors": "1.3.2", "Outline Level": 3},
]

# 1. Assign Row IDs (Excel Row #)
# Assuming Header is Row 1, Data starts Row 2.
start_row = 2
for i, task in enumerate(tasks):
    task['Row_ID'] = start_row + i

# 2. Build Map: WBS -> Row_ID
wbs_map = {task['WBS']: str(task['Row_ID']) for task in tasks}

# 3. Resolve Predecessors
def resolve_preds(pred_str):
    if not pred_str:
        return ""
    
    # Split by semicolon (for multiple preds)
    preds = pred_str.split(';')
    resolved_preds = []
    
    for p in preds:
        p = p.strip()
        if not p:
            continue
            
        # Regex to capture WBS part and optional Type/Lag part
        # WBS can be numbers and dots: 1.2.3.4
        # Suffix can be SS, FF, SF, FS, +3 days, etc.
        # Example: "1.2.1SS+3 days" -> WBS="1.2.1", Suffix="SS+3 days"
        
        # We look for the longest matching WBS from the map
        # This is a bit tricky with simple parsing, so let's try finding the WBS code that exists in our map.
        
        found_wbs = None
        suffix = ""
        
        # Heuristic: Match valid WBS codes starting from the longest possible match
        # or simple regex: starts with digits/dots
        match = re.match(r"^([\d\.]+)(.*)", p)
        if match:
            potential_wbs = match.group(1)
            remaining = match.group(2)
            
            if potential_wbs in wbs_map:
                found_wbs = potential_wbs
                suffix = remaining
            else:
                # Iterate to find best match if WBS itself contains something else?
                # Actually our WBS are strict numbers.dots
                pass
        
        if found_wbs:
            row_id = wbs_map[found_wbs]
            resolved_preds.append(f"{row_id}{suffix}")
        else:
            print(f"Warning: Could not resolve WBS in predecessor: '{p}'")
            resolved_preds.append(p) # Keep original if fail
            
    return ";".join(resolved_preds)

# Apply resolution
for task in tasks:
    task['Predecessors_WBS'] = task['Predecessors'] # Keep original for reference
    task['Predecessors'] = resolve_preds(task['Predecessors'])

# Create DataFrame
# We export columns in a specific order for MS Project mapping convenience
cols = ["WBS", "Task Name", "Duration", "Predecessors", "Outline Level", "Row_ID"]
df = pd.DataFrame(tasks, columns=cols)

# Save to Excel
output_file = "d:/my-dev-knowledge-base/Project_Schedule_MSP_Export_v4.xlsx"
df.to_excel(output_file, index=False)
print(f"Schedule V4 exported to {output_file}")
print("Included 'Row_ID' column for verification.")
print("Predecessors converted from WBS (e.g., 1.1) to Excel Row IDs (e.g., 3).")
