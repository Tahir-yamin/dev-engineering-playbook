---
description: Runs linting and code quality checks. Catches style issues, potential bugs, and enforces project standards.
---

# Lint Check

Run linting and code quality checks. Catches issues before they reach CI.

## Phase 1: Detect Linting Tools

Find project's linting configuration:

```bash
# JavaScript/TypeScript
ls .eslintrc* eslint.config.* .prettierrc* 2>/dev/null

# Python
ls pyproject.toml .flake8 .ruff.toml setup.cfg 2>/dev/null

# Go
ls .golangci.yml .golangci.yaml 2>/dev/null

# Rust
ls rustfmt.toml .rustfmt.toml clippy.toml 2>/dev/null
```

## Phase 2: Run Linters

### JavaScript/TypeScript
```bash
npx eslint . --ext .js,.ts,.tsx --format stylish
npx prettier --check .
```

### Python
```bash
ruff check .
# or fallback
flake8 .
black --check .
mypy .
```

### Go
```bash
golangci-lint run
gofmt -l .
go vet ./...
```

### Rust
```bash
cargo clippy -- -D warnings
cargo fmt --check
```

## Phase 3: Categorize Issues

### Critical (Must Fix)
- Security vulnerabilities
- Undefined variables
- Type errors
- Potential null pointer issues
- SQL injection patterns

### Warnings (Should Fix)
- Unused variables/imports
- Missing return types
- Inconsistent naming
- Complex expressions

### Style (Auto-fixable)
- Formatting issues
- Import ordering
- Trailing whitespace
- Line length

## Phase 4: Auto-Fix Option

Offer to auto-fix style issues:

```bash
# JavaScript/TypeScript
npx eslint . --fix
npx prettier --write .

# Python
ruff check . --fix
black .
isort .

# Go
gofmt -w .

# Rust
cargo fmt
```

## Output Format

```
## Lint Results: [PASS/FAIL/WARNINGS]

### Summary
- Errors: X
- Warnings: Y
- Auto-fixable: Z

### Critical Issues (Must Fix)
1. **[Rule]** - `file:line`
   - Message: [linter message]
   - Fix: [how to fix]

### Warnings (Should Fix)
1. **[Rule]** - `file:line`
   - Message: [message]

### Auto-Fixed (if --fix was run)
- [List of auto-fixed issues]

### Commands Used
- [List all linting commands run]

### Recommendation
[ ] Ready to commit
[ ] Fix critical issues first
[ ] Run auto-fix and review changes
```

## Usage

Copy to your project:
```bash
cp templates/subagents/lint-check.md .claude/commands/
```

Invoke with: `/project:lint-check`
