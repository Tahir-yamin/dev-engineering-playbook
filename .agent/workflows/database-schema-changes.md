---
description: Safe workflow for modifying database schema with Prisma migrations
---

# Database Schema Changes Workflow

## When to Use
- Adding new tables
- Modifying existing columns
- Adding relationships
- Performance optimization

---

## Step 1: Plan Schema Change

Use @.claude/database-skills.md Skill #2

Document:
- What's changing
- Why it's changing
- Impact on existing data
- Rollback plan

---

## Step 2: Update Prisma Schema

```prisma
// schema.prisma

// Example: Add new column
model Task {
  id String @id
  title String
  // NEW:
  estimatedTime Int?  // Estimated minutes
  
  @@index([userId])
}
```

---

## Step 3: Create Migration (Development)

// turbo
```bash
cd phase2/backend

# Create migration
npx prisma migrate dev --name add_estimated_time
```

This will:
1. Generate SQL migration file
2. Apply to database
3. Regenerate Prisma Client

---

## Step 4: Review Migration SQL

```bash
# Check generated SQL
cat prisma/migrations/XXXXXX_add_estimated_time/migration.sql

# Verify it does what you expect
# Check for data loss warnings
```

---

## Step 5: Test on Development

// turbo
```bash
# Run Prisma Studio
npx prisma studio
```

Verify:
- New column exists
- Existing data intact
- Can create new records

---

## Step 6: Update Application Code

```typescript
// Update types
interface Task {
  id: string
  title: string
  estimatedTime?: number  // Add new field
}

// Update API/components to use new field
```

---

## Step 7: Test Application

Test CRUD operations:
- Create with new field
- Read includes new field
- Update new field
- Old data still works

---

## Step 8: Deploy to Staging

```bash
# On staging server
npx prisma migrate deploy

# Test thoroughly
```

---

## Step 9: Deploy to Production

```bash
# Backup first!
pg_dump $DATABASE_URL > backup.sql

# Deploy migration
npx prisma migrate deploy

# Verify
npx prisma studio
```

---

## Step 10: Monitor

Watch for:
- Errors in logs
- Application performance
- Database performance

---

## Rollback if Needed

```bash
# Restore from backup
psql $DATABASE_URL < backup.sql

# Or revert code and migrate back
```

---

**Reference**: @.claude/database-skills.md #4, phase2-skills.md #3
