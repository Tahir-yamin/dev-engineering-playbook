---
description: Comprehensive workflow for wrapping up a project, extracting lessons, and updating the knowledge base.
---

# Project Wrap-up & Knowledge Extraction

## When to Use
- After completing a significant project (e.g., Hackathon, Client Delivery).
- When you've learned new patterns or technologies during a sprint.
- To finalize documentation and ensure no knowledge is lost.

---

## Step 1: Finalize Project Artifacts

1. **Verify Task Completion**: Ensure all items in `task.md` are marked `[x]`.
2. **Update Walkthrough**: Finalize the `walkthrough.md` with:
    - **Deployment URLs** (Vercel, Netlify, etc.).
    - **Repository Links**.
    - **Key Technical Achievements**.
    - **Status**: Mark as "MISSION ACCOMPLISHED".
3. **Clean Up**: Remove temporary files, unused assets, or debug logs.

---

## Step 2: Extract New Skills (The "Harvest")

1. **Analyze Codebase**: Look for repeated patterns or novel solutions.
    - *Did I use a new library?* (e.g., Algolia Agent Studio).
    - *Did I solve a complex bug?* (e.g., React 19 Hydration Mismatch).
    - *Did I utilize a new protocol?* (e.g., MCP).
2. **Create Skill Files**:
    - Create `skills/[topic]/SKILL.md`.
    - Use the standard SKILL template.
    - Include "When to Use" and "Pattern" steps.

---

## Step 3: Update Knowledge Base Indexes

1. **Register Skills**: Add new skills to `.agent/skills/INDEX.md` (or `README.md`).
2. **Update Workflow Lists**: If you created new workflows, add them to `workflows/INDEX.md`.
3. **Sync Stats**: Run the `documentation-maintenance` stats script to update file counts.

---

## Step 4: Run Documentation Maintenance

// turbo
```bash
# This is a meta-step. Invoke the orchestrator.
# /@workflow-orchestrator documentation-maintenance
```

---

## Step 5: Final Notification

Notify the user that the project is wrapped, the knowledge is safe, and the system is ready for the next challenge.

---

**Related Workflows**: 
- [Documentation Maintenance](file:///d:/my-dev-knowledge-base/.agent/workflows/documentation-maintenance.md)
- [Skill Upgrade](file:///d:/my-dev-knowledge-base/.agent/workflows/skill-upgrade.md)
