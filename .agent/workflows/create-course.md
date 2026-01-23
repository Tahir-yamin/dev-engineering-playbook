---
description: Design and generate interactive courses on any topic with quizzes, practicals, and assessments
---

# Create Interactive Course

**Invoke with**: `/create-course` or "Create a course on [topic]"

---

## When to Use

- Creating training materials on any topic
- Building e-learning content
- Designing certification programs
- Internal team training

---

## Step 1: Gather Course Information

**Ask the user**:

1. **Course Topic**: What is the main subject?
2. **Target Audience**: Who will take this course?
3. **Level**: Beginner / Intermediate / Advanced
4. **Duration**: Micro (30 min) / Short (2 hrs) / Full (8+ hrs)
5. **Output Format**: HTML (interactive) / Markdown / Both

---

## Step 2: Generate Course Outline

// turbo
```python
# Use the course generator script
python d:\my-dev-knowledge-base\scripts\course_generator.py --topic "[TOPIC]" --level "[LEVEL]" --duration "[DURATION]" --output-dir "D:\Courses\[course-name]"
```

**Or create manually**:

```markdown
# [Course Title]

## Course Overview
- Duration: [X hours]
- Level: [Level]
- Prerequisites: [List]
- Target Audience: [Who]

## Learning Outcomes
1. [Outcome 1 - using Bloom's verbs]
2. [Outcome 2]
3. [Outcome 3]

## Module 1: [Title]
- Lesson 1.1: [Introduction]
- Lesson 1.2: [Core concepts]
- Quiz 1: [5 questions]
- Practical 1: [Hands-on exercise]

## Module 2: [Title]
...
```

---

## Step 3: Create Module Content

For each module, generate:

### A. Theory Content

```markdown
## Module X: [Title]

### Learning Objectives
By the end of this module, you will be able to:
- [Objective 1]
- [Objective 2]

### Key Concepts

#### [Concept 1]
[Explanation with examples]

#### [Concept 2]  
[Explanation with examples]

### Summary
- [Key point 1]
- [Key point 2]
```

### B. Examples & Demonstrations

```markdown
### Example: [Title]

**Scenario**: [Real-world context]

**Step 1**: [Action]
```
[Code or screenshot]
```

**Step 2**: [Action]
...

**Result**: [What learner should see]
```

---

## Step 4: Create Interactive Quizzes

### HTML Quiz Format

```html
<div class="quiz" data-module="1">
  <div class="question" data-id="q1">
    <p class="question-text">What is the critical path?</p>
    <div class="options">
      <label><input type="radio" name="q1" value="a"> The shortest path</label>
      <label><input type="radio" name="q1" value="b"> The longest path</label>
      <label><input type="radio" name="q1" value="c"> The most expensive path</label>
    </div>
    <div class="feedback hidden"></div>
  </div>
</div>
```

### Markdown Quiz Format

```markdown
## Quiz: Module 1

### Question 1
What is the critical path in project scheduling?

- [ ] A) The shortest sequence of activities
- [x] B) The longest sequence of activities determining project duration
- [ ] C) The most resource-intensive path
- [ ] D) The path with highest risk

> **Explanation**: The critical path is the longest sequence of dependent activities that determines the minimum project duration.

---

### Question 2
...
```

---

## Step 5: Create Practical Exercises

```markdown
## Practical Exercise: [Title]

### Objective
[What the learner will accomplish]

### Scenario
[Real-world context and background]

### Your Tasks

**Task 1**: [Specific action]
- [ ] Step 1.1
- [ ] Step 1.2

**Task 2**: [Specific action]
- [ ] Step 2.1
- [ ] Step 2.2

### Resources Provided
- [Sample file 1]
- [Sample file 2]

### Expected Deliverables
1. [What to submit/create]
2. [What to submit/create]

### Success Criteria
- ✅ [Criterion 1]
- ✅ [Criterion 2]

### Time Limit
[X minutes]
```

---

## Step 6: Generate Assessments

### Pre-Assessment (Diagnostic)

```markdown
## Pre-Course Assessment

Test your current knowledge before starting.
This helps us customize your learning path.

**Time**: 10 minutes
**Questions**: 15

[Quiz questions covering all modules at basic level]
```

### Final Assessment (Summative)

```markdown
## Final Assessment

**Passing Score**: 80%
**Time Limit**: 60 minutes
**Attempts**: 2

### Section A: Knowledge Check (40 points)
[20 multiple choice questions]

### Section B: Application (30 points)
[Practical scenario with tasks]

### Section C: Analysis (30 points)
[Case study with questions]
```

---

## Step 7: Package Course

### HTML Output

// turbo
```bash
# Create course folder structure
$courseName = "[course-name]"
$courseDir = "D:\Courses\$courseName"

New-Item -Path $courseDir -ItemType Directory -Force
New-Item -Path "$courseDir\modules" -ItemType Directory -Force
New-Item -Path "$courseDir\quizzes" -ItemType Directory -Force
New-Item -Path "$courseDir\practicals" -ItemType Directory -Force
New-Item -Path "$courseDir\assets" -ItemType Directory -Force
```

**Generate HTML files**:
```
D:\Courses\[course-name]\
├── index.html           # Course home
├── style.css            # Styling
├── course.js            # Quiz engine
├── modules/
│   ├── module-01.html
│   ├── module-02.html
│   └── ...
├── quizzes/
│   ├── quiz-01.html
│   └── ...
├── practicals/
│   └── practical-01.html
└── assets/
    └── images/
```

### Markdown Output

```
D:\Courses\[course-name]\
├── README.md            # Course overview
├── module-01/
│   ├── lesson-01.md
│   ├── lesson-02.md
│   └── quiz.md
├── module-02/
│   └── ...
├── practicals/
│   └── practical-01.md
├── assessments/
│   ├── pre-assessment.md
│   └── final-assessment.md
└── resources/
    └── cheatsheet.md
```

---

## Step 8: Add Certificate Template (Optional)

```markdown
## Certificate of Completion

This certifies that

**[PARTICIPANT NAME]**

has successfully completed the course

**[COURSE TITLE]**

Duration: [X hours] | Date: [DATE]

Score: [SCORE]%

Instructor: [NAME]
```

---

## Output Summary

After running this workflow, you will have:

- [ ] Complete course outline with modules and lessons
- [ ] Learning objectives aligned to Bloom's Taxonomy
- [ ] Theory content for each lesson
- [ ] Interactive quizzes (5-10 questions per module)
- [ ] Practical exercises with scenarios
- [ ] Pre-assessment and final assessment
- [ ] HTML files (if selected) - viewable in browser
- [ ] Markdown files (if selected) - editable text
- [ ] Certificate template

---

## Quick Start Example

**User**: Create a course on Excel basics

**AI Response**:
1. Generated: `D:\Courses\excel-basics\`
2. 4 modules: Interface, Formulas, Formatting, Charts
3. 20 quiz questions
4. 4 practical exercises
5. Final assessment

**Files**:
```
D:\Courses\excel-basics\
├── index.html (open in browser)
├── README.md (course overview)
├── module-01/ ... module-04/
└── assessments/
```

---

## Related Workflows

- `/brainstorm` - Explore topic before course creation
- `/documentation-maintenance` - Add course to knowledge base

---

## Related Skills

- `@[skills/course-design-skills.md]` - ADDIE model, Bloom's Taxonomy
- `@[skills/presentation-skills.md]` - Visual design

---

**Transform knowledge into learning!** 🎓
