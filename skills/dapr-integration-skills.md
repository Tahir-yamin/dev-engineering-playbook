# Phase 5 Dapr Integration Skills

**Purpose**: Dapr pub/sub and state management implementation patterns  
**Source**: Extracted from Phase 5 AKS + Kafka + Dapr deployment  
**Date**: January 2026

---

## Skill #1: Implementing Dapr Pub/Sub in FastAPI

### When to Use
- Building event-driven microservices
- Need to publish/consume events via Kafka
- Want decoupled communication between services

### The Problem
Need to integrate Dapr pub/sub (Kafka) with FastAPI backend to publish task events (created, completed, deleted) and have notification service consume them.

### The Solution

**Step 1: Create Dapr Integration Module**

```python
# dapr_integration.py
import httpx
from fastapi import APIRouter

router = APIRouter(prefix="", tags=["dapr"])
DAPR_HTTP_PORT = "3500"
DAPR_PUBSUB_NAME = "kafka-pubsub"

async def publish_event(topic: str, data: dict):
    """Publish event to Kafka via Dapr"""
    url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{DAPR_PUBSUB_NAME}/{topic}"
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(url, json=data)
        return response.status_code in [200, 204]
```

**Step 2: Add Subscription Endpoint**

```python
@router.get("/dapr/subscribe")
async def subscribe():
    """Dapr calls this to register subscriptions"""
    return [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "task-events",
            "route": "/events/task"
        }
    ]

@router.post("/events/task")
async def handle_task_event(event: CloudEvent):
    """Handle incoming events"""
    data = event.data
    action = data.get("action")
    print(f"📥 Event: {action}")
    return {"success": True}
```

**Step 3: Publish Events from Routes**

```python
# In existing endpoints
@router.post("/tasks")
async def create_task(task: TaskCreate):
    # ... create task logic ...
    await publish_event("task-events", {
        "action": "created",
        "task_id": task.id,
        "data": task.dict()
    })
```

### Key Insights
- ✅ Use Cloud Events v1.0 format for compatibility
- ✅ Make publishing async and non-blocking
- ✅ Handle Dapr unavailability gracefully (try/except)
- ✅ Always include /dapr/subscribe endpoint
- ❌ Don't forget to await async functions
- 💡 Use localhost:3500 - Dapr sidecar is always on this port

**Related Skills**: kubernetes-dapr-skills.md #2, event-driven-architecture-skills.md #1

---

## Skill #2: Dapr State Management API

### When to Use
- Need to cache data across requests
- Want to store user preferences/sessions
- Require distributed state without managing Redis directly

### The Solution

```python
async def save_state(key: str, value: Any):
    """Save to Redis via Dapr"""
    url = f"http://localhost:3500/v1.0/state/statestore"
    payload = [{"key": key, "value": value}]
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

async def get_state(key: str):
    """Retrieve from Redis via Dapr"""
    url = f"http://localhost:3500/v1.0/state/statestore/{key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json() if response.status_code == 200 else None

# Expose as API endpoints
@router.post("/api/state/{key}")
async def save_user_state(key: str, value: dict):
    await save_state(key, value)
    return {"success": True}
```

### Key Insights
- ✅ State store name matches Dapr component name
- ✅ Use array format for bulk save operations
- ✅ 204 status code means "no state found" (not an error)
- ❌ Don't hardcode state store name - use environment variable
- 💡 Useful for user preferences, temp data, feature flags

---

## Skill #3: Dapr Component Configuration

### When to Use
- Setting up Dapr on Kubernetes
- Configuring Kafka or Redis components
- Components not loading in sidecars

### The Problem
Dapr components not showing up in sidecar logs - pods have sidecars but components aren't loaded.

### The Solution

**Critical**: Components must be in the SAME namespace as application pods

```yaml
# kafka-pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: todo-chatbot  # ← MUST match app namespace!
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka-broker:9092"
  - name: authType    # ← CRITICAL: Explicitly set this
    value: "none"
  - name: consumerGroup
    value: "todo-group"
```

**Verify**:
```powershell
# Check components in namespace
kubectl get components -n todo-chatbot

# Verify component loaded in sidecar
kubectl logs -l app=backend -n todo-chatbot -c daprd | Select-String "component loaded"

# Should see: "Component loaded: kafka-pubsub (pubsub.kafka/v1)"
```

### Key Insights
- ✅ Namespace MUST match - components are namespace-scoped
- ✅ Explicitly set `authType: "none"` for Kafka (not defaulted)
- ✅ Use cluster-internal service names for brokers
- ❌ Don't put components in `default` if apps are in other namespace
- 💡 Check sidecar logs first when debugging component issues

**Related Skills**: kubernetes-troubleshooting-skills.md #3

---

## Skill #4: Cloud Events Format for Dapr

### When to Use
- Sending/receiving events via Dapr pub/sub
- Need to match expected event structure

### The Solution

```python
from pydantic import BaseModel
from typing import Dict, Any

class CloudEvent(BaseModel):
    """Cloud Events v1.0 - Dapr standard format"""
    id: str
    source: str
    specversion: str
    type: str
    datacontenttype: str = "application/json"
    data: Dict[str, Any]

# Dapr sends events in this format
@app.post("/events/task")
async def handle_event(event: CloudEvent):
    actual_data = event.data  # Your app data is here
    action = actual_data.get("action")
    task_id = actual_data.get("task_id")
```

### Key Insights
- ✅ Use Pydantic model for type safety
- ✅ Your app data goes in the `data` field
- ✅ Dapr automatically wraps/unwraps Cloud Events
- 💡 Don't manually create Cloud Events - Dapr does it

---

## Skill #5: Debugging Dapr Pub/Sub Flow

### When to Use
- Events not being received
- Not sure if events are being published
- Workflow broken somewhere

### The Solution

**Step 1: Verify Backend Publishing**
```powershell
kubectl logs -l app=backend -n todo-chatbot -c backend | Select-String "Published"
# Should see: "📤 Published to task-events: created"
```

**Step 2: Check Kafka Topics**
```powershell
kubectl exec -n kafka kafka-broker-0 -- \
  kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic task-events --from-beginning --max-messages 5
# Should see JSON events
```

**Step 3: Verify Subscription**
```powershell
kubectl logs -l app=notification -n todo-chatbot -c daprd --tail=100 | Select-String "subscribed"
# Should see subscription confirmation
```

**Step 4: Check Consumer Logs**
```powershell
kubectl logs -l app=notification -n todo-chatbot -c notification --tail=50
# Should see "🔔 TASK EVENT RECEIVED"
```

### Key Insights
- ✅ Check each hop in the flow separately
- ✅ Backend logs show if publish attempt succeeded
- ✅ Kafka console consumer proves events reached Kafka
- ✅ Dapr sidecar logs show subscription registration
- ❌ Don't assume - verify each step
- 💡 If events in Kafka but not received, check subscription endpoint

---

## Quick Reference

```python
# Publish event
await publish_event("topic-name", {"key": "value"})

# Subscribe endpoint (required)
@app.get("/dapr/subscribe")
async def subscribe():
    return [{"pubsubname": "kafka-pubsub", "topic": "my-topic", "route": "/handle"}]

# Handle event
@app.post("/handle")
async def handle(event: CloudEvent):
    data = event.data
    # Process event

# Save state
await save_state("key", {"data": "value"})

# Get state
value = await get_state("key")
```

---

**Total Skills**: 5  
**Last Updated**: January 2026
