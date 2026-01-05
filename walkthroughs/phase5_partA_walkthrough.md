# Phase 5 Part A: Database & Event Architecture - Walkthrough

**Completed**: January 5, 2026  
**Duration**: ~45 minutes

---

## What Was Implemented

### 1. Database Schema Updates

**File**: [models.py](file:///d:/Hackathon%20phase%201%20TODO%20App/todo_hackathon_phase1/phase2/backend/models.py)

Added Phase 5 fields to the Task model:

| Field | Type | Purpose |
|-------|------|---------|
| `recurrence_type` | Optional[str] | NONE, DAILY, WEEKLY, MONTHLY, YEARLY |
| `recurrence_details` | Optional[str] | JSON string for complex rules |
| `remind_at` | Optional[datetime] | When to send reminder |
| `next_occurrence_at` | Optional[datetime] | Next trigger time for recurring tasks |
| `last_triggered_at` | Optional[datetime] | Last time recurrence was triggered |

Also created `TaskFilter` model for advanced search/filter/sort:

```python
class TaskFilter(SQLModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    due_before: Optional[datetime] = None
    due_after: Optional[datetime] = None
    tags: Optional[str] = None
    has_recurrence: Optional[bool] = None
    sort_by: str = "created_at"  # created_at, due_date, priority, title
    sort_order: str = "desc"  # asc, desc
```

---

### 2. Events Module (Dapr Pub/Sub)

**File**: [events.py](file:///d:/Hackathon%20phase%201%20TODO%20App/todo_hackathon_phase1/phase2/backend/events.py)

Created a complete event-driven module with:

| Function | Purpose |
|----------|---------|
| `publish_event()` | Generic event publisher via Dapr |
| `publish_task_event()` | Publish task CRUD events |
| `schedule_reminder()` | Publish reminder events |
| `publish_task_update_for_sync()` | Real-time client sync |
| `schedule_reminder_job()` | Dapr Jobs API for exact-time reminders |
| `cancel_reminder_job()` | Cancel scheduled reminders |

**Kafka Topics**:
- `task-events` - All task CRUD operations
- `reminders` - Scheduled reminder triggers
- `task-updates` - Real-time client sync

---

### 3. Dapr Components

Created 3 Dapr component YAML files in `phase4/dapr-components/`:

| File | Component | Purpose |
|------|-----------|---------|
| [kafka-pubsub.yaml](file:///d:/Hackathon%20phase%201%20TODO%20App/todo_hackathon_phase1/phase4/dapr-components/kafka-pubsub.yaml) | pubsub.kafka | Kafka event streaming |
| [statestore.yaml](file:///d:/Hackathon%20phase%201%20TODO%20App/todo_hackathon_phase1/phase4/dapr-components/statestore.yaml) | state.postgresql | Conversation state in NeonDB |
| [secrets.yaml](file:///d:/Hackathon%20phase%201%20TODO%20App/todo_hackathon_phase1/phase4/dapr-components/secrets.yaml) | secretstores.kubernetes | Secure credential access |

---

### 4. Strimzi Kafka Cluster

**File**: [kafka-cluster.yaml](file:///d:/Hackathon%20phase%201%20TODO%20App/todo_hackathon_phase1/phase4/kubernetes/kafka-cluster.yaml)

Complete Kafka cluster manifest with:
- 1-replica Kafka broker (ephemeral storage for hackathon)
- 1-replica Zookeeper
- 3 pre-configured topics with appropriate retention

---

## Lessons Learned

### ✅ What Worked Well

1. **SQLModel for schema evolution**: Adding fields to existing models is straightforward
2. **Dapr abstraction**: No kafka-python library needed - simple HTTP calls!
3. **Strimzi KafkaTopic CRD**: Declarative topic creation is cleaner than CLI

### ⚠️ Challenges Encountered

1. **JSON in PostgreSQL**: Used `Optional[str]` for `recurrence_details` instead of native JSON column for SQLModel compatibility
2. **Dapr Jobs API is alpha**: v1.0-alpha1 - may change in future versions

### 💡 Key Insights

1. **Event-Driven > Polling**: Dapr Jobs API eliminates cron-based polling for reminders
2. **Separation of Concerns**: Events module is completely decoupled from models
3. **Ephemeral Storage OK for Hackathon**: Production would need persistent volumes

---

## Skills Upgraded

| Skill | Level | What Was Learned |
|-------|-------|------------------|
| SQLModel | ⬆️ Advanced | Schema evolution with optional fields |
| Dapr Pub/Sub | 🆕 Intermediate | HTTP-based event publishing |
| Dapr Jobs API | 🆕 Beginner | Exact-time scheduling |
| Strimzi | 🆕 Intermediate | Kafka on Kubernetes with CRDs |

---

## Next Steps

- [ ] Part B: Integrate events with MCP tools
- [ ] Part C: Create Notification Service (consumer)
- [ ] Part D: Deploy Kafka + Dapr to Minikube
- [ ] Part E: Azure AKS deployment
