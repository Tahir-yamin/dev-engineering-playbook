# Phase 5 Part C: Notification Service - Walkthrough

**Completed**: January 5, 2026  
**Duration**: ~20 minutes

---

## What Was Implemented

### 1. Notification Service Application

**File**: [main.py](file:///d:/Hackathon%20phase%201%20TODO%20App/todo_hackathon_phase1/phase4/services/notification-service/main.py)

A FastAPI application that acts as a Kafka consumer via Dapr:

| Endpoint | Purpose |
|----------|---------|
| `GET /dapr/subscribe` | Dapr subscription declaration |
| `POST /events/reminders` | Handle reminder events |
| `POST /events/tasks` | Handle task CRUD events |
| `POST /events/updates` | Handle real-time sync events |
| `POST /api/jobs/trigger` | Dapr Jobs API callback |

### 2. Kafka Topic Subscriptions

```python
return [
    {"pubsubname": "kafka-pubsub", "topic": "reminders", "route": "/events/reminders"},
    {"pubsubname": "kafka-pubsub", "topic": "task-events", "route": "/events/tasks"},
    {"pubsubname": "kafka-pubsub", "topic": "task-updates", "route": "/events/updates"}
]
```

### 3. Docker & Kubernetes

| File | Purpose |
|------|---------|
| [Dockerfile](file:///d:/Hackathon%20phase%201%20TODO%20App/todo_hackathon_phase1/phase4/services/notification-service/Dockerfile) | Multi-stage build |
| [notification-service.yaml](file:///d:/Hackathon%20phase%201%20TODO%20App/todo_hackathon_phase1/phase4/kubernetes/notification-service.yaml) | K8s deployment with Dapr |

Key Dapr annotations:
```yaml
dapr.io/enabled: "true"
dapr.io/app-id: "notification-service"
dapr.io/app-port: "8001"
```

---

## Architecture

```
┌─────────────┐     ┌─────────┐     ┌─────────────────────┐
│   Backend   │────▶│  Kafka  │────▶│ Notification Service│
│ (Publisher) │     │ Broker  │     │     (Consumer)      │
└─────────────┘     └─────────┘     └─────────────────────┘
       │                                     │
       │                                     ▼
       │                            ┌─────────────────┐
       │                            │  Send Reminder  │
       └───────────────────────────▶│  Push/Email/WS  │
                                    └─────────────────┘
```

---

## Lessons Learned

### ✅ What Worked Well

1. **Dapr subscription pattern**: `/dapr/subscribe` endpoint is simple and declarative
2. **Graceful event handling**: Each handler returns success/failure status
3. **Jobs API integration**: Callback endpoint for exact-time triggers

### 💡 Key Insights

1. **Dapr calls your app**: You don't poll Kafka, Dapr pushes events to your HTTP endpoints
2. **CloudEvents format**: Dapr wraps all events in CloudEvents structure
3. **Separate service = separate pod**: Better resource isolation and scaling

---

## Skills Upgraded

| Skill | Level | What Was Learned |
|-------|-------|------------------|
| Dapr Pub/Sub | ⬆️ Advanced | Consumer subscription pattern |
| Microservices | ⬆️ Advanced | Event-driven service design |
| Kubernetes | ⬆️ Advanced | Dapr sidecar annotations |

---

## Files Created

| File | Lines | Purpose |
|------|-------|---------|
| `services/notification-service/main.py` | ~245 | FastAPI consumer |
| `services/notification-service/requirements.txt` | 8 | Dependencies |
| `services/notification-service/Dockerfile` | 25 | Docker build |
| `kubernetes/notification-service.yaml` | 75 | K8s deployment |

---

## Next Steps

- [ ] Part D: Deploy to Minikube with Dapr + Kafka
- [ ] Part E: Azure AKS CI/CD pipeline
- [ ] Part F: Implement actual notification channels (email, push)
