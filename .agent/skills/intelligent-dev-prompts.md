# Intelligent Development Prompts (GitLab Duo Library)

**Topics**: Code Analysis, Refactoring, Planning, Security, Review, Debugging
**Source**: [GitLab Duo Prompt Library](https://about.gitlab.com/gitlab-duo/prompt-library/)
**Version**: 1.0
**Last Updated**: 2026-02-10

---

## Overview

This skill contains a curated collection of development-centric prompts inspired by the GitLab Duo Prompt Library. These patterns are platform-agnostic and can be used with GitHub Copilot, Gemini CLI, or any AI assistant to accelerate the software development lifecycle.

---

## 🔍 Category: Code Understanding

### Skill #1: Understand Code Before Making Changes
**When to Use**: You are about to refactor or modify unfamiliar code.

**Prompt Template**:
```markdown
I'm making changes to [FILE/COMPONENT NAME] and need to understand what else might be affected. Here's my change:

Current code:
[PASTE ORIGINAL CODE]

My proposed change:
[PASTE MODIFIED CODE OR DESCRIBE THE CHANGE]

Please help me understand:
1. What other files or components directly use this code?
2. What could break if I make this change?
3. Are there any tests I should update or add?
4. What specific things should I search for in the codebase to find impacted areas?
```

### Skill #2: Explain Unfamiliar Code or MR
**When to Use**: Reviewing a complex Merge Request or onboarding to a new codebase.
**Prompt**: `Explain this [Issue / MR / each function in this MR]`

### Skill #3: Find Where Functions Are Called
**When to Use**: Planning a refactor or understanding the blast radius of a change.
**Prompt**: `List all the places where [FUNCTION_NAME] is called.`

### Skill #4: Summarize Recent Changes to MR/Issue
**When to Use**: Catching up on a long-running discussion or change list.
**Prompt**: `Summarize the last 5 comments in this MR/issue.`

### Skill #5: Trace Function Usage Across Codebase
**When to Use**: Understanding the full context of a function's lifecycle.
**Prompt**: `Show me where [FUNCTION] is called and how it's used.`

---

## 🏗️ Category: Analysis & Architecture

### Skill #6: Design New Feature Architecture
**When to Use**: Starting a new feature from scratch.

**Prompt Template**:
```markdown
Design the architecture for:
[FEATURE DESCRIPTION]

Consider:
1. System components needed
2. Data models
3. API contracts
4. Integration points
5. Scalability requirements
```

### Skill #7: Understand Class Hierarchy and Inheritance
**When to Use**: Working with complex Object-Oriented codebases.
**Prompt**: `Explain the class hierarchy for [CLASS_NAME] and its inheritance relationship.`

### Skill #8: Understand Data Flow Through System
**When to Use**: Tracking how input data is transformed across multiple components.
**Prompt**: `Trace the data flow for [DATA_OBJECT] from input to storage.`

### Skill #9: Analyze Database Schema and Relationships
**When to Use**: Understanding how tables interconnect and optimizing queries.
**Prompt**: `Explain the database schema for [TABLE_NAME] and its relationships with other tables.`

### Skill #10: Map Component Dependencies
**When to Use**: Visualizing the inner workings of a modular system.
**Prompt**: `Show the dependencies for the [COMPONENT_NAME] module.`

---

## 🛡️ Category: Code Review & Security

### Skill #11: Review MR for Logical Errors
**When to Use**: Supplementing automated linters with semantic checks.
**Prompt**: `Check this MR for logical errors and potential bugs.`

### Skill #12: Suggest Code Improvements in MR
**When to Use**: Identifying opportunities for cleaner, faster, or more readable code.
**Prompt**: `Suggest improvements for code quality, efficiency, and readability in this MR.`

### Skill #13: Identify Security Issues in MR
**When to Use**: Proreactive safety checks before merging.

**Prompt Template**:
```markdown
Review this MR for security issues:
1. SQL injection risks
2. XSS vulnerabilities
3. Authentication/authorization problems
4. Data exposure risks
5. Input validation issues
```

### Skill #14: Assess MR Test Coverage
**When to Use**: Ensuring quality gates are met.
**Prompt**: `Analyze the test coverage in this MR: 1. What's tested? 2. What's missing? 3. Are edge cases covered? 4. Suggest additional test cases`

---

## ⚙️ Category: Configuration & Debugging

### Skill #15: Understand Configuration and Environment Setup
**When to Use**: Debugging environment-specific issues or onboarding.
**Prompt**: `Explain how [FEATURE] is configured and what environment variables are used.`

### Skill #16: Find Code Examples of Patterns
**When to Use**: Learning how your team implements specific design patterns.
**Prompt**: `Find examples in our codebase where we use the [DESIGN_PATTERN].`

### Skill #17: Understand Error Handling Patterns
**When to Use**: Identifying gaps in error propagation.
**Prompt**: `How does our codebase handle [TYPE OF ERROR]? Show me the pattern we use and any inconsistencies.`

---

## 🚀 Pro Tips for GitHub & GitLab
*   **Context is King**: Always provide the relevant code snippets or issue descriptions.
*   **Iterate**: Use these prompts as starting points and ask follow-up questions to drill down.
*   **Platform Agnostic**: While inspired by GitLab Duo, these work perfectly in any CI/CD environment or IDE.

---
