---
description: Advanced workflow for analyzing new project requirements and mapping them to relevant knowledge base resources (skills, workflows, docs).
---

# Detailed Project Inception Workflow

**Purpose**: Analyze new project requirements in depth and provide a curated list of relevant skills, workflows, and documents from the knowledge base to accelerate development.

---

## Step 0: External Root Verification (Isolation Policy) 📂

**CRITICAL**: To keep the knowledge base archive clean and optimized (~14k files), **new projects MUST be created outside** the `my-dev-knowledge-base` directory.

**Action**: Verify the current path and target path.
- ✅ **CORRECT**: `d:\my-new-project`
- ❌ **INCORRECT**: `d:\my-dev-knowledge-base\my-new-project`

---

## Step 1: Requirements Discovery (Socratic Phase)

Before providing solutions, you must understand the "What", "Why", and "Who".

**Action**: Trigger the **Socratic Gate**. Ask at least 5 strategic questions covering:
- **Business Goal**: What problem does this solve?
- **User Personas**: Who are the primary users?
- **Technical Stack**: Are there preferred technologies (e.g., Next.js, FastAPI, Dapr)?
- **Constraints**: Security requirements, performance targets, or legacy integrations?
- **Success Criteria**: What does "done" look like?

---

## Step 1.5: Security-by-Design Discovery 🛡️

**Action**: Ask 3 targeted security questions:
1. **Data Sensitivity**: Will the app handle PII (Personally Identifiable Information), credentials, or financial data?
2. **Access Control**: Does it need RBAC (Role-Based Access Control) or simple Auth?
3. **Attack Surface**: Is this a public-facing API or an internal tool?

**Reference**: Use `@[skills/env-skills.md]` Skill #1 for secret management planning.

---

## Step 2: Detailed Requirement Analysis

Once questions are answered, document the findings in `docs/project/requirements.md`.

---

## Step 2.5: Internal Exemplar & Pattern Discovery (Monorepo Mastery) 🔍

In a workspace of 14,000+ files, **reusability is mandatory**.

**Action**: Analyze existing patterns to avoid reinventing the wheel.
1. **Search for Similar Features**: `grep` or `find_by_name` for keywords related to the new project.
2. **Identify Exemplars**: Find 2-3 files that represent the "Gold Standard" implementation for this tech stack in the current repo.
3. **Reference Blueprints**: Use `@[.agent/workflows/code-exemplars-blueprint-generator.prompt.md]` to find high-quality patterns.

---

## Step 2.6: Monorepo Impact & Conflict Assessment ⚠️

**Action**: Ensure the new project doesn't clash with the existing 14k+ files.
1. **Directory Conflict**: Verify the proposed folder doesn't already exist or overlap with another project's scope.
2. **Resource Conflict**: Check for Port conflicts (if local dev), Environment variable name clashes, or shared dependency version mismatches.
3. **Infrastructure Reuse**: Can existing Helm charts, Dockerfiles, or CI/CD workflows be extended instead of created from scratch?

---

## Step 3: Knowledge Base Resource Mapping

Map the project requirements to the existing knowledge base tools.

**Action**: Scan the following locations to find relevant matches:
- `skills/INDEX.md` and `skills/` directory.
- `.agent/workflows/README.md` and `.agent/workflows/` directory.
- `guides/` and `docs/` for architectural patterns.

**Output**: Provide a **Project Resource Map** in the chat.

**Resource Map Format**:
```markdown
### 📂 Relevant Knowledge Base Resources

#### 🛠️ Recommended Skills
- **@[skills/name-of-skill.md]**: For [specific reason]
- **@[skills/another-skill.md]**: For [specific reason]

#### 🚀 Recommended Workflows
- **@[.agent/workflows/workflow-name.md]**: Use this for [Step/Phase]
- **@[.agent/workflows/another-one.md]**: Use this for [Problem]
- **@[.agent/workflows/security-audit.md]**: Run this before any Git commit or deploy.

#### 📖 Supporting Documentation
- [Document Link]: For [Subject]
```

---

## Step 4: Propose Implementation Plan

// turbo
```bash
# Use the creation tool to start the plan
# Invoke create-implementation-plan.prompt if available
```

**Action**: Create `docs/project/implementation_plan.md` using the mapped resources as the foundation.

---

## Step 5: Initialize Project Structure

If the user approves the plan, proceed with:
- `@[.agent/workflows/starting-new-project.md]`

> [!IMPORTANT]
> Ensure you are in a sibling directory (e.g., `d:\`) and NOT inside the knowledge base when running initialization commands.

---

**Related Skills**:
- @[skills/ai-skills.md]
- @[skills/architecture.md]
