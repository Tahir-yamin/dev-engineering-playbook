---
description: Validates project build process. Run after changes to ensure the project compiles/transpiles correctly.
---

# Validate Build

Validate that the project builds successfully. Run BEFORE commits to catch build failures early.

## Phase 1: Detect Build System

Identify the project's build system:

```bash
# Check for common build configurations
ls package.json Makefile setup.py pyproject.toml go.mod Cargo.toml CMakeLists.txt 2>/dev/null
```

## Phase 2: Run Build Commands

Based on detected system:

### Node.js/TypeScript
```bash
npm run build 2>&1 || yarn build 2>&1 || pnpm build 2>&1 || bun run build 2>&1
```

### Python
```bash
python -m py_compile **/*.py
# or for packages:
pip install -e . --dry-run
```

### Go
```bash
go build ./...
```

### Rust
```bash
cargo build
```

## Phase 3: Verify Build Artifacts

Check that expected outputs exist:
- `dist/` or `build/` directory for JS/TS
- Compiled binaries for Go/Rust
- No missing dependencies

```bash
# Example for Node.js
ls -la dist/ build/ 2>/dev/null
```

## Phase 4: Check for Warnings

Parse build output for:
- Deprecation warnings
- Unused variables/imports
- Performance warnings
- Type coercion warnings

## Output Format

```
## Build Validation: [PASS/FAIL]

### Build Command
[command used]

### Result
- Exit code: [0/non-zero]
- Duration: [time if available]

### Artifacts
- [x] Output directory created
- [x] Expected files present
- [ ] Source maps generated (if applicable)

### Warnings
- [List any build warnings]

### Errors (if failed)
- [Parse and list specific errors]
- [Suggested fixes for each]
```

## Auto-Fix Suggestions

If build fails, suggest:
1. Missing dependency installation commands
2. Type errors with file:line locations
3. Syntax errors with context
4. Configuration issues

## Usage

Copy to your project:
```bash
cp templates/subagents/validate-build.md .claude/commands/
```

Invoke with: `/project:validate-build`
