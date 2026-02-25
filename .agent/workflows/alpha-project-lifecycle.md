---
description: The master Alpha Project Lifecycle covering Inception, Creation, Feature Development, and Wrap-up.
---

# 🚀 ALPHA PROJECT LIFECYCLE (SOVEREIGN COMMAND)

**Unified Workflow**: `detailed-project-inception.md`, `starting-new-project.md`, `adding-new-feature.md`, `project-wrap-up.md`.

---

## 📂 PHASE 0: INCEPTION & ISOLATION POLICY

**CRITICAL**: To keep the knowledge base clean, **new projects MUST be created outside** `d:\my-dev-knowledge-base\`.
- ✅ **CORRECT**: `d:\my-new-app`
- ❌ **INCORRECT**: `d:\my-dev-knowledge-base\my-new-app`

### Step 1: Requirements Discovery (Socratic Gate)
Ask 5-8 strategic questions:
1. **Business Goal**: What problem does this solve?
2. **User Personas**: Who are the primary users?
3. **Tech Stack**: Preferred frameworks (Next.js, FastAPI, etc.)?
4. **Security**: PII, Auth, or Internal tool?
5. **Impact**: Does it reuse existing patterns/exemplars in the repo?

---

## 🛠️ PHASE 1: STARTING A NEW PROJECT

1. **Plan**: Define Tech Stack and Database Schema.
2. **Structure**: 
   ```bash
   npx create-next-app@latest frontend --typescript --tailwind --app
   mkdir backend && cd backend && python -m venv venv
   ```
3. **Git**: `git init` + `.gitignore` (node_modules, .env, venv).
4. **DB**: Use Prisma for schema management and migrations.
5. **Env**: Create `.env.example` first. Never hardcode secrets.

---

## ⚡ PHASE 2: ADDING NEW FEATURES

1. **Database**: Update `schema.prisma` → `npx prisma migrate dev`.
2. **Backend**:
   - Define Pydantic schemas.
   - Implement FastAPI routers.
   - Test via `/docs` (Swagger).
3. **Frontend**:
   - Create functional components with Hooks.
   - Implement loading/error states.
   - Hook up API with `fetch` or `SWR`/`React Query`.
4. **Verification**: Verify End-to-End flow from UI to DB.

---

## 🏁 PHASE 3: PROJECT WRAP-UP & SYNERGY

When a project or major phase is complete:
1. **Audit**: Run `checklist.py` and security scans.
2. **Extract**: Identify "Gold Standard" files for future reuse.
3. **Memory**: Update `.github/instructions/memory.instruction.md` with lessons learned.
4. **Knowledge**: Run `python scripts/distill_knowledge.py` if new libraries were mastered.

---
**Standard**: Phase 5 Sovereign Logic
**Status**: Alpha Optimized
