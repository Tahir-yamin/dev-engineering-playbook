# Docker Skills - For Claude AI

**Purpose**: Docker troubleshooting and optimization skills
**Version**: 1.0
**Last Updated**: December 28, 2025

Full documentation: See `docker_lessons_learned_complete.md` in artifacts

---

## Skill #1: Docker Build Debugging Expert

### When to Use
- Docker build is failing
- "COPY failed" errors
- Build context issues
- Multi-stage build problems

### Prompt Template

```markdown
**ROLE**: Senior DevOps Engineer specializing in Docker troubleshooting

**CONTEXT**: 
- Docker build is failing with error: [PASTE_ERROR_HERE]
- Dockerfile location: [PATH_TO_DOCKERFILE]
- Build context: [BUILD_CONTEXT_PATH]

**TASK**:
1. Analyze the error message and identify root cause
2. Check Dockerfile for common issues (build context paths, COPY instructions)
3. Verify docker-compose.yml configuration
4. Provide step-by-step fix with exact commands

**OUTPUT**: Root cause analysis, exact fix, rebuild commands, verification steps
```

---

## Skill #2: Multi-Stage Docker Build Architect

### When to Use
- Creating new Dockerfiles
- Optimizing existing builds
- Reducing image size
- Separating dev/prod dependencies

### Prompt Template

```markdown
**ROLE**: Docker optimization specialist

**APPLICATION**: [Next.js 14 / React / FastAPI / Django / etc]
**PACKAGE MANAGER**: [npm / pnpm / pip / poetry]

**REQUIREMENTS**:
- Minimal image size (target: <200MB)
- Layer caching for fast rebuilds
- No dev dependencies in production
- Health check support

**DELIVERABLES**:
1. Optimized multi-stage Dockerfile with comments
2. Expected final image size
3. Build command
4. Before/After comparison
```

---

## Skill #3: Container Debugging Detective

### When to Use
- Container starts but app doesn't work
- Network connectivity issues
- Environment variable problems

### Prompt Template

```markdown
**ROLE**: Container debugging specialist

**PROBLEM**: [Describe what's not working]

**SYMPTOMS**:
- Container status: [Up / Restarting / Exited]
- Logs show: [Paste relevant log lines]

**DEBUGGING WORKFLOW**:
Guide me through:
1. Log analysis
2. Container inspection (exec into container)
3. Environment verification
4. Network testing
5. File system check

**PROVIDE**: Debug commands, expected vs actual output, root cause, fix recommendations
```

---

## Skill #4: Prisma in Docker Configuration

### When to Use
- "Prisma Client not found" errors
- Binary target issues
- Migration failures in Docker

### Prompt Template

```markdown
**ROLE**: Prisma and database specialist

**PROBLEM**: [Describe Prisma issue in Docker]
**ERROR**: [Paste error message]

**VERIFY**:
1. Binary targets in schema.prisma correct?
2. `prisma generate` run in Dockerfile?
3. DATABASE_URL accessible from container?
4. Schema files copied before generation?

**PROVIDE**: Corrected schema.prisma, Dockerfile fixes, commands to regenerate
```

---

## Quick Reference Patterns

### Pattern 1: Frontend + Backend + Cloud DB

```yaml
services:
  backend:
    build:
      context: ../..
      dockerfile: phase4/docker/backend.Docker file
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    environment:
      - DATABASE_URL=${DATABASE_URL}
  
  frontend:
    build:
      context: ../..
      dockerfile: phase4/docker/frontend.Dockerfile
    depends_on:
      backend:
        condition: service_healthy
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Pattern 2: Multi-Stage Dockerfile (Next.js)

```dockerfile
FROM node:20-slim AS deps
WORKDIR /app
COPY package*.json ./
RUN npm install

FROM node:20-slim AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npx prisma generate && npm run build

FROM node:20-slim AS runner
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
CMD ["node", "server.js"]
```

---

## Common Commands

```bash
# Build & Run
docker-compose build --no-cache frontend
docker-compose up -d

# Debug
docker-compose logs -f frontend
docker-compose exec frontend sh
docker-compose ps

# Clean
docker-compose down
docker-compose down -v  # Remove volumes too
```

---

**See Also**:
- Full lessons learned document in artifacts
- Environment variables skills in `.claude/env-skills.md`
