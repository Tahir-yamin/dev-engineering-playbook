# Course Design Skills

**Topics**: Interactive Course Creation, ADDIE Model, Learning Objectives, Assessments  
**Version**: 1.0  
**Last Updated**: 2026-01-20

---

## Skill #1: Course Structure Design (ADDIE Model)

### When to Use
- Starting a new course from scratch
- Restructuring existing training content
- Planning educational programs

### The ADDIE Framework

| Phase | Activities | Output |
|-------|------------|--------|
| **A**nalyze | Identify learners, needs, goals | Needs Analysis |
| **D**esign | Create learning objectives, structure | Course Blueprint |
| **D**evelop | Write content, create activities | Course Materials |
| **I**mplement | Deliver course, facilitate | Running Course |
| **E**valuate | Assess effectiveness, gather feedback | Improvement Plan |

### Course Structure Template

```markdown
# [Course Title]

## Course Overview
- **Duration**: [X hours/days]
- **Level**: [Beginner/Intermediate/Advanced]
- **Prerequisites**: [List requirements]
- **Target Audience**: [Who should take this]

## Learning Outcomes
By completing this course, learners will be able to:
1. [Action verb] + [Content] + [Context]
2. [Action verb] + [Content] + [Context]

## Modules

### Module 1: [Title]
- Duration: [X min]
- Lessons:
  - 1.1 [Lesson title]
  - 1.2 [Lesson title]
- Quiz: [Y questions]
- Practical: [Exercise description]
```

---

## Skill #2: Learning Objectives (Bloom's Taxonomy)

### Bloom's Taxonomy Levels

| Level | Verbs | Example |
|-------|-------|---------|
| **Remember** | Define, list, recall, identify | List the 5 P6 layout views |
| **Understand** | Explain, describe, summarize | Explain critical path analysis |
| **Apply** | Use, implement, demonstrate | Create a WBS structure in P6 |
| **Analyze** | Compare, differentiate, examine | Analyze schedule variance |
| **Evaluate** | Assess, critique, judge | Evaluate resource loading |
| **Create** | Design, develop, construct | Design a master schedule |

### SMART Objectives Template

```
By the end of [lesson/module], learners will be able to:
[VERB from Bloom's] + [WHAT content] + [HOW/WITH WHAT conditions]
in [TIME] with [ACCURACY LEVEL].
```

**Example**:
> By the end of Module 3, learners will be able to **create** a baseline schedule in Primavera P6 **using imported activities** in **15 minutes** with **no critical errors**.

---

## Skill #3: Interactive Content Generation

### Content Types

| Type | Use Case | Engagement |
|------|----------|------------|
| **Video** | Demonstrations, tutorials | High |
| **Text + Images** | Concepts, theory | Medium |
| **Interactive Quiz** | Knowledge check | High |
| **Simulation** | Hands-on practice | Very High |
| **Case Study** | Real-world application | High |
| **Discussion** | Peer learning | Medium |

### Quiz Question Types

**Multiple Choice**
```json
{
  "type": "multiple-choice",
  "question": "What does WBS stand for?",
  "options": [
    "Work Breakdown Structure",
    "Work Balance Schedule",
    "Weekly Budget Summary",
    "Work Baseline Standard"
  ],
  "correct": 0,
  "explanation": "WBS stands for Work Breakdown Structure..."
}
```

**True/False**
```json
{
  "type": "true-false",
  "question": "Critical path activities have zero float.",
  "correct": true,
  "explanation": "Activities on the critical path have zero total float..."
}
```

**Drag and Drop**
```json
{
  "type": "drag-drop",
  "question": "Match P6 views to their purposes:",
  "pairs": [
    {"item": "Gantt Chart", "match": "Visual timeline"},
    {"item": "Activity Table", "match": "Tabular data view"},
    {"item": "Resource Usage", "match": "Workload analysis"}
  ]
}
```

---

## Skill #4: Assessment Design

### Assessment Types

| Type | Purpose | Timing |
|------|---------|--------|
| **Diagnostic** | Pre-assess knowledge | Before course |
| **Formative** | Check progress | During lessons |
| **Summative** | Final evaluation | End of course |
| **Practical** | Apply skills | After theory |

### Rubric Template

| Criteria | Excellent (4) | Good (3) | Adequate (2) | Needs Work (1) |
|----------|---------------|----------|--------------|----------------|
| Accuracy | 100% correct | 90%+ | 75%+ | Below 75% |
| Completion | Fully complete | Minor gaps | Some gaps | Incomplete |
| Application | Advanced use | Correct use | Basic use | Incorrect |

### Practical Exercise Template

```markdown
## Practical Exercise: [Title]

**Objective**: [What learner will accomplish]

**Scenario**: 
[Real-world situation description]

**Tasks**:
1. [ ] [Specific task 1]
2. [ ] [Specific task 2]
3. [ ] [Specific task 3]

**Expected Output**:
- [Deliverable 1]
- [Deliverable 2]

**Success Criteria**:
- [Criterion 1]
- [Criterion 2]

**Time Allowed**: [X minutes]
```

---

## Skill #5: Course Output Formats

### HTML Interactive Course

```html
<!DOCTYPE html>
<html>
<head>
  <title>[Course Title]</title>
  <link rel="stylesheet" href="course-style.css">
</head>
<body>
  <nav id="course-nav"><!-- Module navigation --></nav>
  <main id="course-content"><!-- Lesson content --></main>
  <aside id="quiz-panel"><!-- Interactive quizzes --></aside>
  <script src="course-engine.js"></script>
</body>
</html>
```

### Markdown Course Structure

```
course-name/
├── README.md           # Course overview
├── module-01/
│   ├── lesson-01.md
│   ├── lesson-02.md
│   └── quiz-01.md
├── module-02/
│   └── ...
├── assessments/
│   └── final-test.md
└── resources/
    └── cheatsheet.md
```

---

## Quick Reference

### Course Planning Checklist

- [ ] Identify target audience and prerequisites
- [ ] Define 3-5 main learning outcomes
- [ ] Structure into 3-7 modules
- [ ] Create 2-4 lessons per module
- [ ] Add quiz after each module (5-10 questions)
- [ ] Include 1+ practical exercise per module
- [ ] Design final assessment
- [ ] Add resources/references

### Time Estimation

| Content Type | Development Time |
|--------------|------------------|
| 1 hour of video | 10-15 hours |
| 1 lesson text | 1-2 hours |
| 10 quiz questions | 30-60 min |
| Practical exercise | 1-2 hours |
| Full course (4 hrs) | 40-60 hours |

---

## Related Skills
- `presentation-skills.md` - Slide design
- `documentation-skills.md` - Technical writing

---

**Transform any topic into an engaging learning experience!** 🎓
