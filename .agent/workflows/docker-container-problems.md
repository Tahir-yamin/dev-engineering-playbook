---
description: Fix container startup, crashes, unhealthy status, and Docker-related issues
---

# Docker Container Problems Workflow

## When to Use
- Container won't start
- Container crashes immediately
- Container running but app not working
- "unhealthy" status

---

## Step 1: Check Container Status

// turbo
```bash
cd phase4/docker
docker-compose ps
```

Expected output:
- `todo-frontend` - running, healthy
- `todo-backend` - running, healthy

---

## Step 2: Check Logs

// turbo
```bash
# View logs
docker-compose logs frontend
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f frontend
```

Look for:
- Error messages
- Stack traces
- "listening on port" messages (success)

---

## Step 3: Common Container Issues

### Container Exits Immediately

```bash
# Check logs for error
docker-compose logs frontend

# Common causes:
# - Build failed (check build logs)
# - Environment variables missing
# - Port already in use
```

**Fix**: Check docker-compose.yml environment section

### Container "Unhealthy"

```bash
# Check health check endpoint
curl http://localhost:8000/health  # Backend
curl http://localhost:3000          # Frontend
```

**Fix**: Review health check in docker-compose.yml, increase `start_period`

### Port Already in Use

```bash
# Find process using port (Windows)
netstat -ano | findstr :3000

# Kill the process or change port in docker-compose.yml
ports:
  - "3001:3000"  # Map different host port
```

### Prisma Issues in Container

```bash
# "Prisma Client not found"
# Fix binary targets in schema.prisma

generator client {
  provider      = "prisma-client-js"
  binaryTargets = ["native", "debian-openssl-3.0.x"]
}

# Rebuild
docker-compose build --no-cache frontend
docker-compose up -d
```

**Reference**: @.claude/docker-skills.md Skill #4

---

## Step 4: Debug Inside Container

```bash
# Exec into running container
docker-compose exec frontend sh

# Check files
ls -la
cat .env.local

# Check processes
ps aux

# Exit
exit
```

---

## Step 5: Nuclear Option (Last Resort)

```bash
# Stop everything
docker-compose down

# Remove volumes (CAUTION: Loses data)
docker-compose down -v

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

---

## Step 6: Verify Fix

// turbo
```bash
docker-compose ps
# All should be "running" and "healthy"

curl http://localhost:3000
curl http://localhost:8000/health
```

---

**Related Skills**: docker-skills.md #3-4, debug-skills.md #1
