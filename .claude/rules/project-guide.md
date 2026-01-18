# TODO Hackathon - Complete Project Guide

**Version**: 1.0  
**Last Updated**: December 28, 2025  
**Project Phase**: Phase 3 (Advanced Features Complete)

---

## 🎯 Project Overview

### What This Is
A production-grade, full-stack TODO application with AI integration, built across 3 development phases.

### Key Features
- ✅ Full CRUD operations for tasks
- ✅ Better Auth with email/password + GitHub OAuth
- ✅ AI chat assistant (OpenRouter/DeepSeek)
- ✅ Dark mode support
- ✅ Docker deployment ready
- ✅ Real-time task suggestions
- ✅ Secure session management

### Architecture
```
Frontend (Next.js 14 App Router)
    ↕ HTTP/REST
Backend (FastAPI Python)
    ↕ Prisma ORM
Database (NeonDB PostgreSQL)
```

---

## 📚 Technology Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 14.x | React framework (App Router) |
| TypeScript | 5.x | Type safety |
| TailwindCSS | 3.x | Styling |
| Better Auth | Latest | Authentication |
| SWR | Latest | Data fetching/caching |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.100+ | Python web framework |
| Python | 3.10+ | Programming language |
| Prisma | Latest | Database ORM |
| Pydantic | 2.x | Data validation |
| Uvicorn | Latest | ASGI server |

### Database & Services
| Service | Purpose |
|---------|---------|
| NeonDB | PostgreSQL database (serverless) |
| OpenRouter | AI/LLM API gateway |
| GitHub OAuth | Social authentication |

### DevOps
| Tool | Purpose |
|------|---------|
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Git | Version control |

---

## 🗂️ Project Structure

```
todo_hackathon_phase1/
├── .agent/
│   └── workflows/           # 12 step-by-step workflows ✅
├── .claude/
│   ├── skills.md            # 60+ skills index ✅
│   ├── workflows.md         # Combined workflows ✅
│   ├── phase1-skills.md     # Foundation skills ✅
│   ├── phase2-skills.md     # Full-stack skills ✅
│   ├── phase3-skills.md     # Advanced skills ✅
│   ├── docker-skills.md     # Docker skills ✅
│   ├── env-skills.md        # Environment skills ✅
│   ├── database-skills.md   # Database skills ✅
│   ├── auth-skills.md       # Auth skills ✅
│   ├── frontend-skills.md   # Frontend skills ✅
│   ├── backend-skills.md    # Backend skills ✅
│   ├── ai-skills.md         # AI skills ✅
│   ├── debug-skills.md      # Debug skills ✅
│   └── rules/
│       └── project-guide.md # This file
├── .spec-kit/
│   └── COMPLIANCE_SUMMARY.md # Requirements tracking
├── .specify/                # Design system (to create)
├── .history/
│   └── prompts/             # Successful prompts
├── phase2/
│   ├── frontend/            # Next.js app
│   │   ├── src/
│   │   │   ├── app/         # App Router pages
│   │   │   ├── components/  # React components
│   │   │   └── lib/         # Utilities
│   │   ├── .env.local       # Frontend env (gitignored)
│   │   └── .env.example     # Template
│   └── backend/             # FastAPI app
│       ├── routers/         # API routes
│       ├── models/          # Pydantic models
│       ├── prisma/          # Database schema
│       ├── .env             # Backend env (gitignored)
│       └── .env.example     # Template
├── phase4/
│   └── docker/
│       ├── docker-compose.yml
│       ├── .env             # Docker env (gitignored)
│       └── .env.example     # Template
└── scripts/
    ├── validate-env.ps1     # Environment validator ✅
    └── migrate-secrets.ps1  # Secret migration ✅
```

---

## 🔐 Critical Environment Variables

### Frontend (.env.local)
```bash
# Database (shared with backend)
DATABASE_URL="postgresql://user:pass@host/db?sslmode=require&channel_binding=require"

# Authentication (CRITICAL!)
BETTER_AUTH_SECRET="min-32-characters-from-openssl-rand"
BETTER_AUTH_URL="http://localhost:3000"  # NO trailing slash!
TRUSTED_ORIGINS="http://localhost:3000"

# OAuth
GITHUB_CLIENT_ID="Ov23liXXXXXXXXXXXXXX"
GITHUB_CLIENT_SECRET="secret_here"

# API
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

### Backend (.env)
```bash
# Database (same as frontend)
DATABASE_URL="postgresql://user:pass@host/db?sslmode=require&channel_binding=require"

# AI Integration
OPENROUTER_API_KEY="sk-or-v1-xxxxx"
AI_MODEL="deepseek/deepseek-chat"
GEMINI_API_KEY="optional"

# CORS
CORS_ORIGINS='["http://localhost:3000"]'
```

### Docker (.env)
```bash
# Combines all above variables
# Used by docker-compose.yml
```

---

## ⚠️ Critical Rules

### 1. Environment Variables
- ❌ **NEVER** commit `.env`, `.env.local`, or `.env.production`
- ✅ **ALWAYS** use `.env.example` as templates
- ✅ **VALIDATE** before running: `.\scripts\validate-env.ps1`
- ✅ **ROTATE** all secrets for production

### 2. Authentication
```bash
# BETTER_AUTH_SECRET
✅ Must be 32+ characters
✅ Generate with: openssl rand -base64 32
❌ Never use short or predictable values

# BETTER_AUTH_URL
✅ Must match access URL exactly
✅ Include protocol (http/https)
❌ No trailing slash
❌ Don't mismatch http vs https

# Example:
✅ BETTER_AUTH_URL="http://localhost:3000"
❌ BETTER_AUTH_URL="http://localhost:3000/"
❌ BETTER_AUTH_URL="localhost:3000"
```

### 3. Database (NeonDB)
```bash
# Connection String Format
✅ postgresql://user:pass@host/db?sslmode=require&channel_binding=require
❌ postgres://...  # Wrong protocol
❌ Missing ?sslmode=require  # Will fail
❌ Missing &channel_binding=require  # NeonDB specific requirement

# Prisma Schema
generator client {
  provider      = "prisma-client-js"
  binaryTargets = ["native", "debian-openssl-3.0.x"]  # For Docker!
}
```

### 4. Docker
```dockerfile
# Build Context (in docker-compose.yml)
build:
  context: ../..  # Two levels up (from phase4/docker/)
  dockerfile: phase4/docker/Dockerfile.frontend

# Copying Files (in Dockerfile)
COPY phase2/frontend/package.json ./  # Relative to context
```

### 5. CORS
```python
# FastAPI Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specific origins
    allow_credentials=True,  # Required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

# Production
✅ List specific domains
❌ Never use ["*"] with credentials
```

---

## 🚀 Quick Start Guide

### For New Developers

**1. Prerequisites**
```bash
node --version    # 18+
python --version  # 3.10+
docker --version
git --version
```

**2. Clone & Setup**
```bash
git clone <repo>
cd todo_hackathon_phase1

# Copy environment templates
cp phase2/frontend/.env.example phase2/frontend/.env.local
cp phase2/backend/.env.example phase2/backend/.env
cp phase4/docker/.env.example phase4/docker/.env

# Fill in values (see .env.example for guidance)
```

**3. Generate Secrets**
```bash
# Generate BETTER_AUTH_SECRET
openssl rand -base64 32
# Add to .env.local
```

**4. Validate**
```bash
.\scripts\validate-env.ps1
# Should show all green checkmarks
```

**5. Start Development**

**Option A: Docker (Recommended)**
```bash
cd phase4/docker
docker-compose up -d
```

**Option B: Local**
```bash
# Terminal 1 - Frontend
cd phase2/frontend
npm install
npm run dev

# Terminal 2 - Backend
cd phase2/backend
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload
```

**6. Access**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📖 Documentation Reference

### When You Need Help

| Problem | Check Here |
|---------|-----------|
| Build failing | `.agent/workflows/build-failures.md` |
| Auth not working | `.agent/workflows/authentication-issues.md` |
| Docker issues | `.agent/workflows/docker-container-problems.md` |
| Database errors | `.agent/workflows/database-connection-issues.md` |
| CORS errors | `.agent/workflows/cors-errors.md` |
| Performance | `.agent/workflows/performance-problems.md` |
| Any error | `.claude/debug-skills.md` Skill #1 |

### Skills Library
- **Index**: `.claude/skills.md` - Start here
- **By Phase**: `.claude/phase1-3-skills.md`
- **By Topic**: `.claude/docker-skills.md`, etc.
- **60+ Skills** with prompt templates

### Workflows
- **Index**: `.agent/workflows/README.md`
- **12 Workflows** with step-by-step instructions
- **Auto-run** commands marked with `// turbo`

---

## 🎨 Code Style & Patterns

### Frontend (Next.js)

**Server vs Client Components**
```typescript
// Server Component (default)
// Can fetch data, no hooks
async function ServerPage() {
  const data = await fetch('...')
  return <div>{data}</div>
}

// Client Component (interactive)
'use client'
function ClientComponent() {
  const [state, setState] = useState()
  return <button onClick={...}>
}
```

**File Structure**
```typescript
// app/tasks/page.tsx
export default function TasksPage() { }

// components/TaskCard.tsx
export function TaskCard({ task }: Props) { }

// lib/utils.ts
export function helper() { }
```

### Backend (FastAPI)

**Router Pattern**
```python
# routers/tasks.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/tasks")
async def get_tasks():
    return await prisma.task.find_many()

# main.py
from routers import tasks
app.include_router(tasks.router, prefix="/api")
```

**Pydantic Validation**
```python
# models/schemas.py
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
```

---

## 🔧 Common Commands

### Development
```bash
# Frontend
npm run dev          # Start dev server
npm run build        # Production build
npm run lint         # Run linter

# Backend
uvicorn main:app --reload  # Start dev server
npx prisma studio          # Database GUI
npx prisma migrate dev     # Create migration

# Docker
docker-compose up -d       # Start containers
docker-compose logs -f     # View logs
docker-compose ps          # Check status
docker-compose down        # Stop containers
```

### Database
```bash
# Prisma
npx prisma generate        # Generate client
npx prisma migrate dev     # Dev migration
npx prisma migrate deploy  # Production migration
npx prisma studio          # GUI

# Direct PostgreSQL
psql "$DATABASE_URL"       # Connect
psql "$DATABASE_URL" -c "SELECT 1;"  # Test query
```

### Validation
```bash
.\scripts\validate-env.ps1  # Validate environment
```

---

## 🐛 Troubleshooting Quick Reference

### Build Errors
```bash
# Module not found
rm -rf node_modules package-lock.json
npm install

# Prisma Client not found
npx prisma generate

# TypeScript errors
npm run build  # See detailed errors
```

### Auth Errors
```bash
# CSRF token mismatch
# 1. Check BETTER_AUTH_URL matches browser URL
# 2. Verify TRUSTED_ORIGINS includes frontend
# 3. Restart services
```

### Docker Errors
```bash
# Container fails
docker-compose logs frontend  # Check logs
docker-compose logs backend

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Database Errors
```bash
# Connection failed
# Check DATABASE_URL has:
# - protocol: postgresql://
# - SSL: ?sslmode=require&channel_binding=require

# Test connection
psql "$DATABASE_URL"
```

---

## 🎯 AI Assistant Guidelines

When you (AI assistant) are helping with this project:

### DO:
1. ✅ **Check `.claude/skills.md` first** for relevant skills
2. ✅ **Reference workflows** in `.agent/workflows/` for procedures
3. ✅ **Validate environment** before suggesting code
4. ✅ **Consider both** local and Docker setups
5. ✅ **Use proper** TypeScript types
6. ✅ **Follow** Next.js App Router patterns
7. ✅ **Test** database connections before assuming they work

### DON'T:
1. ❌ **Never** suggest committing `.env` files
2. ❌ **Never** use raw SQL (use Prisma)
3. ❌ **Never** hardcode secrets in code
4. ❌ **Don't** assume environment variables are set
5. ❌ **Don't** use Server Components for interactive UI
6. ❌ **Don't** forget CORS when adding API routes
7. ❌ **Don't** skip TypeScript types

### Before Suggesting Code:
1. Understand the context (Frontend? Backend? Docker?)
2. Check if similar code exists (patterns)
3. Verify environment variables needed
4. Consider error handling
5. Think about TypeScript types

---

## 📈 Project Status

### Completed Phases
- ✅ **Phase 1**: Foundation (Planning, Schema, Stack)
- ✅ **Phase 2**: Core Implementation (CRUD, API, UI)
- ✅ **Phase 3**: Advanced Features (Auth, AI, OAuth)

### Current State
- ✅ Full CRUD operations working
- ✅ Better Auth with email/password
- ✅ GitHub OAuth integration
- ✅ AI chat assistant
- ✅ Docker deployment ready
- ✅ Environment validation scripts
- ✅ Comprehensive documentation

### Known Issues
- None (all major issues resolved)

### Technical Debt
- None critical
- Consider adding E2E tests
- Consider adding rate limiting

---

## 🔗 Quick Links

**Documentation**
- Skills Index: `.claude/skills.md`
- Workflows Index: `.agent/workflows/README.md`
- This Guide: `.claude/rules/project-guide.md`

**Scripts**
- Validate: `.\scripts\validate-env.ps1`
- Migrate: `.\scripts\migrate-secrets.ps1`

**Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Prisma Studio: http://localhost:5555 (when running)

---

## 📝 Changelog

### v1.0 - December 28, 2025
- Initial comprehensive project guide
- Documented all 3 phases
- Added troubleshooting quick reference
- Included AI assistant guidelines

---

**This is your single source of truth for the project. Keep it updated!**
