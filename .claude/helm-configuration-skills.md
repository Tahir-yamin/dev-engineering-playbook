# Helm Configuration Skills

**Purpose**: Optimize Helm charts for small clusters and resource-constrained environments  
**Source**: Extracted from Phase 5 AKS Deployment  
**Date**: January 2026

---

## Skill #1: Deployment Strategy Selection

### When to Use
- Small Kubernetes clusters with limited resources
- Single-node environments
- Need to minimize resource overhead during deployments

### The Problem
Default Rolling Update strategy requires extra capacity (surge pods) that small clusters can't provide.

### The Solution

**Check current strategy:**
```yaml
# In deployment template
spec:
  strategy:
    type: RollingUpdate  # Default
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

**For small clusters, use Recreate:**
```yaml
spec:
  replicas: 1
  strategy:
    type: Recreate  # Kills old pods first
```

**Comparison:**

| Strategy | Pros | Cons | Use When |
|----------|------|------|----------|
| RollingUpdate | Zero downtime | Needs 2x resources | Production, large clusters |
| Recreate | Minimal resources | Brief downtime | Dev, small clusters, hackathons |

### Key Insights
- ✅ Recreate = 0 extra resource overhead
- ✅ Perfect for demo/dev environments
- ❌ Don't use RollingUpdate with limited nodes
- 💡 Can switch strategies per environment

**Related Skills**: kubernetes-resource-management-skills.md #1

---

## Skill #2: ImagePullSecrets Configuration

### When to Use
- Pulling from private Docker registry (ACR, DockerHub, etc.)
- Getting `ErrImageNeverPull` or `ImagePullBackOff` errors

### The Problem
Kubernetes can't authenticate with private registries without credentials.

### The Solution

**Step 1: Add to values.yaml**
```yaml
imagePullSecrets:
  - name: acr-secret  # Must match secret name in cluster
```

**Step 2: Reference in deployment template**
```yaml
spec:
  imagePullSecrets:
    {{- toYaml .Values.imagePullSecrets | nindent 8 }}
  containers:
    - name: {{ .Chart.Name }}
      image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
      imagePullPolicy: {{ .Values.imagePullPolicy }}
```

**Step 3: Create secret in workflow**
```bash
kubectl create secret docker-registry acr-secret \
  --namespace={{ .Values.namespace }} \
  --docker-server=$ACR_LOGIN_SERVER \
  --docker-username=$ACR_USERNAME \
  --docker-password=$ACR_PASSWORD
```

### Key Insights
- ✅ Secret must be in same namespace as pods
- ✅ Use `toYaml` helper for proper formatting
- 💡 Create secret before Helm install
- ❌ Never hardcode credentials in values files

**Related Skills**: aks-troubleshooting-skills.md #2, kubernetes-secrets-skills.md #1

---

## Skill #3: Resource Request Optimization

### When to Use
- Pods stuck in Pending state
- Small cluster with limited CPU/RAM
- Need to fit multiple services on minimal nodes

### The Problem
Default resource requests are often too high for small clusters.

### The Solution

**Step 1: Define minimal defaults in values.yaml**
```yaml
resources:
  requests:
    memory: "64Mi"   # Start small
    cpu: "50m"       # 0.05 CPU cores
  limits:
    memory: "256Mi"  # 4x requests
    cpu: "200m"      # 4x requests
```

**Step 2: Use in deployment template**
```yaml
resources:
  {{- toYaml .Values.resources | nindent 12 }}
```

**Step 3: Override per service if needed**
```yaml
backend:
  resources:
    requests:
      memory: "128Mi"  # Backend needs more
      cpu: "100m"
      
frontend:
  resources:
    requests:
      memory: "64Mi"   # Frontend can be minimal
      cpu: "50m"
```

**Resource Sizing Guide:**

| Service Type | Minimal | Recommended | Production |
|--------------|---------|-------------|------------|
| Static frontend | 64Mi/50m | 128Mi/100m | 256Mi/250m |
| API backend | 128Mi/100m | 256Mi/250m | 512Mi/500m |
| Database | 256Mi/250m | 512Mi/500m | 1Gi/1000m |

### Key Insights
- ✅ Start minimal, scale up if needed
- ✅ Limits should be 2-4x requests
- 💡 Monitor actual usage with `kubectl top pods`
- ❌ Don't over-provision on small clusters

**Related Skills**: aks-troubleshooting-skills.md #3, kubernetes-resource-management-skills.md #2

---

## Skill #4: Health Probe Timing

### When to Use
- Pods failing readiness/liveness checks
- Applications take time to start
- Running on slow nodes

### The Problem
Default probe timing is too aggressive for slow-starting apps or resource-constrained environments.

### The Solution

**Adjust timing in values.yaml:**
```yaml
livenessProbe:
  enabled: true
  initialDelaySeconds: 120  # Wait 2 minutes after start
  periodSeconds: 10         # Check every 10 seconds
  timeoutSeconds: 5         # 5 second timeout
  failureThreshold: 3       # 3 failures = restart

readinessProbe:
  enabled: true
  initialDelaySeconds: 120  # Wait 2 minutes
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

**Timing Guidelines:**

| Environment | initialDelaySeconds | Rationale |
|-------------|---------------------|-----------|
| Local (fast SSD) | 30s | Quick startup |
| Small cloud nodes | 60-120s | Slower provisioning |
| Large apps (DB+cache) | 120-180s | Complex initialization |

**In deployment template:**
```yaml
{{- if .Values.livenessProbe.enabled }}
livenessProbe:
  httpGet:
    path: {{ .Values.livenessProbe.path }}
    port: {{ .Values.containerPort }}
  initialDelaySeconds: {{ .Values.livenessProbe.initialDelaySeconds }}
  periodSeconds: {{ .Values.livenessProbe.periodSeconds }}
{{- end }}
```

### Key Insights
- ✅ Increase delays for slow environments
- ✅ Liveness = restart if unhealthy (be conservative)
- ✅ Readiness = route traffic when ready (can be aggressive)
- 💡 Set `initialDelaySeconds` > app startup time
- ❌ Don't set too low or pods restart unnecessarily

**Related Skills**: None

---

## Quick Reference

### Essential Values.yaml Patterns

```yaml
# Global settings
namespace:  todo-chatbot
imagePullPolicy: IfNotPresent
imagePullSecrets:
  - name: acr-secret

# Resource defaults (override per service)
resources:
  requests:
    memory: "64Mi"
    cpu: "50m"
  limits:
    memory: "256Mi"
    cpu: "200m"

# Per-service pattern
backend:
  enabled: true
  replicaCount: 1
  
  image:
    repository: todo-backend
    tag: v1
    pullPolicy: IfNotPresent
  
  strategy:
    type: Recreate
  
  resources:  # Override defaults if needed
   requests:
      memory: "128Mi"
      cpu: "100m"
  
  livenessProbe:
    enabled: true
    path: /health
    initialDelaySeconds: 120
    periodSeconds: 10
```

### Helm Command Patterns

```bash
# Install with custom values
helm install my-app ./chart \
  --namespace my-namespace \
  --set image.tag=v2.0 \
  --set resources.requests.memory=128Mi

# Upgrade (use Recreate strategy)
helm upgrade my-app ./chart \
  --namespace my-namespace \
  --set image.tag=v2.1

# Debug (see generated YAML)
helm template my-app ./chart --debug

# Get values
helm get values my-app -n my-namespace
```

---

**Total Skills**: 4  
**Last Updated**: January 2026  
**Optimized For**: Small clusters, resource-constrained environments, hackathons
