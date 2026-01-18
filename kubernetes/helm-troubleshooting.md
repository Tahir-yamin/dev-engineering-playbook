# Helm Deployment Fix - Quick Commands

**Issue**: `spec.selector: Invalid value: field is immutable`  
**Cause**: Kubernetes won't let you change selector labels on existing Deployments

---

## 🔧 Fix Steps

### Step 1: Connect to AKS

```powershell
az aks get-credentials --resource-group myResourceGroup --name todo-aks-cluster --overwrite-existing
```

### Step 2: Delete Old Deployments

```powershell
# Delete deployments with old selectors
kubectl delete deployment todo-chatbot-backend -n todo-chatbot
kubectl delete deployment todo-chatbot-frontend -n todo-chatbot
kubectl delete deployment todo-chatbot-notification-service -n todo-chatbot

# Verify deletion
kubectl get deployments -n todo-chatbot
```

### Step 3: Re-trigger GitHub Action

**Option A: Via GitHub UI**
1. Go to: https://github.com/Tahir-yamin/todo_hackathon_phase2/actions
2. Click latest failed workflow
3. Click "Re-run failed jobs"

**Option B: Push empty commit**
```powershell
git commit --allow-empty -m "ci: retrigger deployment after fixing selectors"
git push origin main
```

---

## ✅ Verification

After redeployment:
```powershell
# Check pod status
kubectl get pods -n todo-chatbot

# Check deployment status
kubectl get deployments -n todo-chatbot

# Check services
kubectl get svc -n todo-chatbot
```

Expected output:
```
NAME                        READY   STATUS    RESTARTS
todo-chatbot-backend-xxx    1/1     Running   0
todo-chatbot-frontend-xxx   1/1     Running   0
```

---

## 🚨 If Namespace Doesn't Exist

```powershell
kubectl create namespace todo-chatbot
```

---

**Time**: ~5 minutes  
**Risk**: Low (just recreating deployments)
