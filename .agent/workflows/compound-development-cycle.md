---
description: Execute the Plan -> Work -> Review -> Compound development cycle
---

# Compound Engineering Cycle

## When to Use
- Starting a new complex feature.
- You want to prevent technical debt.
- You are working in a team or with AI agents.

---

## Step 1: Plan Phase (`/workflows:plan`)

**Do not write code yet.**

1.  Create a new branch/worktree.
2.  Write a detailed specification.
3.  Break down the spec into atomic tasks (2-5 mins each).
4.  **Verify**: Does every task have a test case?

```bash
# Example
git checkout -b feature/user-auth
touch implementation_plan.md
```

---

## Step 2: Work Phase (`/workflows:work`)

Execute tasks one by one.

1.  **Red**: Write a failing test.
2.  **Green**: Write simplest code to pass.
3.  **Refactor**: Clean up.
4.  **Check**: Move to next task in plan.

**Agent Command**:
`@[skills/subagent-architecture.md]` "Act as Build Agent. Execute Task #1 from plan."

---

## Step 3: Review Phase (`/workflows:review`)

Before merging:

1.  Run the full test suite.
2.  Review code against the *original plan*.
3.  Check for "drift" (did we solve a different problem?).
4.  **Action**: Fix criticial issues immediately.

---

## Step 4: Compound Phase (`/workflows:compound`)

Capture knowledge for the next cycle.

1.  Did we learn a new pattern? -> **Create Skill**.
2.  Did a script fail? -> **Fix Script**.
3.  Did the plan miss something? -> **Update Planning Template**.

```bash
# Example: Create new skill
touch skills/new-pattern.md
```

---

**Related Skills**: `compound-engineering.md`
