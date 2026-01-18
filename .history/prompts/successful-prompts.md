# Successful Prompts - History

**Project**: TODO Hackathon  
**Purpose**: Archive of successful AI prompts and their outcomes  
**Last Updated**: December 28, 2025

---

## 🎯 How to Use This File

When working with AI assistants:
1. Check this file for similar problems solved before
2. Copy successful prompts and adapt them
3. Add new successful prompts after resolving issues

---

## 📚 Prompt Categories

### [Docker & Build Issues](#docker--build-issues)
### [Authentication & Security](#authentication--security)
### [Database & Prisma](#database--prisma)
### [Frontend Development](#frontend-development)
### [Backend Development](#backend-development)
### [Environment Setup](#environment-setup)

---

## Docker & Build Issues

### Prompt: Fix Docker Build COPY Failed Error
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/docker-skills.md

I'm getting this Docker build error:
```
ERROR: failed to solve: failed to compute cache key: failed to calculate checksum of ref: 
"/phase2/frontend/package.json": not found
```

My Dockerfile has:
```dockerfile
COPY phase2/frontend/package.json ./package.json
```

Use Skill #1 to help me debug the build context issue.
```

**Outcome**:
- Identified build context was incorrect
- Fixed docker-compose.yml context path to `../..`
- Updated Dockerfile COPY paths to be relative to context
- Build successful

**Key Learning**: Docker build context must be set correctly in docker-compose.yml, and COPY commands are relative to that context.

---

### Prompt: Prisma Client Not Found in Docker
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/docker-skills.md Skill #4

Getting "Prisma Client not found" error when running frontend in Docker container.

Error:
```
PrismaClient is unable to run in this browser environment
```

Help me fix the Prisma binary targets for Docker.
```

**Outcome**:
- Added binary target to schema.prisma:
  ```prisma
  binaryTargets = ["native", "debian-openssl-3.0.x"]
  ```
- Rebuilt Docker image
- Prisma Client generated correctly for container environment

**Key Learning**: Prisma needs explicit binary targets when running in Docker containers different from development OS.

---

## Authentication & Security

### Prompt: CSRF Token Mismatch Error
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/auth-skills.md Skill #1

I'm getting "CSRF token mismatch" when trying to log in.

Current environment:
- BETTER_AUTH_URL=http://localhost:3000
- TRUSTED_ORIGINS=http://localhost:3000
- Accessing app at: http://localhost:3000

What's wrong?
```

**Outcome**:
- Verified BETTER_AUTH_URL was correct (no trailing slash)
- Added missing TRUSTED_ORIGINS to frontend .env.local
- Restarted Docker containers
- Auth working correctly

**Key Learning**: BETTER_AUTH_URL must match EXACTLY (no trailing slash), and TRUSTED_ORIGINS must be set in both frontend and backend environments.

---

### Prompt: Generate Secure BETTER_AUTH_SECRET
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/env-skills.md

I need to generate a secure BETTER_AUTH_SECRET for production.
Provide commands for both Mac/Linux and Windows.
```

**Outcome**:
```bash
# Mac/Linux
openssl rand -base64 32

# Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

Generated 32+ character secret and updated .env files.

**Key Learning**: Always use cryptographically secure random generators for auth secrets, minimum 32 characters.

---

## Database & Prisma

### Prompt: SSL Negotiation Failed with NeonDB
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/database-skills.md Skill #1

Getting "SSL negotiation failed" when connecting to NeonDB.

My connection string:
```
postgresql://user:pass@host.neon.tech/db
```

What's missing?
```

**Outcome**:
- Added SSL parameters to connection string:
  ```
  postgresql://user:pass@host.neon.tech/db?sslmode=require&channel_binding=require
  ```
- NeonDB specifically requires `channel_binding=require`
- Connection successful

**Key Learning**: NeonDB requires both `sslmode=require` AND `channel_binding=require` parameters.

---

### Prompt: Safe Database Migration to Production
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/database-skills.md Skill #4

I need to add a new column to the Task table in production.
What's the safe migration process?

New column:
```prisma
estimatedTime Int?  // Estimated minutes
```
```

**Outcome**:
1. Created migration in development
2. Reviewed generated SQL
3. Tested on staging environment
4. Backed up production database
5. Deployed migration during low-traffic period
6. Verified changes in Prisma Studio

**Key Learning**: Always test migrations on staging, backup production, and deploy during low-traffic times.

---

## Frontend Development

### Prompt: Fix Hydration Mismatch Error
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/frontend-skills.md Skill #6

Getting hydration error:
```
Hydration failed because the initial UI does not match what was rendered on the server
```

Component is using Math.random() for IDs. How to fix?
```

**Outcome**:
- Added `'use client'` directive
- Used `useEffect` to set random values after mount:
  ```typescript
  'use client'
  const [id, setId] = useState('')
  useEffect(() => setId(Math.random().toString()), [])
  ```
- Hydration error resolved

**Key Learning**: Random values or browser APIs cause hydration mismatches. Use client components and set values after mount.

---

### Prompt: Optimize Re-rendering TaskList
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/frontend-skills.md Skill #2

TaskList component re-renders on every keystroke when editing a task.
How to optimize?

Current code re-renders entire list of 100+ tasks.
```

**Outcome**:
- Wrapped TaskCard in `React.memo()`
- Used `useCallback` for delete handler
- Memoized filtered/sorted tasks with `useMemo`
- Re-renders reduced from 100+ to  1 per keystroke

**Key Learning**: Use React.memo, useCallback, and useMemo strategically for lists with many items.

---

## Backend Development

### Prompt: Fix CORS Error Between Frontend and Backend
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/backend-skills.md Skill #3

Getting CORS error:
```
Access to fetch at 'http://localhost:8000/api/tasks' from origin 
'http://localhost:3000' has been blocked by CORS policy
```

Help me configure FastAPI CORS correctly.
```

**Outcome**:
- Added CORS middleware to main.py:
  ```python
  from fastapi.middleware.cors import CORSMiddleware
  
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:3000"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```
- CORS error resolved

**Key Learning**: Always configure CORS when frontend and backend are on different ports/domains. Include `allow_credentials=True` for auth.

---

### Prompt: Implement Pydantic Validation
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/backend-skills.md Skill #2

Help me create Pydantic schemas for Task CRUD operations:
- TaskCreate (for POST)
- TaskUpdate (for PUT)
- TaskResponse (for GET)

Requirements:
- title: required string
- description: optional string
- priority: enum (low, medium, high)
- dueDate: optional datetime
```

**Outcome**:
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = Field("medium", regex="^(low|medium|high)$")
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    priority: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskResponse(TaskCreate):
    id: str
    user_id: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

**Key Learning**: Pydantic provides automatic validation and clear error messages. Separate schemas for Create/Update/Response.

---

## Environment Setup

### Prompt: Validate All Environment Variables
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/env-skills.md

Run the validation script to check all environment variables are correctly set.

Use: .\scripts\validate-env.ps1
```

**Outcome**:
- Script checked all required variables
- Identified missing BETTER_AUTH_URL in frontend
- Identified missing TRUSTED_ORIGINS
- Added missing variables
- All checks passed ✅

**Key Learning**: Always validate environment before starting development or deployment. The validate-env.ps1 script catches common issues early.

---

### Prompt: Migrate Secrets from docker-compose to .env
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/env-skills.md Skill #2

I have hardcoded secrets in docker-compose.yml that need to be moved to .env file.

Help me migrate:
- DATABASE_URL
- BETTER_AUTH_SECRET
- GITHUB_CLIENT_ID
- GITHUB_CLIENT_SECRET
etc.
```

**Outcome**:
- Created `phase4/docker/.env` file
- Moved all secrets from docker-compose.yml
- Updated docker-compose.yml to use `${VARIABLE_NAME}` syntax
- Created `.env.example` template
- Secrets no longer in version control

**Key Learning**: Never commit secrets to git. Use environment variables and provide .env.example as template.

---

## AI Integration

### Prompt: Set Up OpenRouter for Cost-Effective AI
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/ai-skills.md Skill #1

I want to add AI chat to my TODO app but OpenAI is expensive.
Help me set up OpenRouter with DeepSeek model.

Requirements:
- Cost-effective
- Chat completions
- Streaming responses
```

**Outcome**:
- Configured OpenRouter API:
  ```python
  OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
  AI_MODEL = "deepseek/deepseek-chat"  # $0.0002/1K tokens vs OpenAI $0.03/1K
  ```
- Implemented streaming responses
- 150x cheaper than GPT-4!

**Key Learning**: OpenRouter provides access to many LLMs at different price points. DeepSeek is high-quality and very cost-effective.

---

## Performance Optimization

### Prompt: Fix N+1 Query Problem
**Date**: December 2025  
**Success Rate**: ✅ 100%

```markdown
@.claude/database-skills.md Skill #5

My task list is loading slowly. Suspect N+1 query problem.

Current code:
```typescript
const tasks = await prisma.task.findMany()
for (const task of tasks) {
  const user = await prisma.user.findUnique({ where: { id: task.userId }})
}
```

How to optimize?
```

**Outcome**:
- Refactored to use Prisma `include`:
  ```typescript
  const tasks = await prisma.task.findMany({
    include: { user: true }
  })
  ```
- Reduced queries from N+1 to 1
- Page load time improved dramatically

**Key Learning**: Always use Prisma's `include` or `select` to fetch related data in a single query. Avoid fetching in loops.

---

## File Organization & Documentation

### Prompt: Organize All Learnings into Skills Library
**Date**: December 28, 2025  
**Success Rate**: ✅ 100%

```markdown
I want to organize all the lessons learned from this project into a searchable skills library for Claude.

Structure:
- By phase (Phase 1, 2, 3)
- By topic (Docker, Auth, Database, etc.)
- Each skill should have a prompt template
- Cross-referenced

Create a comprehensive .claude/ folder structure.
```

**Outcome**:
- Created `.claude/skills.md` index
- Created 12 skill files (phase-based + topic-based)
- 60+ documented skills with prompt templates
- Created 12 workflows in `.agent/workflows/`
- Created comprehensive project guide

**Key Learning**: Organizing knowledge into a searchable library dramatically speeds up future development. Reusable prompt templates save time.

---

## 📝 Template for Adding New Prompts

When you solve a problem successfully, add it here:

```markdown
### Prompt: [Brief Description]
**Date**: [Month Year]  
**Success Rate**: ✅/⚠️/❌

```markdown
[Paste the successful prompt you used]
```

**Outcome**:
- [What happened]
- [What you learned]
- [Code changes if applicable]

**Key Learning**: [One-liner lesson]
```

---

## 🎯 Most Useful Prompts (Top 10)

1. **Environment Validation** - `.\scripts\validate-env.ps1`
2. **CSRF Fix** - Check BETTER_AUTH_URL and TRUSTED_ORIGINS
3. **Docker Build Context** - Set context to `../..` in docker-compose.yml
4. **NeonDB Connection** - Add `?sslmode=require&channel_binding=require`
5. **Prisma in Docker** - Add binary target `debian-openssl-3.0.x`
6. **CORS Setup** - Configure FastAPI CORSMiddleware
7. **Hydration Fix** - Use client components for browser APIs
8. **N+1 Optimization** - Use Prisma `include`
9. **Secret Generation** - `openssl rand -base64 32`
10. **Systematic Debugging** - `.claude/debug-skills.md` Skill #1

---

**Keep this file updated! Your future self will thank you.** 🎉
