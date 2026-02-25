# Phase 4 Deployment Scripts

This directory contains automated scripts for building, deploying, and managing the Evolution of Todo application in Kubernetes.

---

## 📁 Script Inventory

### 1. **`1-build-images.ps1`** / **`1-build-images.sh`**
**Purpose**: Autonomous Docker build with Prisma verification

**What it does**:
- ✅ Auto-detects and fixes missing Prisma binary targets
- ✅ Builds frontend and backend Docker images
- ✅ Loads images into Minikube registry
- ✅ Verifies successful injection

**Usage**:
```powershell
# PowerShell (Windows)
cd phase4/scripts
.\1-build-images.ps1

# Bash (Linux/Mac)
chmod +x 1-build-images.sh
./1-build-images.sh
```

**When to use**:
- First time setup
- After Dockerfile changes
- After Prisma schema changes
- When experiencing ImagePullBackOff errors

---

### 2. **`2-start-minikube.ps1`** / **`2-start-minikube.sh`**
**Purpose**: AIOps cluster initialization with full observability

**What it does**:
- ✅ Starts Minikube with optimized resources (4 CPUs, 4GB RAM)
- ✅ Enables Ingress (Nginx) for HTTP routing
- ✅ Enables Metrics Server for resource monitoring
- ✅ Enables Dashboard for visual management
- ✅ Sets kubectl context
- ✅ Verifies all addons are running

**Usage**:
```powershell
# PowerShell (Windows)
cd phase4/scripts
.\2-start-minikube.ps1

# Bash (Linux/Mac)
chmod +x 2-start-minikube.sh
./2-start-minikube.sh
```

**When to use**:
- First time setup (before building images)
- After deleting Minikube cluster
- When addons are disabled
- Setting up new development environment

---

### 3. **`verify-build.ps1`**
**Purpose**: Automated quality checks after build

**What it checks**:
- ✅ Image sizes (< 500MB frontend, < 300MB backend)
- ✅ Prisma binary presence (linux-musl-openssl-3.0.x)
- ✅ Backend health endpoint connectivity
- ✅ Minikube registry availability
- ✅ Basic security (non-root user, no secrets)

**Usage**:
```powershell
cd phase4/scripts
.\verify-build.ps1
```

**When to use**:
- After `1-build-images.ps1`
- Before deploying to Kubernetes
- Pre-production verification

---

### 3. **`deploy-minikube.ps1`**
**Purpose**: Full stack deployment using raw kubectl

**What it does**:
- ✅ Starts Minikube
- ✅ Builds images
- ✅ Deploys infrastructure (namespace, ConfigMap, secrets)
- ✅ Deploys database (PostgreSQL StatefulSet)
- ✅ Deploys application (frontend + backend)
- ✅ Initializes database schema

**Usage**:
```powershell
cd phase4/scripts
.\deploy-minikube.ps1
```

**When to use**:
- Learning kubectl commands
- Debugging deployment issues
- When Helm is not available

---

### 4. **`deploy-helm.ps1`** ⭐ **RECOMMENDED**
**Purpose**: Production-grade deployment using Helm

**What it does**:
- ✅ Everything in `deploy-minikube.ps1`
- ✅ Uses Helm for version control
- ✅ Enables easy upgrades and rollbacks
- ✅ Single command deployment

**Usage**:
```powershell
cd phase4/scripts
.\deploy-helm.ps1
```

**When to use**:
- Production deployments
- When you need rollback capability
- Managing multiple environments

---

## 🚀 Quick Start Workflows

### Workflow 1: First Time Setup (Recommended)

```powershell
# 1. Initialize cluster
cd phase4/scripts
.\2-start-minikube.ps1

# 2. Build images
.\1-build-images.ps1

# 3. Verify build
.\verify-build.ps1

# 4. Deploy with Helm
.\deploy-helm.ps1

# 5. Access application
minikube service frontend-service -n todo-chatbot
```

---

### Workflow 2: After Code Changes

```powershell
# 1. Rebuild images
.\1-build-images.ps1

# 2. Upgrade deployment
helm upgrade evolution-todo ..\helm\todo-chatbot -n todo-chatbot
```

---

### Workflow 3: Debugging Build Issues

```powershell
# 1. Build with verbose output
docker build --progress=plain -t todo-frontend:v1 -f ..\docker\frontend.Dockerfile ..\..

# 2. Check build log for errors

# 3. Fix issue (e.g., Prisma schema)

# 4. Rebuild
.\1-build-images.ps1

# 5. Verify
.\verify-build.ps1
```

---

### Workflow 4: Rollback After Failed Deploy

```powershell
# 1. Check history
helm history evolution-todo -n todo-chatbot

# 2. Rollback to previous version
helm rollback evolution-todo -n todo-chatbot

# 3. Verify pods
kubectl get pods -n todo-chatbot
```

---

## 🧠 Agent Integration

These scripts are designed to work with the Antigravity Agent:

### Agent: "Deploy the application"
```
Agent workflow:
1. Calls: 1-build-images.ps1
2. Waits for completion
3. Calls: verify-build.ps1
4. If checks pass → Calls: deploy-helm.ps1
5. Monitors: kubectl get pods -n todo-chatbot -w
6. Reports: "✅ Application deployed and healthy"
```

### Agent: "Fix ImagePullBackOff"
```
Agent workflow:
1. Detects: ImagePullBackOff in pod status
2. Analyzes: Missing image in Minikube registry
3. Calls: 1-build-images.ps1 (rebuilds and loads)
4. Calls: kubectl rollout restart deployment/<name>
5. Verifies: Pods Running
6. Reports: "✅ Issue resolved, pods running"
```

### Agent: "Optimize image size"
```
Agent workflow:
1. Calls: verify-build.ps1
2. Detects: Frontend 842MB (too large)
3. Analyzes: /docker/analyze-layers
4. Suggests: Multi-stage build optimization
5. User approves changes
6. Calls: 1-build-images.ps1 (rebuild)
7. Calls: /docker/compare-sizes
8. Reports: "✅ Size reduced from 842MB to 512MB (39%)"
```

---

## 🔍 Troubleshooting

### Problem: "Minikube not found"
```powershell
# Install Minikube
choco install minikube

# Or download from: https://minikube.sigs.k8s.io/docs/start/
```

### Problem: "Docker daemon not running"
```powershell
# Start Docker Desktop
# Ensure it's fully started (green icon in system tray)
```

### Problem: "Prisma binary missing"
```powershell
# The build script should fix this automatically
# If not, manually add to schema.prisma:
binaryTargets = ["native", "linux-musl-openssl-3.0.x"]

# Then rebuild
.\1-build-images.ps1
```

### Problem: "Port 8000 or 3000 already in use"
```powershell
# Find and kill the process
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process
```

### Problem: "Helm not found"
```powershell
# Install Helm
choco install kubernetes-helm

# Or use deploy-minikube.ps1 instead (uses kubectl)
```

---

## 📊 Script Dependencies

```
1-build-images.ps1
    ├── Requires: Docker Desktop running
    ├── Requires: Minikube installed
    └── Outputs: Images in Minikube registry

verify-build.ps1
    ├── Requires: Images built by 1-build-images.ps1
    └── Outputs: Checklist results

deploy-minikube.ps1
    ├── Requires: 1-build-images.ps1 completed
    ├── Uses: kubectl
    └── Outputs: Running K8s cluster

deploy-helm.ps1 ⭐
    ├── Requires: 1-build-images.ps1 completed
    ├── Requires: Helm installed
    └── Outputs: Helm release
```

---

## 🎯 Best Practices

1. **Always run verify-build.ps1** after building images
2. **Use Helm for deployments** (deploy-helm.ps1) in production
3. **Keep images versioned** (v1, v2, v3, not :latest)
4. **Monitor build times** - should be < 5 minutes
5. **Check image sizes** - optimize if > 500MB

---

## 📚 Related Documentation

- **Docker Skills**: `../agent/docker-README.md`
- **Helm Guide**: `../helm/README.md`
- **K8s Guide**: `../k8s/README.md`
- **kubectl Cheat Sheet**: `../docs/kubectl-cheatsheet.md`

---

## 🔄 Script Execution Order

For first-time deployment:

```
1. 1-build-images.ps1      # Build and load images
   ↓
2. verify-build.ps1        # Verify build quality
   ↓
3. deploy-helm.ps1         # Deploy with Helm ⭐
   OR
   deploy-minikube.ps1     # Deploy with kubectl
```

For updates:

```
1. 1-build-images.ps1      # Rebuild with changes
   ↓
2. helm upgrade ...        # Update deployment
```

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-26  
**Status**: Production Ready
