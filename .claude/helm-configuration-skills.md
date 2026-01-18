# Helm Configuration and Optimization Skills

**Purpose**: Optimize Helm chart configurations for different environments  
**Source**: Todo Hackathon Phase 5 - Single-node AKS optimization  
**Date**: January 2026

---

## Skill #1: Creating Environment-Specific Values Files

### When to Use
- Need different resource allocations for dev/staging/prod
- Want to optimize costs in development
- Single-node vs multi-node clusters

### The Problem
One-size-fits-all Helm values waste resources or cause scheduling failures.

### The Solution

**File structure**:
```
helm/todo-chatbot/
├── values.yaml                    # Production (base)
├── values-dev.yaml                # Development (minimal)
├── values-staging.yaml            # Staging (balanced)
└── values-optimized-cpu.yaml      # Single-node (optimized)
```

**values.yaml** (production baseline):
```yaml
backend:
  replicaCount: 2  # HA in production
  resources:
    requests:
      cpu: "250m"
      memory: "256Mi"
    limits:
      memory: "512Mi"
      cpu: "500m"
```

**values-optimized-cpu.yaml** (single-node):
```yaml
backend:
  replicaCount: 1
  resources:
    requests:
      cpu: "100m"      # 60% reduction
      memory: "192Mi"
    limits:
      memory: "384Mi"
      # NO CPU LIMIT for bursting
```

**Deploy with environment values**:
```bash
# Development
helm upgrade app ./chart -n ns -f values-dev.yaml

# Single-node cluster
helm upgrade app ./chart -n ns -f values-optimized-cpu.yaml

# Production (default)
helm upgrade app ./chart -n ns
```

### Key Insights
- ✅ Base values.yaml should be production-ready
- ✅ Use `-f` to overlay environment-specific changes
- ✅ Multiple `-f` flags merge (last wins)
- 💡 Document which file is used in each environment

---

## Skill #2: Optimizing for Single-Node Clusters

### When to Use
- Deploying to free-tier AKS (single node)
- Pods stuck in Pending state
- CPU constraints preventing scheduling

### The Problem
Default resource requests designed for multi-node clusters don't fit on single node.

### The Solution

**Calculate available resources**:
```
2-vCPU Node:
Total:           2000m CPU
AKS Reserved:    -100m
Dapr Control:    -500m
System Pods:     -200m
Buffer (10%):    -200m
-------------------
Available:       ~1000m CPU
```

**Optimization strategy**:
1. Start with Dapr recommendations (100m per sidecar)
2. Remove CPU limits (allow bursting)
3. Disable non-critical services
4. Keep memory limits (prevent OOM)

**Example optimized values**:
```yaml
# Global defaults
resources:
  requests:
    cpu: "50m"
    memory: "64Mi"
  limits:
    memory: "128Mi"

# Backend (critical)
backend:
  resources:
    requests:
      cpu: "100m"
      memory: "192Mi"
    limits:
      memory: "384Mi"

# Frontend (critical)
frontend:
  resources:
    requests:
      cpu: "100m"
      memory: "192Mi"
    limits:
      memory: "384Mi"

# Database (critical)
database:
  resources:
    requests:
      cpu: "100m"
      memory: "256Mi"
    limits:
      memory: "512Mi"

# Notification (non-critical)
notificationService:
  enabled: false  # Disable to save CPU
```

### Key Insights
- ✅ Total requests: 300m (fits comfortably)
- ✅ Freed 450m CPU vs defaults
- ❌ Don't reduce below Dapr minimums (100m)
- 💡 Monitor actual usage, can reduce further if stable

---

## Skill #3: Helm Upgrade vs Install

### When to Use
- Understanding when to use `upgrade` vs `install`
- Avoiding "release already exists" errors

### The Problem
`helm install` fails if release exists, `helm upgrade` fails if release doesn't exist.

### The Solution

**Use `upgrade --install` (best practice)**:
```bash
# Works for both new and existing releases
helm upgrade --install todo-chatbot ./chart -n namespace \
  -f values-optimized-cpu.yaml
```

**Benefits**:
- ✅ Creates release if doesn't exist
- ✅ Upgrades if already exists
- ✅ Idempotent (can run multiple times)

**Alternative - Check first**:
```bash
# Check if release exists
if helm list -n namespace | grep -q "todo-chatbot"; then
  helm upgrade todo-chatbot ./chart -n namespace
else
  helm install todo-chatbot ./chart -n namespace
fi
```

### Key Insights
- ✅ `upgrade --install` is idempotent
- ✅ Use for CI/CD pipelines
- 💡 Add `--atomic` for automatic rollback on failure

---

## Skill #4: Viewing and Comparing Helm Values

### When to Use
- Debugging Helm deployments
- Verifying which values are actually applied
- Comparing environments

### The Solution

**See current deployed values**:
```bash
# Get user-supplied values
helm get values todo-chatbot -n namespace

# Get all computed values (includes defaults)
helm get values todo-chatbot -n namespace --all

# Get specific nested value
helm get values todo-chatbot -n namespace -o json | jq '.backend.resources'
```

**Compare values files**:
```powershell
# Compare dev vs prod values
$dev = Get-Content values-dev.yaml
$prod = Get-Content values.yaml
Compare-Object $dev $prod
```

**Test values before deploying**:
```bash
# Dry-run with template
helm template todo-chatbot ./chart -f values-optimized-cpu.yaml > /tmp/rendered.yaml

# Review rendered YAML
cat /tmp/rendered.yaml | grep -A 5 "resources:"
```

### Key Insights
- ✅ `helm get values` shows what's actually deployed
- ✅ `helm template` previews without deploying
- ✅ Use `--debug` to see merge logic
- 💡 Compare rendered YAML between environments

---

## Skill #5: Helm Rollback Strategy

### When to Use
- New deployment breaks production
- Need to quickly revert to previous version
- Testing new configurations

### The Solution

**List revision history**:
```bash
# See all revisions
helm history todo-chatbot -n namespace

# Sample output:
# REVISION  STATUS      CHART           DESCRIPTION
# 1         superseded  todo-chatbot-1  Install complete
# 2         superseded  todo-chatbot-1  Upgrade complete
# 3         deployed    todo-chatbot-1  Upgrade complete
```

**Rollback to previous version**:
```bash
# Rollback to previous revision
helm rollback todo-chatbot -n namespace

# Rollback to specific revision
helm rollback todo-chatbot 2 -n namespace
```

**Atomic upgrades** (auto-rollback on failure):
```bash
helm upgrade --install todo-chatbot ./chart -n namespace \
  --atomic \
  --timeout 5m
```

**What `--atomic` does**:
1. Deploys new version
2. Waits for pods to be Ready
3. If timeout or failure → automatic rollback
4. Returns error code (good for CI/CD)

### Key Insights
- ✅ `--atomic` prevents broken deployments
- ✅ Helm stores last ~10 revisions by default
- ✅ Rollback is instant (just updates K8s resources)
- 💡 Use `--wait` to ensure rollout succeeds

---

## Quick Reference

### Common Helm Commands

```bash
# Install or upgrade
helm upgrade --install <release> ./chart -n <ns>

# With custom values
helm upgrade --install <release> ./chart -n <ns> \
  -f values-custom.yaml \
  --set image.tag=v1.2.3

# Atomic upgrade (auto-rollback)
helm upgrade --install <release> ./chart -n <ns> \
  --atomic --timeout 5m

# Dry-run
helm upgrade --install <release> ./chart -n <ns> --dry-run

# Template (preview)
helm template <release> ./chart -f values.yaml

# Get deployed values
helm get values <release> -n <ns>

# Rollback
helm rollback <release> -n <ns>

# Uninstall
helm uninstall <release> -n <ns>
```

### Values File Merge Order

```bash
# Last value wins
helm upgrade app ./chart \
  -f values.yaml \           # Base
  -f values-prod.yaml \      # Overrides base
  --set image.tag=latest    # Overrides everything
```

### Resource Optimization Checklist

For single-node optimization:
- [ ] Calculate available CPU (Total - Reserved - System)
- [ ] Set requests to Dapr minimums (100m)
- [ ] Remove CPU limits
- [ ] Keep memory limits
- [ ] Disable non-critical services
- [ ] Test with `helm template` first
- [ ] Deploy with `--atomic`
- [ ] Monitor with `kubectl top pods`

---

**Total Skills**: 5  
**Last Updated**: January 18, 2026  
**Production Tested**: ✅ Single-node AKS (Phase 5)
