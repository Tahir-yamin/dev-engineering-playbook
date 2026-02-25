# Quick Command Reference - Kubernetes Management

## 🚀 Deployment Commands

### Initial Deployment
```powershell
# Automated (Recommended)
cd phase4/scripts
.\deploy-minikube.ps1

# Manual
kubectl apply -f phase4/k8s/infrastructure.yaml
kubectl apply -f phase4/k8s/secrets.yaml
kubectl apply -f phase4/k8s/database.yaml
kubectl apply -f phase4/k8s/app-deployments.yaml
```

### Access Application
```powershell
# Get URL
minikube service frontend-service -n todo-chatbot --url

# Or use NodePort
$minikubeIP = minikube ip
# Access: http://$minikubeIP:30000
```

## 📊 Monitoring Commands

### View All Resources
```bash
kubectl get all -n todo-chatbot
```

### Check Pods
```bash
# List all pods
kubectl get pods -n todo-chatbot

# Watch pods (auto-refresh)
kubectl get pods -n todo-chatbot -w

# Detailed pod info
kubectl describe pod <pod-name> -n todo-chatbot
```

### Check Deployments
```bash
kubectl get deployments -n todo-chatbot
kubectl describe deployment <deployment-name> -n todo-chatbot
```

### Check Services
```bash
kubectl get svc -n todo-chatbot
kubectl describe svc <service-name> -n todo-chatbot
```

### Check Storage
```bash
kubectl get pvc -n todo-chatbot
kubectl describe pvc postgres-pvc -n todo-chatbot
```

## 🔍 Debugging Commands

### View Logs
```bash
# Tail logs (live)
kubectl logs -f <pod-name> -n todo-chatbot

# Last 50 lines
kubectl logs --tail=50 <pod-name> -n todo-chatbot

# All containers in a pod
kubectl logs <pod-name> --all-containers -n todo-chatbot
```

### Execute Commands in Pod
```bash
# Interactive shell
kubectl exec -it <pod-name> -n todo-chatbot -- /bin/sh

# Single command
kubectl exec <pod-name> -n todo-chatbot -- <command>

# Example: Check database
kubectl exec postgres-0 -n todo-chatbot -- psql -U postgres -d tododb -c "SELECT version();"
```

### Port Forwarding
```bash
# Forward database port
kubectl port-forward pod/postgres-0 5432:5432 -n todo-chatbot

# Forward backend port
kubectl port-forward svc/backend-service 8000:8000 -n todo-chatbot

# Forward frontend port
kubectl port-forward svc/frontend-service 3000:3000 -n todo-chatbot
```

### View Events
```bash
# Recent events
kubectl get events -n todo-chatbot --sort-by='.lastTimestamp'

# Watch events
kubectl get events -n todo-chatbot -w
```

## ⚙️ Management Commands

### Scale Deployments
```bash
# Scale frontend
kubectl scale deployment frontend-deployment --replicas=3 -n todo-chatbot

# Scale backend
kubectl scale deployment backend-deployment --replicas=2 -n todo-chatbot
```

### Restart Deployments
```bash
# Rolling restart frontend
kubectl rollout restart deployment/frontend-deployment -n todo-chatbot

# Rolling restart backend
kubectl rollout restart deployment/backend-deployment -n todo-chatbot

# Restart database (use with caution)
kubectl rollout restart statefulset/postgres -n todo-chatbot
```

### Check Rollout Status
```bash
kubectl rollout status deployment/frontend-deployment -n todo-chatbot
kubectl rollout status deployment/backend-deployment -n todo-chatbot
```

### Rollback Deployment
```bash
# View rollout history
kubectl rollout history deployment/frontend-deployment -n todo-chatbot

# Rollback to previous version
kubectl rollout undo deployment/frontend-deployment -n todo-chatbot

# Rollback to specific revision
kubectl rollout undo deployment/frontend-deployment --to-revision=2 -n todo-chatbot
```

## 🔧 Configuration Management

### View ConfigMap
```bash
kubectl get configmap todo-config -n todo-chatbot -o yaml
```

### View Secrets (encoded)
```bash
kubectl get secret todo-secrets -n todo-chatbot -o yaml
```

### Decode Secret
```powershell
# PowerShell
$encoded = kubectl get secret todo-secrets -n todo-chatbot -o jsonpath='{.data.BETTER_AUTH_SECRET}'
[System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($encoded))
```

```bash
# Linux/Mac
kubectl get secret todo-secrets -n todo-chatbot -o jsonpath='{.data.BETTER_AUTH_SECRET}' | base64 --decode
```

### Update ConfigMap
```bash
kubectl edit configmap todo-config -n todo-chatbot
# After saving, restart deployments to pick up changes
```

## 🗑️ Cleanup Commands

### Delete Specific Resources
```bash
# Delete application
kubectl delete -f phase4/k8s/app-deployments.yaml

# Delete database
kubectl delete -f phase4/k8s/database.yaml

# Delete infrastructure
kubectl delete -f phase4/k8s/infrastructure.yaml
kubectl delete -f phase4/k8s/secrets.yaml
```

### Delete Entire Namespace
```bash
# ⚠️ WARNING: This deletes EVERYTHING in the namespace
kubectl delete namespace todo-chatbot
```

### Reset Minikube
```powershell
# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete

# Start fresh
minikube start --cpus=4 --memory=4096 --driver=docker
```

## 📈 Resource Usage

### Check Node Resources
```bash
kubectl top nodes
```

### Check Pod Resources
```bash
kubectl top pods -n todo-chatbot
```

### Describe Node
```bash
kubectl describe node minikube
```

## 🌐 Network Commands

### Test Service Connectivity
```bash
# From within cluster
kubectl run -it --rm debug --image=busybox --restart=Never -n todo-chatbot -- sh

# Then inside the pod:
wget -qO- http://backend-service:8000/health
wget -qO- http://frontend-service:3000
nslookup backend-service
nslookup db-service
```

### Check Service Endpoints
```bash
kubectl get endpoints -n todo-chatbot
```

## 🎯 Agent Tool Equivalents

| Agent Tool | kubectl Equivalent |
|-----------|-------------------|
| `k8s_cluster_status` | `kubectl get pods -n todo-chatbot -o json` |
| `scale_deployment` | `kubectl scale deployment/<name> --replicas=N` |
| `restart_deployment` | `kubectl rollout restart deployment/<name>` |
| `analyze_pod_logs` | `kubectl logs <pod-name> --tail=N` |
| `get_service_endpoints` | `kubectl get svc -n todo-chatbot -o json` |
| `check_pvc_storage` | `kubectl get pvc -n todo-chatbot -o json` |

## 🔄 Common Workflows

### Deploy New Version
```bash
# 1. Build new image
docker build -t todo-frontend:v2 -f phase4/docker/frontend.Dockerfile .

# 2. Update deployment
kubectl set image deployment/frontend-deployment frontend=todo-frontend:v2 -n todo-chatbot

# 3. Watch rollout
kubectl rollout status deployment/frontend-deployment -n todo-chatbot
```

### Debug Crash Loop
```bash
# 1. Check pod status
kubectl get pods -n todo-chatbot

# 2. View logs
kubectl logs --previous <crashed-pod-name> -n todo-chatbot

# 3. Describe pod for events
kubectl describe pod <crashed-pod-name> -n todo-chatbot

# 4. Check recent events
kubectl get events -n todo-chatbot --sort-by='.lastTimestamp' | head -20
```

### Backup Database
```bash
# 1. Port-forward to database
kubectl port-forward pod/postgres-0 5432:5432 -n todo-chatbot &

# 2. Create backup
pg_dump -h localhost -U postgres -d tododb > backup.sql

# 3. Stop port-forward
fg  # Bring to foreground
Ctrl+C  # Stop
```

---

**Quick Access**:
- Dashboard: `minikube dashboard`
- Frontend: `minikube service frontend-service -n todo-chatbot`
- Stop: `minikube stop`
- Start: `minikube start`
