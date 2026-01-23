# Dapr Configuration Skills

**Purpose**: Configure and troubleshoot Dapr sidecars in Kubernetes deployments  
**Source**: Todo Hackathon Phase 5 - Dapr sidecar integration  
**Date**: January 2026

---

## Skill #1: Installing Dapr on AKS

### When to Use
- Setting up Dapr for first time on AKS cluster
- Need distributed runtime capabilities (Pub/Sub, State, Service Invocation)

### The Problem
Dapr needs to be installed in Kubernetes cluster before applications can use it.

### The Solution

**Step 1: Install Dapr CLI locally**
```powershell
# Windows
powershell -Command "iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex"

# Verify
dapr --version
```

**Step 2: Install Dapr on Kubernetes**
```bash
# Initialize Dapr in Kubernetes
dapr init -k --wait

# Verify installation
dapr status -k
kubectl get pods -n dapr-system
```

Expected output:
```
NAME                                    READY   STATUS    
dapr-dashboard-xxxxx                    1/1     Running
dapr-operator-xxxxx                     1/1     Running
dapr-placement-server-0                 1/1     Running
dapr-sentry-xxxxx                       1/1     Running
dapr-sidecar-injector-xxxxx            1/1     Running
```

**Step 3: Enable sidecar injection**
```yaml
# In your deployment YAML
metadata:
  annotations:
    dapr.io/enabled: "true"
    dapr.io/app-id: "todo-backend"
    dapr.io/app-port: "8000"
```

### Key Insights
- ✅ Dapr control plane uses ~500m CPU - factor into resource planning
- ✅ Sidecar injector watches for annotations and injects automatically
- ✅ Each pod gets 2 containers: app + daprd sidecar
- 💡 Use `dapr dashboard` for GUI management

---

## Skill #2: Configuring Dapr Resource Limits

### When to Use
- Pods pending due to insufficient resources
- Following Dapr production best practices
- Optimizing for small/single-node clusters

### The Problem
Default Dapr sidecar resources may be too high or not set, causing resource issues.

### The Solution

**Official Dapr Recommendations** (from docs.dapr.io):

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Sidecar | 100m | 300m | 128Mi | 256Mi |
| Control Plane | Varies | Varies | Varies | Varies |

**Method 1: Via Annotations** (per-pod)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "backend"
        dapr.io/sidecar-cpu-request: "100m"
        dapr.io/sidecar-cpu-limit: "300m"
        dapr.io/sidecar-memory-request: "128Mi"
        dapr.io/sidecar-memory-limit: "256Mi"
```

**Method 2: Via Helm Values** (global default)
```yaml
# values.yaml
dapr:
  sidecar:
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
      limits:
        cpu: "300m"
        memory: "256Mi"
```

**Key Configuration Notes**:
- Remove CPU limits to allow bursting (Dapr recommendation)
- Keep memory limits to prevent OOM
- 100m CPU request is the recommended starting point

### Key Insights
- ✅ Dapr handles I/O-heavy lifting, so app container can use less CPU
- ✅ Remove CPU limits but keep memory limits
- ❌ Don't set memory limits on control plane (causes OOMKilled)
- 💡 Monitor actual usage for 24hrs before reducing further

---

## Skill #3: Dapr Pub/Sub with Kafka

### When to Use
- Need event-driven architecture
- Publishing task events to Kafka
- Want Dapr to abstract Kafka complexity

### The Problem
Direct Kafka integration requires kafka-python library and connection management.

### The Solution

**Step 1: Create Dapr Pub/Sub Component**
```yaml
# components/kafka-pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka-cluster-kafka-bootstrap:9092"
  - name: consumerGroup
    value: "todo-chatbot"
  - name: authType
    value: "none"
```

**Step 2: Apply component**
```bash
kubectl apply -f components/kafka-pubsub.yaml -n namespace
```

**Step 3: Publish events via Dapr HTTP API**
```python
# In FastAPI backend
import httpx

async def publish_task_event(event_type, data):
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://localhost:3500/v1.0/publish/kafka-pubsub/task-events",
            json={
                "event_type": event_type,
                "data": data
            }
        )
```

**Alternative: Lightweight event bus** (if Kafka disabled)
```python
# simple_events.py
class EventBus:
    def publish(self, topic, data):
        print(f"📤 Event: {topic} - {data}")
        
event_bus = EventBus()
```

### Key Insights
- ✅ Dapr abstracts Kafka - no kafka-python needed
- ✅ Can swap Kafka for RabbitMQ by changing component YAML
- ✅ Port 3500 is Dapr sidecar HTTP API
- 💡 Use lightweight event bus for local dev

---

## Skill #4: Debugging Dapr Sidecar Issues

### When to Use
- Pod shows 1/2 ready (sidecar not starting)
- Dapr sidecar crashlooping
- Can't publish to Kafka via Dapr

### The Problem
Dapr sidecar issues prevent application from using Dapr features.

### The Solution

**Step 1: Check sidecar logs**
```bash
# View daprd sidecar logs
kubectl logs <pod-name> -c daprd -n namespace

# Follow logs
kubectl logs <pod-name> -c daprd -n namespace --follow
```

**Step 2: Check Dapr annotations**
```bash
kubectl get pod <pod-name> -n namespace -o yaml | grep -A 10 "annotations:"
```

Required annotations:
- `dapr.io/enabled: "true"`
- `dapr.io/app-id: "your-app-id"`
- `dapr.io/app-port: "8000"` (if app has HTTP server)

**Step 3: Verify Dapr components**
```bash
# List Dapr components
kubectl get components -n namespace

# Describe component
kubectl describe component kafka-pubsub -n namespace
```

**Common Issues**:

| Symptom | Cause | Fix |
|---------|-------|-----|
| 1/2 Ready | Sidecar crashlooping | Check daprd logs |
| Can't connect to Kafka | Component misconfigured | Verify brokers address |
| Port 3500 connection refused | Sidecar not started | Check annotations |

### Key Insights
- ✅ Always check BOTH containers: app + daprd
- ✅ daprd logs show component initialization
- ✅ Port 3500 is Dapr HTTP API, 50001 is gRPC
- 💡 Use `dapr dashboard` for visual debugging

---

## Skill #5: Dapr State Management (Optional)

### When to Use
- Need distributed key-value store
- Want state abstraction
- Planning for horizontal scaling

### The Solution

**Create State Store Component**:
```yaml
# components/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "host=postgres port=5432 user=postgres password=postgres dbname=tododb"
```

**Use in application**:
```python
# Save state
await client.post(
    "http://localhost:3500/v1.0/state/statestore",
    json=[{
        "key": "conversation_state",
        "value": {"messages": []}
    }]
)

# Get state
response = await client.get(
    "http://localhost:3500/v1.0/state/statestore/conversation_state"
)
```

### Key Insights
- ✅ Can use Postgres, Redis, CosmosDB without code changes
- ✅ Dapr handles connection pooling
- 💡 Not required for Phase 5 - PostgreSQL directly is fine

---

## Quick Reference

### Dapr Sidecar Ports
```
3500  - HTTP API
50001 - gRPC API
```

### Common Dapr Annotations
```yaml
dapr.io/enabled: "true"               # Enable sidecar injection
dapr.io/app-id: "my-app"              # Unique app identifier
dapr.io/app-port: "8000"              # App's HTTP port
dapr.io/sidecar-cpu-request: "100m"   # CPU request
dapr.io/sidecar-memory-request: "128Mi" # Memory request
```

### Useful Commands
```bash
# Dapr status
dapr status -k

# Dashboard (forwards to localhost:8080)
dapr dashboard -k

# Uninstall Dapr
dapr uninstall -k
```

---

**Total Skills**: 5  
**Last Updated**: January 18, 2026  
**Production Validated**: ✅ Todo Hackathon Phase 5
