---
description: Complete production deployment checklist and troubleshooting guide
---

# Deployment Issues Workflow

## When to Use
- Moving to production
- Deploying to cloud
- Environment-specific errors
- SSL/HTTPS issues

---

## Step 1: Pre-Deployment Checklist

### Environment
- [ ] All secrets rotated (different from dev)
- [ ] .env files not in git
- [ ] HTTPS enabled
- [ ] CORS restricted to domain
- [ ] Rate limiting enabled
- [ ] Health checks configured

### Database
- [ ] Migrations tested on staging
- [ ] Backup created
- [ ] Connection pooling configured
- [ ] SSL/TLS enabled

### Security
- [ ] Secrets in vault (not .env files)
- [ ] API keys have usage limits
- [ ] Input validation on all endpoints
- [ ] CSRF protection enabled
- [ ] SQL injection prevention

---

## Step 2: Environment Configuration

Production .env example:
```bash
# Different from development!
NODE_ENV=production
DEBUG=false

# HTTPS URLs
BETTER_AUTH_URL=https://yourdomain.com
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
TRUSTED_ORIGINS=https://yourdomain.com

# Strong secrets (rotated)
BETTER_AUTH_SECRET=new-32+-char-secret-here

# Production database
DATABASE_URL=postgresql://...production...

# API keys with limits
OPENAI_API_KEY=production-key
```

---

## Step 3: Docker for Production

Multi-Stage Optimization:
```dockerfile
# Use optimized production build
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:20-slim AS runner
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

ENV NODE_ENV=production
CMD ["node", "server.js"]
```

**Reference**: @.claude/docker-skills.md Skill #2

---

## Step 4: Database Migration

Safe Migration Process:
```bash
# Step 1: Backup production database
pg_dump $DATABASE_URL > backup.sql

# Step 2: Test on staging first
npx prisma migrate deploy --preview-feature

# Step 3: Verify on staging
# Test all functionality

# Step 4: Deploy to production during low-traffic
npx prisma migrate deploy

# Step 5: Verify
npx prisma studio
# Check schema changes applied
```

**Reference**: @.claude/database-skills.md Skill #4

---

## Step 5: SSL/HTTPS

Force HTTPS (Next.js middleware):
```typescript
export function middleware(request: NextRequest) {
  if (
    process.env.NODE_ENV === 'production' &&
    request.headers.get('x-forwarded-proto') !== 'https'
  ) {
    return NextResponse.redirect(
      `https://${request.headers.get('host')}${request.nextUrl.pathname}`,
      301
    )
  }
}
```

Update CORS for HTTPS:
```python
# Backend - production only accepts HTTPS
allow_origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
]
```

---

## Step 6: Monitoring

Health Checks:
```bash
# Backend
curl https://api.yourdomain.com/health

# Frontend
curl https://yourdomain.com

# Database
psql "$DATABASE_URL" -c "SELECT 1;"
```

---

## Step 7: Rollback Plan

If deployment fails:
```bash
# Step 1: Revert to previous Docker image
docker-compose down
docker-compose pull previous-tag
docker-compose up -d

# Step 2: Rollback database if needed
psql $DATABASE_URL < backup.sql

# Step 3: Verify
curl https://yourdomain.com/health
```

---

**Related Skills**: env-skills.md, docker-skills.md #2, database-skills.md #4
