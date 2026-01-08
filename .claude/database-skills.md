# Database Skills - NeonDB & Prisma

**Topics**: PostgreSQL, NeonDB, Prisma ORM, migrations, connection issues
**Version**: 1.0

---

## Skill #1: NeonDB Connection String Setup

### When to Use
- Configuring NeonDB connection
- SSL/TLS connection errors
- Connection pooling issues

### Prompt Template

```markdown
**ROLE**: Database connectivity specialist

**DATABASE**: NeonDB (PostgreSQL)
**ERROR** (if any): [Paste error]

**REQUIRED FORMAT**:
```
postgresql://user:password@host.region.aws.neon.tech/database?sslmode=require&channel_binding=require
```

**CHECK**:
1. Protocol: `postgresql://` (not `postgres://`)
2. SSL mode: `sslmode=require`
3. Channel binding: `channel_binding=require` (NeonDB specific!)
4. No spaces or line breaks

**TEST**:
```bash
psql "$DATABASE_URL"
```

**DELIVERABLES**:
- Corrected connection string
- Environment variable setup
- Connection test commands
```

### Lesson: NeonDB requires `channel_binding=require` - without it, connections fail!

---

## Skill #2: Prisma Schema Design

### When to Use
- Creating database models
- Defining relationships
- Setting up indexes

### Prompt Template

```markdown
**ROLE**: Prisma schema architect

**MODELS NEEDED**: [User, Task, Category, etc.]

**REQUIREMENTS**:
- Relationships: [one-to-many, many-to-many]
- Indexes on: [frequently queried fields]
- Soft deletes: [Yes/No]

**EXAMPLE**:
```prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  tasks     Task[]
  createdAt DateTime @default(now())
}

model Task {
  id          String   @id @default(uuid())
  title       String
  description String?
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  @@index([userId])
}
```

**DELIVERABLES**:
- Complete schema.prisma
- Relationship explanations
- Index strategy
```

### Lessons Learned:
1. Always index foreign keys
2. Use `@unique` for lookup fields
3. `@@index` for filtered queries
4. Consider soft deletes early

---

## Skill #3: Prisma in Docker

### When to Use
- "Prisma Client not found" errors
- Binary target issues
- Docker build failures

### Prompt Template

```markdown
**ROLE**: Prisma Docker specialist

**ERROR**: [Paste error message]
**IMAGE**: [node:20-slim / alpine / etc]

**FIX CHECKLIST**:
1. Binary targets in schema.prisma:
```prisma
generator client {
  provider      = "prisma-client-js"
  binaryTargets = ["native", "debian-openssl-3.0.x"]
}
```

2. Dockerfile build order:
```dockerfile
COPY prisma ./prisma/
RUN npm install
RUN npx prisma generate  ← MUST be after npm install
```

3. Environment:
- DATABASE_URL accessible from container
- SSL certificates available

**DELIVERABLES**:
- Corrected schema.prisma
- Dockerfile fixes
- Build commands
```

### Critical: Binary targets must match Docker image OS!

---

## Skill #4: Database Migrations

### When to Use
- Schema changes
- Adding new tables/columns
- Production deployments

### Prompt Template

```markdown
**ROLE**: Database migration specialist

**CHANGE NEEDED**: [Add column / New table / etc]
**ENVIRONMENT**: [Development / Staging / Production]

**SAFE MIGRATION PROCESS**:
1. Development:
```bash
npx prisma migrate dev --name add_column_name
```

2. Review generated SQL
3. Test migration on staging
4. Production:
```bash
npx prisma migrate deploy
```

**ROLLBACK PLAN**:
- Can this be rolled back?
- Data loss risk?
- Backup strategy?

**DELIVERABLES**:
- Migration file
- Rollback plan
- Testing checklist
```

### Lessons: Always test migrations on non-prod first!

---

## Skill #5: Query Optimization

### When to Use
- Slow queries
- N+1 problem
- High database load

### Prompt Template

```markdown
**ROLE**: Database performance specialist

**SLOW QUERY**:
```typescript
[Paste slow Prisma query]
```

**OPTIMIZE WITH**:
1. Include related data:
```typescript
const tasks = await prisma.task.findMany({
  include: { user: true, category: true }  // Prevents N+1
})
```

2. Select only needed fields:
```typescript
select: { id: true, title: true }  // Reduces data transfer
```

3. Add indexes to schema
4. Use pagination/cursors
5. Consider caching

**DELIVERABLES**:
- Optimized query
- Performance comparison
- Index recommendations
```

---

## Quick Reference

### Common Prisma Commands
```bash
# Generate client
npx prisma generate

# Create migration
npx prisma migrate dev

# Deploy migrations
npx prisma migrate deploy

# Reset database (DEV ONLY!)
npx prisma migrate reset

# Seed database
npx prisma db seed

# Studio (GUI)
npx prisma studio
```

### Common Errors & Fixes

| Error | Solution |
|-------|----------|
| "Prisma Client not found" | Run `npx prisma generate` |
| "SSL negotiation failed" | Add `sslmode=require&channel_binding=require` |
| "Binary target issue" | Add correct target to schema |
| "Migration failed" | Check SQL syntax, rollback if needed |

---

## Related Skills
- Environment Skills: DATABASE_URL configuration
- Docker Skills: Containerizing Prisma
- Backend Skills: Using Prisma in FastAPI

**Database is the foundation - get it right!**
