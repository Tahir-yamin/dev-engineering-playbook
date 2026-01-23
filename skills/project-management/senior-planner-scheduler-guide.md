# Senior Planner & Scheduler Professional Guide

> **Comprehensive Planning & Scheduling Reference Aligned with International Standards**  
> *PMI | AACE International | GAO | DCMA | Guild of Project Controls*

---

## 📋 Table of Contents

1. [Professional Standards Framework](#professional-standards-framework)
2. [Schedule Development Lifecycle](#schedule-development-lifecycle)
3. [GAO 10 Best Practices](#gao-10-best-practices)
4. [DCMA 14-Point Assessment](#dcma-14-point-assessment)
5. [PMI Practice Standard Conformance](#pmi-practice-standard-conformance)
6. [AACE Recommended Practices](#aace-recommended-practices)
7. [Schedule Quality Metrics](#schedule-quality-metrics)
8. [Critical Path Analysis](#critical-path-analysis)
9. [Schedule Risk Analysis](#schedule-risk-analysis)
10. [Schedule Control & Reporting](#schedule-control--reporting)

---

## Professional Standards Framework

### Governing Standards

| Organization | Standard | Focus Area |
|--------------|----------|------------|
| **PMI** | PMBOK Guide 7th Edition | Project Management Framework |
| **PMI** | Practice Standard for Scheduling, 3rd Ed | Schedule Model Best Practices |
| **AACE International** | Total Cost Management Framework | Integrated Cost/Schedule |
| **AACE International** | RP 91R-16 Schedule Development | Development Process |
| **AACE International** | RP 37R-06 Schedule Levels of Detail | Detail Requirements |
| **AACE International** | RP 52R-06 Time Impact Analysis | Prospective Analysis |
| **AACE International** | RP 29R-03 Forensic Schedule Analysis | Retrospective Analysis |
| **AACE International** | RP 128R-23 Practitioner Responsibilities | Role Definition |
| **GAO** | Schedule Assessment Guide | 10 Best Practices |
| **DCMA** | Earned Value Management System | 14-Point Schedule Assessment |

### Professional Certifications

| Certification | Organization | Focus |
|---------------|--------------|-------|
| **PSP** | AACE International | Planning & Scheduling Professional |
| **PMP** | PMI | Project Management Professional |
| **PMI-SP** | PMI | Scheduling Professional |
| **EVP** | AACE International | Earned Value Professional |

---

## Schedule Development Lifecycle

### Phase 1: Schedule Planning

#### 1.1 Define Scheduling Approach
```
□ Select scheduling methodology (CPM, Critical Chain, Agile hybrid)
□ Determine schedule levels (Master → Detail → Working)
□ Establish calendar requirements
□ Define WBS structure and coding
□ Identify scheduling software and versions
□ Document scheduling specification per AACE RP 26R-21
```

#### 1.2 Scope Integration
```
□ Review contract scope and deliverables
□ Verify scope breakdown structure alignment with WBS
□ Integrate contractor/subcontractor schedules
□ Identify interface milestones
□ Document scope assumptions and exclusions
```

#### 1.3 Schedule Management Plan
**Per PMI Practice Standard:**
- Scheduling methodology and tool
- Level of accuracy (±5%, ±10%)
- Units of measure (hours, days, weeks)
- Control thresholds for variance
- Reporting formats and frequency
- Change control procedures

### Phase 2: Schedule Development

#### 2.1 Work Breakdown Structure (WBS)
**Per PMI Practice Standard:**
- 100% Rule: WBS must capture 100% of scope
- Deliverable-oriented decomposition
- Work packages as lowest level for schedule activities
- WBS Dictionary for descriptions

**Levels:**
```
Level 1: Project
Level 2: Major Phases/Deliverables  
Level 3: Control Accounts
Level 4: Work Packages
Level 5: Planning Packages (if needed)
```

#### 2.2 Activity Definition
**Per AACE RP 91R-16:**
- Break work packages into discrete activities
- Each activity = single work effort with defined scope
- Milestones for key events (zero duration)
- Activity duration: 5-44 working days (DCMA guideline)
- Unique activity IDs with logical coding

**Activity Types:**
| Type | Description | Duration |
|------|-------------|----------|
| Task Dependent | Duration based on work content | Calculated |
| Resource Dependent | Duration based on resource availability | Calculated |
| Level of Effort (LOE) | Support activities | Spans other activities |
| Milestone | Key event | 0 days |

#### 2.3 Activity Sequencing
**Per PMI PMBOK:**
- Precedence Diagramming Method (PDM)
- Dependency Types:
  - **Finish-to-Start (FS)** - 90%+ preferred
  - **Start-to-Start (SS)** - Use sparingly
  - **Finish-to-Finish (FF)** - Use sparingly
  - **Start-to-Finish (SF)** - Rarely used

**Dependency Categories:**
| Category | Description | Example |
|----------|-------------|---------|
| Mandatory | Inherent to work | Pour concrete before framing |
| Discretionary | Best practice | Design review before fabrication |
| External | Outside project | Permit approval |
| Internal | Within project | Team availability |

**Logic Guidelines:**
- Minimize leads (negative lag) - Target: 0%
- Minimize lags - Target: <5%
- Document justification for all leads/lags
- Every activity must have predecessor AND successor
- Only project start and finish milestones have open ends

#### 2.4 Duration Estimation
**Per PMI Practice Standard:**

**Techniques:**
| Method | When to Use | Formula |
|--------|-------------|---------|
| PERT | Uncertain activities | (O + 4M + P) / 6 |
| Analogous | Similar past work | Historical × Factor |
| Parametric | Unit-rate based | Quantity × Unit Rate |
| Expert Judgment | SME input | Delphi method |

**PERT Formula:**
```
Expected Duration = (Optimistic + 4×Most Likely + Pessimistic) / 6
Standard Deviation = (Pessimistic - Optimistic) / 6
```

**Documentation Required:**
- Basis of Estimate (BOE)
- Assumptions
- Historical reference (if analogous)
- Calculation method
- Contingency included

#### 2.5 Resource Assignment
**Per GAO Best Practice #3:**
- All activities must be resource-loaded
- Resource types: Labor, Equipment, Material, Cost
- Maximum units and availability calendars
- Resource leveling to resolve over-allocation
- Budget integration (BCWS development)

### Phase 3: Schedule Calculation & Analysis

#### 3.1 Critical Path Method (CPM)
**Per PMI Practice Standard:**

**Forward Pass (Early Dates):**
```
ES(successor) = MAX(EF of all predecessors)
EF = ES + Duration - 1
```

**Backward Pass (Late Dates):**
```
LF(predecessor) = MIN(LS of all successors)
LS = LF - Duration + 1
```

**Float Calculations:**
```
Total Float (TF) = LS - ES = LF - EF
Free Float (FF) = MIN(ES of successors) - EF - 1
```

**Critical Path Characteristics:**
- Longest path through network
- Total Float = 0 on critical activities
- Delay on critical path = Project delay
- May have multiple critical paths
- Near-critical paths (low float) require monitoring

#### 3.2 Schedule Constraints

| Constraint Type | Effect | Use Case |
|-----------------|--------|----------|
| As Soon As Possible | Default - no constraint | Normal activities |
| As Late As Possible | Start as late as possible | JIT activities |
| Start No Earlier Than | Cannot start before date | External dependency |
| Start No Later Than | Must start by date | Contract milestone |
| Finish No Earlier Than | Cannot finish before date | Delivery date |
| Finish No Later Than | Must finish by date | Contract deadline |
| Must Start On | Fixed start date | Mandatory date |
| Must Finish On | Fixed finish date | Mandatory deadline |

**Best Practice:** Minimize hard constraints (<5% of activities)

### Phase 4: Schedule Quality Validation

See detailed sections:
- [GAO 10 Best Practices](#gao-10-best-practices)
- [DCMA 14-Point Assessment](#dcma-14-point-assessment)

### Phase 5: Baseline & Control

#### 5.1 Baseline Approval
```
□ Complete all quality checks (DCMA 14-Point)
□ Obtain stakeholder review and sign-off
□ Verify resource availability commitment
□ Lock baseline in software
□ Document baseline date and version
□ Distribute baseline to stakeholders
```

#### 5.2 Schedule Updates
**Per GAO Best Practice #9:**
- Update frequency: Weekly (construction), Bi-weekly (engineering)
- Status actual start/finish dates
- Update percent complete (physical or duration-based)
- Update remaining duration
- Recalculate schedule
- Analyze variances

#### 5.3 Performance Measurement
**Key Metrics:**
```
Schedule Variance (SV) = BCWP - BCWS
Schedule Performance Index (SPI) = BCWP / BCWS
Baseline Execution Index (BEI) = Tasks Complete / Tasks Planned Complete
To-Complete Schedule Performance Index (TSPI) = Work Remaining / Time Remaining
```

---

## GAO 10 Best Practices

### U.S. Government Accountability Office Schedule Assessment Guide

| # | Best Practice | Requirement | Quality Check |
|---|---------------|-------------|---------------|
| 1 | **Capture All Activities** | 100% of WBS work represented | WBS-to-schedule trace |
| 2 | **Sequence All Activities** | Logical order with predecessors/successors | <5% missing logic |
| 3 | **Assign Resources** | All activities resource-loaded | 100% resource assignment |
| 4 | **Establish Durations** | Realistic, documented estimates | BOE for all activities |
| 5 | **Horizontal Traceability** | Products link across activities | Deliverable handoffs mapped |
| 6 | **Vertical Traceability** | Data consistent across levels | Summary = Detail roll-up |
| 7 | **Valid Critical Path** | Identified and credible | Critical path integrity test |
| 8 | **Reasonable Float** | Appropriate total float | No excessive float (>44 days) |
| 9 | **Schedule Risk Analysis** | Risk-adjusted schedule | Monte Carlo simulation |
| 10 | **Update with Actuals** | Current progress reflected | Weekly/bi-weekly updates |

### GAO Characteristics of Good Schedules

| Characteristic | Description |
|----------------|-------------|
| **Comprehensive** | Captures all work, horizontally and vertically traceable |
| **Well-Constructed** | Logical sequence, valid critical path, reasonable float |
| **Credible** | Risk analysis performed, resources assigned |
| **Controlled** | Baseline maintained, updated with progress |

---

## DCMA 14-Point Assessment

### Defense Contract Management Agency Schedule Assessment

| # | Metric | Threshold | Formula | Guidance |
|---|--------|-----------|---------|----------|
| 1 | **Logic** | <5% | (Missing Pred + Missing Succ) / (2 × Tasks) | All tasks need logic |
| 2 | **Leads** | 0% | Tasks with negative lag / Total Tasks | Eliminate all leads |
| 3 | **Lags** | <5% | Tasks with positive lag / Total Tasks | Minimize, justify |
| 4 | **Relationship Types** | >90% FS | FS Relationships / Total Relationships | Prefer Finish-to-Start |
| 5 | **Hard Constraints** | <5% | Constrained Tasks / Total Tasks | Minimize constraints |
| 6 | **High Float** | <5% | Float >44 days / Total Tasks | Review logic |
| 7 | **Negative Float** | 0% | Tasks with TF < 0 | Fix immediately |
| 8 | **High Duration** | <5% | Duration >44 days / Total Tasks | Break down tasks |
| 9 | **Invalid Dates** | 0% | Actual in future + Forecast in past | Correct dates |
| 10 | **Resources** | 100% | Resourced Tasks / Total Tasks | All must be loaded |
| 11 | **Missed Tasks** | <5% | Missed baseline finish / Total | Track performance |
| 12 | **Critical Path Test** | Pass | Extend critical activity = Extend project | Verify integrity |
| 13 | **CPLI** | >0.95 | CP Length / (CP Length + TF Remaining) | Completion forecast |
| 14 | **BEI** | >0.95 | Tasks Complete / Tasks Planned Complete | Baseline adherence |

### DCMA Critical Path Length Index (CPLI)
```
CPLI = Critical Path Length / (Critical Path Length + Total Float of Critical Path)

Interpretation:
- CPLI > 1.0: Ahead of schedule
- CPLI = 1.0: On schedule
- CPLI < 1.0: Behind schedule (needs recovery)
- CPLI < 0.95: Critical - recovery plan required
```

### DCMA Baseline Execution Index (BEI)
```
BEI = Number of Tasks Completed / Number of Tasks Planned to Complete

Interpretation:
- BEI > 1.0: Ahead of baseline
- BEI = 1.0: On track
- BEI < 1.0: Behind baseline
- BEI < 0.95: Recovery plan required
```

---

## PMI Practice Standard Conformance

### Core Required Components (CRC)

**Per PMI Practice Standard for Scheduling, 3rd Edition:**

| Component | Requirement |
|-----------|-------------|
| Schedule Model | Documented scheduling tool and version |
| Activity List | Complete list with unique IDs |
| Activity Attributes | Duration, predecessors, resources, constraints |
| Activity Sequence | Network diagram with dependencies |
| Resource Requirements | Resource types and quantities |
| Duration Estimates | BOE documentation |
| Schedule Baseline | Approved reference schedule |
| Project Calendars | Working/non-working time defined |

### Schedule Model vs Schedule Instance

| Term | Definition |
|------|------------|
| **Schedule Model** | Template structure, logic, and relationships |
| **Schedule Instance** | Specific calculation at a point in time |
| **Schedule Presentation** | Output format (Gantt, network, table) |

---

## AACE Recommended Practices

### Key AACE RPs for Scheduling

| RP Number | Title | Application |
|-----------|-------|-------------|
| **91R-16** | Schedule Development | Schedule creation process |
| **37R-06** | Schedule Levels of Detail | Detail requirements |
| **52R-06** | Time Impact Analysis | Prospective delay analysis |
| **29R-03** | Forensic Schedule Analysis | Retrospective analysis |
| **49R-06** | Identifying the Critical Path | CPM analysis methods |
| **57R-09** | Integrated Cost & Schedule | Cost/schedule integration |
| **128R-23** | Practitioner Responsibilities | Role definition |

### AACE Schedule Levels of Detail

| Level | Name | Activities | Use |
|-------|------|------------|-----|
| **L1** | Summary | 10-50 | Executive review |
| **L2** | Control | 50-200 | Management control |
| **L3** | Detailed | 200-500 | Execution management |
| **L4** | Working | 500+ | Field-level control |

### AACE Time Impact Analysis (RP 52R-06)

**Prospective TIA Process:**
1. Identify change/delay event
2. Select unimpacted baseline schedule
3. Model the delay as a fragnet
4. Insert fragnet with appropriate logic
5. Recalculate schedule
6. Measure impact to completion
7. Document analysis and findings

---

## Schedule Quality Metrics

### Health Check Dashboard

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Missing Logic | <5% | 5-10% | >10% |
| Hard Constraints | <5% | 5-10% | >10% |
| High Float (>44d) | <5% | 5-10% | >10% |
| High Duration (>44d) | <5% | 5-10% | >10% |
| FS Relationships | >90% | 80-90% | <80% |
| Leads | 0% | 1-5% | >5% |
| Lags | <5% | 5-10% | >10% |
| Negative Float | 0% | Any | Any |
| Invalid Dates | 0% | Any | Any |
| Resources Loaded | 100% | 95-99% | <95% |

### Float Distribution Analysis

```
Float Band Analysis:
- Zero Float: Critical path activities
- 1-10 days: Near-critical, high risk
- 11-20 days: Monitor closely
- 21-44 days: Normal range
- >44 days: Review for logic errors
```

---

## Critical Path Analysis

### Critical Path Identification Methods

**Per AACE RP 49R-06:**

| Method | Description | Use Case |
|--------|-------------|----------|
| Total Float | TF = 0 identifies critical | Standard analysis |
| Longest Path | Trace longest duration sequence | Complex networks |
| Driving Path | Path driving constraint | Constraint analysis |
| Near-Critical | TF < threshold (e.g., 10 days) | Risk awareness |

### Critical Path Integrity Test

**Procedure:**
1. Select activity on calculated critical path
2. Add 100 days to its duration
3. Recalculate schedule
4. Verify project end date moved 100 days
5. Restore original duration

**Pass:** Project end moved exactly as expected  
**Fail:** Logic errors present, review network

### Multiple Critical Paths

- Common in complex projects
- All paths with zero TF are critical
- Monitor near-critical paths (<10 days TF)
- Parallel critical paths increase risk

---

## Schedule Risk Analysis

### Quantitative Schedule Risk Analysis (QSRA)

**Per GAO Best Practice #8:**

#### Monte Carlo Simulation
```
Process:
1. Assign 3-point estimates (O, M, P) to activities
2. Select distribution (Beta, Triangular, Uniform)
3. Run 1,000-10,000 iterations
4. Analyze probability distribution of completion
5. Report confidence levels (P50, P70, P80, P90)
```

#### Risk Distribution
```
- P50 (50% confidence): Expected completion
- P80 (80% confidence): Common target
- P90 (90% confidence): Conservative estimate
```

#### Risk Drivers
```
Tornado Chart Analysis:
- Identifies activities with highest impact on completion
- Focus risk mitigation on top drivers
- Rerun simulation after mitigation
```

---

## Schedule Control & Reporting

### Status Update Process

**Weekly/Bi-weekly Cycle:**
```
1. Collect actual progress from field
2. Update actual start/finish dates
3. Update percent complete
4. Update remaining durations
5. Recalculate schedule
6. Analyze variances from baseline
7. Identify critical path changes
8. Report to stakeholders
```

### Variance Analysis

| Variance | Formula | Action Threshold |
|----------|---------|------------------|
| Schedule Variance (SV$) | BCWP - BCWS | ±10% |
| Schedule Variance (days) | Actual - Baseline | ±5 days |
| SPI | BCWP / BCWS | <0.95 or >1.05 |
| BEI | Complete / Planned | <0.95 |
| CPLI | CPL / (CPL + Float) | <0.95 |

### Standard Reports

| Report | Frequency | Audience |
|--------|-----------|----------|
| Executive Summary | Monthly | Leadership |
| Schedule Status | Weekly | Management |
| Critical Path Report | Weekly | PM Team |
| Milestone Status | Bi-weekly | Stakeholders |
| Resource Loading | Monthly | Resource Managers |
| Look-Ahead (2-week) | Weekly | Field Teams |
| Variance Report | As needed | All |

---

## Automation Scripts Reference

### Available Automation

| Script | Purpose | Location |
|--------|---------|----------|
| **po_to_wbs_parser.py** | PO/Scope → WBS | `scripts/` |
| **ms_project_automation.py** | MS Project Control | `scripts/` |
| **p6_automation.py** | P6 XER Analysis | `scripts/` |

### Integration Workflow
```python
# Complete workflow: PO → WBS → Schedule → Assessment
from po_to_wbs_parser import POParser
from ms_project_automation import MSProjectScheduler

# Step 1: Parse PO/Scope document
parser = POParser()
result = parser.parse_file("contract_scope.docx")

# Step 2: Create schedule
scheduler = MSProjectScheduler()
scheduler.connect()
scheduler.create_new_project(result['metadata']['project_name'], "2026-02-01")
scheduler.create_wbs_structure(result['wbs'])

# Step 3: Run DCMA 14-Point assessment
assessment = scheduler.run_dcma_14_point_assessment()
scheduler.print_dcma_report(assessment)

# Step 4: Save baseline
scheduler.set_baseline()
scheduler.save_project("project.mpp")
```

---

## Quick Reference Cards

### Schedule Development Checklist
```
□ WBS complete and coded
□ All activities defined with unique IDs
□ Activity durations 5-44 days
□ All activities have predecessors AND successors
□ >90% Finish-to-Start relationships
□ 0% leads, <5% lags
□ <5% hard constraints
□ All activities resource-loaded
□ Calendars configured (holidays, working hours)
□ Critical path identified and valid
□ No negative float
□ DCMA 14-Point assessment passed
□ Baseline approved and saved
```

### Common Scheduling Errors
```
❌ Open-ended activities (missing logic)
❌ Excessive use of constraints
❌ Leads without justification
❌ Activities >44 days without breakdown
❌ Negative float not addressed
❌ Resources not assigned
❌ Logic overrides used
❌ Out-of-sequence progress not resolved
```

---

*Document Version: 2.0*  
*Last Updated: January 2026*  
*Compliance: PMI, AACE, GAO, DCMA*
