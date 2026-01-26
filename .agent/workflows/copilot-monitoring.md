---
description: Monitor and sync updates from GitHub's awesome-copilot repository
---

# GitHub Copilot Monitoring Workflow

## When to Use
- Weekly to check for new community agents/prompts
- After hearing about major updates to github/awesome-copilot
- To keep local native integration in sync

---

## Step 1: Update Repository

// turbo
```powershell
cd d:\my-dev-knowledge-base\external-libs\github-awesome-copilot
git pull origin main
```

---

## Step 2: Sync to Native Brain

**Sync Agents to Personas**:
// turbo
```powershell
Copy-Item "d:\my-dev-knowledge-base\external-libs\github-awesome-copilot\agents\*" "d:\my-dev-knowledge-base\.agent\rules\" -Recurse -Force
```

**Sync Prompts to Workflows**:
// turbo
```powershell
Copy-Item "d:\my-dev-knowledge-base\external-libs\github-awesome-copilot\prompts\*" "d:\my-dev-knowledge-base\.agent\workflows\" -Recurse -Force
```

**Sync Skills**:
// turbo
```powershell
Copy-Item "d:\my-dev-knowledge-base\external-libs\github-awesome-copilot\skills\*" "d:\my-dev-knowledge-base\skills\" -Recurse -Force
```

**Sync Instructions**:
// turbo
```powershell
Copy-Item "d:\my-dev-knowledge-base\external-libs\github-awesome-copilot\instructions\*" "d:\my-dev-knowledge-base\docs\instructions\" -Recurse -Force
```

---

## Step 3: Update Indexes

Check for new files and update categorizations if needed.

1. Review `d:\my-dev-knowledge-base\docs\external-libs\GITHUB_COPILOT_AGENTS_INDEX.md`
2. Review `d:\my-dev-knowledge-base\docs\external-libs\GITHUB_COPILOT_PROMPTS_INDEX.md`
3. Review `d:\my-dev-knowledge-base\docs\external-libs\GITHUB_COPILOT_INSTRUCTIONS_INDEX.md`

---

## Step 4: Verification

// turbo
```powershell
# Verify counts
(Get-ChildItem "d:\my-dev-knowledge-base\.agent\rules" -Filter "*.agent.md").Count
(Get-ChildItem "d:\my-dev-knowledge-base\.agent\workflows" -Filter "*.prompt.md").Count
```

---

**Related Workflows**:
- [documentation-maintenance](documentation-maintenance.md)
- [workflow-orchestrator](workflow-orchestrator.md)
