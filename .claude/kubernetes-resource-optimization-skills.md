# Kubernetes Resource Optimization Skills

**Purpose**: Optimize Kubernetes resource requests/limits for cost-effective single-node deployments  
**Source**: Extracted from Todo Hackathon Phase 5 - AKS single-node optimization  
**Date**: January 2026

---

## Skill #1: Reducing CPU Requests for Dapr Sidecars

### When to Use
- Pods stuck in `Pending` state with CPU constraint messages
- Single-node or small K8s cluster
- Using Dapr sidecars (adds ~100-300m CPU per pod)

### The Problem
Default CPU requests are too high for small clusters. Dapr sidecar defaults can consume more CPU than the application itself.

### The Solution

**Step 1: Research Dapr's official recommendations**

Source: [Dapr Production Guidelines](https://docs.dapr.io/operations/hosting/kubernetes/kubernetes-production/)

Dapr recommends STARTING POINTS (not minimums):
| Component | CPU Request | CPU Limit |
|-----------|-------------|-----------|
| Dapr Sidecar | 100m | 300m |
| App Container | 100m | Remove limit |

**Step 2: Create CPU-optimized Helm values**

```yaml
# values-optimized-cpu.yaml
backend:
  resources:
    requests:
      cpu: "100m"      # Reduced from 250m
      memory: "192Mi"  
    limits:
      memory: "384Mi"  
      # NO CPU LIMIT - allows bursting
  
  dapr:
    sidecar:
      cpuRequest: "100m"   # Dapr recommended
      cpuLimit: "300m"     # Dapr recommended
```

**Step 3: Apply optimization**

```bash
helm upgrade <release> ./chart -n namespace \
  -f values-optimized-cpu.yaml
```

### Key Insights
- ✅ Removing CPU limits allows bursting (Dapr best practice)
- ✅ Start with Dapr's recommended values, not arbitrary minimums
- ❌ Don't remove memory limits (prevents OOM kills)
- 💡 60% CPU reduction freed 450m CPU on single-node cluster

**Related Skills**: helm-configuration-skills.md, dapr-skills.md

---

## Skill #2: Debugging "Pending" Pods

### When to Use
- Pods stuck in `Pending` state
- New deployments don't schedule
- Rollouts timeout

### The Problem
Insufficient CPU/memory on nodes to satisfy pod resource requests.

### The Solution

**Step 1: Describe the pending pod**

```bash
kubectl describe pod <pod-name> -n namespace | grep -A 5 "Events:"
```

Look for:
```
Warning  FailedScheduling  ... Insufficient cpu
```

**Step 2: Check node capacity**

```bash
# See total capacity and allocated resources
kubectl describe node <node-name>

# Quick view
kubectl top node
```

**Step 3: Identify resource hogs**

```bash
# See CPU requests by pod
kubectl get pods -n namespace -o json | \
  jq '.items[] | {name: .metadata.name, cpu: .spec.containers[].resources.requests.cpu}'
```

**Step 4: Free up resources**

Option A: Scale down non-critical services
```bash
kubectl scale deployment <non-critical-service> --replicas=0 -n namespace
```

Option B: Reduce resource requests (use Skill #1)

Option C: Add nodes (if budget allows)
```bash
az aks nodepool scale --name <pool> --cluster-name <cluster> --resource-group <rg> --node-count 2
```

### Key Insights
- ✅ Always check Events in `kubectl describe pod`
- ✅ Notification/monitoring services are often first to scale down
- ➤ CPU: Insufficient cpu (lowercase 'c')
- ➤ Memory: Insufficient memory
- 💡 Reserved CPU exists - node shows less than vCPU count

**Related Skills**: kubernetes-troubleshooting-skills.md

---

## Skill #3: AKS Reserved Resources

### When to Use
- Calculating actual available resources on AKS nodes
- Planning resource allocations
- Understanding why pods don't fit despite "enough" CPU

### The Problem
AKS reserves CPU/memory for system components. A 2-vCPU node does NOT have 2000m CPU available.

### The Solution

**AKS CPU Reservations** (from Microsoft docs):

| vCPU Count | Reserved CPU |
|------------|--------------|
| 1 core | 60m |
| 2 cores | 100m |
| 4 cores | 140m |

**Example Calculation**:
```
2-vCPU Node:
- Total: 2000m
- Reserved: 100m  
- Allocatable: 1900m

But also need space for:
- Dapr control plane (~500m)
- System pods (~200m)
- Buffer (~100m)
= Only ~1100m actually safe to use
```

**Check actual allocatable**:
```bash
kubectl get node -o json | \
  jq '.items[] | {name: .metadata.name, allocatable: .status.allocatable}'
```

### Key Insights
- ✅ Always account for system reservations
- ✅ Dapr control plane uses significant CPU (500m+)
- ✅ Leave 10-15% buffer for bursting
- 💡 Source: [AKS Resource Reservations](https://learn.microsoft.com/en-us/azure/aks/concepts-clusters-workloads#resource-reservations)

---

## Skill #4: Helm Values for Different Environments

### When to Use
- Need different resources for dev/staging/prod
- Want to optimize costs in development
- Single-node dev cluster vs multi-node production

### The Solution

**Create environment-specific values files**:

```
helm/
├── values.yaml                    # Base/production values
├── values-dev.yaml                # Minimal resources
├── values-staging.yaml            # Medium resources
└── values-optimized-cpu.yaml      # Single-node optimized
```

**values-dev.yaml** (minimal):
```yaml
backend:
  resources:
    requests:
      cpu: "50m"      # Minimal
      memory: "128Mi"
    limits:
      memory: "256Mi"

# Disable non-essential services
notificationService:
  enabled: false
```

**values-staging.yaml** (balanced):
```yaml
backend:
  resources:
    requests:
      cpu: "100m"
      memory: "256Mi"
    limits:
      memory: "512Mi"
```

**Deploy with environment-specific values**:
```bash
# Development
helm upgrade app ./chart -f values-dev.yaml

# Staging
helm upgrade app ./chart -f values-staging.yaml

# Production (use base values.yaml)
helm upgrade app ./chart
```

### Key Insights
- ✅ Base `values.yaml` should be production-ready
- ✅ Override with `-f` flag for other environments
- ✅ Multiple `-f` flags merge (last wins)
- 💡 Document which values file is used in CI/CD

**Related Skills**: helm-configuration-skills.md

---

## Skill #5: Monitoring Resource Usage

### When to Use
- After applying resource optimizations
- To validate actual usage vs requests
- Identifying underutilized pods

### The Solution

**Install metrics-server** (if not present):
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

**Check current usage**:
```bash
# Node usage
kubectl top node

# Pod usage (all namespaces)
kubectl top pod -A

# Specific namespace
kubectl top pod -n namespace

# Sort by CPU
kubectl top pod -n namespace --sort-by=cpu

# Sort by memory
kubectl top pod -n namespace --sort-by=memory
```

**Compare usage to requests**:
```bash
# Show requests and limits
kubectl get pods -n namespace -o custom-columns=\
NAME:.metadata.name,\
CPU_REQ:.spec.containers[*].resources.requests.cpu,\
CPU_LIM:.spec.containers[*].resources.limits.cpu,\
MEM_REQ:.spec.containers[*].resources.requests.memory,\
MEM_LIM:.spec.containers[*].resources.limits.memory
```

**Interpretation**:
- Usage < 50% of request → Over-provisioned, can reduce
- Usage > 80% of request → Under-provisioned, may need more
- Usage > limit → Pod will be throttled (CPU) or killed (memory)

### Key Insights
- ✅ Monitor for at least 24 hours under normal load
- ✅ Account for traffic spikes when setting limits
- ✅ CPU throttling is invisible - no errors, just slow
- 💡 Prometheus + Grafana for historical trends

---

## Quick Reference

### Resource Units

```
CPU:
1 core = 1000m (millicores)
100m = 0.1 core = 10% of 1 CPU

Memory:
Ki, Mi, Gi = Binary (1024-based)
K, M, G = Decimal (1000-based)
Use Mi/Gi for consistency
```

### Common CPU Allocations

| Service Type | Typical Request | Typical Limit |
|--------------|-----------------|---------------|
| Lightweight API | 100m | 500m or none |
| Database | 250m-500m | 1000m |
| Frontend (Next.js) | 100-200m | 500m or none |
| Dapr Sidecar | 100m | 300m |

### Optimization Checklist

Before reducing resources:
- [ ] Monitor actual usage for 24+ hours
- [ ] Test under load
- [ ] Keep memory limits (OOM protection)
- [ ] Remove CPU limits (allow bursting)
- [ ] Leave 10-15% buffer
- [ ] Document decisions

---

**Total Skills**: 5  
**Last Updated**: January 18, 2026  
**Production Validated**: ✅ Single-node AKS (Phase 5)
