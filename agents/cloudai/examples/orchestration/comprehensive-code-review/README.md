# Comprehensive Code Review Workflow

A 6-agent sequential workflow for thorough code analysis before merging.

## Overview

This workflow coordinates 6 specialist agents to provide comprehensive code review:

```
orchestrator → code-reviewer → security-auditor → test-architect → refactorer → docs-writer
```

Each agent focuses on a specific aspect:

| Order | Agent | Focus Area |
|-------|-------|------------|
| 1 | orchestrator | Coordinates the workflow, synthesizes results |
| 2 | code-reviewer | Quality, patterns, maintainability |
| 3 | security-auditor | OWASP Top 10, vulnerabilities, secrets |
| 4 | test-architect | Test coverage, testing strategy |
| 5 | refactorer | Technical debt, code improvements |
| 6 | docs-writer | Documentation completeness |

## When to Use

- Before merging a significant PR
- After implementing a new feature
- During code audit/review cycles
- When onboarding to understand code quality

## Prerequisites

- Claude Code v1.0.33+
- project-starter plugin loaded
- A codebase with recent changes to review

## Quick Start

Simply ask Claude to perform a comprehensive review:

```
Review the recent changes comprehensively. Check code quality,
security, test coverage, and documentation. Provide actionable
recommendations.
```

The orchestrator will automatically delegate to specialists.

## What You'll Get

1. **Code Quality Report** - Patterns, best practices, maintainability issues
2. **Security Audit** - Vulnerabilities, OWASP findings, remediation steps
3. **Test Analysis** - Coverage gaps, recommended test cases
4. **Refactoring Suggestions** - Technical debt, improvement opportunities
5. **Documentation Review** - Missing docs, outdated content
6. **Executive Summary** - Aggregated findings with priorities

## Files in This Example

| File | Description |
|------|-------------|
| [workflow.md](workflow.md) | Exact prompts and expected agent behavior |
| [verification.md](verification.md) | How to verify the workflow works |
| [sample-outputs/](sample-outputs/) | Example outputs from each agent |

## Time Estimate

15-30 minutes depending on codebase size and complexity.

## Customization

You can customize by specifying focus areas:

```
Review the authentication module. Focus especially on security
and test coverage. Skip documentation review.
```

Or by targeting specific files:

```
Review src/api/auth.js and src/middleware/jwt.js.
Run full security audit and suggest tests.
```
