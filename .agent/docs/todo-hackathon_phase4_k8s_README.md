# Kubernetes Deployment for Evolution of Todo - Phase 4

This directory contains all Kubernetes manifests for deploying the todo-chatbot application to a local Minikube cluster.

## 📁 Manifest Files

### 1. `infrastructure.yaml`
**Purpose**: Foundation layer with namespace and configuration

**Contains**:
- **Namespace**: `todo-chatbot` - Isolated environment
- **ConfigMap**: `todo-config` - Non-sensitive environment variables
  - Frontend/Backend service URLs
  - Database connection strings
  - Environment settings

**Deploy**:
```bash
kubectl apply -f infrastructure.yaml
```

### 2. `secrets.yaml`
**Purpose**: Secure storage for sensitive data

**Contains**:
- **Secret**: `todo-secrets` - Base64-encoded secrets
  - `BETTER_AUTH_SECRET` - JWT signing key
  - `GEMINI_API_KEY` - AI service API key
  - `OPENROUTER_API_KEY` - Alternative AI provider

**Helper**: Includes `secrets-helper` ConfigMap with encoding/decoding commands

**🔐 Generating Your Own Secrets**:

PowerShell:
```powershell
# Encode
$secret = "your-secret-here"
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($secret))

# Decode (verification)
$encoded = "ZGV2X3NlY3JldF9rZXk="
[System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($encoded))
```

Linux/Mac:
```bash
# Encode
echo -n "your-secret-here" | base64

# Decode
echo "ZGV2X3NlY3JldF9rZXk=" | base64 --decode
```

### 3. `database.yaml`
**Purpose**: Persistent PostgreSQL database with StatefulSet

**Contains**:
- **PVC**: `postgres-pvc` - 1Gi persistent storage
- **Service**: `db-service` - Headless service for StatefulSet
- **StatefulSet**: `postgres` - PostgreSQL 15 Alpine
  - Health probes (liveness + readiness)
  - Resource limits (256Mi-512Mi memory)
  - Persistent volume mount

**Why StatefulSet?**:
- ✅ Stable network identity (`postgres-0`)
- ✅ Persistent storage survives pod restarts
- ✅ Ordered deployment and scaling

**Deploy**:
```bash
kubectl apply -f database.yaml
kubectl wait --for=condition=ready pod -l app=postgres -n todo-chatbot --timeout=120s
```

## 🚀 Quick Start

### Option 1: Automated Deployment (Recommended)
Run the PowerShell deployment script:

```powershell
cd phase4/scripts
.\deploy-minikube.ps1
```

This script will:
1. ✅ Start Minikube with optimal resources
2. ✅ Configure Docker to use Minikube registry
3. ✅ Build frontend and backend images
4. ✅ Deploy infrastructure, secrets, and database
5. ✅ Initialize database schema with Prisma

### Option 2: Manual Deployment

#### Step 1: Start Minikube
```powershell
minikube start --cpus=4 --memory=4096 --driver=docker
```

#### Step 2: Configure Docker
```powershell
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

#### Step 3: Build Images
```powershell
docker build -t todo-frontend:v1 -f phase4/docker/frontend.Dockerfile .
docker build -t todo-backend:v1 -f phase4/docker/backend.Dockerfile .
```

#### Step 4: Deploy Infrastructure
```powershell
kubectl apply -f phase4/k8s/infrastructure.yaml
kubectl apply -f phase4/k8s/secrets.yaml
kubectl apply -f phase4/k8s/database.yaml
```

#### Step 5: Initialize Database
```powershell
# Port-forward to database
kubectl port-forward pod/postgres-0 5432:5432 -n todo-chatbot

# In another terminal
cd phase2/frontend
npx prisma db push
```

## 📊 Verifying Deployment

### Check All Resources
```bash
kubectl get all -n todo-chatbot
```

### Check Specific Components
```bash
# Namespace
kubectl get ns | grep todo-chatbot

# ConfigMaps and Secrets
kubectl get configmap,secret -n todo-chatbot

# Pods and StatefulSets
kubectl get pods,statefulsets -n todo-chatbot

# Persistent Storage
kubectl get pvc -n todo-chatbot

# Services
kubectl get svc -n todo-chatbot
```

### View Logs
```bash
# Database logs
kubectl logs -f postgres-0 -n todo-chatbot

# All pod logs
kubectl logs -f <pod-name> -n todo-chatbot
```

## 🔧 Troubleshooting

### Database Not Ready
```bash
# Check pod status
kubectl describe pod postgres-0 -n todo-chatbot

# Check PVC binding
kubectl get pvc -n todo-chatbot

# Check events
kubectl get events -n todo-chatbot --sort-by='.lastTimestamp'
```

### Image Pull Issues
```bash
# Verify images are in Minikube registry
eval $(minikube docker-env)
docker images | grep todo-
```

### Connection Issues
```bash
# Test database connectivity
kubectl run -it --rm debug --image=postgres:15-alpine --restart=Never -n todo-chatbot -- \
  psql -h db-service -U postgres -d tododb -c "SELECT version();"
```

## 🎯 Next Steps

1. **Deploy Application Services** (frontend & backend Deployments)
2. **Configure Ingress** for external access
3. **Enable MCP Endpoints** for agent integration
4. **Set up Monitoring** with Prometheus/Grafana (optional)

## 📚 Architecture

```
todo-chatbot Namespace
├── ConfigMap (todo-config)
│   └── Environment variables
├── Secret (todo-secrets)
│   └── Sensitive credentials
└── PostgreSQL StatefulSet
    ├── PersistentVolumeClaim (1Gi)
    ├── Headless Service (db-service)
    └── Pod (postgres-0)
        └── Volume Mount → PVC
```

## 🔐 Security Notes

⚠️ **Default secrets are for DEVELOPMENT ONLY**

Before deploying to production:
1. Generate strong, random secrets
2. Use Kubernetes Secrets encryption at rest
3. Consider external secret management (HashiCorp Vault, AWS Secrets Manager)
4. Rotate secrets regularly

## 📖 References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Minikube](https://minikube.sigs.k8s.io/docs/)

---

**Version**: 1.0.0  
**Namespace**: todo-chatbot  
**Last Updated**: 2025-12-26
