# Manual Operations Guide for Judges

**Purpose**: This guide provides step-by-step instructions for judges to manually build, deploy, and operate the TODO Hackathon application using Docker and Kubernetes.

**Last Updated**: 2025-12-30  
**Target Audience**: Hackathon judges, evaluators, technical reviewers

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Docker Manual Operations](#docker-manual-operations)
3. [Kubernetes Manual Operations](#kubernetes-manual-operations)
4. [Common Operations](#common-operations)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Docker Desktop**: Version 4.x or higher (with Kubernetes enabled)
- **kubectl**: Version 1.28.x or higher
- **Helm** (Optional): Version 3.x
- **Git**: For cloning the repository
- **PowerShell** (Windows) or Bash (Linux/Mac)

### Verify Installation

```powershell
# Check Docker
docker --version
docker ps

# Check Kubernetes
kubectl version --client
kubectl cluster-info

# Check Helm (optional)
helm version
```

---

## Part 1: Docker Manual Operations

### 1.1 Build Docker Images Manually

#### Navigate to Project Directory
```powershell
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1"
```

#### Build Backend Image
```powershell
# Build from phase4 directory
docker build -t todo-backend:v1 `
  -f phase4/docker/backend.Dockerfile `
  phase2/backend

# Verify build
docker images | Select-String "todo-backend"
```

**Expected Output**: Image size ~200-300MB

#### Build Frontend Image
```powershell
# Build frontend with required build arguments
docker build -t todo-frontend:v2 `
  -f phase4/docker/frontend.Dockerfile `
  --build-arg NEXT_PUBLIC_API_URL=http://localhost:30001 `
  --build-arg BETTER_AUTH_URL=http://localhost:30000 `
  --build-arg NEXT_PUBLIC_APP_URL=http://localhost:30000 `
  phase2/frontend

# Verify build
docker images | Select-String "todo-frontend"
```

**Expected Output**: Image size ~400-600MB

**Build Time**: 5-15 minutes depending on your system

---

### 1.2 Run Containers Locally (Docker Only)

#### Step 1: Create Docker Network
```powershell
docker network create todo-network
```

#### Step 2: Run Backend Container
```powershell
docker run -d `
  --name todo-backend `
  --network todo-network `
  -p 8000:8000 `
  -e DATABASE_URL="postgresql://neondb_owner:npg_LDWBY2FaORu5@ep-curly-dust-ahteg33k-pooler.us-east-1.aws.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require" `
  -e OPENROUTER_API_KEY="your_key_here" `
  -e GEMINI_API_KEY="your_key_here" `
  todo-backend:v1
```

#### Step 3: Run Frontend Container
```powershell
docker run -d `
  --name todo-frontend `
  --network todo-network `
  -p 3000:3000 `
  -e DATABASE_URL="postgresql://neondb_owner:npg_LDWBY2FaORu5@ep-curly-dust-ahteg33k-pooler.us-east-1.aws.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require" `
  -e BETTER_AUTH_SECRET="your_secret_here" `
  todo-frontend:v2
```

#### Step 4: Verify Containers are Running
```powershell
docker ps
```

**Expected**: 2 containers running (todo-backend, todo-frontend)

#### Step 5: Access Application
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000/health`

---

### 1.3 Docker Container Management

#### View Logs
```powershell
# Backend logs
docker logs todo-backend

# Frontend logs
docker logs todo-frontend

# Follow logs (real-time)
docker logs -f todo-backend
```

#### Stop Containers
```powershell
docker stop todo-backend todo-frontend
```

#### Start Containers
```powershell
docker start todo-backend todo-frontend
```

#### Remove Containers
```powershell
docker rm -f todo-backend todo-frontend
docker network rm todo-network
```

#### Inspect Container
```powershell
# View container details
docker inspect todo-backend

# View environment variables
docker exec todo-backend env
```

---

## Part 2: Kubernetes Manual Operations

### 2.1 Enable Kubernetes in Docker Desktop

1. Open **Docker Desktop**
2. Go to **Settings** → **Kubernetes**
3. Check **Enable Kubernetes**
4. Click **Apply & Restart**
5. Wait for Kubernetes to start (green icon in bottom-left)

#### Verify Kubernetes is Running
```powershell
kubectl get nodes
```

**Expected**: 1 node in **Ready** status (docker-desktop)

---

### 2.2 Deploy to Kubernetes Manually (Method 1: kubectl)

#### Step 1: Create Namespace
```powershell
kubectl create namespace todo-chatbot
```

#### Step 2: Create ConfigMap
```powershell
# Create a file: phase4/k8s/configmap.yaml
kubectl create configmap todo-app-config -n todo-chatbot `
  --from-literal=DATABASE_URL="postgresql://neondb_owner:npg_LDWBY2FaORu5@ep-curly-dust-ahteg33k-pooler.us-east-1.aws.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require" `
  --from-literal=BETTER_AUTH_URL="http://localhost:30000" `
  --from-literal=NEXT_PUBLIC_API_URL="http://localhost:30001" `
  --from-literal=NODE_ENV="production"
```

#### Step 3: Create Secrets
```powershell
kubectl create secret generic todo-app-secrets -n todo-chatbot `
  --from-literal=BETTER_AUTH_SECRET="your_secret_here" `
  --from-literal=OPENROUTER_API_KEY="your_key_here" `
  --from-literal=GEMINI_API_KEY="your_key_here" `
  --from-literal=GITHUB_CLIENT_ID="your_id_here" `
  --from-literal=GITHUB_CLIENT_SECRET="your_secret_here" `
  --from-literal=GOOGLE_CLIENT_ID="your_id_here" `
  --from-literal=GOOGLE_CLIENT_SECRET="your_secret_here" `
  --from-literal=RESEND_API_KEY="your_key_here"
```

#### Step 4: Load Images to Kubernetes
```powershell
# Docker Desktop automatically shares images with Kubernetes
# Verify images are available
kubectl run test-image --image=todo-backend:v1 --dry-run=client -o yaml
```

#### Step 5: Deploy Backend
```powershell
kubectl create deployment todo-app-backend -n todo-chatbot `
  --image=todo-backend:v1
  
# Set image pull policy to Never (local image)
kubectl patch deployment todo-app-backend -n todo-chatbot `
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"todo-backend","imagePullPolicy":"Never"}]}}}}'

# Add environment variables from ConfigMap
kubectl set env deployment/todo-app-backend -n todo-chatbot `
  --from configmap/todo-app-config

# Add environment variables from Secret
kubectl set env deployment/todo-app-backend -n todo-chatbot `
  --from secret/todo-app-secrets

# Expose as NodePort
kubectl expose deployment todo-app-backend -n todo-chatbot `
  --type=NodePort --port=8000 --target-port=8000 --name=backend-service

# Set specific NodePort
kubectl patch service backend-service -n todo-chatbot `
  -p '{"spec":{"ports":[{"port":8000,"nodePort":30001}]}}'
```

#### Step 6: Deploy Frontend
```powershell
kubectl create deployment todo-app-frontend -n todo-chatbot `
  --image=todo-frontend:v2 --replicas=2

# Set image pull policy
kubectl patch deployment todo-app-frontend -n todo-chatbot `
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"todo-frontend","imagePullPolicy":"Never"}]}}}}'

# Add environment variables
kubectl set env deployment/todo-app-frontend -n todo-chatbot `
  --from configmap/todo-app-config

kubectl set env deployment/todo-app-frontend -n todo-chatbot `
  --from secret/todo-app-secrets

# Expose as NodePort
kubectl expose deployment todo-app-frontend -n todo-chatbot `
  --type=NodePort --port=3000 --target-port=3000 --name=frontend-service

# Set specific NodePort
kubectl patch service frontend-service -n todo-chatbot `
  -p '{"spec":{"ports":[{"port":3000,"nodePort":30000}]}}'
```

#### Step 7: Verify Deployment
```powershell
kubectl get all -n todo-chatbot
kubectl get pods -n todo-chatbot
```

**Expected**: All pods in **Running** status

#### Step 8: Access Application
- Frontend: `http://localhost:30000`
- Backend API: `http://localhost:30001/health`

---

### 2.3 Deploy to Kubernetes Using Helm (Method 2: Recommended)

#### Step 1: Navigate to Helm Chart Directory
```powershell
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase4"
```

#### Step 2: Update values.yaml
Edit `helm/todo-chatbot/values.yaml` and update:
- Image tags
- Database URL
- API keys (or use existing ones)

#### Step 3: Install Helm Chart
```powershell
helm install todo-chatbot helm/todo-chatbot -n todo-chatbot --create-namespace
```

#### Step 4: Verify Installation
```powershell
helm list -n todo-chatbot
kubectl get all -n todo-chatbot
```

#### Step 5: Access Application
```powershell
# Get NodePort URLs
kubectl get service -n todo-chatbot
```

---

### 2.4 Kubernetes Management Operations

#### View Pod Status
```powershell
kubectl get pods -n todo-chatbot
```

#### View Pod Logs
```powershell
# List pods first
kubectl get pods -n todo-chatbot

# View logs (replace <pod-name> with actual pod name)
kubectl logs <pod-name> -n todo-chatbot

# Follow logs
kubectl logs -f <pod-name> -n todo-chatbot
```

#### Execute Commands in Pod
```powershell
# Interactive shell
kubectl exec -it <pod-name> -n todo-chatbot -- /bin/sh

# Run single command
kubectl exec <pod-name> -n todo-chatbot -- env
```

#### Scale Deployment
```powershell
# Scale frontend to 3 replicas
kubectl scale deployment todo-app-frontend -n todo-chatbot --replicas=3
```

#### Restart Deployment
```powershell
kubectl rollout restart deployment/todo-app-backend -n todo-chatbot
kubectl rollout restart deployment/todo-app-frontend -n todo-chatbot
```

#### View ConfigMap
```powershell
kubectl get configmap todo-app-config -n todo-chatbot -o yaml
```

#### Update ConfigMap
```powershell
kubectl edit configmap todo-app-config -n todo-chatbot
```

#### View Secrets (Base64 Encoded)
```powershell
kubectl get secret todo-app-secrets -n todo-chatbot -o yaml
```

#### Delete Deployment
```powershell
# Delete specific deployment
kubectl delete deployment todo-app-backend -n todo-chatbot

# Delete entire namespace (removes everything)
kubectl delete namespace todo-chatbot
```

#### Delete Helm Release
```powershell
helm uninstall todo-chatbot -n todo-chatbot
```

---

## Part 3: Common Operations

### 3.1 Health Checks

#### Docker
```powershell
# Check backend health
Invoke-WebRequest http://localhost:8000/health

# Check frontend
Invoke-WebRequest http://localhost:3000
```

#### Kubernetes
```powershell
# Check backend health via NodePort
Invoke-WebRequest http://localhost:30001/health

# Check frontend
Invoke-WebRequest http://localhost:30000
```

---

### 3.2 Database Verification

```powershell
# From Kubernetes pod
kubectl exec deployment/todo-app-backend -n todo-chatbot -- python -c "
from sqlmodel import create_engine, Session
import os
engine = create_engine(os.getenv('DATABASE_URL'))
with Session(engine) as session:
    print('Database connection successful!')
"
```

---

### 3.3 Updating Environment Variables

#### Docker
```powershell
# Stop and remove containers
docker stop todo-backend todo-frontend
docker rm todo-backend todo-frontend

# Re-run with new environment variables (see 1.2)
```

#### Kubernetes
```powershell
# Update ConfigMap
kubectl patch configmap todo-app-config -n todo-chatbot \
  -p '{"data":{"NEW_VAR":"new_value"}}'

# Restart deployments to pick up changes
kubectl rollout restart deployment/todo-app-backend -n todo-chatbot
kubectl rollout restart deployment/todo-app-frontend -n todo-chatbot
```

---

## Part 4: Troubleshooting

### Issue 1: Container Won't Start

**Docker Symptoms**:
```powershell
docker ps -a
# STATUS: Exited or Restarting
```

**Solution**:
```powershell
# Check logs
docker logs todo-backend

# Common issues:
# - Missing DATABASE_URL
# - Invalid credentials
# - Port already in use (3000, 8000)
```

---

### Issue 2: Kubernetes Pod CrashLoopBackOff

**Symptoms**:
```powershell
kubectl get pods -n todo-chatbot
# STATUS: CrashLoopBackOff
```

**Solution**:
```powershell
# Check logs
kubectl logs <pod-name> -n todo-chatbot

# Common issues:
# - Missing environment variables
# - Image pull error (set imagePullPolicy: Never)
# - Database connection error
```

---

### Issue 3: Can't Access Application

**Symptoms**: Browser shows "Connection Refused"

**Solution**:
```powershell
# Docker: Check if containers are running
docker ps

# Kubernetes: Check if pods are running
kubectl get pods -n todo-chatbot

# Kubernetes: Check services
kubectl get service -n todo-chatbot

# Verify NodePort is 30000 and 30001
```

---

### Issue 4: Frontend Shows Blank Page

**Solution**:
```powershell
# Check browser console for errors
# Common issue: Wrong NEXT_PUBLIC_API_URL

# For Docker: Rebuild with correct build args
# For Kubernetes: Rebuild frontend image with correct args
```

---

## Part 5: Quick Reference Commands

### Docker Cheat Sheet
```powershell
docker ps                          # List running containers
docker ps -a                       # List all containers
docker images                      # List images
docker logs <container>            # View logs
docker exec -it <container> sh     # Interactive shell
docker stop <container>            # Stop container
docker rm <container>              # Remove container
docker rmi <image>                 # Remove image
```

### Kubernetes Cheat Sheet
```powershell
kubectl get pods -n todo-chatbot               # List pods
kubectl get all -n todo-chatbot                # List all resources
kubectl logs <pod> -n todo-chatbot             # View logs
kubectl exec -it <pod> -n todo-chatbot -- sh   # Interactive shell
kubectl describe pod <pod> -n todo-chatbot     # Detailed pod info
kubectl delete pod <pod> -n todo-chatbot       # Delete pod
kubectl rollout status deployment/<name>       # Check rollout status
kubectl scale deployment <name> --replicas=3   # Scale deployment
```

---

## Part 6: Judge Demonstration Flow

### Recommended Demonstration Order:

1. **Show the code** (5 minutes)
   - Navigate through project structure
   - Highlight key files (Dockerfiles, Helm charts)

2. **Build Docker images** (10 minutes)
   - Build backend and frontend images
   - Explain multi-stage builds

3. **Deploy to Kubernetes** (5 minutes)
   - Use Helm for one-command deployment
   - Show pods starting up

4. **Show live application** (5 minutes)
   - Access frontend at localhost:30000
   - Demonstrate signup, task creation, AI chat

5. **Show operations** (5 minutes)
   - Scale deployment
   - View logs
   - Restart pods

**Total Time**: ~30 minutes

---

## Appendix: Full Deployment Script

For judges who want a quick automated deployment:

```powershell
# phase4/scripts/judge-demo.ps1

# Build images
docker build -t todo-backend:v1 -f phase4/docker/backend.Dockerfile phase2/backend
docker build -t todo-frontend:v2 -f phase4/docker/frontend.Dockerfile --build-arg NEXT_PUBLIC_API_URL=http://localhost:30001 --build-arg BETTER_AUTH_URL=http://localhost:30000 --build-arg NEXT_PUBLIC_APP_URL=http://localhost:30000 phase2/frontend

# Deploy with Helm
helm install todo-chatbot phase4/helm/todo-chatbot -n todo-chatbot --create-namespace

# Wait for pods
kubectl wait --for=condition=ready pod -l tier=frontend -n todo-chatbot --timeout=120s

# Show status
kubectl get all -n todo-chatbot

Write-Host "`nApplication ready at:"
Write-Host "  Frontend: http://localhost:30000"
Write-Host "  Backend:  http://localhost:30001/health"
```

---

**Questions?** Contact the development team or refer to the main `README.md` in phase4/.

**Last Updated**: 2025-12-30
