---
description: Runs project tests intelligently. Identifies affected tests from changes and runs them first, then full suite.
---

# Run Tests

Run tests efficiently with tiered approach: affected tests first, then full suite.

## Phase 1: Detect Test Framework

Identify testing setup:

```bash
# Node.js
cat package.json | grep -E '"(jest|vitest|mocha|ava|tap)"'

# Python
ls pytest.ini pyproject.toml setup.cfg 2>/dev/null | head -1

# Go
ls *_test.go 2>/dev/null | head -1

# Rust
ls Cargo.toml 2>/dev/null
```

## Phase 2: Identify Affected Tests

Based on git diff, find related tests:

```bash
# Get changed files
git diff --name-only HEAD~1

# Find corresponding test files
# Convention: foo.ts -> foo.test.ts or foo.spec.ts
```

## Phase 3: Run Tests (Tiered Approach)

### Tier 1: Affected Tests Only (Fast)

```bash
# Node.js with Jest/Vitest
npm test -- --findRelatedTests [changed files]
npx vitest run --changed

# Python with pytest
pytest [specific test files] -x --tb=short

# Go
go test -run [TestName] ./...
```

### Tier 2: Full Unit Test Suite

If Tier 1 passes:

```bash
npm test
pytest tests/unit/
go test ./...
cargo test
```

### Tier 3: Integration Tests

If Tier 2 passes:

```bash
npm run test:integration
pytest tests/integration/
go test -tags=integration ./...
```

## Phase 4: Analyze Failures

For each failure:
1. Parse error message
2. Identify failing assertion
3. Trace to source code
4. Suggest fix

## Output Format

```
## Test Results: [PASS/FAIL]

### Summary
- Total: X tests
- Passed: Y
- Failed: Z
- Skipped: W
- Duration: [time]

### Failed Tests
1. **test_name** - `file:line`
   - Expected: [value]
   - Actual: [value]
   - Likely cause: [analysis]
   - Suggested fix: [fix]

### Flaky Test Detection
- [Any tests that passed on retry]

### Coverage (if available)
- Lines: X%
- Branches: Y%
- Functions: Z%

### Recommendation
[SAFE TO COMMIT / FIX REQUIRED / INVESTIGATE FLAKY]
```

## Continue Until Green

If tests fail:
1. Report the failure clearly
2. Attempt to fix the failing code (not just the test)
3. Re-run tests
4. Repeat until green or max 3 attempts

## Usage

Copy to your project:
```bash
cp templates/subagents/run-tests.md .claude/commands/
```

Invoke with: `/project:run-tests`
