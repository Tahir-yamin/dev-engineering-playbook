---
description: Fix "Connection refused", SSL errors, channel_binding issues, and Prisma connection problems
---

# Database Connection Issues Workflow

## When to Use
- "Connection refused"
- "SSL negotiation failed"
- "channel_binding required"
- Timeout errors
- Prisma can't connect

---

## Step 1: Validate Connection String

```bash
# Check format
echo $DATABASE_URL

# Required format for NeonDB:
postgresql://user:password@host.region.aws.neon.tech/database?sslmode=require&channel_binding=require
```

---

## Step 2: Parse Connection String

Verify these components:
- Protocol: `postgresql://` ✅ (not `postgres://`)
- User: `neondb_owner`
- Password: `npg_XXXXX`
- Host: `ep-xxx.region.aws.neon.tech`
- Database: `database_name`
- SSL Mode: `?sslmode=require` ✅ Required
- Channel: `&channel_binding=require` ✅ Required for NeonDB

---

## Step 3: Test Connection

```bash
# Using psql
psql "$DATABASE_URL"

# Should connect successfully
# If it works, DATABASE_URL is correct
```

---

## Step 4: Common Connection Errors

### "SSL negotiation failed"

```bash
# Missing SSL parameters
# Add to connection string:
?sslmode=require&channel_binding=require

# NeonDB specifically requires both
```

**Reference**: @.claude/database-skills.md Skill #1

### "Connection timeout"

```bash
# Check network
ping host.neon.tech

# Check NeonDB status (console.neon.tech)
# Database might be paused (free tier)
```

### "Authentication failed"

```bash
# Wrong password or user
# Get fresh connection string from NeonDB console
# Copy-paste carefully (no extra spaces)
```

---

## Step 5: Prisma-Specific Issues

```bash
# Prisma can't connect
# Check environment variable is set
echo $DATABASE_URL

# Regenerate Prisma Client
npx prisma generate

# Test with Prisma Studio
npx prisma studio
# Should open browser interface
```

---

## Step 6: Verify Fix

// turbo
```bash
# Test connection
psql "$DATABASE_URL"

# Run query
psql "$DATABASE_URL" -c "SELECT 1;"

---
description: Fix "Connection refused", SSL errors, channel_binding issues, and Prisma connection problems
---

# Database Connection Issues Workflow

## When to Use
- "Connection refused"
- "SSL negotiation failed"
- "channel_binding required"
- Timeout errors
- Prisma can't connect

---

## Step 1: Validate Connection String

```bash
# Check format
echo $DATABASE_URL

# Required format for NeonDB:
postgresql://user:password@host.region.aws.neon.tech/database?sslmode=require&channel_binding=require
```

---

## Step 2: Parse Connection String

Verify these components:
- Protocol: `postgresql://` ✅ (not `postgres://`)
- User: `neondb_owner`
- Password: `npg_XXXXX`
- Host: `ep-xxx.region.aws.neon.tech`
- Database: `database_name`
- SSL Mode: `?sslmode=require` ✅ Required
- Channel: `&channel_binding=require` ✅ Required for NeonDB

---

## Step 3: Test Connection

```bash
# Using psql
psql "$DATABASE_URL"

# Should connect successfully
# If it works, DATABASE_URL is correct
```

---

## Step 4: Common Connection Errors

### "SSL negotiation failed"

```bash
# Missing SSL parameters
# Add to connection string:
?sslmode=require&channel_binding=require

# NeonDB specifically requires both
```

**Reference**: @.claude/database-skills.md Skill #1

### "Connection timeout"

```bash
# Check network
ping host.neon.tech

# Check NeonDB status (console.neon.tech)
# Database might be paused (free tier)
```

### "Authentication failed"

```bash
# Wrong password or user
# Get fresh connection string from NeonDB console
# Copy-paste carefully (no extra spaces)
```

---

## Step 5: Prisma-Specific Issues

```bash
# Prisma can't connect
# Check environment variable is set
echo $DATABASE_URL

# Regenerate Prisma Client
npx prisma generate

# Test with Prisma Studio
npx prisma studio
```

---

## Issue 5: Missing Prisma Migrations

### Symptoms
- 500 errors on API endpoints that use database
- "relation does not exist" errors
- Authentication not working (session table missing)
- Some features work, others don't

### Diagnosis

Check which tables exist:
```bash
# For Docker
docker exec -it todo-postgres psql -U postgres -d tododb -c "\dt"

# For Kubernetes
kubectl exec statefulset/postgres -n todo-chatbot -- \
  psql -U postgres -d tododb -c "\dt"

# Compare with Prisma schema
cat phase2/frontend/prisma/schema.prisma | grep "model "
```

**Common Missing Tables**:
- `session` - Required for Better Auth
- `verification` - Required for email verification
- New tables after schema changes

### Fix

#### Option 1: Run Migrations (Recommended)
```bash
# Development
cd phase2/frontend
npx prisma migrate deploy

# Docker
docker exec todo-frontend npx prisma migrate deploy

# Kubernetes
kubectl exec deployment/todo-app-frontend -n todo-chatbot -- \
  npx prisma migrate deploy
```

#### Option 2: Reset Database (Development Only)
```bash
# ⚠️ WARNING: Deletes all data!
cd phase2/frontend
npx prisma migrate reset
```

#### Option 3: Manual SQL (Advanced)
```bash
# Connect to database
psql -U postgres -d tododb

# Create missing tables (example: session)
CREATE TABLE "session" (
  "id" TEXT NOT NULL PRIMARY KEY,
  "userId" TEXT NOT NULL,
  "token" TEXT NOT NULL UNIQUE,
  "expiresAt" TIMESTAMP(3) NOT NULL,
  "ipAddress" TEXT,
  "userAgent" TEXT,
  "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updatedAt" TIMESTAMP(3) NOT NULL,
  FOREIGN KEY ("userId") REFERENCES "user"("id") ON DELETE CASCADE
);
```

### Verification
```bash
# Check table now exists
psql -U postgres -d tododb -c "\d session"

# Test application
# Try signup/signin - should work now
```

### Prevention
1. **Always run migrations after schema changes**
2. **Include migrations in deployment process**
3. **Add init container for automatic migrations** (see Kubernetes workflow)
4. **Version control migration files** (prisma/migrations/)

---

**Related Workflows**: `/kubernetes-deployment-testing`, `/database-schema-changes`

**Related Skills**: `.claude/database-skills.md`
1, env-skills.md #3

---

## Step 6: Verify Fix

// turbo
```bash
# Test connection
psql "$DATABASE_URL"

# Run query
psql "$DATABASE_URL" -c "SELECT 1;"

# Or use Prisma
npx prisma studio
```

---

**Related Skills**: database-skills.md #1, env-skills.md #3
