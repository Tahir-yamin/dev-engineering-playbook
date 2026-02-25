import pandas as pd
import os

# Audit Configuration
SCHEDULE_FILE = "d:/my-dev-knowledge-base/Project_Schedule_MSP_Export_v13.xlsx"
REQUIRED_PHASES = ["Admin", "Execution", "Closing"]
REQUIRED_ZONES = ["Zone 1", "Zone 2"]

def audit_schedule():
    print("🚀 Running Gemini Schedule Audit (v1.0 Sovereign)...\n")
    
    if not os.path.exists(SCHEDULE_FILE):
        print(f"❌ CRITICAL: Schedule file not found: {SCHEDULE_FILE}")
        return

    try:
        df = pd.read_excel(SCHEDULE_FILE)
        print(f"✅ Loaded Schedule: {len(df)} items.")
    except Exception as e:
        print(f"❌ Error reading Excel: {e}")
        return

    issues = []
    warnings = []

    # 1. Structure Audit (Phases/Zones)
    task_names = df['Task Name'].astype(str).tolist()
    print("\n🔍 Structure Audit:")
    for phase in REQUIRED_PHASES:
        found = any(phase in t for t in task_names)
        if found:
            print(f"✅ Phase Found: {phase}")
        else:
            issues.append(f"Missing Phase: {phase}")
            print(f"❌ Missing Phase: {phase}")

    # 2. Logic Audit (Predecessors)
    print("\n🧠 Logic & Constraints Audit:")
    # Check for Open Ends (Tasks with no successors/predecessors - simplified check for preds here)
    # Filter for leaf tasks (Outline Level > highest level)
    # For now, just check if Predecessors column serves data
    pred_filled = df[df['Predecessors'].notna() & (df['Predecessors'] != "")]
    print(f"✅ Tasks with Logic Links: {len(pred_filled)}/{len(df)}")
    
    if len(pred_filled) < len(df) * 0.8: # 80% coverage expected
        warnings.append("Low Logic Coverage (<80%)")
    
    # 3. Duration Audit
    total_duration_display = df.iloc[0]['Duration']
    print(f"\n⏱️ Duration Audit:")
    print(f"stated Project Duration: {total_duration_display}")
    if "100 days" in str(total_duration_display).lower():
         print("✅ Target Duration (100 Days) Met.")
    else:
         warnings.append(f"Duration Mismatch: {total_duration_display}")

    # 4. Pro-Level Item Check
    pro_items = [
        "Excavation", "Termite Proofing", "Lean Concrete", "Footing", "Short Column", "Plinth Beam", 
        "Bitumen", "Backfill", "Super-Structure Columns", "Roof Slab", "Curing",
        "MEP Rough-Ins", "Anchor Bolts", "Space Frame", "As-Built", "Training"
    ]
    print("\n🏗️ Construction Detail Audit:")
    for item in pro_items:
        found = any(item.lower() in t.lower() for t in task_names)
        if not found:
            warnings.append(f"Missing Pro-Detail: {item}")
        # else:
            # print(f"✅ Found: {item}")
    
    if not warnings:
        print("✅ All Pro-Level Details verified.")

    # Final Report
    print("\n" + "="*30)
    if not issues and not warnings:
        print("✨ SCHEDULE AUDIT PASSED: SOVEREIGN STATUS REACHED.")
    else:
        print("⚠️  AUDIT FINDINGS:")
        for i in issues: print(f"🔴 {i}")
        for w in warnings: print(f"KJ {w}")
    print("="*30)

if __name__ == "__main__":
    audit_schedule()
