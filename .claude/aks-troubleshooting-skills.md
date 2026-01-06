# AKS Troubleshooting Skills

**Purpose**: Systematic approaches to diagnose and resolve Azure Kubernetes Service deployment failures  
**Source**: Extracted from Phase 5 AKS Deployment (20 iterations to success)  
**Date**: January 2026

---

## Skill #1: Systematic Deployment Failure Analysis

### When to Use
- AKS deployment failing repeatedly
- GitHub Actions workflow errors
- Need to isolate root cause from symptoms

### The Problem
Complex deployment failures often have multiple symptoms but single root causes. Random troubleshooting wastes time.

### The Solution

**Step 1: Isolate the failing stage**
```bash
# Check GitHub Actions logs - identify which job fails:
# - Build & Push
# - Deploy Infrastructure  
# - Deploy Application
# - Verify Deployment
```

**Step 2: Get detailed error**
```bash
# For Build failures - check Docker build logs
# For Deploy failures - check Helm output
# For Pod failures - check pod describe

kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
```

**Step 3: Work backwards from error**
- Image pull error → Check imagePullPolicy + secrets
- CrashLoopBackOff → Check logs for application error
- Pending → Check resources + node capacity
- ErrImageNeverPull →  imagePullPolicy set to Never

### Key Insights
- ✅ One issue at a time - fix, test, repeat
- ✅ Read FULL error messages, not just first line
- ❌ Don't skip verification steps
- 💡 Each failure teaches something - document it

**Related Skills**: kubernetes-resource-management-skills.md #1, helm-configuration-skills.md #2

---

## Skill #2: Image Pull Debugging

### When to Use
- Pods stuck in `ErrImageNeverPull` status
- Pods stuck in `ImagePullBackOff` status
- Authentication errors pulling from ACR

### The Problem
Kubernetes can't pull Docker images from Azure Container Registry.

### The Solution

**Check 1: Image pull policy**
```yaml
# In Helm values or deployment YAML
imagePullPolicy: IfNotPresent  # NOT "Never" for cloud registries
```

**Check 2: Image pull secrets**
```bash
# Verify secret exists
kubectl get secret acr-secret -n <namespace>

# Create if missing
kubectl create secret docker-registry acr-secret \
  --namespace=<namespace> \
  --docker-server=<ACR_LOGIN_SERVER> \
  --docker-username=<ACR_USERNAME> \
  --docker-password=<ACR_PASSWORD>
```

**Check 3: Deployment references secret**
```yaml
spec:
  imagePullSecrets:
    - name: acr-secret
```

### Key Insights
- ✅ `imagePullPolicy: Never` only works for minikube/local images
- ✅ Cloud registries ALWAYS need `IfNotPresent` or `Always`
- 💡 ACR secrets must be in same namespace as pods
- ❌ Don't put credentials in Helm values files

**Related Skills**: kubernetes-secrets-skills.md #1

---

## Skill #3: Resource Constraint Diagnosis

### When to Use
- Pods stuck in `Pending` state
- Deployment times out waiting for pods
- "Insufficient cpu/memory" events

### The Problem
Small AKS clusters can't handle resource-hungry deployments.

### The Solution

**Step 1: Check node capacity**
```bash
kubectl describe nodes
kubectl top nodes  # See actual usage
```

**Step 2: Check pod requests**
```bash
kubectl describe pod <pod-name> -n <namespace>
# Look for "Requests" section
```

**Step 3: Compare requests vs available**
```
If pod requests > node capacity → Reduce requests OR scale cluster
```

**Step 4: Optimize resources**
```yaml
resources:
  requests:
    memory: "64Mi"   # Start minimal
    cpu: "50m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

### Key Insights
- ✅ For hackathon/dev: 64Mi/50m CPU often sufficient
- ✅ Limits should be 2-4x requests
- ❌ Don't request more than you need
- 💡 RollingUpdate needs extra space - use Recreate for tight clusters

**Related Skills**: helm-configuration-skills.md #3, kubernetes-resource-management-skills.md #2

---

## Skill #4: Multi-Replica Resource Deadlock

### When to Use
- RollingUpdate deployments hang
- New pods pending while old pods running
- Resource-constrained cluster

### The Problem
RollingUpdate tries to run new + old pods simultaneously, exceeding cluster capacity.

### The Solution

**Option 1: Switch to Recreate strategy**
```yaml
spec:
  replicas: 1
  strategy:
    type: Recreate  # Kills old pods before starting new ones
```

**Option 2: Reduce replicas during update**
```bash
# Scale down temporarily
kubectl scale deployment <name> --replicas=1 -n <namespace>

# Update
helm upgrade ...

# Scale back up
kubectl scale deployment <name> --replicas=2 -n <namespace>
```

**Option 3: Increase cluster resources**
```bash
# Azure CLI
az aks scale --resource-group <rg> --name <cluster> --node-count 3
```

###Key Insights
- ✅ Recreate strategy = zero extra resources needed
- ✅ Small clusters should use Recreate, large clusters use RollingUpdate
- ❌ Don't use RollingUpdate with replicas > 1 on tiny clusters
- 💡 Acceptable brief downtime beats failed deployments

**Related Skills**: helm-configuration-skills.md #3

---

## Skill #5: GitHub Actions AKS Context Issues

### When to Use
- GitHub Actions can deploy locally but fails on AKS
- kubectl commands work locally but not in CI/CD
- Authentication issues in workflows

### The Problem
GitHub Actions needs AKS credentials and context configuration.

### The Solution

**Step 1: Set up Azure credentials as secrets**
```yaml
# In GitHub repo settings → Secrets
AZURE_CREDENTIALS  # Service principal JSON
ACR_LOGIN_SERVER
ACR_USERNAME
ACR_PASSWORD
```

**Step 2: Configure kubectl context in workflow**
```yaml
- name: Set up kubectl
  uses: azure/k8s-set-context@v1
  with:
    method: kubeconfig
    kubeconfig: ${{ secrets.KUBE_CONFIG }}
    
# OR

- name: Azure Login
  uses: azure/login@v1
  with:
    creds: ${{ secrets.AZURE_CREDENTIALS }}

- name: Get AKS credentials
  run: |
    az aks get-credentials \
      --resource-group ${{ secrets.RESOURCE_GROUP }} \
      --name ${{ secrets.CLUSTER_NAME }} \
      --overwrite-existing
```

**Step 3: Verify context**
```yaml
- name: Verify connection
  run: |
    kubectl config current-context
    kubectl get nodes
```

### Key Insights
- ✅ Always verify kubectl context before deploying
- ✅ Use service principal for CI/CD, not personal credentials
- 💡 `--overwrite-existing` prevents conflicts
- ❌ Don't commit kubeconfig files to git

**Related Skills**: github-actions-skills.md (if exists)

---

## Quick Reference

### Common Error → Solution Mapping

| Error | Quick Fix |
|-------|-----------|
| `ErrImageNeverPull` | Change `imagePullPolicy: Never` → `IfNotPresent` |
| `ImagePullBackOff` | Check ACR secrets, verify imagePullSecrets in deployment |
| Pods `Pending` | Reduce resource requests OR scale cluster |
| RollingUpdate hangs | Switch to `Recreate` strategy |
| Timeout after 10m | Increase Helm `--timeout` flag |
| "Insufficient memory" | Lower `requests.memory` |
| "Insufficient cpu" | Lower `requests.cpu` |

### Essential Commands

```bash
# Diagnosis
kubectl get pods -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Resource check
kubectl top nodes
kubectl describe nodes

# Quick fixes
kubectl delete pod <pod-name> -n <namespace>  # Force restart
kubectl rollout restart deployment/<name> -n <namespace>
kubectl scale deployment/<name> --replicas=0 -n <namespace>  # Full reset
```

---

**Total Skills**: 5  
**Last Updated**: January 2026  
**Success Rate**: 100% (after applying these techniques)
