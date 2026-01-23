# Docker AI Agent (Gordon) - Complete Guide & Integration

**Purpose**: AI-assisted Docker operations using natural language  
**Availability**: Docker Desktop 4.35+ (Beta Feature)  
**Status**: Optional but impressive enhancement  
**Last Updated**: December 30, 2025

---

## What is Gordon?

**Gordon** is Docker's AI Agent that allows you to interact with Docker using natural language commands. Instead of remembering complex Docker CLI syntax, you can ask Gordon in plain English.

**Key Features**:
- Natural language Docker operations
- Image building assistance
- Container management
- Troubleshooting and debugging
- Best practices recommendations
- Interactive learning mode

---

## Installation & Setup

### Prerequisites

1. **Docker Desktop 4.35 or later**
2. **Beta Features enabled**
3. **Docker account** (free - just sign in)
4. **❌ NO OpenAI API key needed!** (Gordon runs locally)

### How Gordon Works (Corrected)

**Important**: Gordon does NOT require you to provide API keys! Here's how it actually works:

- **Local Execution**: Gordon uses Docker's built-in AI models or Docker Model Runner
- **Automatic Authentication**: Handled by Docker Desktop when you sign in
- **No Cloud API Calls**: Can run entirely locally on your machine
- **Zero Fees**: No external API charges

**Docker Model Runner**:
- Runs AI models locally on your computer
- No data sent to cloud
- No API keys required
- Private and secure

### Step 1: Update Docker Desktop

```powershell
# Check current version
docker --version

# Expected: Docker version 4.35.0 or higher
```

**If older version**:
1. Download latest Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Install and restart

### Step 2: Sign In to Docker

```powershell
# Sign in to Docker (required for Gordon)
docker login

# Follow prompts to authenticate
```

**Note**: Docker account is free. This enables Gordon's AI features.

### Step 3: Enable Gordon in Docker Desktop

1. Open **Docker Desktop**
2. Click **Settings** (gear icon)
3. Navigate to **Beta features**
4. Toggle **ON**: "Enable Docker AI" or "Enable Ask Gordon"
5. (Optional) Enable "Docker Model Runner" for fully local AI
6. Click **Apply & Restart**

### Step 4: Verify Installation

```powershell
# Test Gordon
docker ai "What can you do?"
```

**Expected Response**:
```
I'm Gordon, Docker's AI agent! I can help you with:
- Building Docker images
- Running and managing containers
- Debugging container issues
- Writing Dockerfiles
- Docker Compose operations
- Best practices and optimization
- Troubleshooting errors

How can I assist you today?
```

**If Gordon doesn't respond**:
- Verify Docker Desktop is running
- Check you're signed in: `docker login`
- Ensure Beta Features are enabled
- Restart Docker Desktop

---

## No API Keys Needed! ✅

### Common Misconception (Corrected)

❌ **WRONG**: "Gordon requires OpenAI API key"  
✅ **CORRECT**: "Gordon runs locally, no external API keys needed"

### How Gordon is Different from Other AI Tools

| Feature | Gordon | kubectl-ai/kagent | Custom AI App |
|---------|--------|-------------------|---------------|
| API Keys | ❌ Not needed | ✅ Require OpenAI | ✅ Require |
| Local Execution | ✅ Yes (Model Runner) | ❌ Cloud only | Varies |
| Cost | 🆓 Free | 💰 Pay per use | 💰 Pay per use |
| Authentication | Docker sign-in | API key env var | API key |
| Privacy | 🔒 Can be local | ☁️ Cloud | Varies |

### Optional: Docker Model Runner (Fully Local AI)

For complete privacy and offline use:

1. Enable "Docker Model Runner" in Settings → Beta Features
2. Gordon will download and run AI models locally
3. **Zero cloud API calls**
4. **Zero fees**
5. Works without internet (after model download)

```powershell
# Check if Model Runner is active
docker info | Select-String "Model Runner"
```

---

## Gordon for Phase IV TODO App

### Use Case 1: Building Docker Images

#### Traditional Way:
```powershell
docker build -t todo-frontend:v2 `
  -f phase4/docker/frontend.Dockerfile `
  --build-arg NEXT_PUBLIC_API_URL=http://localhost:30001 `
  --build-arg BETTER_AUTH_URL=http://localhost:30000 `
  --build-arg NEXT_PUBLIC_APP_URL=http://localhost:30000 `
  phase2/frontend
```

#### With Gordon:
````powershell
docker ai "Build a production-optimized Next.js Docker image from phase2/frontend using phase4/docker/frontend.Dockerfile. Tag it as todo-frontend:v2. Set build arguments: NEXT_PUBLIC_API_URL=http://localhost:30001, BETTER_AUTH_URL=http://localhost:30000, NEXT_PUBLIC_APP_URL=http://localhost:30000"
```

**Gordon's Response**:
```
I'll build that for you. Here's the command I'm running:

docker build -t todo-frontend:v2 \
  -f phase4/docker/frontend.Dockerfile \
  --build-arg NEXT_PUBLIC_API_URL=http://localhost:30001 \
  --build-arg BETTER_AUTH_URL=http://localhost:30000 \
  --build-arg NEXT_PUBLIC_APP_URL=http://localhost:30000 \
  phase2/frontend

[Build output follows...]
✓ Successfully built todo-frontend:v2

Tip: This is a multi-stage build. Your image size is 485MB, which is optimized for production.
```

---

### Use Case 2: Troubleshooting Build Errors

**Scenario**: Your Docker build is failing with Prisma errors

#### With Gordon:
```powershell
docker ai "My Next.js Docker build is failing with 'Prisma binary target missing for linux-musl'. How do I fix this?"
```

**Gordon's Response**:
```
This error occurs because Prisma needs to know which platform target to build for. 
In your Alpine Linux Docker image, you need to specify the linux-musl binary target.

Fix:
1. Update your prisma/schema.prisma:

generator client {
  provider = "prisma-client-js"
  binaryTargets = ["native", "linux-musl"]
}

2. Rebuild the Prisma client in your Dockerfile before the final stage:

RUN npx prisma generate

This ensures the correct binary is included in your production image.

Would you like me to update your Dockerfile with this fix?
```

---

### Use Case 3: Container Management

#### Check Running Containers

**Traditional**:
```powershell
docker ps
docker ps -a
docker stats
```

**With Gordon**:
```powershell
# Quick status
docker ai "Show me all running containers and their resource usage"

# Specific query
docker ai "Which containers are using the most memory?"

# Troubleshooting
docker ai "Why is my todo-frontend container constantly restarting?"
```

---

### Use Case 4: Image Optimization

**Ask Gordon for optimization tips**:
```powershell
docker ai "Analyze my frontend Dockerfile and suggest optimizations"
```

**Gordon's Analysis**:
```
Analyzing phase4/docker/frontend.Dockerfile...

Current image size: 485MB

Optimization opportunities:
1. ✓ Already using multi-stage build (good!)
2. ✓ Using Node alpine base (lightweight)
3. ⚠ Consider using .dockerignore to exclude:
   - node_modules
   - .next
   - .git
   - README.md
   Potential savings: ~50MB

4. ⚠ Cache optimization:
   - Layer order is good, but consider copying package.json before all files
   - This improves cache hit rate during development

5. ✓ Dependencies are installed in separate layer (good!)

Suggested improvements could reduce size to ~430MB.

Would you like me to generate an optimized Dockerfile?
```

---

### Use Case 5: Testing Containers Locally

**Test before Kubernetes deployment**:

```powershell
# Run frontend locally
docker ai "Run the todo-frontend:v2 image on port 3000 with environment variables from my .env file"
```

**Gordon's Command**:
```powershell
docker run -d `
  --name todo-frontend-test `
  -p 3000:3000 `
  --env-file phase2/frontend/.env `
  todo-frontend:v2

Container started: todo-frontend-test
Access at: http://localhost:3000

Tip: Use 'docker logs todo-frontend-test' to view logs
```

---

## Gordon Testing Capabilities

### Can Gordon Run Tests?

**Yes!** Gordon can help with containerized testing:

#### 1. Unit Tests in Container

```powershell
docker ai "Run the frontend tests inside a container"
```

**Gordon executes**:
```powershell
docker run --rm `
  -v ${PWD}/phase2/frontend:/app `
  -w /app `
  node:18-alpine `
  npm test
```

#### 2. Integration Tests

```powershell
docker ai "Start a test environment with frontend, backend, and test database, then run integration tests"
```

**Gordon's Response**:
```
I'll create a docker-compose test environment:

version: '3.8'
services:
  test-db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=testdb
      - POSTGRES_USER=test
      - POSTGRES_PASSWORD=test
  
  backend:
    image: todo-backend:v1
    depends_on:
      - test-db
    environment:
      - DATABASE_URL=postgresql://test:test@test-db:5432/testdb
  
  frontend:
    image: todo-frontend:v2
    depends_on:
      - backend
    ports:
      - "3000:3000"

Starting test environment...
Running integration tests...
[Test output]
```

#### 3. Health Check Tests

```powershell
docker ai "Test if my backend container is healthy"
```

**Gordon's Actions**:
```powershell
# Checks health endpoint
docker run --rm todo-backend:v1 sh -c "curl http://localhost:8000/health"

# If custom health check needed
docker ai "Add a health check to my backend that pings /health every 30 seconds"
```

#### 4. Load Testing

```powershell
docker ai "Run a load test against my containerized application with 100 concurrent users"
```

**Gordon sets up**:
```dockerfile
# Uses tools like wrk or ab in a container
docker run --rm williamyeh/wrk `
  -t 4 -c 100 -d 30s `
  http://host.docker.internal:30001/api/tasks
```

---

## Gordon Workflows for Phase IV

### Workflow 1: Build & Test Pipeline

```powershell
# Step 1: Build images  
docker ai "Build both frontend and backend images for production"

# Step 2: Test images
docker ai "Run health checks on both images"

# Step 3: Scan for vulnerabilities
docker ai "Scan todo-frontend:v2 and todo-backend:v1 for security vulnerabilities"

# Step 4: Push to registry (if using)
docker ai "Tag and push images to my Docker Hub repository"
```

### Workflow 2: Debugging Failed Builds

```powershell
# When build fails
docker ai "My backend build is failing at line 23 with 'pip install error'. Show me why and how to fix it"

# Gordon analyzes Dockerfile and error logs
# Provides fix suggestions with explanation
```

### Workflow 3: Container Cleanup

```powershell
# Clean up old images
docker ai "Remove all unused Docker images and containers to free up space"

# Specific cleanup
docker ai "Delete all images tagged 'v1' except the latest"
```

---

## Gordon vs Traditional Docker CLI

| Task | Traditional CLI | With Gordon | Time Saved |
|------|-----------------|-------------|------------|
| Build with multiple args | 3-5 min (lookup syntax) | 1 min (natural language) | ~3 min |
| Troubleshoot error | 10-15 min (Google/docs) | 2-3 min (Gordon explains) | ~10 min |
| Multi-container setup | 5-10 min (write compose file) | 2 min (Gordon generates) | ~5 min |
| Optimize Dockerfile | 20-30 min (research patterns) | 5 min (Gordon analyzes) | ~20 min |

**Total Time Saved**: ~1-2 hours for Phase IV development

---

## Demonstrating Gordon for Hackathon

### Demo Script for Judges (2 minutes)

```powershell
# 1. Show Gordon introduction (15s)
docker ai "What can you do?"

# 2. Build an image (30s)
docker ai "Build the frontend image with optimizations"

# 3. Troubleshoot (20s)
docker ai "Check if my containers are using too much memory"

# 4. Run tests (20s)
docker ai "Run unit tests for the backend"

# 5. Cleanup (15s)
docker ai "Clean up all stopped containers and dangling images"

# Total: ~100 seconds
```

### Documentation for CLAUDE.md

Add this section:

```markdown
## Docker AI Agent (Gordon) Usage

### Building Images with Gordon

Instead of memorizing Docker build syntax, we used Gordon for natural language operations:

```powershell
docker ai "Build production frontend with build args for Kubernetes deployment"
```

Gordon automatically:
- Applied multi-stage builds
- Set correct build arguments
- Optimized layer caching
- Suggested improvements

### Troubleshooting with Gordon

When encountering Prisma binary target errors:
```powershell
docker ai "Fix Prisma binary missing error in Alpine Linux"
```

Gordon identified the issue and provided the exact fix for 
prisma/schema.prisma.
```

---

## Gordon Limitations & Workarounds

### Limitation 1: Beta Feature Availability

**Issue**: Gordon is a Beta feature, not available in all Docker Desktop versions.

**Requirements**:
- Docker Desktop 4.35+ required
- Beta features must be enabled
- Must be signed in to Docker account

**Workaround**: If Gordon is unavailable:
- Use Claude Code to generate Docker commands (acceptable per hackathon rules)
- Use standard Docker CLI
- Document what you would have done with Gordon

### Limitation 2: Requires Docker Desktop

**Issue**: Gordon only works with Docker Desktop, not Docker Engine alone.

**Workaround**: 
- Install Docker Desktop (free)
- Or use traditional Docker CLI commands

### Limitation 3: Complex Multi-Step Operations

**Issue**: Gordon works best for single focused tasks, not complex multi-step workflows.

**Workaround**: Break down into smaller Gordon commands or use traditional CLI for very specific scenarios.

### Limitation 4: Internet Connection (Depends on Mode)

**With Docker Model Runner** (Recommended):
- ✅ Works offline after initial model download
- ✅ No internet needed
- ✅ Completely private

**Without Docker Model Runner** (Cloud Mode):
- ⚠️ Requires internet connection
- ⚠️ May send data to Docker cloud services

**Workaround**: Enable Docker Model Runner for offline use.

---

## Gordon Best Practices

### 1. Be Specific

❌ **Vague**: "Build my app"  
✅ **Specific**: "Build a production Next.js image from phase2/frontend using phase4/docker/frontend.Dockerfile, tagged as todo-frontend:v2"

### 2. Ask for Explanations

```powershell
docker ai "Build my frontend image and explain each step"
```

Gordon will show the command AND explain what each part does.

### 3. Iterate with Feedback

```powershell
# First try
docker ai "Make my Docker image smaller"

# Gordon suggests optimizations

# Apply and verify
docker ai "Show me the new image size compared to the old one"
```

### 4. Use Gordon for Learning

```powershell
docker ai "Explain the difference between COPY and ADD in Dockerfiles"
docker ai "What are Docker multi-stage builds and why should I use them?"
```

---

## Integrating Gordon into Phase IV

### Update CLAUDE.md

Add Gordon usage examples:
- How Gordon helped with Dockerfile creation
- Troubleshooting assistance from Gordon
- Gordon's optimization suggestions

### Update MANUAL-OPERATIONS-GUIDE.md

Add Gordon alternative for each Docker command:

```markdown
### Alternative: Using Docker AI (Gordon)

Instead of manual Docker commands, you can use Gordon:

```powershell
docker ai "Build and tag all images for the TODO application"
```

Gordon will build both frontend and backend with optimal settings.
```

### Add to Demo Video Script

**Optional 10-second segment**:
```
[45-55 seconds mark]
Narrator: "We leverage Docker AI (Gordon) for intelligent operations"
[Show command]
docker ai "Build production images with optimization"
[Show Gordon's response with recommendations]
```

---

## Cloud-Native Testing with Gordon

### Test 1: Application Health

```powershell
docker ai "Verify all TODO app containers are healthy and responding"
```

### Test 2: Resource Usage

```powershell
docker ai "Check if any container is using more than 80% CPU or memory"
```

### Test 3: Multi-Container Communication

```powershell
docker ai "Test if frontend can reach backend API"
```

### Test 4: Database Connectivity

```powershell
docker ai "Test if backend can connect to NeonDB through the container"
```

### Test 5: Build Reproducibility

```powershell
docker ai "Rebuild all images and verify they match the production tags"
```

---

## Bonus Points: Gordon in Documentation

### How to Document Gordon Usage for +200 Bonus

**Reusable Intelligence Section**:

```markdown
### AI-Assisted Docker Operations with Gordon

We created reusable Gordon prompts for common operations:

1. **Image Building**:
   ```
   docker ai "Build [component] image for Kubernetes with [specific config]"
   ```

2. **Troubleshooting**:
   ```
   docker ai "Diagnose why [container] is failing"
   ```

3. **Optimization**:
   ```
   docker ai "Analyze [Dockerfile] and suggest improvements"
   ```

These prompts are documented in `phase4/scripts/gordon-prompts.md` for team reuse.
```

---

## Gordon Checklist for Phase IV

- [ ] **Docker Desktop 4.35+ installed**
- [ ] **Signed in to Docker account** (`docker login`)
- [ ] **Enabled "Docker AI" in Beta Features**
- [ ] **(Optional) Enabled "Docker Model Runner" for local AI**
- [ ] **Tested Gordon with "What can you do?"**
- [ ] **Used Gordon to build at least one image**
- [ ] **Documented Gordon usage in CLAUDE.md**
- [ ] **Added Gordon alternative to Manual Operations Guide**
- [ ] **Created reusable Gordon prompts library** (bonus)
- [ ] **Mentioned Gordon in demo video** (optional)
- [ ] **Showed Gordon troubleshooting example** (bonus impression)

**Note**: ❌ **No OpenAI API keys needed!** Gordon runs locally.

---

## Example: Complete Gordon Session for Phase IV

```powershell
# Session start
PS> docker ai "Hello, I'm building a Kubernetes-native TODO app. Can you help?"

Gordon: "Absolutely! I can assist with:
- Building Docker images
- Creating docker-compose for local testing
- Running containers
- Troubleshooting issues
- Optimizing for Kubernetes deployment

What would you like to start with?"

PS> docker ai "Build production-optimized images for both frontend (Next.js) and backend (FastAPI)"

Gordon: "I'll build both images with production best practices.

Building frontend (Next.js)...
✓ Using multi-stage build
✓ Node 18 Alpine (lightweight)
✓ Production dependencies only
✓ Build cache optimized
Image: todo-frontend:v2 (485MB)

Building backend (FastAPI)...
✓ Using Python 3.13 slim
✓ System dependencies for PostgreSQL
✓ Virtual environment isolated
✓ Health check configured
Image: todo-backend:v1 (245MB)

Both images are ready for Kubernetes deployment!

Next steps:
- Test locally: docker ai 'Run both containers with docker-compose'
- Deploy to K8s: kubectl apply -f your-manifests/
"

PS> docker ai "Test the images locally before I deploy to Kubernetes"

Gordon: "Creating test environment...

version: '3.8'
services:
  backend:
    image: todo-backend:v1
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: ${DATABASE_URL}
  
  frontend:
    image: todo-frontend:v2
    ports: ["3000:3000"]
    depends_on: [backend]

Starting containers...
✓ backend: Running on http://localhost:8000
✓ frontend: Running on http://localhost:3000

Health checks:
✓ Backend /health: 200 OK
✓ Frontend: UI loaded successfully

All tests passed! Ready for Kubernetes deployment.
"
```

---

## Summary

### Gordon Capabilities for Phase IV

✅ **Can Do**:
- Build Docker images with AI assistance
- Troubleshoot build errors
- Optimize Dockerfiles
- Run containerized tests
- Health checks and monitoring
- Image analysis and recommendations
- Container management
- Cleanup and maintenance

✅ **Benefits**:
- **Zero cost** - No API fees
- **Local execution** - Privacy and security
- **Faster development** - Natural language commands
- **Better error messages** - AI explanations
- **Best practices by default** - AI suggestions
- **Learning while building** - Interactive troubleshooting
- **No API key management** - Just sign in to Docker

⚠️ **Cannot Do**:
- Kubernetes operations (use kubectl-ai/kagent instead)
- Replace all manual Docker commands
- Work without Docker Desktop

### Key Advantages Over Other AI Tools

**Gordon vs kubectl-ai/kagent**:
- ✅ Gordon: Free, no API keys, local execution
- ⚠️ kubectl-ai/kagent: Requires OpenAI API key, pay per use

**Gordon vs Custom AI Apps**:
- ✅ Gordon: Built into Docker, zero setup
- ⚠️ Custom: Requires integration, API key management

### Recommendation

**If you have Docker Desktop 4.35+**:
1. ✅ **Enable Gordon** (takes 2 minutes)
2. ✅ **Sign in to Docker** (free account)
3. ✅ **(Optional) Enable Model Runner** for fully local AI
4. ✅ **Use it!** - Impressive for judges, zero cost
5. ✅ **Document usage** in CLAUDE.md
6. ✅ **Show in demo video** (10 seconds)
7. ✅ **Create reusable prompts** (+200 bonus potential)

**If Gordon is unavailable**:
- Use standard Docker CLI ✅ (explicitly allowed)
- Use Claude Code for command generation ✅ (explicitly allowed)
- Document why Gordon wasn't used
- No penalty per hackathon rules

---

**Gordon Status**: **Optional but highly recommended** if available  
**Cost**: **🆓 FREE** - No API keys, no fees  
**Time Investment**: 5 min setup + ongoing use  
**Bonus Value**: +Demo credibility, +reusable intelligence documentation  
**Privacy**: Can run completely locally with Model Runner  
**Updated**: December 30, 2025 (**Corrected - No API keys needed!**)
