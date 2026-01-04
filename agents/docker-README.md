# Docker-Architect Agent - Autonomous Build & Repair System

## 🎯 Overview

The Docker-Architect Agent transforms Docker from a static packaging tool into an **autonomous, self-optimizing build system**. Using the MCP (Model Context Protocol), the agent can:

- 🔍 **Monitor** container resource usage in real-time
- 🔧 **Debug** build failures automatically
- ⚡ **Optimize** image layers and build cache
- 🔐 **Secure** images before production
- 🎯 **Verify** critical artifacts (like Prisma binaries)

---

## 📋 Available Skills (8 Total)

### 1. Monitoring
**`analyze_container_stats`**
- Real-time CPU, RAM, Network, Block I/O monitoring
- Identifies resource bottlenecks
- Suggests resource limit adjustments

**Example Use**:
```
User: "Is the frontend container using too much memory?"

Agent:
[Calls: /docker/analyze-stats with container_name="frontend"]

Result: Frontend using 180MB / 512MB (35%)
Status: ✅ Within healthy limits
```

---

### 2. Validation
**`verify_prisma_binary`**
- Checks for correct Prisma engine binary (linux-musl-openssl-3.0.x)
- Critical for Alpine-based containers
- Prevents 500 PrismaClientInitializationError

**Example Use**:
```
User: "Getting Prisma errors in production"

Agent:
[Calls: /docker/verify-prisma with container_name="backend"]

Result: ❌ linux-musl binary not found
Fix: Add binaryTargets to schema.prisma
```

---

### 3. Optimization  
**`analyze_image_layers`**
- Lists all Docker layers with sizes
- Identifies bloated layers
- Suggests multi-stage build improvements

**`compare_image_sizes`**
- Measures optimization impact
- Shows size reduction in MB and percentage

**`optimize_build_cache`**
- Analyzes COPY/RUN ordering
- Suggests cache-friendly restructuring

**Example Use**:
```
User: "Build takes forever, make it faster"

Agent:
[Calls: /docker/analyze-layers with image_name="todo-frontend:v1"]

Found: 842MB total, 456MB in node_modules layer

[Calls: /docker/optimize-cache with dockerfile_path]

Suggestions:
1. Copy package.json first (before source code)
2. Combine 5 RUN commands into 2
3. Use .dockerignore for .git, .next

Estimated improvement: 40% faster rebuilds
```

---

### 4. Debugging
**`detect_build_failures`**
- Pattern matches common errors:
  - ETIMEDOUT (network timeouts)
  - PrismaClientInitializationError (missing binaries)
  - Google Fonts timeout
  - ENOSPC (disk space)
- Provides specific fixes for each

**`suggest_dockerfile_fixes`**
- Analyzes Dockerfile structure
- Checks for best practices
- Provides improvement suggestions

**Example Use**:
```
User: "Docker build fails with ETIMEDOUT"

Agent:
[Calls: /docker/detect-failures with build_log]

Detected: ETIMEDOUT during npm install
Cause: Network timeout

Fix: Add retry configuration:
RUN npm config set fetch-retries 5 && \
    npm config set fetch-retry-mintimeout 20000 && \
    npm ci
```

---

### 5. Security
**`check_security_vulnerabilities`**
- Checks if running as root
- Verifies specific image tags (not `latest`)
- Detects secrets in environment variables
- Provides security score

**Example Use**:
```
User: "Is the image production-ready?"

Agent:
[Calls: /docker/security-scan with image_name="todo-backend:v1"]

Security Audit:
❌ Running as root (risk)
⚠️  Using 'latest' tag
✅ No secrets in env vars

Score: 40/100
Status: NOT ready for production

Recommended fixes:
1. Add non-root user
2. Use specific tags
3. Run Trivy scan
```

---

## 🔗 MCP Endpoints

All Docker skills are accessible via the FastAPI backend:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/docker/skills` | GET | List available skills |
| `/docker/analyze-stats` | POST | Container resource monitoring |
| `/docker/verify-prisma` | POST | Prisma binary validation |
| `/docker/analyze-layers` | POST | Image layer analysis |
| `/docker/detect-failures` | POST | Build failure detection |
| `/docker/suggest-fixes` | POST | Dockerfile improvement suggestions |
| `/docker/compare-sizes` | POST | Image size comparison |
| `/docker/security-scan` | POST | Security vulnerability check |
| `/docker/optimize-cache` | POST | Build cache optimization |

---

## 🧠 Agent Workflow Examples

### Workflow 1: Automatic Prisma Fix

```
CHECKPOINT: User reports 500 error in production

Agent Detective Work:
1. Checks backend logs → PrismaClientInitializationError
2. Calls /docker/verify-prisma → Missing linux-musl binary
3. Analyzes schema.prisma → Missing binaryTargets
4. Suggests fix: Add linux-musl-openssl-3.0.x to binaryTargets
5. Verifies Dockerfile has explicit `npx prisma generate`
6. After rebuild: Calls /docker/verify-prisma → ✅ Binary found
7. Reports: "Prisma fixed. Redeploy to resolve 500 errors."
```

### Workflow 2: Build Optimization

```
CHECKPOINT: User complains builds are slow

Agent Optimization:
1. Calls /docker/analyze-layers → 842MB image, many layers
2. Calls /docker/optimize-cache → Found cache issues
3. Suggests fixes:
   - Reorder COPY commands (package.json before source)
   - Combine RUN statements
   - Add .dockerignore
4. User approves changes
5. After rebuild: Calls /docker/compare-sizes
   - Before: 842MB
   - After: 512MB
   - Reduction: 39.2%
6. Reports: "Build time reduced by 45%, image size by 39%"
```

### Workflow 3: Pre-Production Security Check

```
CHECKPOINT: Before deploying to production

Agent Security Audit:
1. Calls /docker/security-scan → Finds issues
2. Reports:
   - ❌ Running as root
   - ❌ No health check defined
   - ⚠️  Large image size
3. Blocks deployment
4. Suggests fixes with exact code
5. After fixes: Re-scans
6. Security score: 85/100
7. Approves deployment
```

---

## 🛠️ Implementation Files

1. **`docker-skills.json`** - AgentSkills manifest
   - Defines all 8 capabilities
   - Specifies parameters and risk levels
   - Documents workflow patterns

2. **`docker_skills.py`** - Python implementation
   - Actual skill implementations
   - Error pattern matching
   - Docker CLI integrations

3. **`docker-pilot-instructions.md`** - Agent prompts
   - Workflow protocols
   - Best practices
   - Example scenarios

4. **`phase2/backend/main.py`** - MCP endpoints
   - HTTP API for all skills
   - Request/response handling

---

## 🎯 Success Metrics

The Docker-Architect Agent tracks:

| Metric | Target | Impact |
|--------|--------|--------|
| Build Time | < 5 min | Faster iterations |
| Image Size | < 500MB | Faster deployments |
| Cache Hit Rate | > 80% | Faster rebuilds |
| Security Score | > 80/100 | Production-ready |
| Layer Count | < 15 | Optimized |

---

## 📚 Best Practices Enforced

The agent automatically enforces:

✅ **Multi-stage builds** (deps → builder → runner)  
✅ **`.dockerignore`** exists and is complete  
✅ **No secrets** in image layers  
✅ **Specific image tags** (not `latest`)  
✅ **Non-root user** in production  
✅ **Explicit Prisma generation** (if applicable)  
✅ **Retry logic** for npm install  
✅ **Layer ordering** for cache efficiency  
✅ **Health checks** defined  
✅ **Resource limits** considered  

---

## 🚀 Getting Started

### 1. Start the Backend
```bash
cd phase2/backend
python main.py
```

### 2. Test Docker Skills
```bash
# List available skills
curl http://localhost:8000/docker/skills

# Analyze a container
curl -X POST http://localhost:8000/docker/analyze-stats \
  -H "Content-Type: application/json" \
  -d '{"container_name": "frontend"}'

# Verify Prisma binary
curl -X POST http://localhost:8000/docker/verify-prisma \
  -H "Content-Type: application/json" \
  -d '{"container_name": "backend"}'
```

### 3. Load Agent Instructions
Use `docker-pilot-instructions.md` as Antigravity custom instructions.

---

## 🔄 Integration with Existing Tools

The Docker-Architect works alongside:
- **Kubernetes Tools** (k8s_cluster_status, scale_deployment, etc.)
- **Helm Management** (install, upgrade, rollback)
- **Database Tools** (check_pvc_storage, db_query_stats)

Together, they form a **complete autonomous infrastructure management system**.

---

## 📖 Common Issue Patterns

| Error | Pattern | Auto-Fix |
|-------|---------|----------|
| Network Timeout | `ETIMEDOUT` | Add npm retry config |
| Prisma Missing | `PrismaClientInitializationError` | Add binaryTargets |
| Font Download | `Failed to fetch...Google Fonts` | Comment out or mock |
| Disk Full | `ENOSPC` | Suggest docker system prune |
| Permission | `Permission denied` | Add non-root user |

---

## 🎓 Learning Mode

The agent learns from every build:
- **Error encountered** → Pattern recognized → Fix suggested
- **Optimization applied** → Impact measured → Best practice updated
- **Security issue found** → Blocked → User educated

**Result**: Every build makes the system smarter.

---

## 📞 Support

- **Docker Skills**: See this README
- **Agent Instructions**: `docker-pilot-instructions.md`
- **MCP Endpoints**: `/docker/skills` endpoint
- **Examples**: See workflow examples above

---

**Version**: 1.0.0  
**Protocol**: MCP (Model Context Protocol)  
**Agent**: Docker-Architect  
**Status**: Fully Operational  
**Last Updated**: 2025-12-26

---

**Transform your Docker builds from manual packaging to autonomous optimization.**  
🐳 → 🤖
