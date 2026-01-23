---
description: Create a professional project schedule from scratch using PMI/AACE best practices
---

# Create Project Schedule from Scratch

// turbo-all

## Prerequisites
- MS Project 2016+ installed OR Primavera P6
- Project scope/contract available
- WBS or scope breakdown

---

## Phase 1: Preparation (Day 1)

### 1.1 Gather Inputs
- [ ] Obtain project scope/contract
- [ ] Review WBS or create one
- [ ] Identify contractual milestones
- [ ] List key stakeholders

### 1.2 Set Up Project Calendar
```
MS Project: Project → Change Working Time
- Set working days (Mon-Fri or Mon-Sat)
- Define working hours (8:00-17:00)
- Add holidays and exceptions
```

### 1.3 Define Schedule Structure
Determine level of detail based on project size:
- **Level 1** (Summary): 10-50 activities
- **Level 2** (Control): 50-200 activities  
- **Level 3** (Detailed): 200-500 activities
- **Level 4** (Working): 500+ activities

---

## Phase 2: WBS Development (Day 1-2)

### 2.1 Create WBS Hierarchy
```
Enter in MS Project Task Name column:
1.0 Project Management
  1.1 Project Initiation
  1.2 Project Planning
  1.3 Project Monitoring
2.0 Design Phase
  2.1 Conceptual Design
  2.2 Detailed Design
3.0 Execution Phase
  ...
```

### 2.2 Apply WBS Codes
```
MS Project: Project → WBS → Define Code
- Level 1: 1.0, 2.0, 3.0...
- Level 2: 1.1, 1.2, 2.1...
- Level 3: 1.1.1, 1.1.2...
```

### 2.3 Decompose into Activities
Break work packages into:
- Discrete, measurable tasks
- 5-44 day durations (DCMA guideline)
- Clear start/finish definitions

---

## Phase 3: Logic Development (Day 2-3)

### 3.1 Sequence Activities
```
In Predecessors column, enter:
- Task ID for Finish-to-Start (e.g., "5")
- SS for Start-to-Start (e.g., "5SS")
- FF for Finish-to-Finish (e.g., "5FF")
```

### 3.2 Dependency Guidelines
**Use 90%+ Finish-to-Start (FS) relationships**

| Relationship | When to Use |
|--------------|-------------|
| FS | Default - predecessor must finish before successor starts |
| SS | Activities must start together |
| FF | Activities must finish together |
| SF | Rare - successor needs predecessor to start |

### 3.3 Minimize Leads and Lags
- **Leads** (negative lag): Avoid if possible (<5%)
- **Lags** (positive lag): Use sparingly (<5%)
- Document reason for any lead/lag

---

## Phase 4: Duration Estimation (Day 3-4)

### 4.1 Choose Estimation Method
**PERT (Three-Point) for uncertain activities:**
```
Expected = (Optimistic + 4×Most Likely + Pessimistic) / 6
```

**Analogous for similar past work:**
```
Duration = Historical duration × adjustment factor
```

### 4.2 Enter Durations
```
In Duration column:
- Days: "5d" or "5 days"
- Weeks: "2w" or "2 weeks"
- Months: "1mo" or "1 mon"
- Milestones: "0d"
```

### 4.3 Document Basis of Estimates
For each activity, record:
- Source of estimate (SME, historical, parametric)
- Assumptions made
- Risk factors considered

---

## Phase 5: Resource Loading (Day 4-5)

### 5.1 Create Resource Pool
```
MS Project: View → Resource Sheet
Enter: Name, Type, Max Units, Standard Rate
```

| Type | Examples |
|------|----------|
| Work | PM, Engineers, Operators |
| Material | Concrete, Steel, Equipment |
| Cost | Travel, Permits, Subcontracts |

### 5.2 Assign Resources to Tasks
```
Select task → Resource Tab → Assign Resources
OR
Enter in Resource Names column: "Engineer[50%], PM[25%]"
```

### 5.3 Level Resources
```
MS Project: Resource → Level All
- Resolve over-allocations
- Check resource histogram
```

---

## Phase 6: Schedule Calculation (Day 5)

### 6.1 Calculate Schedule
```
MS Project automatically calculates when in Auto Schedule mode
```

### 6.2 Identify Critical Path
```
MS Project: Format → Critical Tasks (check box)
OR
View → Gantt Chart → Format → Bar Styles
```

### 6.3 Analyze Float
```
Add columns: Total Slack, Free Slack
- Critical activities: Total Float = 0
- Non-critical: Total Float > 0
```

---

## Phase 7: Quality Check - DCMA 14-Point (Day 5-6)

Run these checks before baseline:

| # | Check | Target | Action if Fail |
|---|-------|--------|----------------|
| 1 | Missing Logic | <5% | Add predecessors/successors |
| 2 | Leads | 0% | Remove negative lags |
| 3 | Lags | <5% | Minimize or document |
| 4 | Relationship Types | >90% FS | Convert to Finish-Start |
| 5 | Hard Constraints | <5% | Remove unnecessary constraints |
| 6 | High Float | <5% | Review logic |
| 7 | Negative Float | 0% | Fix critical path issues |
| 8 | High Duration | <5% | Break into smaller tasks |
| 9 | Invalid Dates | 0% | Correct forecast/actual dates |
| 10 | Resources | 100% | Assign all resources |
| 11 | Missed Tasks | <5% | Update actuals |
| 12 | Critical Path Test | Pass | Verify logic integrity |
| 13 | CPLI | >0.95 | Improve performance |
| 14 | BEI | >0.95 | Address delays |

---

## Phase 8: Baseline (Day 6)

### 8.1 Review and Approve
- [ ] Walkthrough with team
- [ ] Stakeholder review
- [ ] Management approval

### 8.2 Save Baseline
```
MS Project: Project → Set Baseline → Set Baseline
- Select "Entire Project"
- Choose Baseline (1-10)
- Click OK
```

### 8.3 Document Baseline
- Record baseline date
- Export baseline report
- Distribute to stakeholders

---

## Deliverables Checklist

- [ ] Project calendar configured
- [ ] WBS structure complete
- [ ] All activities defined with IDs
- [ ] Logic established (>90% FS)
- [ ] Durations estimated and documented
- [ ] Resources assigned
- [ ] Critical path identified
- [ ] DCMA 14-Point assessment passed
- [ ] Baseline saved
- [ ] Schedule distributed

---

## Related Skills
- [Project Scheduling Best Practices](file:///d:/my-dev-knowledge-base/skills/project-scheduling-best-practices.md)
- [MS Project Skills](file:///d:/my-dev-knowledge-base/skills/ms-project-skills.md)
- [Primavera P6 Skills](file:///d:/my-dev-knowledge-base/skills/primavera-p6-skills.md)
