---
description: Meta-workflow for updating documentation - workflows, skills, design specs, and requirements
---

# Documentation Maintenance Workflow

**Purpose**: Keep the documentation system up-to-date  
**When to Use**: After solving new problems, adding features, or learning new patterns  
**Frequency**: After each major task or weekly

---

## 🎯 Overview

This workflow helps you maintain:
- `.agent/workflows/` - Step-by-step workflows
- `.claude/` - Skills library
- `.specify/` - Design system
- `.spec-kit/` - Requirements tracking
- `.history/prompts/` - Successful prompts

---

## Step 1: Identify What Needs Updating

**Ask yourself**:
- [ ] Did I solve a new type of problem? → **New Workflow**
- [ ] Did I learn a new technique/pattern? → **New Skill**
- [ ] Did I create/modify UI components? → **Update Design System**
- [ ] Did I complete a feature? → **Update Requirements**
- [ ] Did I use a successful prompt? → **Document Prompt**

---

## Step 2: Create New Workflow

### When to Create
- Solved a complex problem with multiple steps
- Found a repeatable process
- Common task that will be done again

### How to Create

**1. Choose filename** (lowercase with hyphens):
```bash
# Examples:
# api-integration.md
# setting-up-tests.md
# optimizing-bundle-size.md
```

**2. Use this template**:

```markdown
---
description: Brief description of what this workflow solves
---

# [Workflow Name]

## When to Use
- [Specific scenario 1]
- [Specific scenario 2]

---

## Step 1: [First Step Name]

[Instructions for step 1]

```bash
# Commands if applicable
command here
```

---

## Step 2: [Second Step Name]

[Instructions for step 2]

### [Subsection if needed]

[Details]

---

## Step 3: Verify Fix

// turbo  # Add this if command is safe to auto-run
```bash
# Verification commands
```

---

**Related Skills**: [link to relevant skills]
```

**3. Save to**:
```
.agent/workflows/[your-workflow-name].md
```

**4. Update index**:
Add entry to `.agent/workflows/README.md`:
```markdown
### X. [New Workflow Name](./your-workflow-name.md)
**Use when**: Brief description
**Fixes**: What it solves
```

---

## Step 3: Create New Skill

### When to Create
- Discovered a useful AI prompt pattern
- Have reusable solution to common problem
- Want to standardize an approach

### How to Create

**Option A: Add to Existing Skill File**

If it fits an existing category (docker, auth, etc.):

1. Open relevant file: `.claude/[topic]-skills.md`
2. Add new skill using this template:

```markdown
## Skill #X: [Skill Name]

### When to Use
- [Specific scenario]

### Prompt Template

```markdown
**ROLE**: [Role for AI to assume]

**[CONTEXT VARIABLE]**: [What user provides]

**REQUIREMENTS**:
- [Requirement 1]
- [Requirement 2]

**DELIVERABLES**:
- [Expected output 1]
- [Expected output 2]
```

### Lessons Learned:
- ✅ [Key insight 1]
- ✅ [Key insight 2]
- ❌ [Common mistake]

---
```

3. Update skill count in file header
4. Update `.claude/skills.md` index

**Option B: Create New Topic File**

If it's a completely new topic:

1. Create: `.claude/[new-topic]-skills.md`
2. Use this structure:

```markdown
# [Topic] Skills

**Topics**: [List topics covered]
**Version**: 1.0

---

## Skill #1: [First Skill]

[Use template from Option A]

---

## Quick Reference

[Commands, patterns, etc.]

---

## Related Skills
- [Links to related skill files]

---

**[Closing note about the topic]**
```

3. Add to `.claude/skills.md` index under appropriate section

---

## Step 4: Update Design System

### When to Update
- Created new UI component
- Changed color palette
- Added new typography scale
- Modified spacing system
- New interaction patterns

### How to Update

**1. Open**: `.specify/design-system.md`

**2. Find relevant section**:
- Colors → `## 🎨 Color System`
- Typography → `## 📝 Typography`
- Components → `## 🎭 Component Specifications`
- Animations → `## ✨ Animations`

**3. Add new specification**:

**For new component**:
```markdown
### [Component Name]
```typescript
const [component]Styles = {
  base: "...",
  variants: {
    default: "...",
    [variant]: "..."
  },
  sizes: {
    sm: "...",
    md: "...",
    lg: "..."
  }
}
```

**Include**:
- Base styles
- Variants
- Sizes
- States (hover, active, disabled)
- Accessibility considerations
```

**For new color/token**:
```markdown
### [Token Name]
```json
{
  "[token-name]": {
    "50": "#HEX",
    "100": "#HEX",
    ...
  }
}
```
```

**4. Update component library list** if new component

---

## Step 5: Update Requirements Tracking

### When to Update
- Feature completed
- Bug fixed
- Requirement changed
- New requirement added

### How to Update

**1. Open**: `.spec-kit/COMPLIANCE_SUMMARY.md`

**2. Find feature section**

**3. Update status**:
```markdown
- [x] Completed feature
- [ ] Pending feature
- [⚠️] Partially complete
```

**4. Add notes if needed**:
```markdown
**Notes**: 
- Implemented on [date]
- Technology used: [tech]
- Known limitations: [if any]
```

**5. Update completion percentage** at top of file

---

## Step 6: Document Successful Prompt

### When to Document
- Prompt worked perfectly
- Solved complex problem
- Reusable solution
- Want to remember approach

### How to Document

**1. Open**: `.history/prompts/successful-prompts.md`

**2. Find appropriate category**:
- Docker & Build Issues
- Authentication & Security
- Database & Prisma
- Frontend Development
- Backend Development
- Environment Setup
- AI Integration
- Performance Optimization
- File Organization & Documentation

Or create new category if needed.

**3. Add entry using template**:

```markdown
### Prompt: [Brief Description]
**Date**: [Month Year]  
**Success Rate**: ✅ 100%

```markdown
[Paste the exact prompt you used]
```

**Outcome**:
- [What happened]
- [What changed]
- [Code snippet if applicable]

**Key Learning**: [One-liner insight]

---
```

**4. If it's a top prompt**, add to "Most Useful Prompts" section

---

## Step 7: Update Indexes

**After adding new files, update these indexes**:

### For New Workflow
Update `.agent/workflows/README.md`:
- Add to appropriate section (Troubleshooting or Development)
- Add to Quick Problem → Workflow Mapping table

### For New Skill
Update `.claude/skills.md`:
- Add to Phase-Based or Topic-Based section
- Add to Complete Skills Reference table
- Add to Quick Problem → Solution Mapping

### For New Skill File
Update `.claude/skills.md`:
- Add file to "Skills by Topic" section
- Create navigation link
- Update total count

---

## Step 8: Cross-Reference

**Link related documentation**:

1. **In Workflows** → Reference relevant skills:
   ```markdown
   **Reference**: @.claude/auth-skills.md Skill #1
   ```

2. **In Skills** → Link to related skills:
   ```markdown
   ## Related Skills
   - auth-skills.md #2
   - env-skills.md #1
   ```

3. **In Prompts** → Reference skills/workflows used:
   ```markdown
   Used: @.claude/docker-skills.md Skill #1
   ```

---

## Step 9: Validation

**Check your updates**:

- [ ] File is in correct location
- [ ] Uses consistent formatting
- [ ] Added to appropriate index
- [ ] Cross-references are correct
- [ ] Markdown renders properly
- [ ] Code examples are tested
- [ ] No typos in commands

---

## Step 10: Commit Changes

// turbo
```bash
git add .
git commit -m "docs: [what you updated]"

# Examples:
# docs: add API integration workflow
# docs: add Redis caching skill to database-skills
# docs: update Button component in design system
# docs: document successful Docker optimization prompt
```

---

## 📝 Quick Reference

### File Locations
```
.agent/workflows/         # Workflows
.claude/                  # Skills
.claude/rules/            # Project guide
.specify/                 # Design system
.spec-kit/                # Requirements
.history/prompts/         # Successful prompts
```

### Naming Conventions
```
# Workflows
[action]-[thing].md
Examples: fix-cors-errors.md, setup-testing.md

# Skills
[topic]-skills.md
Examples: redis-skills.md, testing-skills.md

# Keep consistent!
- Lowercase
- Hyphens (not underscores or spaces)
- Descriptive
```

### When to Create vs Update

**Create New**:
- Completely new problem type
- Different technology/tool
- Separate concern

**Update Existing**:
- Variation of existing problem
- Same topic, new technique
- Enhancement/improvement

---

## 🎯 Real-World Example

**Scenario**: You just added Redis caching to improve performance

**Step-by-step**:

1. **New Skill?** Yes, Redis is new
   - Create: `.claude/cache-skills.md`
   - Or add to: `.claude/database-skills.md` as Skill #6

2. **New Workflow?** Maybe
   - If complex: Create `.agent/workflows/adding-caching.md`
   - If simple: Add to performance-problems.md

3. **Design System?** No (backend only)

4. **Requirements?** Yes
   - Update `.spec-kit/COMPLIANCE_SUMMARY.md`
   - Mark caching feature as complete

5. **Successful Prompt?** Yes
   - Add to `.history/prompts/successful-prompts.md`
   - Under "Performance Optimization" category

6. **Update Indexes?**
   - Add Redis skill to `.claude/skills.md`
   - Link from performance-problems.md workflow

7. **Cross-Reference?**
   - Link from database-skills.md
   - Link from performance workflow

8. **Commit**:
   ```bash
   git add .
   git commit -m "docs: add Redis caching skill and update performance workflow"
   ```

---

## 💡 Best Practices

### DO:
✅ Update documentation immediately after solving problem  
✅ Use templates for consistency  
✅ Include code examples  
✅ Cross-reference related docs  
✅ Keep prompts exact (copy-paste)  
✅ Test commands before documenting  
✅ Update indexes  

### DON'T:
❌ Wait to document (you'll forget)  
❌ Skip cross-references  
❌ Forget to update indexes  
❌ Use vague descriptions  
❌ Leave broken links  
❌ Mix different documentation styles  

---

## 🔄 Regular Maintenance

### Weekly
- [ ] Review successful prompts from the week
- [ ] Document any new patterns discovered
- [ ] Update skill files with new learnings
- [ ] Check for broken cross-references

### Monthly
- [ ] Review and consolidate similar skills
- [ ] Update indexes with accurate counts
- [ ] Archive outdated information
- [ ] Verify all examples still work

### Quarterly
- [ ] Major review of entire documentation
- [ ] Update technology versions
- [ ] Refresh code examples
- [ ] Reorganize if needed

---

## 📊 Documentation Health Checklist

**Your documentation is healthy if**:
- ✅ All indexes are up-to-date
- ✅ Cross-references work
- ✅ No duplicate information
- ✅ Examples are tested and work
- ✅ Consistent formatting throughout
- ✅ Recent activity (last 30 days)
- ✅ Growing (new skills/workflows added)

---

## 🚨 Common Mistakes

### Mistake 1: Not Updating Indexes
**Impact**: New files are invisible  
**Fix**: Always update README.md and skills.md

### Mistake 2: Vague Skill Names
**Impact**: Hard to find when needed  
**Fix**: Use specific, searchable names

### Mistake 3: No Cross-References
**Impact**: Related info is hard to find  
**Fix**: Always link to related skills/workflows

### Mistake 4: Untested Examples
**Impact**: Documentation becomes unreliable  
**Fix**: Test every command/code example

### Mistake 5: Delayed Documentation
**Impact**: You forget important details  
**Fix**: Document immediately while fresh

---

## 🎓 Meta-Learning

**This workflow itself should be updated when**:
- New documentation type is added
- Process improvements discovered
- Templates need refinement
- New best practices emerge

**To update this workflow**:
1. Edit: `.agent/workflows/documentation-maintenance.md`
2. Update version/date at top
3. Add to changelog at bottom
4. Commit changes

---

## 📅 Changelog

### v1.0 - December 29, 2025
- Initial creation of meta-workflow
- Covers all documentation types
- Includes templates and examples
- Real-world scenario provided

---

**Keep your documentation alive - update it regularly!** 🎉

**Related Files**: 
- All files in `.agent/workflows/`
- All files in `.claude/`
- `.specify/design-system.md`
- `.spec-kit/COMPLIANCE_SUMMARY.md`
- `.history/prompts/successful-prompts.md`
