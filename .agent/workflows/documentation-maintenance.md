---
description: Meta-workflow for updating documentation - workflows, skills, design specs, and requirements
---

# Documentation Maintenance Workflow

**Purpose**: Keep the documentation system up-to-date with automatic scanning and duplicate detection  
**When to Use**: After solving new problems, adding features, or learning new patterns  
**Frequency**: After each major task or weekly  
**Last Major Update**: 2026-01-13 (AI ecosystem updates integrated)  
**New**: Automatically scans workspace for updates, merges duplicates, tracks AI trends

---

## 🎯 Overview

This workflow helps you maintain:
- `agents/workflows/` - Step-by-step workflows
- `skills/` - Skills library  
- `guides/` - Design and architecture docs
- `community/` - Community resource tracking
- `WORKSPACE_STATS.md` - File counts and statistics

**What's Automated**:
- ✅ Workspace scanning for file changes
- ✅ Duplicate file detection
- ✅ Document update recommendations
- ✅ Stats recalculation
- ✅ AI ecosystem monitoring (weekly)
- ✅ Latest trend integration

---

## Step 0: Automatic Workspace Scan (NEW)

**Run this FIRST every time you invoke this workflow**

### Scan Workspace for Changes

```bash
# Count total files
$totalFiles = (Get-ChildItem "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base" -Recurse -File | Measure-Object).Count

# Count by category
$skillsCount = (Get-ChildItem "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base\skills" -Recurse -File | Measure-Object).Count
$agentsCount = (Get-ChildItem "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base\agents" -Recurse -File | Measure-Object).Count
$workflowsCount = (Get-ChildItem "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base\workflows" -Recurse -File | Measure-Object).Count
$guidesCount = (Get-ChildItem "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base\guides" -Recurse -File | Measure-Object).Count

Write-Host "Total: $totalFiles | Skills: $skillsCount | Agents: $agentsCount | Workflows: $workflowsCount | Guides: $guidesCount"
```

**Action**: Compare counts with `README.md` and `WORKSPACE_STATS.md`. If different → **Update needed**.

---

## Step 1: Detect and Merge Duplicate Files (NEW)

**Purpose**: Find similar files and merge them to avoid redundancy

### A. Scan for Duplicate/Similar Files

**Common duplicate patterns to check**:

```bash
# Find files with similar names
Get-ChildItem "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\my-dev-knowledge-base" -Recurse -File -Filter "*.md" | 
  Group-Object Name | 
  Where-Object { $_.Count -gt 1 } |
  Select-Object Name, Count, @{Name="Locations";Expression={$_.Group.DirectoryName -join ", "}}
```

**Manual checks**:
- [ ] Multiple INDEX.md or README.md files with same content?
- [ ] Skill files covering same topic in different locations?
- [ ] Duplicate workflow files?
- [ ] Similar agent configurations?

### B. Merge Duplicate Files

**If duplicates found, use this process**:

1. **Identify which to keep**:
   - Keep the most complete version
   - Keep the one in the correct directory structure
   - Prefer newer files with more detail

2. **Merge content**:
   ```markdown
   # Combined [Topic] 
   
   [Content from File 1]
   
   ---
   
   ## Additional from [File 2 source]
   
   [Unique content from File 2]
   
   ---
   
   **Sources merged**: 
   - [File 1 location]
   - [File 2 location]
   ```

3. **Update cross-references**:
   - Search workspace for links to old file
   - Update all references to point to merged file
   
4. **Delete duplicate**:
   ```bash
   Remove-Item "path/to/duplicate/file.md"
   ```

5. **Document in CHANGELOG**:
   Update `community/CHANGELOG.md`:
   ```markdown
   ### [Date]: Merged Duplicates
   - Merged [file1] and [file2] into [final-file]
   - Reason: [why they were duplicates]
   ```

---

## Step 2: Update All Documentation (NEW)

**Systematically update all main documentation files**

### ⭐ ALWAYS Update These Files First:

#### 1. **README.md** (MOST IMPORTANT - Update EVERY time!)

**Required Updates**:
- [ ] **File counts** - Update total files and categories (from Step 0 scan)
- [ ] **Growth percentage** - Recalculate growth from original 84 files
- [ ] **Last Updated date** - Change to current date
- [ ] **Tier counts** - Verify Tier 1, 2, 3 file counts are accurate
- [ ] **Credits section** - Ensure all contributors are listed
- [ ] **Latest Updates section** - Reference newest AI update report
- [ ] **Your maintainer info** - Keep your GitHub link current

**Template to follow**:
```markdown
## 📊 Stats

- **Total Files**: [CURRENT_COUNT] (was 84)
- **Skills**: [SKILLS_COUNT]+ (was 8)
- **Agents**: [AGENTS_COUNT]+ (was 37)
- **Workflows**: [WORKFLOWS_COUNT]+ (was 24)
- **Guides**: [GUIDES_COUNT]+ (was 15)

**Growth**: **[GROWTH_%] expansion** - Almost 20x larger!

### Community Sources:
**Tier 1 - Official & Multi-Agent** ([TIER1_COUNT] files):
[List sources...]

**Tier 2 - Business & Production** ([TIER2_COUNT] files):
[List sources...]

**Tier 3 - Advanced Orchestration** ([TIER3_COUNT] files):
[List sources...]

---

## 🙏 Credits & Acknowledgments

[Full credits section - keep updated]

---

**Last Updated**: [YYYY-MM-DD] (**ALL 3 TIERS COMPLETE!**)
**Maintainer**: Tahir Yamin ([@tahir-yamin](https://github.com/tahir-yamin))
```

---

#### 2. `WORKSPACE_STATS.md`
- [ ] Update total file count (from Step 0)
- [ ] Update stats by category
- [ ] Update growth percentage
- [ ] Update "Last Updated" date
- [ ] Add any new sections if needed

#### 2. `WORKSPACE_STATS.md`
- [ ] Update file counts by tier
- [ ] Update category breakdowns
- [ ] Recalculate growth percentages
- [ ] Update timestamp

#### 3. `skills/INDEX.md`
- [ ] Check for new skills added to workspace
- [ ] Add entries for new skill files
- [ ] Update categorization if needed
- [ ] Verify all links work

#### 4. `agents/INDEX.md` (if exists, create if not)
- [ ] List all agent categories
- [ ] Add new agents from recent additions
- [ ] Organize by use case
- [ ] Add quick search section

#### 5. `workflows/INDEX.md` (if exists, create if not)
- [ ] List all workflows
- [ ] Organize by problem type
- [ ] Add your original workflows + community ones
- [ ] Add cross-references

#### 6. `community/SOURCES.md`
- [ ] Ensure all sources are credited
- [ ] Add license information for new additions
- [ ] Update changelog
- [ ] Add usage guidelines

#### 7. AI Update Tracking Files
- [ ] `claude_update_log.md` - Add new monitoring entries
- [ ] `claude_updates_knowledge_base.md` - Integrate latest findings
- [ ] `claude_update_report_*.md` - Create new reports as needed
- [ ] `AGENTS.md` - Update with latest agent developments
- [ ] `SKILL_PATH_B_AI_ENGINEERING.md` - Add new AI skills

---

## Step 3: Identify What Needs Updating

**Ask yourself**:
- [ ] Did I solve a new type of problem? → **New Workflow**
- [ ] Did I learn a new technique/pattern? → **New Skill**
- [ ] Did I create/modify UI components? → **Update Design System**
- [ ] Did I complete a feature? → **Update Requirements**
- [ ] Did I use a successful prompt? → **Document Prompt**
- [ ] Did I add community resources? → **Update attribution**

---

## Step 4: Create New Workflow

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

## Step 5: Create New Skill

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

### v2.0 - January 5, 2026
- Added GitHub Knowledge Base sync (my-dev-knowledge-base)
- Added Phase 5 skills/agents documentation
- Added Claude contributor repos with credits
- Added local folder sync for easy retrieval

---

## 🔄 Step 11: Sync to GitHub Knowledge Base

### Purpose
Automatically sync all documentation updates to your GitHub knowledge base repository for future reuse across projects.

### Target Repository
- **Local Path**: `my-dev-knowledge-base/`
- **GitHub URL**: `https://github.com/Tahir-yamin/dev-engineering-playbook`

### Files to Sync

| Source | Destination | Content |
|--------|-------------|---------|
## 📦 Step 12: Update Phase 5 Skills & Agents

### When to Update
- New Phase 5 feature implemented (Kafka, Dapr, AKS)
- New skill learned from cloned repos
- New agent configuration added

### Source Repositories (Cloned)

| Folder | Source | Credits |
|--------|--------|---------|
| `claude-skills-library/` | [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | @travisvn |
| `claude-subagents/` | [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | @VoltAgent |
| `dapr-quickstarts/` | [dapr/quickstarts](https://github.com/dapr/quickstarts) | @dapr |
| `claude-cookbooks/` | [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | @anthropic |

### How to Add New Skill from Cloned Repos

**1. Browse the cloned repo**:
```bash
# Check available skills
dir claude-skills-library\

# Check available subagents
dir claude-subagents\categories\
```

**2. Copy relevant skill to your project**:
```bash
# Example: Copy a skill from claude-skills-library
Copy-Item -Path ".\claude-skills-library\skills\kubernetes-skills.md" -Destination ".\docs\misc\" -Force
```

**3. Add credit in the copied file**:
```markdown
---
Original Source: https://github.com/travisvn/awesome-claude-skills
Author: @travisvn
License: MIT
Modified: January 2026 by @Tahir-yamin
---
```

**4. Update skills.json**:
```json
{
  "name": "new_skill_from_community",
  "category": "phase5_community",
  "description": "Description here",
  "source": "travisvn/awesome-claude-skills",
  "credit": "@travisvn"
}
```

### Phase 5 Skills Locations

| File | Purpose |
|------|---------|
| `docs/misc/SKILL_PATH_PHASE5.md` | Kafka, Dapr, AKS micro-skills |
| `phase4/agent/skills.json` | Agent skill definitions (v2.0.0) |
| `.agent/workflows/phase5-troubleshooting.md` | Phase 5 troubleshooting |

---

## 🔗 Step 13: Update Recommended GitHub Repos

### Purpose
Keep track of valuable community repos for future reference.

### File Location
`docs/misc/RECOMMENDED_GITHUB_REPOS.md`

### Template for Adding New Repo

```markdown
### N. **owner/repo-name** ⭐
**Type**: [Skills/Subagents/Templates] | **Stars**: X,XXX | **Updated**: Month Year
```
https://github.com/owner/repo-name
```
Brief description of what this repo offers.

---
```

### Current Categories

| Category | Count | Description |
|----------|-------|-------------|
| Claude Skills | 4 | Claude prompt templates and skills |
| Claude Subagents | 3 | Specialized AI agents |
| Claude Tools | 3 | Workflow and integration tools |
| Dapr | 4 | Distributed runtime examples |
| Kafka | 3 | Event streaming resources |
| AKS/CI-CD | 3 | Cloud deployment guides |

### When to Add New Repo
- Found useful community resource
- Forked a valuable repo
- Discovered Phase 5 related tools

---

## 💾 Step 14: Sync Local Skill Folders

### Purpose
Maintain local copies of all skills for easy retrieval without internet.

### Local Skill Folders

| Folder | Content | File Count |
|--------|---------|------------|
| `claude-skills-library/` | 50+ Claude skills | 3 files |
| `claude-subagents/categories/` | 137 specialized agents | 10 subdirs |
| `dapr-quickstarts/` | Dapr examples | 1,223 files |
| `claude-cookbooks/` | Official Anthropic guides | 387 files |

### Quick Access Commands

// turbo
```bash
# List all available Claude skills
Get-ChildItem -Path "claude-skills-library\" -Recurse -Filter "*.md"

# List all subagent categories
Get-ChildItem -Path "claude-subagents\categories\" -Directory

# List Dapr Python examples
Get-ChildItem -Path "dapr-quickstarts\pub_sub\python" -Recurse

# Search for a specific skill
Select-String -Path "claude-skills-library\*.md" -Pattern "kubernetes"
```

### Sync from Upstream

// turbo
```bash
# Update cloned repos from upstream
cd claude-skills-library
git pull origin main
cd ..

cd claude-subagents
git pull origin main
cd ..

cd dapr-quickstarts
git pull origin main
cd ..

cd claude-cookbooks
git pull origin main
cd ..

# NEW: GitHub Copilot Resources
cd github-awesome-copilot
git pull origin main
cd ..

cd WriteHERE
git pull origin main
cd ..
```

---

## 🧠 Step 15: Antigravity Brain Sync (AUTO)

**Purpose**: Automatically move new resources into the active Antigravity brain folders.

### Sync Logic

| File Type | Source Pattern | Destination |
|-----------|----------------|-------------|
| **Agents** | `*.agent.md` | `.agent/rules/` |
| **Workflows** | `*.workflow.md` | `.agent/workflows/` |
| **Prompts** | `*.prompt.md` | `.agent/workflows/` |
| **Skills** | `skills/*/` | `skills/` |

### Execution Command

// turbo
```powershell
# 1. Sync Agents (Personas)
Get-ChildItem -Path "external-libs" -Recurse -Filter "*.agent.md" | 
    ForEach-Object {
        $dest = Join-Path ".agent\rules" $_.Name
        if (-not (Test-Path $dest) -or (Get-Item $_.FullName).LastWriteTime -gt (Get-Item $dest).LastWriteTime) {
            Copy-Item $_.FullName -Destination ".agent\rules" -Force
            Write-Host "Synced Agent: $($_.Name)"
        }
    }

# 2. Sync Workflows & Prompts
Get-ChildItem -Path "external-libs" -Recurse -Include "*.prompt.md", "*.workflow.md" | 
    ForEach-Object {
        $dest = Join-Path ".agent\workflows" $_.Name
        if (-not (Test-Path $dest) -or (Get-Item $_.FullName).LastWriteTime -gt (Get-Item $dest).LastWriteTime) {
            Copy-Item $_.FullName -Destination ".agent\workflows" -Force
            Write-Host "Synced Workflow: $($_.Name)"
        }
    }

# 3. Sync Skills
$copilotSkills = "external-libs\github-awesome-copilot\skills"
if (Test-Path $copilotSkills) {
    Copy-Item "$copilotSkills\*" -Destination "skills\" -Recurse -Force
    Write-Host "Synced GitHub Copilot Skills"
}
```

---

## 🚀 Full Documentation Sync Workflow

When running `/documentation-maintenance`, follow these additional steps:

### Checklist
- [ ] **Run Step 15 (Brain Sync)** to update native folders
- [ ] Run `/@workflow-orchestrator copilot-monitoring`
- [ ] Verify `COMMAND_CENTER.md` counts match `WORKSPACE_STATS.md`

- [ ] **Step 11**: Sync files to `my-dev-knowledge-base/`
- [ ] **Step 12**: Update Phase 5 skills with credits
- [ ] **Step 13**: Add any new recommended repos
- [ ] **Step 14**: Pull latest from cloned repos
- [ ] **Commit**: Push changes to GitHub

### One-Command Sync

// turbo
```bash
# Full sync script
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1"

# Sync to knowledge base
Copy-Item -Path ".\.agent\workflows\*.md" -Destination ".\my-dev-knowledge-base\workflows\" -Force
Copy-Item -Path ".\docs\misc\SKILL_PATH_*.md" -Destination ".\my-dev-knowledge-base\skills\" -Force
Copy-Item -Path ".\docs\misc\RECOMMENDED_GITHUB_REPOS.md" -Destination ".\my-dev-knowledge-base\" -Force
Copy-Item -Path ".\phase4\agent\skills.json" -Destination ".\my-dev-knowledge-base\agents\" -Force
Copy-Item -Path ".\docs\misc\MODERN_SKILLS.md" -Destination ".\my-dev-knowledge-base\skills\" -Force

# Commit knowledge base
cd my-dev-knowledge-base
git add .
git commit -m "docs: sync latest Phase 5 documentation"
git push origin main
cd ..

Write-Host "✅ Documentation synced to my-dev-knowledge-base!" -ForegroundColor Green
```

---

**Keep your documentation alive - update it regularly!** 🎉

**Related Files**: 
- All files in `.agent/workflows/`
- All files in `.claude/`
- `.specify/design-system.md`
- `.spec-kit/COMPLIANCE_SUMMARY.md`
- `.history/prompts/successful-prompts.md`
- `my-dev-knowledge-base/` (GitHub: dev-engineering-playbook)
- `claude-skills-library/`, `claude-subagents/`, `dapr-quickstarts/`, `claude-cookbooks/`
