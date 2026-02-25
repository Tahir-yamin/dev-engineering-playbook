---
description: Complete troubleshooting and development workflows for TODO Hackathon project
---

# Development Workflows - Complete Reference

**Project**: TODO Hackathon Phase 1
**Version**: 1.0
**Last Updated**: December 28, 2025

---

## 📋 Table of Contents

### Troubleshooting Workflows
1. [Build Failures](#workflow-1-build-failures)
2. [Authentication Issues](#workflow-2-authentication-issues)
3. [Docker Container Problems](#workflow-3-docker-container-problems)
4. [Database Connection Issues](#workflow-4-database-connection-issues)
5. [CORS Errors](#workflow-5-cors-errors)
6. [Performance Problems](#workflow-6-performance-problems)
7. [Deployment Issues](#workflow-7-deployment-issues)

### Development Workflows
8. [Starting New Project](#workflow-8-starting-new-project)
9. [Adding New Feature](#workflow-9-adding-new-feature)
10. [Code Review & Testing](#workflow-10-code-review--testing)
11. [Environment Setup](#workflow-11-environment-setup)
12. [Database Schema Changes](#workflow-12-database-schema-changes)

---

## 🚨 TROUBLESHOOTING WORKFLOWS

---

## Workflow 1: Build Failures

### When to Use
- npm build fails
- Docker build fails
- TypeScript compilation errors
- Dependency issues

### Steps

**1. Identify Build Type**
```bash
# Check what's failing
npm run build           # Frontend build
docker-compose build    # Docker build
npx prisma generate     # Prisma build
```

**2. Read Full Error Message**
```bash
# Don't skip this! Error messages contain the solution
# Look for:
# - File paths (case sensitivity matters)
# - Line numbers
# - Module names
# - Specific error codes
```

**3. Common Build Errors & Fixes**

**Error: "COPY failed: file not found"**
```bash
# Docker build context issue
# Fix: Check Dockerfile COPY paths match build context

# Reference: @.claude/docker-skills.md Skill #1
cd phase4/docker
# Verify paths in Dockerfile
# Build context should be: ../..
docker-compose build --no-cache frontend
```

**Error: "Module not found"**
```bash
# Missing dependency or wrong import path
npm install                    # Reinstall dependencies
rm -rf node_modules package-lock.json
npm install                    # Clean install

# Check tsconfig.json paths
# Verify import statements match file structure
# Reference: @.claude/debug-skills.md Skill #4
```

**Error: "Prisma Client could not be found"**
```bash
# Prisma not generated
npx prisma generate

# In Docker: Check binary targets in schema.prisma
# Reference: @.claude/database-skills.md Skill #3
```

**Error: TypeScript compilation errors**
```bash
# Type errors
# Fix types in the file mentioned
# Add proper type annotations
# Check interface definitions

# Reference: @.claude/frontend-skills.md Skill #6
```

**4. Verify Fix**
```bash
# Test the build
npm run build
# OR
docker-compose build
# OR
npx prisma validate
```

**5. If Still Failing**
```
@.claude/debug-skills.md Skill #1
Use systematic error analysis
```

---

## Workflow 2: Authentication Issues

### When to Use
- Login not working
- "CSRF token mismatch"
- "Session not found"
- OAuth redirect fails
- Users getting logged out

### Steps

**1. Check Environment Variables**
```bash
# Run validation
.\scripts\validate-env.ps1

# Required variables:
BETTER_AUTH_SECRET=           # Must be 32+ characters
BETTER_AUTH_URL=              # Must match access URL exactly
TRUSTED_ORIGINS=              # Must include frontend URL
DATABASE_URL=                 # Must have SSL params
```

**2. Verify Configuration**

**BETTER_AUTH_SECRET**
```bash
# Check length
echo $BETTER_AUTH_SECRET | wc -c  # Should be 32+

# Generate new if needed (Mac/Linux)
openssl rand -base64 32

# Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

**BETTER_AUTH_URL**
```bash
# Must match EXACTLY what browser shows
# ✅ Correct: http://localhost:3000
# ❌ Wrong: http://localhost:3000/
# ❌ Wrong: https://localhost:3000 (if accessing via http)

# Check match
echo $BETTER_AUTH_URL
# Should be: http://localhost:3000 (for local dev)
```

**TRUSTED_ORIGINS**
```bash
# Must include all client URLs
TRUSTED_ORIGINS=http://localhost:3000

# For production, add your domain
TRUSTED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

**3. Specific Error Fixes**

**"CSRF token mismatch"**
```bash
# Step 1: Verify BETTER_AUTH_URL matches your access URL
BETTER_AUTH_URL=http://localhost:3000

# Step 2: Check TRUSTED_ORIGINS includes frontend
TRUSTED_ORIGINS=http://localhost:3000

# Step 3: Restart services
cd phase4/docker
docker-compose restart frontend

# Reference: @.claude/auth-skills.md Skill #1
```

**"Session not found"**
```bash
# Check database connection
psql "$DATABASE_URL"

# Verify session table exists
npx prisma studio
# Look for session table

# Check cookie settings in browser DevTools
# Application → Cookies → Look for better-auth.session_token

# Reference: @.claude/auth-skills.md Skill #3
```

**OAuth redirect fails**
```bash
# Step 1: Check callback URL in provider (GitHub/Google)
# Should be: http://localhost:3000/api/auth/callback/github

# Step 2: Verify client ID and secret
echo $GITHUB_CLIENT_ID
echo $GITHUB_CLIENT_SECRET

# Step 3: Check for typos in environment variables

# Reference: @.claude/auth-skills.md Skill #2
```

**4. Test Authentication**
```bash
# Clear browser cache and cookies
# Try logging in again
# Check browser console for errors
# Check Network tab for failed requests
```

**5. Deep Dive if Needed**
```
@.claude/auth-skills.md
Use Skill #1 for complete setup guide
```

---

## Workflow 3: Docker Container Problems

### When to Use
- Container won't start
- Container crashes immediately
- Container running but app not working
- "unhealthy" status

### Steps

**1. Check Container Status**
```bash
cd phase4/docker

# List all containers
docker-compose ps

# Expected output:
# todo-frontend   running   healthy
# todo-backend    running   healthy
```

**2. Check Logs**
```bash
# View logs
docker-compose logs frontend
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f frontend

# Look for:
# - Error messages
# - Stack traces
# - "listening on port" messages (success)
```

**3. Common Container Issues**

**Container Exits Immediately**
```bash
# Check logs for error
docker-compose logs frontend

# Common causes:
# - Build failed (check build logs)
# - Environment variables missing
# - Port already in use

# Fix: Check docker-compose.yml environment section
# Verify all required env vars are set
```

**Container "Unhealthy"**
```bash
# Check health check endpoint
curl http://localhost:8000/health  # Backend
curl http://localhost:3000          # Frontend

# Review health check in docker-compose.yml
# Increase start_period if needed
```

**Port Already in Use**
```bash
# Find process using port
# Windows
netstat -ano | findstr :3000

# Kill the process or change port in docker-compose.yml
ports:
  - "3001:3000"  # Map different host port
```

**Prisma Issues in Container**
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

# Reference: @.claude/docker-skills.md Skill #4
```

**4. Debug Inside Container**
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

**5. Nuclear Option (Last Resort)**
```bash
# Stop everything
docker-compose down

# Remove volumes (CAUTION: Loses data)
docker-compose down -v

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

**6. Verify Fix**
```bash
docker-compose ps
# All should be "running" and "healthy"

# Test endpoints
curl http://localhost:3000
curl http://localhost:8000/health
```

---

## Workflow 4: Database Connection Issues

### When to Use
- "Connection refused"
- "SSL negotiation failed"
- "channel_binding required"
- Timeout errors
- Prisma can't connect

### Steps

**1. Validate Connection String**
```bash
# Check format
echo $DATABASE_URL

# Required format for NeonDB:
postgresql://user:password@host.region.aws.neon.tech/database?sslmode=require&channel_binding=require
```

**2. Parse Connection String**
```
Protocol:    postgresql://     ✅ (not postgres://)
User:        neondb_owner
Password:    npg_XXXXX
Host:        ep-xxx.region.aws.neon.tech
Database:    database_name
SSL Mode:    ?sslmode=require  ✅ Required
Channel:     &channel_binding=require  ✅ Required for NeonDB
```

**3. Test Connection**
```bash
# Using psql
psql "$DATABASE_URL"

# Should connect successfully
# If it works, DATABASE_URL is correct

# If fails, check error message
```

**4. Common Connection Errors**

**"SSL negotiation failed"**
```bash
# Missing SSL parameters
# Add to connection string:
?sslmode=require&channel_binding=require

# NeonDB specifically requires both
# Reference: @.claude/database-skills.md Skill #1
```

**"Connection timeout"**
```bash
# Check network
ping host.neon.tech

# Check firewall
# Check NeonDB status (console.neon.tech)
# Database might be paused (free tier)
```

**"Authentication failed"**
```bash
# Wrong password or user
# Get fresh connection string from NeonDB console
# Copy-paste carefully (no extra spaces)
```

**5. Prisma-Specific Issues**
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

**6. Verify Fix**
```bash
# Test connection
psql "$DATABASE_URL"

# Run query
psql "$DATABASE_URL" -c "SELECT 1;"

# Or use Prisma
npx prisma studio
```

---

## Workflow 5: CORS Errors

### When to Use
- "Access to fetch blocked by CORS policy"
- Frontend can't reach backend
- API calls fail with CORS error

### Steps

**1. Identify the Error**
```
Browser Console Error:
Access to fetch at 'http://localhost:8000/api/tasks' from origin 
'http://localhost:3000' has been blocked by CORS policy: No 
'Access-Control-Allow-Origin' header is present
```

**2. Check Backend CORS Configuration**
```python
# In backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Must match frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**3. Common CORS Fixes**

**Frontend URL Not in allow_origins**
```python
# Add your frontend URL
allow_origins=[
    "http://localhost:3000",      # Local dev
    "https://yourdomain.com",     # Production
]
```

**Using Environment Variable**
```python
import os

origins = os.getenv("CORS_ORIGINS", '["http://localhost:3000"]')
origins = eval(origins)  # Parse JSON string

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Credentials Issue**
```python
# If using cookies/auth
allow_credentials=True  # Must be True

# And never use:
# allow_origins=["*"]  # Doesn't work with credentials
```

**4. Verify Backend is Running**
```bash
# Check backend is accessible
curl http://localhost:8000/health

# Should return: {"status": "healthy"}
```

**5. Test CORS**
```bash
# From browser console
fetch('http://localhost:8000/api/tasks', {
  credentials: 'include'
})
.then(r => r.json())
.then(console.log)

# Should not show CORS error
```

**6. Restart Backend**
```bash
# After changing CORS config
cd phase4/docker
docker-compose restart backend

# Or local dev
# Ctrl+C to stop
uvicorn main:app --reload
```

**Reference**: @.claude/backend-skills.md Skill #3

---

## Workflow 6: Performance Problems

### When to Use
- Slow page load
- Laggy interactions
- High memory usage
- Unresponsive UI

### Steps

**1. Measure Performance**
```bash
# Chrome DevTools
# Cmd+Option+I (Mac) / F12 (Windows)
# → Performance tab
# → Click Record
# → Interact with app
# → Stop recording

# Look for:
# - Long tasks (>50ms) - yellow/red bars
# - Layout shifts
# - Large bundles
```

**2. Identify Bottleneck**

**Slow Initial Load**
```
Causes:
- Large JavaScript bundle
- Unoptimized images
- Too many API calls
- No code splitting
```

**Laggy Interactions**
```
Causes:
- Too many re-renders
- Heavy computations in render
- No virtualization for long lists
- Blocking main thread
```

**Slow API Responses**
```
Causes:
- N+1 query problem
- Missing database indexes
- No caching
- Inefficient queries
```

**3. Frontend Optimizations**

**Reduce Bundle Size**
```typescript
// Use dynamic imports
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />
})

// Code split routes
```

**Optimize Re-renders**
```typescript
// Use React.memo
const TaskCard = React.memo(({ task }) => {
  return <div>{task.title}</div>
})

// Use useCallback
const handleDelete = useCallback((id) => {
  deleteTask(id)
}, [deleteTask])

// Reference: @.claude/frontend-skills.md Skill #2
```

**Optimize Images**
```typescript
// Use Next.js Image
import Image from 'next/image'

<Image 
  src="/image.jpg"
  width={500}
  height={300}
  alt="Description"
/>
```

**Virtual Scrolling**
```typescript
// For lists with 100+ items
import { FixedSizeList } from 'react-window'

<FixedSizeList
  height={600}
  itemCount={1000}
  itemSize={50}
>
  {Row}
</FixedSizeList>
```

**4. Backend Optimizations**

**Fix N+1 Queries**
```typescript
// Bad: N+1 problem
const tasks = await prisma.task.findMany()
for (const task of tasks) {
  const user = await prisma.user.findUnique({ where: { id: task.userId }})
}

// Good: Include relation
const tasks = await prisma.task.findMany({
  include: { user: true }
})

// Reference: @.claude/database-skills.md Skill #5
```

**Add Database Indexes**
```prisma
model Task {
  id String @id
  userId String
  
  @@index([userId])  // Index for faster filtering
}
```

**Implement Caching**
```typescript
// Frontend: Use SWR or React Query
import useSWR from 'swr'

const { data: tasks } = useSWR('/api/tasks', fetcher, {
  revalidateOnFocus: false,
  dedupingInterval: 60000  // Cache for 1 minute
})
```

**5. Measure Improvement**
```bash
# Before and after metrics
# Chrome DevTools → Performance
# Compare:
# - Load time
# - Time to Interactive
# - Bundle size
# - Number of re-renders
```

**Reference**: @.claude/debug-skills.md Skill #6

---

## Workflow 7: Deployment Issues

### When to Use
- Moving to production
- Deploying to cloud
- Environment-specific errors
- SSL/HTTPS issues

### Steps

**1. Pre-Deployment Checklist**
```
Environment:
[ ] All secrets rotated (different from dev)
[ ] .env files not in git
[ ] HTTPS enabled
[ ] CORS restricted to domain
[ ] Rate limiting enabled
[ ] Health checks configured

Database:
[ ] Migrations tested on staging
[ ] Backup created
[ ] Connection pooling configured
[ ] SSL/TLS enabled

Security:
[ ] Secrets in vault (not .env files)
[ ] API keys have usage limits
[ ] Input validation on all endpoints
[ ] CSRF protection enabled
[ ] SQL injection prevention
```

**2. Environment Configuration**

**Production .env**
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

**3. Docker for Production**

**Multi-Stage Optimization**
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

# Reference: @.claude/docker-skills.md Skill #2
```

**4. Database Migration**

**Safe Migration Process**
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

# Reference: @.claude/database-skills.md Skill #4
```

**5. SSL/HTTPS**

**Force HTTPS**
```typescript
// Next.js middleware
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

**Update CORS for HTTPS**
```python
# Backend - production only accepts HTTPS
allow_origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
]
```

**6. Monitoring**

**Health Checks**
```bash
# Backend
curl https://api.yourdomain.com/health

# Frontend
curl https://yourdomain.com

# Database
psql "$DATABASE_URL" -c "SELECT 1;"
```

**Logs**
```bash
# Docker logs
docker-compose logs -f --tail=100

# Application logs
# Use logging service (CloudWatch, LogDNA, etc.)
```

**7. Rollback Plan**
```bash
# If deployment fails

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

## 🚀 DEVELOPMENT WORKFLOWS

---

## Workflow 8: Starting New Project

### When to Use
- Beginning a new full-stack application
- Setting up project structure
- Initial configuration

### Steps

**1. Project Planning**
```
@.claude/phase1-skills.md Skill #1

Define:
- Project type (SaaS / Internal tool / etc)
- Tech stack (Next.js + FastAPI + PostgreSQL)
- Database schema
- Core features
```

**2. Create Project Structure**
```bash
mkdir my-project
cd my-project

# Frontend
npx create-next-app@latest frontend --typescript --tailwind --app

# Backend
mkdir backend
cd backend
python -m venv venv
source venv/bin/activate  # Mac/Linux
.\venv\Scripts\activate   # Windows
pip install fastapi uvicorn prisma
```

**3. Initialize Git**
```bash
git init
echo "node_modules/" > .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo "venv/" >> .gitignore

git add .
git commit -m "Initial commit"
```

**4. Set Up Database**
```
@.claude/database-skills.md Skill #2

1. Design schema
2. Create Prisma schema file
3. Set up NeonDB connection
4. Run migrations
```

**5. Configure Environment**
```bash
# Create .env.example files
# Reference: @.claude/env-skills.md Skill #1

# Frontend: .env.example
cp frontend/.env.example frontend/.env.local

# Backend: .env.example
cp backend/.env.example backend/.env
```

**6. Development Setup**
```bash
# Install dependencies
cd frontend && npm install
cd ../backend && pip install -r requirements.txt

# Start dev servers
npm run dev          # Frontend (terminal 1)
uvicorn main:app --reload  # Backend (terminal 2)
```

**Reference**: @.claude/phase1-skills.md for complete guide

---

## Workflow 9: Adding New Feature

### When to Use
- Implementing new functionality
- Adding new page or component
- Creating new API endpoint

### Steps

**1. Plan the Feature**
```
Define:
- What it does
- API endpoints needed
- Database changes needed
- UI components needed
```

**2. Database Changes (if needed)**
```
@.claude/database-skills.md Skill #4

1. Update Prisma schema
2. Create migration
3. Test migration
4. Apply to database
```

**3. Backend Implementation**
```
@.claude/backend-skills.md

1. Create Pydantic schemas
2. Add router (backend/routers/feature.py)
3. Implement endpoints
4. Add to main.py
5. Test with docs (/docs)
```

**4. Frontend Implementation**
```
@.claude/frontend-skills.md

1. Create components
2. Add API integration
3. Implement UI
4. Add routing
5. Handle loading/error states
```

**5. Testing**
```
Test:
- API endpoints work
- UI renders correctly
- Error handling works
- Loading states show
- Edge cases handled
```

**6. Integration**
```bash
# Test full flow
1. User action → Backend → Database → Response → UI update

# Check:
- Network tab (request/response)
- Console (no errors)
- State updates correctly
- UI reflects changes
```

**7. Commit**
```bash
git add .
git commit -m "feat: add [feature name]"
```

---

## Workflow 10: Code Review & Testing

### When to Use
- Before deploying
- Pull request review
- QA testing
- Pre-production verification

### Steps

**1. Code Review Checklist**
```
Code Quality:
[ ] No console.logs in production code
[ ] Error handling present
[ ] Types defined (TypeScript)
[ ] Comments for complex logic
[ ] No hardcoded values
[ ] Environment variables used

Security:
[ ] Input validation
[ ] SQL injection prevention
[ ] XSS prevention
[ ] CSRF protection
[ ] Authentication on protected routes

Performance:
[ ] No N+1 queries
[ ] Database indexes
[ ] Images optimized
[ ] Code split (if needed)
[ ] Memoization (if needed)
```

**2. Manual Testing**
```
Happy Path:
[ ] Feature works as expected
[ ] UI looks correct
[ ] Data persists
[ ] Navigation works

Edge Cases:
[ ] Empty states
[ ] Error states
[ ] Network failures
[ ] Invalid inputs
[ ] Concurrent operations

Cross-Browser:
[ ] Chrome
[ ] Firefox
[ ] Safari (if Mac)
[ ] Edge
```

**3. Automated Testing (if implemented)**
```bash
# Unit tests
npm test

# E2E tests
npm run test:e2e

# Coverage
npm run test:coverage
```

**4. Performance Testing**
```
@.claude/debug-skills.md Skill #6

1. Chrome DevTools → Performance
2. Record interaction
3. Check for:
   - Long tasks
   - Memory leaks
   - Bundle size
```

**5. Security Testing**
```
Check:
- Authentication works
- Authorization enforced
- Secrets not exposed
- CORS configured
- Rate limiting (if implemented)
```

---

## Workflow 11: Environment Setup

### When to Use
- New team member onboarding
- Fresh machine setup
- Recovering from crash
- Setting up CI/CD

### Steps

**1. Prerequisites**
```bash
# Check installed
node --version    # Should be 18+
npm --version
python --version  # Should be 3.10+
docker --version
git --version

# Install if missing:
# Node.js: https://nodejs.org
# Python: https://python.org
# Docker: https://docker.com
```

**2. Clone Repository**
```bash
git clone https://github.com/your-repo/project.git
cd project
```

**3. Environment Files**
```bash
# Copy templates
cp phase2/frontend/.env.example phase2/frontend/.env.local
cp phase2/backend/.env.example phase2/backend/.env
cp phase4/docker/.env.example phase4/docker/.env

# Fill in values
# Reference: @.claude/env-skills.md Skill #1
```

**4. Generate Secrets**
```bash
# BETTER_AUTH_SECRET
openssl rand -base64 32

# Update in .env.local
```

**5. Database Setup**
```bash
# Get DATABASE_URL from NeonDB
# Add to .env files

# Test connection
psql "$DATABASE_URL"

# Run migrations
cd phase2/backend
npx prisma migrate deploy
```

**6. Install Dependencies**
```bash
# Frontend
cd phase2/frontend
npm install

# Backend
cd ../backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**7. Validate Setup**
```bash
# Run validation
.\scripts\validate-env.ps1

# Should show all green checkmarks
```

**8. Start Development**
```bash
# Option 1: Docker
cd phase4/docker
docker-compose up -d

# Option 2: Local
# Terminal 1
cd phase2/frontend
npm run dev

# Terminal 2
cd phase2/backend
uvicorn main:app --reload
```

**9. Verify**
```bash
# Frontend
curl http://localhost:3000

# Backend
curl http://localhost:8000/health

# Expected: Both return successfully
```

---

## Workflow 12: Database Schema Changes

### When to Use
- Adding new tables
- Modifying existing columns
- Adding relationships
- Performance optimization

### Steps

**1. Plan Schema Change**
```
@.claude/database-skills.md Skill #2

Document:
- What's changing
- Why it's changing
- Impact on existing data
- Rollback plan
```

**2. Update Prisma Schema**
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

**3. Create Migration (Development)**
```bash
cd phase2/backend

# Create migration
npx prisma migrate dev --name add_estimated_time

# This will:
# 1. Generate SQL migration file
# 2. Apply to database
# 3. Regenerate Prisma Client
```

**4. Review Migration SQL**
```bash
# Check generated SQL
cat prisma/migrations/XXXXXX_add_estimated_time/migration.sql

# Verify it does what you expect
# Check for data loss warnings
```

**5. Test on Development**
```bash
# Run Prisma Studio
npx prisma studio

# Verify:
# - New column exists
# - Existing data intact
# - Can create new records
```

**6. Update Application Code**
```typescript
// Update types
interface Task {
  id: string
  title: string
  estimatedTime?: number  // Add new field
}

// Update API/components to use new field
```

**7. Test Application**
```bash
# Test CRUD operations
# - Create with new field
# - Read includes new field
# - Update new field
# - Old data still works
```

**8. Deploy to Staging**
```bash
# On staging server
npx prisma migrate deploy

# Test thoroughly
```

**9. Deploy to Production**
```bash
# Backup first!
pg_dump $DATABASE_URL > backup.sql

# Deploy migration
npx prisma migrate deploy

# Verify
npx prisma studio
```

**10. Monitor**
```bash
# Watch for errors
# Check application logs
# Monitor database performance
```

**Rollback if Needed**
```bash
# Restore from backup
psql $DATABASE_URL < backup.sql

# Or revert code and migrate back
```

---

## 📚 Workflow Quick Reference

| Workflow | Use When | Key Tools |
|----------|----------|-----------|
| Build Failures | Won't build | docker-skills.md #1, debug-skills.md #4 |
| Auth Issues | Login broken | auth-skills.md #1-3, validate-env.ps1 |
| Docker Problems | Container fails | docker-skills.md #3, docker-compose logs |
| DB Connection | Can't connect | database-skills.md #1, psql |
| CORS Errors | API blocked | backend-skills.md #3 |
| Performance | App slow | frontend-skills.md #2, debug-skills.md #6 |
| Deployment | Going live | env-skills.md, docker-skills.md #2 |
| New Project | Starting fresh | phase1-skills.md |
| New Feature | Adding functionality | phase2/3-skills.md |
| Code Review | Before merge | debug-skills.md |
| Environment | Initial setup | env-skills.md #1, validate-env.ps1 |
| Schema Changes | DB modifications | database-skills.md #4 |

---

## 💡 Pro Tips

1. **Always validate environment first**: `.\scripts\validate-env.ps1`
2. **Check logs before asking**: `docker-compose logs -f`
3. **Test database connection**: `psql "$DATABASE_URL"`
4. **Read error messages completely**
5. **One change at a time**
6. **Commit often**
7. **Document as you go**
8. **Use the skills library**: `@.claude/skills.md`

---

**All workflows tested and verified on this project!** 🎉

**For detailed skill guides, reference the .claude/ folder**
