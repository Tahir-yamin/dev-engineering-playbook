---
description: Fix npm build, Docker build, TypeScript compilation errors, and dependency issues
---

# Build Failures Workflow

## When to Use
- npm build fails
- Docker build fails
- TypeScript compilation errors
- Dependency issues

---

## Step 1: Identify Build Type

```bash
# Check what's failing
npm run build           # Frontend build
docker-compose build    # Docker build
npx prisma generate     # Prisma build
```

---

## Step 2: Read Full Error Message

```bash
# Don't skip this! Error messages contain the solution
# Look for:
# - File paths (case sensitivity matters)
# - Line numbers
# - Module names
# - Specific error codes
```

---

## Step 3: Common Build Errors & Fixes

### Error: "COPY failed: file not found"

```bash
# Docker build context issue
# Reference: @.claude/docker-skills.md Skill #1

cd phase4/docker
# Verify paths in Dockerfile
# Build context should be: ../..
docker-compose build --no-cache frontend
```

### Error: "Module not found"

```bash
# Missing dependency or wrong import path
npm install                    # Reinstall dependencies
rm -rf node_modules package-lock.json
npm install                    # Clean install

# Check tsconfig.json paths
# Verify import statements match file structure
# Reference: @.claude/debug-skills.md Skill #4
```

### Error: "Prisma Client could not be found"

```bash
# Prisma not generated
npx prisma generate

# In Docker: Check binary targets in schema.prisma
# Reference: @.claude/database-skills.md Skill #3
```

### Error: TypeScript compilation errors

```bash
# Type errors
# Fix types in the file mentioned
# Add proper type annotations
# Check interface definitions

# Reference: @.claude/frontend-skills.md Skill #6
```

---

## Step 4: Verify Fix

```bash
# Test the build
npm run build
# OR
docker-compose build
# OR
npx prisma validate
```

---

## Step 5: If Still Failing

```
@.claude/debug-skills.md Skill #1
Use systematic error analysis
```

---

**Related Skills**: docker-skills.md #1, debug-skills.md #4, database-skills.md #3
