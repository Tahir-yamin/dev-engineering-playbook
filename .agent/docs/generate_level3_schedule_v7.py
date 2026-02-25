import pandas as pd
from datetime import datetime, timedelta
import re

# --- Project Configuration ---
# Start Date: 13 Feb 2026
# Working Days: 7 days/week (Implied by standard day calculation in Python)
PROJECT_START_DATE = datetime(2026, 2, 13).date()

# Helper to calculate End Date based on Duration (Approximation for Display)
def calc_end_date(start_date, duration_days):
    return start_date + timedelta(days=duration_days)

tasks = [
    # --- LEVEL 1: PROJECT SUMMARY ---
    {"WBS": "1", "Task Name": "Rehabilitation of CF Site MS. Globe FS (Target: 100 Days)", "Duration": "100 days", "Predecessors": "", "Outline Level": 1},
    
    # --- PHASE 1: ADMIN & APPROVALS (30 Days) ---
    {"WBS": "1.1", "Task Name": "Phase 1: Admin, NOCs & Approvals", "Duration": "30 days", "Predecessors": "", "Outline Level": 2},
    {"WBS": "1.1.1", "Task Name": "Topographic Survey & Layout", "Duration": "5 days", "Predecessors": "1SS", "Outline Level": 3},
    {"WBS": "1.1.2", "Task Name": "Structural Vetting (Office & Canopy)", "Duration": "10 days", "Predecessors": "1.1.1", "Outline Level": 3},
    {"WBS": "1.1.3", "Task Name": "NOC Application & Processing (DC, KMC, KWSB)", "Duration": "30 days", "Predecessors": "1SS", "Outline Level": 3},
    {"WBS": "1.1.4", "Task Name": "Item 1.033: Enhancement of Power Connection (K-Electric) & CIE Approval", "Duration": "30 days", "Predecessors": "1SS", "Outline Level": 3},

    # --- PHASE 2: EXECUTION (70 Days) ---
    # OPTIMIZATION: Overlap Phase 2 with Phase 1. 
    # Mobilization starts after 15 days of Admin (Provisional/Parallel start).
    {"WBS": "1.2", "Task Name": "Phase 2: Execution (Civil, MEP, Finishing)", "Duration": "70 days", "Predecessors": "1.1SS+15d", "Outline Level": 2},
    
    # --- 2.1 MOBILIZATION & PREP (Item 1.001) ---
    {"WBS": "1.2.1", "Task Name": "Item 1.001: Mobilization & Preparatory Works", "Duration": "10 days", "Predecessors": "1.1SS+15d", "Outline Level": 3},
    {"WBS": "1.2.1.1", "Task Name": "Mobilization of Staff, Eqpt & Safety Hoarding (Item 1.001)", "Duration": "3 days", "Predecessors": "1.1SS+15d", "Outline Level": 4},
    {"WBS": "1.2.1.2", "Task Name": "Dismantling Existing Structures/Pavers (Item 1.001)", "Duration": "7 days", "Predecessors": "1.2.1.1SS+1d", "Outline Level": 4},
    {"WBS": "1.2.1.3", "Task Name": "Debris Removal & Site Leveling", "Duration": "5 days", "Predecessors": "1.2.1.2", "Outline Level": 4},

    # --- 2.2 ZONE 1: OFFICE BUILDING (Item 1.002) ---
    {"WBS": "1.2.2", "Task Name": "Zone 1: Office Kiosk Conversion (Item 1.002)", "Duration": "55 days", "Predecessors": "1.2.1.2", "Outline Level": 3},
    
    # 2.2.1 Civil / Structure
    {"WBS": "1.2.2.1", "Task Name": "Civil & Structural Works (Office)", "Duration": "20 days", "Predecessors": "1.2.1.2", "Outline Level": 4},
    {"WBS": "1.2.2.1.1", "Task Name": "Excavation & Termite Proofing (Item 1.018)", "Duration": "3 days", "Predecessors": "1.2.1.2", "Outline Level": 5},
    {"WBS": "1.2.2.1.2", "Task Name": "Lean Concrete 1:4:8 (Item 1.022)", "Duration": "2 days", "Predecessors": "1.2.2.1.1", "Outline Level": 5},
    {"WBS": "1.2.2.1.3", "Task Name": "RCC 1:2:4 Footings & Columns (Item 1.023, 1.024)", "Duration": "5 days", "Predecessors": "1.2.2.1.2", "Outline Level": 5},
    {"WBS": "1.2.2.1.4", "Task Name": "Brick/Block Masonry Walls (Item 1.027)", "Duration": "10 days", "Predecessors": "1.2.2.1.3", "Outline Level": 5},
    
    # 2.2.2 Finishing
    {"WBS": "1.2.2.2", "Task Name": "Finishing Works (Office)", "Duration": "30 days", "Predecessors": "1.2.2.1.4", "Outline Level": 4},
    {"WBS": "1.2.2.2.1", "Task Name": "Internal Plaster 1/2\" (Item 1.025)", "Duration": "8 days", "Predecessors": "1.2.2.1.4", "Outline Level": 5},
    {"WBS": "1.2.2.2.2", "Task Name": "External Plaster 3/4\" (Item 1.026)", "Duration": "8 days", "Predecessors": "1.2.2.2.1", "Outline Level": 5},
    {"WBS": "1.2.2.2.3", "Task Name": "Flooring (Porcelain Tiles) (Item 1.002)", "Duration": "7 days", "Predecessors": "1.2.2.2.1", "Outline Level": 5},
    {"WBS": "1.2.2.2.4", "Task Name": "Plastic Emulsion Paint (Internal) (Item 1.028)", "Duration": "5 days", "Predecessors": "1.2.2.2.3", "Outline Level": 5},
    {"WBS": "1.2.2.2.5", "Task Name": "Weather Shield Paint (External) (Item 1.029)", "Duration": "5 days", "Predecessors": "1.2.2.2.2", "Outline Level": 5},

    # 2.2.3 MEP (Office)
    {"WBS": "1.2.2.3", "Task Name": "MEP Works (Office)", "Duration": "15 days", "Predecessors": "1.2.2.1.4", "Outline Level": 4},
    {"WBS": "1.2.2.3.1", "Task Name": "Electrical Wiring (Light/Power) (Item 1.002)", "Duration": "5 days", "Predecessors": "1.2.2.1.4", "Outline Level": 5},
    {"WBS": "1.2.2.3.2", "Task Name": "Plumbing & Sanitary Works (Item 1.002)", "Duration": "5 days", "Predecessors": "1.2.2.1.4", "Outline Level": 5},
    {"WBS": "1.2.2.3.3", "Task Name": "Install Split AC 1.5 Ton (Item 2) & 1 Ton (Item 3)", "Duration": "2 days", "Predecessors": "1.2.2.2.4", "Outline Level": 5},

    # --- 2.3 ZONE 2: EXTERNAL INFRASTRUCTURE ---
    {"WBS": "1.2.3", "Task Name": "Zone 2: External Infrastructure (Canopy, Fuel, Paving)", "Duration": "65 days", "Predecessors": "1.2.1.2", "Outline Level": 3},
    
    # 2.3.1 Canopy Structure (Item 1.003)
    {"WBS": "1.2.3.1", "Task Name": "Sub-Zone 2A: Steel Canopy (Item 1.003)", "Duration": "40 days", "Predecessors": "1.2.1.3", "Outline Level": 4},
    {"WBS": "1.2.3.1.1", "Task Name": "Canopy Foundations (Excavation, Rebar, Concrete) (Item 1.003)", "Duration": "8 days", "Predecessors": "1.2.1.3", "Outline Level": 5},
    {"WBS": "1.2.3.1.2", "Task Name": "Steel Column Erection & Clean/Paint", "Duration": "5 days", "Predecessors": "1.2.3.1.1", "Outline Level": 5},
    {"WBS": "1.2.3.1.3", "Task Name": "Space Frame Fabrication & Sheet Install (Item 1.003)", "Duration": "15 days", "Predecessors": "1.2.3.1.2", "Outline Level": 5},
    {"WBS": "1.2.3.1.4", "Task Name": "False Ceiling & Gutter Installation (Item 1.003)", "Duration": "10 days", "Predecessors": "1.2.3.1.3", "Outline Level": 5},
    {"WBS": "1.2.3.1.5", "Task Name": "Quick Oil Change Canopy Shifting (Item 1.032)", "Duration": "5 days", "Predecessors": "1.2.3.1.4", "Outline Level": 5},
    
    # 2.3.2 Fuel System (Items 1.004-1.010, 1.034-1.035)
    {"WBS": "1.2.3.2", "Task Name": "Sub-Zone 2B: Fuel System (UGFS & Pumps)", "Duration": "45 days", "Predecessors": "1.2.1.2", "Outline Level": 4},
    {"WBS": "1.2.3.2.1", "Task Name": "RCC Pit Excavation & Construction (Item 1.018-1.024)", "Duration": "10 days", "Predecessors": "1.2.1.2", "Outline Level": 5},
    {"WBS": "1.2.3.2.2", "Task Name": "Install UGFS Tank 15/25KL (Item 1.006)", "Duration": "5 days", "Predecessors": "1.2.3.2.1", "Outline Level": 5},
    {"WBS": "1.2.3.2.3", "Task Name": "Repair Existing UGFS Tank Pit (Item 1.007)", "Duration": "8 days", "Predecessors": "1.2.3.2.1", "Outline Level": 5},
    {"WBS": "1.2.3.2.4", "Task Name": "Install UPP Fuel Pipe 54mm (Item 1.008)", "Duration": "7 days", "Predecessors": "1.2.3.2.2", "Outline Level": 5},
    {"WBS": "1.2.3.2.5", "Task Name": "Decantation Piping 3\" dia (Item 1.009)", "Duration": "5 days", "Predecessors": "1.2.3.2.4", "Outline Level": 5},
    {"WBS": "1.2.3.2.6", "Task Name": "Pump Island Construction & Tiling (Item 1.004, 1.005)", "Duration": "10 days", "Predecessors": "1.2.3.2.4", "Outline Level": 5},
    {"WBS": "1.2.3.2.7", "Task Name": "Guard Rail Installation at Fill Point (Item 1.010)", "Duration": "3 days", "Predecessors": "1.2.3.2.6", "Outline Level": 5},
    {"WBS": "1.2.3.2.8", "Task Name": "Wiring for DU & Motor (Item 1.035) & Spreader (Item 1.034)", "Duration": "5 days", "Predecessors": "1.2.3.2.6", "Outline Level": 5},

    # 2.3.3 Civil & External Works (Items 1.011-1.014, 1.030-1.031)
    {"WBS": "1.2.3.3", "Task Name": "Sub-Zone 2C: Driveway, Paving & Drainage", "Duration": "30 days", "Predecessors": "1.2.3.2.4", "Outline Level": 4},
    {"WBS": "1.2.3.3.1", "Task Name": "Underground Water Tank Construction (Item 1.014)", "Duration": "15 days", "Predecessors": "1.2.1.3", "Outline Level": 5},
    {"WBS": "1.2.3.3.2", "Task Name": "Manhole Construction (Item 1.030, 1.031)", "Duration": "8 days", "Predecessors": "1.2.3.3.1SS", "Outline Level": 5},
    {"WBS": "1.2.3.3.3", "Task Name": "Cut-off Drain Construction (Item 1.013)", "Duration": "10 days", "Predecessors": "1.2.3.3.1", "Outline Level": 5},
    {"WBS": "1.2.3.3.4", "Task Name": "Stone Soling for Paving (Item 1.020)", "Duration": "5 days", "Predecessors": "1.2.3.3.3", "Outline Level": 5},
    {"WBS": "1.2.3.3.5", "Task Name": "Supply & Lay 60mm Pavers (Item 1.011)", "Duration": "12 days", "Predecessors": "1.2.3.3.4", "Outline Level": 5},
    {"WBS": "1.2.3.3.6", "Task Name": "Curb Stone Installation (Item 1.012)", "Duration": "8 days", "Predecessors": "1.2.3.3.5SS", "Outline Level": 5},
    {"WBS": "1.2.3.3.7", "Task Name": "Drain Lines UPVC 8\" (Item 1.038)", "Duration": "5 days", "Predecessors": "1.2.3.3.3", "Outline Level": 5},
    {"WBS": "1.2.3.3.8", "Task Name": "Install 1-HP Centrifugal Pump (Item 1.037)", "Duration": "2 days", "Predecessors": "1.2.3.3.1", "Outline Level": 5},

    # 2.3.4 External Electrical (Items 1.015-1.017, 1.036, 1.039-1.042)
    {"WBS": "1.2.3.4", "Task Name": "Sub-Zone 2D: External Electrical & Lighting", "Duration": "20 days", "Predecessors": "1.2.3.3.4", "Outline Level": 4},
    {"WBS": "1.2.3.4.1", "Task Name": "Cable Sleeves UPVC 6\", 4\", 2\" (Item 1.039, 1.040, 1.041)", "Duration": "5 days", "Predecessors": "1.2.3.3.4SS", "Outline Level": 5},
    {"WBS": "1.2.3.4.2", "Task Name": "Main Wiring 4x35 sq.mm (Item 1.036)", "Duration": "5 days", "Predecessors": "1.2.3.4.1", "Outline Level": 5},
    {"WBS": "1.2.3.4.3", "Task Name": "Single Light Pole 24-Ft (Item 1.015)", "Duration": "5 days", "Predecessors": "1.2.3.4.1", "Outline Level": 5},
    {"WBS": "1.2.3.4.4", "Task Name": "Double Light Pole 24-Ft (Item 1.016)", "Duration": "5 days", "Predecessors": "1.2.3.4.1", "Outline Level": 5},
    {"WBS": "1.2.3.4.5", "Task Name": "Wiring for Light Poles (Item 1.017)", "Duration": "5 days", "Predecessors": "1.2.3.4.3;1.2.3.4.4", "Outline Level": 5},
    {"WBS": "1.2.3.4.6", "Task Name": "Wiring for Monolith (Item 1.042)", "Duration": "3 days", "Predecessors": "1.2.3.4.1", "Outline Level": 5},

    # --- PHASE 3: CLOSING (10 Days) ---
    {"WBS": "1.3", "Task Name": "Phase 3: Closing & Handover", "Duration": "10 days", "Predecessors": "1.2.2.2.5;1.2.3.3.5;1.2.3.4.5", "Outline Level": 2},
    {"WBS": "1.3.1", "Task Name": "Testing & Commissioning (Fuel, Electric, Light)", "Duration": "5 days", "Predecessors": "1.2.2.2.5;1.2.3.3.5", "Outline Level": 3},
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
    
    # Normalize separators to semicolon for processing
    pred_str = pred_str.replace(",", ";") 
    preds = pred_str.split(';')
    resolved_preds = []
    
    for p in preds:
        p = p.strip()
        if not p:
            continue
            
        found_wbs = None
        suffix = ""
        
        # Match valid WBS codes
        match = re.match(r"^([\d\.]+)(.*)", p)
        if match:
            potential_wbs = match.group(1)
            raw_suffix = match.group(2)
            
            if potential_wbs in wbs_map:
                found_wbs = potential_wbs
                # Cleanup Suffix: " days" -> "d", remove spaces
                suffix = raw_suffix.replace(" days", "d").replace(" ", "")
        
        if found_wbs:
            row_id = wbs_map[found_wbs]
            resolved_preds.append(f"{row_id}{suffix}")
        else:
            print(f"Warning: Could not resolve WBS in predecessor: '{p}'")
            resolved_preds.append(p) 
            
    # Join with comma for MS Project (US/Standard)
    return ",".join(resolved_preds)

# Apply resolution
for task in tasks:
    task['Predecessors_WBS'] = task['Predecessors'] # Keep original for reference
    task['Predecessors'] = resolve_preds(task['Predecessors'])

# Create DataFrame
cols = ["WBS", "Task Name", "Duration", "Predecessors", "Outline Level", "Row_ID"]
df = pd.DataFrame(tasks, columns=cols)

# Output Summary of Verification
print(f"Project Start Date: {PROJECT_START_DATE}")
print(f"Total Items: {len(tasks)}")
print(f"Phase 1 Duration: {tasks[1]['Duration']}")
print(f"Phase 2 Duration: {tasks[6]['Duration']}")
print("Note: Overlap logic '1.1SS+15d' applied to Mobilization to compress total Project Duration.")

# Save to Excel
output_file = "d:/my-dev-knowledge-base/Project_Schedule_MSP_Export_v7.xlsx"
df.to_excel(output_file, index=False)
print(f"Schedule V7 exported to {output_file}")
