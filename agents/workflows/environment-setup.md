---
description: Complete environment setup for new team members or fresh machines
---

# Environment Setup Workflow

## When to Use
- New team member onboarding
- Fresh machine setup
- Recovering from crash
- Setting up CI/CD

---

## Step 1: Prerequisites

// turbo
```bash
# Check installed
node --version    # Should be 18+
npm --version
python --version  # Should be 3.10+
docker --version
git --version
```

Install if missing:
- Node.js: https://nodejs.org
- Python: https://python.org
- Docker: https://docker.com

---

## Step 2: Clone Repository

// turbo
```bash
git clone https://github.com/your-repo/project.git
cd project
```

---

## Step 3: Environment Files

```bash
# Copy templates
cp phase2/frontend/.env.example phase2/frontend/.env.local
cp phase2/backend/.env.example phase2/backend/.env
cp phase4/docker/.env.example phase4/docker/.env
```

Fill in values (Reference: @.claude/env-skills.md Skill #1):
- DATABASE_URL
- BETTER_AUTH_SECRET
- API keys

---

## Step 4: Generate Secrets

```bash
# BETTER_AUTH_SECRET (Mac/Linux)
openssl rand -base64 32

# Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))

# Update in .env.local
```

---

## Step 5: Database Setup

```bash
# Get DATABASE_URL from NeonDB
# Add to .env files

# Test connection
psql "$DATABASE_URL"

# Run migrations
cd phase2/backend
npx prisma migrate deploy
```

---

## Step 6: Install Dependencies

// turbo
```bash
# Frontend
cd phase2/frontend
npm install

# Backend
cd ../backend
python -m venv venv
```

Activate venv:
```bash
# Mac/Linux
source venv/bin/activate

# Windows
.\venv\Scripts\activate
```

// turbo
```bash
pip install -r requirements.txt
```

---

## Step 7: Validate Setup

// turbo
```bash
# Run validation
.\scripts\validate-env.ps1

# Should show all green checkmarks
```

---

## Step 8: Start Development

Option 1: Docker
// turbo
```bash
cd phase4/docker
docker-compose up -d
```

Option 2: Local (2 terminals)
```bash
# Terminal 1
cd phase2/frontend
npm run dev

# Terminal 2
cd phase2/backend
uvicorn main:app --reload
```

---

## Step 9: Verify

// turbo
```bash
# Frontend
curl http://localhost:3000

# Backend
curl http://localhost:8000/health

# Expected: Both return successfully
```

---

**Reference**: @.claude/env-skills.md #1, phase1-skills.md
