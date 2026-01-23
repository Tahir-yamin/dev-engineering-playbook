# Professional Project Schedule Development

> **Purpose**: Create project schedules from scratch using industry best practices from PMI, AACE International, and DCMA standards.

## 📚 Industry Standards Referenced

| Organization | Standard/Document | Focus |
|--------------|-------------------|-------|
| **PMI** | PMBOK Guide 6th/7th Edition | Project Schedule Management |
| **PMI** | Practice Standard for Scheduling | Scheduling techniques |
| **AACE International** | RP 91R-16 Schedule Development | Schedule creation process |
| **AACE International** | RP 37R-06 Schedule Levels of Detail | Detail requirements |
| **AACE International** | RP 128R-23 Practitioner Roles | Scheduler responsibilities |
| **DCMA** | 14-Point Schedule Assessment | Schedule quality metrics |

---

## 🏗️ PMI PMBOK Schedule Management Processes

### The 6 Schedule Management Processes

```
┌─────────────────────────────────────────────────────────────────┐
│                    SCHEDULE MANAGEMENT                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. Plan Schedule Management → Define approach & policies       │
│ 2. Define Activities        → Break WBS into activities        │
│ 3. Sequence Activities      → Establish dependencies           │
│ 4. Estimate Resources       → Identify resource needs          │
│ 5. Estimate Durations       → Calculate time requirements      │
│ 6. Develop Schedule         → Create the schedule model        │
└─────────────────────────────────────────────────────────────────┘
```

### Process Details

#### 1. Plan Schedule Management
**Output**: Schedule Management Plan
- Scheduling methodology (CPM, Agile, hybrid)
- Level of accuracy for estimates
- Units of measure (days, weeks)
- Control thresholds for variance
- Reporting formats

#### 2. Define Activities
**Input**: WBS, Scope Statement
**Output**: Activity List, Activity Attributes
- Decompose work packages into activities
- Each activity = single work effort
- Create unique activity IDs
- Document attributes (description, predecessors, resources)

#### 3. Sequence Activities
**Output**: Project Schedule Network Diagram
- Identify dependencies (FS, SS, FF, SF)
- Mandatory vs. discretionary dependencies
- External dependencies
- Use Precedence Diagramming Method (PDM)

#### 4. Estimate Activity Resources
**Output**: Resource Requirements
- Work resources (people, equipment)
- Material resources
- Cost resources
- Resource availability calendars

#### 5. Estimate Activity Durations
**Output**: Duration Estimates
- Three-point estimating (PERT): (O + 4M + P) / 6
- Analogous (historical comparison)
- Parametric (unit rates)
- Expert judgment

#### 6. Develop Schedule
**Output**: Schedule Baseline, Schedule Model
- Critical Path Method (CPM) analysis
- Resource optimization
- Schedule compression (crashing, fast-tracking)
- Gantt chart creation

---

## 📐 Key Scheduling Techniques

### Work Breakdown Structure (WBS)
The foundation of all scheduling:

```
PROJECT
├── 1.0 Planning Phase
│   ├── 1.1 Requirements Gathering
│   ├── 1.2 Stakeholder Analysis
│   └── 1.3 Project Charter
├── 2.0 Design Phase
│   ├── 2.1 Conceptual Design
│   ├── 2.2 Detailed Design
│   └── 2.3 Design Review
├── 3.0 Execution Phase
│   ├── 3.1 Development
│   ├── 3.2 Testing
│   └── 3.3 Deployment
└── 4.0 Closeout Phase
    ├── 4.1 Documentation
    └── 4.2 Lessons Learned
```

### Critical Path Method (CPM)
Calculate the longest path through the network:

1. **Forward Pass**: Calculate Early Start (ES) and Early Finish (EF)
2. **Backward Pass**: Calculate Late Start (LS) and Late Finish (LF)
3. **Float/Slack**: LS - ES = Total Float
4. **Critical Path**: Activities with zero float

```
Activity: A → B → C → D → E
Duration: 3   5   2   4   3  = 17 days (Critical Path)

Activity: A → F → G → E
Duration: 3   4   3   3  = 13 days (Non-critical, 4 days float)
```

### PERT (Three-Point Estimating)
For uncertain durations:

```
Expected Duration = (Optimistic + 4×Most Likely + Pessimistic) / 6
                  = (O + 4M + P) / 6

Example:
- Optimistic (O): 5 days
- Most Likely (M): 10 days  
- Pessimistic (P): 21 days
- Expected = (5 + 40 + 21) / 6 = 11 days
```

### Activity Dependencies

| Type | Abbreviation | Meaning |
|------|--------------|---------|
| Finish-to-Start | FS | Predecessor finishes → Successor starts |
| Start-to-Start | SS | Predecessor starts → Successor starts |
| Finish-to-Finish | FF | Predecessor finishes → Successor finishes |
| Start-to-Finish | SF | Predecessor starts → Successor finishes |

**Best Practice**: Use FS relationships predominantly (90%+)

---

## ✅ DCMA 14-Point Schedule Assessment

Quality metrics for schedule validation:

| # | Metric | Threshold | What It Checks |
|---|--------|-----------|----------------|
| 1 | Logic | <5% | Tasks without predecessors/successors |
| 2 | Leads | 0% | Negative lag (overlapping time) |
| 3 | Lags | <5% | Positive lag between activities |
| 4 | Relationship Types | >90% FS | Predominant use of Finish-Start |
| 5 | Hard Constraints | <5% | Forced dates limiting flexibility |
| 6 | High Float | <5% | Excessive slack (>44 days) |
| 7 | Negative Float | 0% | Schedule delays |
| 8 | High Duration | <5% | Overly long activities (>44 days) |
| 9 | Invalid Dates | 0% | Forecast in past / Actual in future |
| 10 | Resources | 100% | All tasks have resources assigned |
| 11 | Missed Tasks | <5% | Tasks behind baseline |
| 12 | Critical Path Test | Pass | Extending critical = extends project |
| 13 | CPLI | >0.95 | Critical Path Length Index |
| 14 | BEI | >0.95 | Baseline Execution Index |

---

## 🗓️ AACE Schedule Levels of Detail

### Level 1: Summary/Master Schedule
- Executive overview
- Major milestones only
- 10-50 activities
- Monthly/quarterly view

### Level 2: Control Schedule
- Project management level
- Key deliverables and phases
- 50-200 activities
- Weekly/monthly view

### Level 3: Detailed Schedule
- Execution level
- All activities for work packages
- 200-500 activities
- Daily/weekly view

### Level 4: Working Schedule
- Field/team level
- Detailed task breakdowns
- 500+ activities
- Daily view

---

## 📋 Schedule Development Workflow

### Step 1: Preparation
- [ ] Gather project scope and contract
- [ ] Review WBS and scope breakdown
- [ ] Identify key milestones (contractual and internal)
- [ ] Determine scheduling methodology
- [ ] Set project calendar (working days, holidays)

### Step 2: Activity Development
- [ ] Decompose WBS work packages into activities
- [ ] Define activity naming convention
- [ ] Create unique activity IDs
- [ ] Document activity descriptions
- [ ] Identify milestones (zero duration)

### Step 3: Logic Development
- [ ] Establish activity sequence
- [ ] Define dependencies (FS preferred)
- [ ] Identify external dependencies
- [ ] Add leads/lags where required (minimize)
- [ ] Create network diagram

### Step 4: Duration Estimation
- [ ] Apply estimation technique (PERT, analogous, parametric)
- [ ] Document basis of estimates
- [ ] Validate with subject matter experts
- [ ] Include contingency where appropriate

### Step 5: Resource Loading
- [ ] Assign resources to activities
- [ ] Define resource calendars
- [ ] Level resources if over-allocated
- [ ] Validate resource availability

### Step 6: Schedule Calculation
- [ ] Run CPM calculation
- [ ] Identify critical path
- [ ] Analyze total float
- [ ] Verify project end date meets target

### Step 7: Quality Check (DCMA 14-Point)
- [ ] Run schedule health check
- [ ] Address any failing metrics
- [ ] Document exceptions/justifications
- [ ] Obtain baseline approval

### Step 8: Baseline
- [ ] Save schedule baseline
- [ ] Document baseline date and version
- [ ] Distribute to stakeholders
- [ ] Begin monitoring and control

---

## 🖥️ MS Project Implementation

### Quick Setup Steps
```
1. File → New → Blank Project
2. Project → Project Information → Set Start Date
3. Project → Change Working Time → Set Calendar
4. Enter WBS in Task Name column
5. Indent tasks to create hierarchy
6. Add durations in Duration column
7. Link tasks in Predecessors column
8. View → Resource Sheet → Add resources
9. Assign resources to tasks
10. Project → Set Baseline → Save Baseline
```

### Key Shortcuts
| Action | Shortcut |
|--------|----------|
| Indent Task | Alt + Shift + Right |
| Outdent Task | Alt + Shift + Left |
| Link Tasks | Ctrl + F2 |
| Unlink Tasks | Ctrl + Shift + F2 |
| Go to Date | Ctrl + G |
| Show Critical Path | Format → Critical Tasks |

---

## 🔗 Related Resources

### PMI References
- [PMI PMBOK Guide](https://www.pmi.org/pmbok-guide-standards)
- [PMI Practice Standard for Scheduling](https://www.pmi.org/standards)

### AACE International
- [RP 91R-16 Schedule Development](https://web.aacei.org/)
- [RP 37R-06 Schedule Levels of Detail](https://web.aacei.org/)
- [PSP Certification](https://web.aacei.org/certifications)

### DCMA
- [DCMA 14-Point Assessment Guide](https://www.dcma.mil/)

---

*Last Updated: January 2026*
