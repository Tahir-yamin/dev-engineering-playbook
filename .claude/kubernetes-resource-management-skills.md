# Kubernetes Resource Management Skills

**Purpose**: Optimize pod resource allocation for small clusters and resource-constrained environments  
**Source**: Extracted from Phase 5 AKS resource optimization  
**Date**: January 2026

---

## Skill #1: Understanding Requests vs Limits

### When to Use
- Designing resource specifications for pods
- Pods getting OOMKilled or throttled
- Need to optimize cluster utilization

### The Problem
Confusion about requests vs limits leads to either resource waste or pod failures.

### The Solution

**Requests** = Minimum guaranteed resources
**Limits** = Maximum allowed resources

```yaml
resources:
  requests:       # Scheduler uses this
    memory: "64Mi"  # Pod guaranteed this minimum
    cpu: "50m"      # Kubernetes reserves this
  limits:         # Kubelet enforces this
    memory: "256Mi" # Pod killed if exceeds
    cpu: "200m"     # Pod throttled if exceeds
```

**Best Practices:**

| Scenario | Request | Limit | Ratio |
|----------|---------|-------|-------|
| Predictable load | Actual usage | 1.5-2x requests | Conservative |
| Bursty traffic | Baseline usage | 3-4x requests | Permissive |
| Critical service | High | Same as request | 1:1 (guaranteed) |
| Best-effort | Low | High | 4-5x |

### Key Insights
- ✅ Requests affect scheduling, limits affect runtime
- ✅ Memory limit breach = OOMKilled, CPU limit = throttled
- 💡 Start with limits 2-4x requests
- ❌ Don't set limits too low (causes crashes)
- ❌ Don't set requests too high (pods won't schedule)

**Related Skills**: helm-configuration-skills.md #3

---

##Skill #2: Sizing for Small Clusters

### When to Use
- Running on free/minimal AKS tier
- Single-node or 2-node clusters
- Hackathon/demo environments

### The Problem
Default resource requests are designed for large clusters and prevent scheduling on small nodes.

### The Solution

**Step 1: Check node capacity**
```bash
kubectl describe nodes
# Look for: Allocatable resources
```

**Step 2: Calculate available resources**
```
Total Allocatable - System Reserved - Running Pods = Available for New Pods
```

**Step 3: Size requests appropriately**

**Minimal Configuration (for demos):**
```yaml
# Fits ~10-15 pods on 2GB node
resources:
  requests:
    memory: "64Mi" 
    cpu: "50m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

**Realistic Configuration:**
```yaml
# Fits ~5-7 pods on 2GB node
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

**Node Capacity Guide:**

| Node RAM | Allocatable | # Pods (64Mi each) | # Pods (128Mi each) |
|----------|-------------|--------------------|--------------------|
| 2GB | ~1.7GB | 15-20 | 8-12 |
| 4GB | ~3.5GB | 30-40 | 15-25 |
| 8GB | ~7GB | 60-80 | 30-50 |

### Key Insights
- ✅ Small nodes need small requests
- ✅ Monitor with `kubectl top nodes`
- 💡 Leave 20-30% buffer for system pods
- ❌ Don't pack nodes to 100% capacity

**Related Skills**: aks-troubleshooting-skills.md #3, helm-configuration-skills.md #3

---

## Skill #3: Handling Pending Pods

### When to Use
- Pod stuck in `Pending` state
- Events show "Insufficient cpu" or "Insufficient memory"
- Deployment times out

### The Problem
Pod resource requests exceed available node capacity.

### The Solution

**Step 1: Diagnose**
```bash
# Get pod details
kubectl describe pod <pod-name> -n <namespace>

# Look for events at bottom:
# "0/1 nodes are available: 1 Insufficient memory"
# "0/1 nodes are available: 1 Insufficient cpu"
```

**Step 2: Check what's requested**
```bash
# See pod requests
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.containers[0].resources.requests}'
```

**Step 3: Fix**

**Option A: Reduce requests**
```yaml
# In values.yaml  
resources:
  requests:
    memory: "64Mi"   # Reduced from 256Mi
    cpu: "50m"       # Reduced from 250m
```

**Option B: Scale cluster**
```bash
# Add more nodes (Azure)
az aks scale --resource-group <rg> --name <cluster> --node-count 3
```

**Option C: Use Recreate strategy**
```yaml
strategy:
  type: Recreate  # Kills old before starting new
```

### Key Insights
- ✅ Pod stays pending until resources available
- ✅ Reduce requests OR add nodes
- 💡 Recreate strategy frees resources immediately
- ❌ Don't wait indefinitely - timeout and fix

**Related Skills**: aks-troubleshooting-skills.md #3, helm-configuration-skills.md #1

---

## Skill #4: Resource Quota Management

### When to Use
- Multi-tenant clusters
- Need to prevent resource hogging
- Implementing resource governance

### The Problem
Without quotas, one namespace can consume all cluster resources.

### The Solution

**Create ResourceQuota:**
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: todo-chatbot
spec:
  hard:
    requests.cpu: "2"        # Max 2 CPU requested
    requests.memory: "4Gi"   # Max 4GB requested
    limits.cpu: "4"          # Max 4 CPU limit
    limits.memory: "8Gi"     # Max 8GB limit
    pods: "10"               # Max 10 pods
```

**Apply:**
```bash
kubectl apply -f resource-quota.yaml
```

**Check usage:**
```bash
kubectl describe resourcequota compute-quota -n todo-chatbot
```

### Key Insights
- ✅ Quotas prevent runaway resource usage
- ✅ Enforceable limits per namespace
- 💡 Set quotas based on cluster capacity
- ❌ Don't set quotas too low (blocks deployments)

**Related Skills**: None

---

## Quick Reference

### Diagnostic Commands

```bash
# Node resources
kubectl describe nodes
kubectl top nodes

# Pod resources
kubectl top pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>

# Events (resource issues show here)
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Resource consumption per namespace
kubectl resource-usage namespaces
```

### Common Resource Issues & Fixes

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| Pod Pending | Requests > available | Reduce requests OR scale cluster |
| OOMKilled | Memory limit too low | Increase limits.memory |
| CPU throttling | CPU limit too low | Increase limits.cpu |
| Can't schedule new pods | No space on nodes | Reduce requests OR add nodes |
| Evicted pods | Node pressure | Increase node size OR reduce pods |

### Resource Sizing Cheat Sheet

```yaml
# Minimal (Hackathon)
requests: {memory: "64Mi", cpu: "50m"}
limits: {memory: "256Mi", cpu: "200m"}

# Small (Dev/Test)
requests: {memory: "128Mi", cpu: "100m"}
limits: {memory: "512Mi", cpu: "500m"}

# Medium (Staging)
requests: {memory: "256Mi", cpu: "250m"}
limits: {memory: "1Gi", cpu: "1000m"}

# Large (Production)
requests: {memory: "512Mi", cpu: "500m"}
limits: {memory: "2Gi", cpu: "2000m"}
```

---

**Total Skills**: 4  
**Last Updated**: January 2026  
**Optimized For**: Small clusters, cost-effective deployments, resource-constrained environments
