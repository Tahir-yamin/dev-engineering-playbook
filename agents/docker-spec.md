# DOCKER SPECIFICATION: PHASE 4

This specification follows the `agentskills` and `anthropics/skills` patterns for autonomous Docker build management.

---

## 🎯 Tool: `build_and_load_images`

### Goal
Transform source code into Kubernetes-ready containers with verified binary compatibility.

### Protocol Steps

1. **Binary Compatibility Check**
   - Verifies `schema.prisma` contains `linux-musl-openssl-3.0.x` target
   - **Critical for Alpine compatibility** (prevents PrismaClientInitializationError)
   - Auto-fixes if missing

2. **Multi-Stage Docker Build**
   - Executes optimized builds for frontend and backend
   - Target: Keep images < 500MB (frontend), < 300MB (backend)
   - Uses build cache for faster iterations

3. **Minikube Registry Injection**
   - Transfers images from local Docker to Minikube internal registry
   - Eliminates need for external registry (Docker Hub, etc.)
   - Uses `minikube image load` command

4. **Verification**
   - Checks image sizes
   - Verifies images are available in Minikube
   - Reports success/failure status

---

## 🔄 Recovery Workflows

### Workflow 1: ImagePullBackOff in Kubernetes

**Trigger**: User reports "ImagePullBackOff" error

**Agent Logic**:
```
<thought>
ImagePullBackOff means Kubernetes can't find the image in the registry.
Since we're using Minikube with local images, the image wasn't loaded.
I should rebuild and load the images.
</thought>

1. Call: build_and_load_images
2. Wait for completion
3. Execute: kubectl rollout restart deployment/<deployment-name>
4. Verify: kubectl get pods -w (watch until Running)
```

**Expected Outcome**: Pods start successfully

---

### Workflow 2: PrismaClientInitializationError

**Trigger**: 500 errors with "Query engine library for current platform" error

**Agent Logic**:
```
<thought>
This is the classic Alpine + Prisma binary mismatch.
The build script should detect and fix this automatically.
</thought>

1. Call: build_and_load_images (auto-fixes schema.prisma)
2. Verify: Check docker/verify-prisma endpoint
3. Execute: helm upgrade (or kubectl rollout restart)
4. Verify: Test /health endpoint
```

**Expected Outcome**: Prisma client works in container

---

### Workflow 3: Build Failure (ETIMEDOUT, etc.)

**Trigger**: Docker build fails with network timeout

**Agent Logic**:
```
<thought>
Build failed. I should analyze the error log first.
</thought>

1. Call: /docker/detect-failures with build_log
2. If ETIMEDOUT detected:
   - Suggest adding npm retry configuration
   - Offer to update Dockerfile
3. If Google Fonts timeout:
   - Suggest commenting out font import
4. Retry: build_and_load_images after fix applied
```

**Expected Outcome**: Build succeeds after fix

---

## 📋 Build Script Capabilities

### Autonomous Fixes

The build script (`1-build-images.sh` / `1-build-images.ps1`) automatically:

- ✅ Detects missing `linux-musl-openssl-3.0.x` in schema.prisma
- ✅ Backs up original schema before modifying
- ✅ Injects correct binary targets
- ✅ Generates Prisma client locally for verification
- ✅ Starts Minikube if not running
- ✅ Loads images into Minikube registry
- ✅ Verifies image sizes and availability

### Manual Invocation

```powershell
# Windows (PowerShell)
cd phase4/scripts
.\1-build-images.ps1

# Linux/Mac (Bash)
cd phase4/scripts
chmod +x 1-build-images.sh
./1-build-images.sh
```

---

## 🎯 Success Criteria

After running `build_and_load_images`:

✅ **Frontend Image**:
- Size: < 500MB
- Contains: `/app/node_modules/.prisma/client/libquery_engine-linux-musl-openssl-3.0.x.so.node`
- Health: Can run standalone and serve on port 3000

✅ **Backend Image**:
- Size: < 300MB
- Contains: Valid FastAPI application
- Health: `/health` endpoint returns 200 OK

✅ **Minikube Registry**:
- Images visible with `minikube image ls | grep todo-`
- No "ImagePullBackOff" errors in deployments

---

## 🧠 Agent Decision Tree

```
User Reports Issue
    │
    ├─ "ImagePullBackOff"
    │   └─> build_and_load_images
    │       └─> kubectl rollout restart
    │
    ├─ "PrismaClientInitializationError"
    │   └─> build_and_load_images (auto-fixes schema)
    │       └─> verify_prisma_binary
    │       └─> redeploy
    │
    ├─ "Build fails"
    │   └─> detect_build_failures
    │       └─> suggest_dockerfile_fixes
    │       └─> apply fix
    │       └─> build_and_load_images
    │
    └─ "Slow startup"
        └─> verify images are cached in Minikube
            └─> if not: build_and_load_images
```

---

## 🔐 Security & Best Practices

The build script enforces:

1. **No secrets in images**: Uses ConfigMaps/Secrets in K8s
2. **Multi-stage builds**: Minimizes final image size
3. **Specific tags**: Always uses versioned tags (v1, v2, etc.)
4. **Binary verification**: Ensures Prisma binaries match target OS
5. **Backup before modify**: Creates `.backup` files before auto-fixes

---

## 📊 Integration with Other Tools

### With Evolution Agent (K8s Tools)
```
build_and_load_images
    ↓
k8s_cluster_status (verify deployment)
    ↓
analyze_pod_logs (if issues found)
```

### With Docker-Architect
```
build_and_load_images
    ↓
analyze_image_layers (optimization check)
    ↓
check_security_vulnerabilities (pre-production)
```

### With Helm
```
build_and_load_images
    ↓
helm upgrade --install evolution-todo ./helm/todo-chatbot
```

---

## 🎓 Learning from Builds

After each build, the agent should:

1. **Record image size**: Track size reduction over time
2. **Note build time**: Identify slow builds
3. **Pattern match errors**: Update error database
4. **Suggest optimizations**: Proactively improve Dockerfiles

---

## 📚 References

- **AgentSkills Spec**: https://github.com/anthropics/skills
- **MCP Protocol**: https://modelcontextprotocol.io
- **Docker Best Practices**: https://docs.docker.com/develop/dev-best-practices/
- **Minikube Image Management**: https://minikube.sigs.k8s.io/docs/commands/image/

---

**Version**: 1.0.0  
**Protocol**: AgentSkills + MCP  
**Last Updated**: 2025-12-26
