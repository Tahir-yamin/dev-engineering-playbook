---
description: Complete guide for starting a new full-stack application from scratch
---

# Starting New Project Workflow

## When to Use
- Beginning a new full-stack application
- Setting up project structure
- Initial configuration

---

## Step 1: Project Planning

Use @.claude/phase1-skills.md Skill #1

Define:
- Project type (SaaS / Internal tool / etc)
- Tech stack (Next.js + FastAPI + PostgreSQL)
- Database schema
- Core features

---

## Step 2: Create Project Structure

// turbo
```bash
mkdir my-project
cd my-project
```

```bash
# Frontend
npx create-next-app@latest frontend --typescript --tailwind --app

# Backend
mkdir backend
cd backend
python -m venv venv
```

Activate virtual environment:
```bash
# Mac/Linux
source venv/bin/activate

# Windows
.\venv\Scripts\activate
```

```bash
# Install backend dependencies
pip install fastapi uvicorn prisma
```

---

## Step 3: Initialize Git

// turbo
```bash
git init
echo "node_modules/" > .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo "venv/" >> .gitignore

git add .
git commit -m "Initial commit"
```

---

## Step 4: Set Up Database

Use @.claude/database-skills.md Skill #2

1. Design schema
2. Create Prisma schema file
3. Set up NeonDB connection
4. Run migrations

---

## Step 5: Configure Environment

```bash
# Create .env.example files
# Reference: @.claude/env-skills.md Skill #1

# Frontend: .env.example
cp frontend/.env.example frontend/.env.local

# Backend: .env.example
cp backend/.env.example backend/.env
```

Fill in:
- DATABASE_URL
- BETTER_AUTH_SECRET (generate with: `openssl rand -base64 32`)
- API keys

---

## Step 6: Development Setup

// turbo
```bash
# Install dependencies
cd frontend && npm install
cd ../backend && pip install -r requirements.txt
```

Start dev servers (2 terminals):
```bash
# Terminal 1
npm run dev          # Frontend

# Terminal 2
uvicorn main:app --reload  # Backend
```

---

## Step 7: Verify

```bash
# Frontend should be at:
http://localhost:3000

# Backend should be at:
http://localhost:8000/docs
```

---

**Reference**: @.claude/phase1-skills.md for complete guide
