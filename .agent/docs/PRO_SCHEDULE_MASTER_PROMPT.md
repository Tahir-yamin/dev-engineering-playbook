# Pro-Level Project Schedule Master Prompt

> **Usage**: Copy and paste the text below into the chat when starting a new Fuel Station or Construction project to instantly apply the "Sovereign" standards we developed.

---

## 📋 Copy This Prompt:

**Role**: You are a Senior Project Scheduler & Construction Manager.
**Task**: Create a Level 3 "Sovereign Status" Project Schedule for a Fuel Station Rehabilitation.

### 1. Mandatory WBS Structure
Decompose the project into these specific Phases and Zones:
*   **Phase 1: Admin**: Survey, Structural Vetting, NOCs, Power Enhancement.
*   **Phase 2: Execution**:
    *   **Mobilization**: Staff, Hoarding, Dismantling.
    *   **Zone 1 (Building)**: Sub-structure (Footings/Plinth), Super-structure (Cols/Roof), MEP, Finishing.
    *   **Zone 2A (Canopy)**: Foundations, Space Frame Fab, Erection, Sheeting.
    *   **Zone 2B (Fuel System)**: Tanks, Anchoring, Piping, Pumps.
    *   **Zone 2C (External)**: Driveway, Pavers, Manholes.
*   **Phase 3: Closing**: Testing, Commissioning, As-Builts.

### 2. "Sovereign" Logic Rules (Crucial)
*   **Curing Constraints**:
    *   **Structural Concrete (Footings/Cols)**: Enforce **7 Days** curing (Task: `[QC] Curing`).
    *   **Roof Slab**: Enforce **14 Days** curing (Task: `[QC] Roof Curing`).
*   **Quality Milestones**:
    *   **Civil**: Field Density Test (FDT) for compaction.
    *   **MEP**: Hydro-Test (Plumbing) & IR Test (Electrical).
    *   **Fuel**: Nitrogen Pressure Test & Tank Coating Inspection.
*   **Fast-Tracking**:
    *   Do **NOT** wait for 14-day roof curing to finish before starting internal work.
    *   **Rule**: Start "Internal Plaster" 3 days after "Roof Pour" (Overlap).
    *   **Target Duration**: Max **100 Days** (or user specified).

### 3. MS Project Compatibility
*   **Predecessors**: Use **ONLY** "FS" (Finish-to-Start), "SS" (Start-to-Start), or "FF". **NEVER** use "SW".
*   **Columns**: Generate an Excel file with: `WBS`, `Task Name`, `Duration`, `Predecessors`, `Outline Level`, `MSP_ID`.
*   **ID Mapping**: Ensure `Predecessors` column references the `MSP_ID` (1, 2, 3...), not the WBS (1.1.2).

### 4. Output Requirements
1.  **Generate Python Script**: Create a script to generate the `.xlsx` file.
2.  **Audit**: Run a self-check to ensure 0 circular loops and 0 missing logic links.
3.  **Import Guide**: Remind me to map `Task Name` -> `Name` and `MSP_ID` -> `ID` when importing to MSP.

---
