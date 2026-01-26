# Python Code Quality with Ruff - Skills

**Topics**: Python linting, code formatting, CI/CD, code quality  
**Tools**: ruff, pytest, git
**Difficulty**: Beginner to Intermediate  
**Version**: 1.0

---

## Skill #1: Auto-Fix Common Lint Errors

### When to Use
- Quick cleanup before committing
- Preparing code for PR review
- Fixing trailing whitespace, import order, quote styles

### Command

```bash
# Auto-fix safe errors
ruff check --fix

# Format code to PEP 8
ruff format

# Verify
ruff check
```

### Lessons Learned
- ✅ Fixes 20-40% of typical lint errors automatically
- ✅ Safe to run - won't change logic
- ✅ Handles W291, B007, I001, Q000 reliably
- ❌ Won't fix E501 or B904 - requires manual intervention

---

## Skill #2: Fix Exception Chaining (B904)

### When to Use
- CI fails with B904 errors
- You're re-raising exceptions
- Stack traces are getting lost

### Pattern

**Problem:**
```python
try:
    import some_module
except ImportError:
    raise RuntimeError("Module not found")
```

**Solution:**
```python
try:
    import some_module
except ImportError as err:
    raise RuntimeError("Module not found") from err
```

### Why It Matters
Without `from err`, the original exception context is lost, making debugging harder.

### Lessons Learned
- ✅ Always use `from err` when re-raising
- ✅ Preserves full stack trace
- ✅ Makes debugging 10x easier
- ❌ Never use `from None` unless intentionally hiding context

---

## Skill #3: Break Long Lines (E501)

### When to Use
- Most common lint error (80%+ of failures)
- Lines exceed 100 characters
- CI blocks PR due to line length

### Techniques

**Technique 1: Implicit String Concatenation**
```python
# Before (123 chars)
error_msg = "This is a very long error message that provides detailed context about what went wrong"

# After
error_msg = (
    "This is a very long error message that provides detailed "
    "context about what went wrong"
)
```

**Technique 2: Break Function Calls**
```python
# Before
result = api.call(endpoint="/v1/users", method="POST", data={"name": "John"}, timeout=30)

# After
result = api.call(
    endpoint="/v1/users",
    method="POST",
    data={"name": "John"},
    timeout=30,
)
```

**Technique 3: Break F-Strings**
```python
# Before
log_msg = f"Processing user {user_id} at {timestamp} with status {status}"

# After
log_msg = (
    f"Processing user {user_id} at {timestamp} "
    f"with status {status}"
)
```

**Technique 4: Break Dictionaries**
```python
# Before
config = {"database": "postgresql://localhost/db", "timeout": 30, "retry": 3}

# After
config = {
    "database": "postgresql://localhost/db",
    "timeout": 30,
    "retry": 3,
}
```

### Lessons Learned
- ✅ Implicit concatenation is cleanest for strings
- ✅ Always add trailing comma in multiline structures
- ✅ Use `ruff format` first - it handles 50%+ automatically
- ❌ Avoid breaking in the middle of logical units

---

## Skill #4: Strategic Use of # noqa

### When to Use
- Line is complex and can't be broken cleanly
- Breaking would hurt readability more than help
- Annotated type hints or complex dicts

### Syntax

```python
# Suppress specific error
long_line = "some content"  # noqa: E501

# Suppress all errors on line (use sparingly!)
complex_stuff = ...  # noqa

# Suppress multiple specific errors
code = "..."  # noqa: E501,F841
```

### Best Practices

**Good uses:**
```python
# Complex Annotated type hints
def create_plan(
    steps: Annotated[str, "JSON array of plan steps with id, description, action, inputs, expected_outputs, dependencies"],  # noqa: E501
) -> str:
    pass

# Conditional imports that modify __all__
try:
    from framework.llm.anthropic import AnthropicProvider  # noqa: F401
    __all__.append("AnthropicProvider")
except ImportError:
    pass
```

**Bad uses:**
```python
# Don't use noqa to avoid fixing actual problems
def bad_function(): pass  # noqa: E501  # BAD: Just break the line!

# Don't suppress logic errors
result = undefined_var  # noqa: F821  # BAD: Fix the undefined variable!
```

### Automated noqa Addition

**For bulk E501 errors, use this script:**
```python
import json, subprocess
from pathlib import Path

def get_e501_errors():
    result = subprocess.run(
        ["ruff", "check", "--select", "E501", "--output-format=json"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout) if result.stdout else []

for error in get_e501_errors():
    file_path = Path(error["filename"])
    lines = file_path.read_text().splitlines(keepends=True)
    line_no = error["location"]["row"] - 1
    
    if '# noqa' not in lines[line_no]:
        lines[line_no] = lines[line_no].rstrip() + "  # noqa: E501\n"
        file_path.write_text(''.join(lines))
```

### Lessons Learned
- ✅ Last resort - try to fix properly first
- ✅ Use specific error codes (E501, not just noqa)
- ✅ Limit to <5% of total lines
- ❌ Don't use to hide real problems

---

## Skill #5: Lint Error Debugging

### When to Use
- Ruff shows errors but unclear why
- "Target content not found" when editing
- Errors persist after apparent fix

### Debugging Commands

```bash
# Show detailed error information
ruff check --output-format=json | jq '.'

# Check specific file
ruff check path/to/file.py

# Check specific rule
ruff check --select E501

# Show statistics
ruff check --statistics

# Clear cache if seeing stale errors
ruff check --no-cache
```

### Common Issues

**Issue 1: Cache Staleness**
```bash
# Solution
rm -rf .ruff_cache
ruff check --no-cache
```

**Issue 2: Line Ending Differences**
```bash
# Check line endings
file path/to/file.py

# Fix if needed (Git will handle)
git add path/to/file.py
```

**Issue 3: Whitespace Mismatch**
```bash
# View exact characters
cat -A path/to/file.py | grep "problem_line"

# Or in PowerShell
Get-Content path/to/file.py | Select-String "problem_line" | Format-Hex
```

### Lessons Learned
- ✅ Always clear cache when debugging
- ✅ Use `--output-format=json` for scripting
- ✅ Check one file at a time when stuck
- ❌ Don't trust line numbers if file recently changed

---

## Skill #6: Ruff Configuration

### When to Use
- Setting up new Python project
- Team needs different rules
- Want to customize line length or ignored rules

### Configuration File

**Create `ruff.toml` or `pyproject.toml`:**

```toml
[tool.ruff]
# Increase line length if needed
line-length = 120

# Select rules to enable
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "B",   # flake8-bugbear
    "I",   # isort
]

# Ignore specific rules
ignore = [
    "E501",  # line too long (if you want to disable)
]

# Exclude directories
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "migrations",
]

# Per-file ignores
[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__
"tests/*" = ["F841"]      # Allow unused variables in tests
```

### Common Configurations

**Strict (Recommended for New Projects):**
```toml
[tool.ruff]
line-length = 100
select = ["ALL"]
ignore = ["D"]  # Ignore docstring rules initially
```

**Legacy (For Existing Codebases):**
```toml
[tool.ruff]
line-length = 120
select = ["E", "F"]
ignore = ["E501"]  # Allow long lines during migration
```

### Lessons Learned
- ✅ Start strict for new projects
- ✅ Gradually tighten rules for legacy code
- ✅ Use per-file ignores for special cases
- ❌ Don't disable all E501 - fix the code instead

---

## Quick Reference

### Most Common Errors

| Code | Description | Fix |
|------|-------------|-----|
| E501 | Line too long | Break into multiple lines |
| B904 | Exception re-raised without `from` | Add `from err` |
| F401 | Unused import | Remove or add `# noqa: F401` |
| B007 | Unused loop variable | Rename to `_variable` |
| W291 | Trailing whitespace | `ruff check --fix` |
| I001 | Imports unsorted | `ruff check --fix` |
| Q000 | Wrong quote style | `ruff check --fix` |

### Command Cheat Sheet

```bash
# Auto-fix
ruff check --fix
ruff format

# Check specific error type
ruff check --select E501
ruff check --select B904

# Statistics
ruff check --statistics

# Ignore cache
ruff check --no-cache

# Output as JSON
ruff check --output-format=json

# Show fixes that would be applied
ruff check --diff

# Apply unsafe fixes
ruff check --unsafe-fixes --fix
```

---

## Related Skills

- `github-ci-cd-troubleshooting.md`
- `python-testing-with-pytest.md`
- `systematic-debugging.md`

---

**Real-World Success: PR #526**

Fixed 118 lint errors in ~2 hours using these skills:
- Skill #1: Auto-fix → 42 errors resolved
- Skill #2: Exception chaining → 4 errors resolved
- Skill #3: Line breaking → 50 errors resolved
- Skill #4: Strategic noqa → 49 errors resolved
- Skill #5: Debugging → Resolved cache/edit issues

**Result:** CI unblocked, PR merged ✅

---

**Last Updated:** 2026-01-26  
**Maintainer:** @tahir-yamin
