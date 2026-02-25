# Using Slash Commands in Antigravity

## Overview

Antigravity supports slash commands similar to Claude CLI, allowing you to interact with your specifications efficiently.

## Available Commands

### `/read` - Read and Analyze Specifications

**Usage:**
```
/read specs/features/task-crud.md
```

**What it does:**
- Analyzes the specification file
- Provides insights and suggestions
- Identifies missing requirements
- Checks compliance status

### `/implement` - Implement from Specification

**Usage:**
```
/implement specs/api/tasks-endpoints.md
```

**What it does:**
- Generates code based on the specification
- Creates implementation scaffolding
- Follows best practices
- Links code to spec requirements

### `/plan` - Create Implementation Plans

**Usage:**
```
/plan specs/features/authentication.md
```

**What it does:**
- Creates detailed implementation plan
- Breaks down into tasks
- Identifies dependencies
- Estimates effort

### `/test` - Generate Tests

**Usage:**
```
/test specs/features/task-crud.md
```

**What it does:**
- Generates test cases from acceptance criteria
- Creates unit, integration, and E2E tests
- Validates against specifications
- Ensures coverage

### `/fix` - Fix Implementation Issues

**Usage:**
```
/fix <describe the issue>
```

**What it does:**
- Analyzes the problem
- References relevant specifications
- Suggests fixes
- Validates against requirements

## How to Use

1. **Type `/` in the chat** - This shows available commands
2. **Select a command** - Choose from the list or type it
3. **Provide arguments** - Add file paths or descriptions as needed
4. **Review results** - Antigravity will execute the command

## Examples

### Example 1: Read a Feature Spec
```
/read specs/features/task-crud.md
```
**Result**: Analyzes the task CRUD specification and provides insights

### Example 2: Implement API Endpoints
```
/implement specs/api/rest-endpoints.md
```
**Result**: Generates FastAPI endpoint code based on the API spec

### Example 3: Create Tests
```
/test specs/features/authentication.md
```
**Result**: Generates authentication test cases

### Example 4: Plan Implementation
```
/plan specs/database/schema.md
```
**Result**: Creates migration plan for database schema

## Workflow Integration

### Typical Development Flow:

1. **Read the spec**
   ```
   /read specs/features/task-crud.md
   ```

2. **Plan implementation**
   ```
   /plan specs/features/task-crud.md
   ```

3. **Implement the feature**
   ```
   /implement specs/api/tasks-endpoints.md
   ```

4. **Generate tests**
   ```
   /test specs/features/task-crud.md
   ```

5. **Fix any issues**
   ```
   /fix Task creation returns 500 error
   ```

## Tips

- **Be specific**: Include file paths when using commands
- **Chain commands**: Use multiple commands in sequence
- **Reference specs**: Always work from specifications
- **Update specs**: Keep specifications in sync with code
- **Track progress**: Mark checkboxes as you complete items

## Differences from Claude CLI

| Feature | Claude CLI | Antigravity |
|---------|-----------|-------------|
| Command prefix | `/` | `/` |
| File reading | ✅ | ✅ |
| Implementation | ✅ | ✅ |
| Planning | ✅ | ✅ |
| Testing | ✅ | ✅ |
| IDE integration | ❌ | ✅ |
| Visual feedback | Limited | Rich |

## Troubleshooting

### Command not recognized
- Make sure you're typing `/` at the start
- Check command spelling
- Verify file paths are correct

### Spec file not found
- Use absolute paths or paths relative to project root
- Check file exists in `specs/` directory
- Verify file extension (`.md`)

### Implementation doesn't match spec
- Re-read the specification
- Update spec if requirements changed
- Use `/fix` to correct issues

## Next Steps

1. Try `/read` on your existing specs
2. Use `/plan` to create implementation strategies
3. Implement features with `/implement`
4. Generate tests with `/test`
5. Keep specs and code in sync

---

**Remember**: Slash commands make spec-driven development faster and more reliable!
