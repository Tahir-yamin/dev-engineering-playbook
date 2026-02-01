# Claude Code Slash Commands Skills

**Topics**: Version Control, Git, Code Analysis, Testing, Context Loading, Project Management
**Version**: 1.0
**Last Updated**: 2026-01-31

---

## Overview

Slash Commands are customized, carefully refined prompts that control Claude's behavior in order to perform specific tasks. This skill library catalogs powerful community-contributed commands for Claude Code.

---

## 🔪 Version Control & Git

### /analyze-issue [jerseycheese]
**When to Use**: Fetches GitHub issue details to create comprehensive implementation specifications.
**Action**: Analyzes requirements and plans a structured approach with clear implementation steps.

### /commit [evmts]
**When to Use**: Creates git commits using conventional commit format with appropriate emojis.
**Action**: Follows project standards and creates descriptive messages explaining the purpose of changes.

### /commit-fast [steadycursor]
**When to Use**: Automates git commit process by selecting the first suggested message.
**Action**: Skips manual confirmation and removes the Claude co-Contributorship footer.

### /create-pr [toyamarinyon]
**When to Use**: Streamlines pull request creation by handling the entire workflow.
**Action**: Creates a new branch, commits changes, formats with Biome, and submits the PR.

### /fix-issue [metabase]
**When to Use**: Addresses GitHub issues by taking issue number as parameter.
**Action**: Analyzes context, implements solution, and tests/validates the fix.

---

## 🧪 Code Analysis & Testing

### /check [rygwdn]
**When to Use**: Performs comprehensive code quality and security checks.
**Action**: Static analysis, security scanning, and style enforcement with detailed reporting.

### /code_analysis [kingler]
**When to Use**: Advanced code analysis for deep inspection.
**Action**: Generates knowledge graphs, optimization suggestions, and quality evaluation.

### /optimize [to4iki]
**When to Use**: Identifies performance bottlenecks.
**Action**: Proposes concrete optimizations with implementation guidance.

### /tdd [zscott]
**When to Use**: Guides development using Test-Driven Development principles.
**Action**: Enforces Red-Green-Refactor discipline and manages PR creation.

---

## 🧠 Context Loading & Priming

### /context-prime [elizaOS]
**When to Use**: Primes Claude with comprehensive project understanding.
**Action**: Loads repository structure, sets development context, and defines project goals.

### /load-llms-txt [ethpandaops]
**When to Use**: Loads LLM configuration files to context.
**Action**: Imports specific terminology and model configurations for AI discussions.

### /prime [yzyydev]
**When to Use**: Sets up initial project context.
**Action**: Views directory structure and reads key files, creating standardized context visualization.

---

## 📋 Project & Task Management

### /prd-generator [Denis Redozubov]
**When to Use**: Generates comprehensive Product Requirements Documents (PRDs) from conversation context.
**Action**: Produces all standard sections (Executive Summary, User Stories, MVP Scope, etc.).

### /todo [chrisleyva]
**When to Use**: Quickly manage project todo items within the interface.
**Action**: Features due dates, sorting, task prioritization, and list management.

### /mermaid [GaloyMoney]
**When to Use**: Generates Mermaid diagrams from SQL schema files.
**Action**: Creates ERDs with table properties and validates diagram compilation.

---

## Related Skills
- [git-skills.md](skills/git-skills.md)
- [testing-skills.md](skills/testing-skills.md)
- [documentation-skills.md](skills/documentation-skills.md)
