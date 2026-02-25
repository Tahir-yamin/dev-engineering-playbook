# Phase 5 - Kafka Integration Requirements

## 1. Install Kafka Python Library

```bash
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2\backend"
pip install kafka-python
```

## 2. Update Backend Environment Variables

Add to `backend/.env`:

```env
# Kafka Configuration (Phase 5)
KAFKA_ENABLED=false  # Set to 'true' when Kafka is running
KAFKA_BROKERS=localhost:9092  # Update when using Redpanda Cloud
```

## 3. Update tasks.py to Publish Events

Add this import at the top of `routers/tasks.py`:

```python
from kafka_producer import (
    publish_task_created,
    publish_task_updated, 
    publish_task_completed,
    publish_task_deleted
)
```

Then add event publishing to each endpoint:

### In create_task (after line 108):
```python
session.refresh(task)

# Phase 5: Publish event
publish_task_created(task.dict())

return {"success": True, "data": task, "message": "Task created successfully"}
```

### In update_task (after line 138):
```python
session.refresh(task)

# Phase 5: Publish event
publish_task_updated(task.dict())

return {"success": True, "data": task}
```

### In delete_task (after session.commit, line 152):
```python
session.commit()

# Phase 5: Publish event
publish_task_deleted(id, task.user_id)

return {"success": True, "message": "Task deleted"}
```

### Add new complete_task endpoint (after delete_task):
```python
@router.post("/{id}/complete")
def complete_task(
    id: str,
    session: Session = Depends(get_session)
):
    """Mark task as complete - triggers recurring task creation via Kafka"""
    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Mark as completed
    task.status = "completed"
    task.completed_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    # Phase 5: Publish event (recurring service will handle next occurrence)
    publish_task_completed(task.dict())
    
    return {"success": True, "data": task, "message": "Task completed"}
```

## 4. Testing Without Kafka

The `kafka_producer.py` is designed to work gracefully when Kafka is disabled:
- Set `KAFKA_ENABLED=false` in `.env`
- Events will be logged but not published
- Application will work normally

## 5. Testing With Kafka (Later)

When ready to test with Kafka:
1. Start Kafka: `docker run -p 9092:9092 apache/kafka:latest`
2. Set `KAFKA_ENABLED=true` in `.env`
3. Restart backend
4. Create a task and check logs for "✅ Published" messages

## 6. Kafka Topics Created

- `task.created` - New task events
- `task.updated` - Task update events
- `task.completed` - Task completion events (triggers recurring)
- `task.deleted` - Task deletion events
- `task-events` - All events (aggregate topic)

---

**Status**: Kafka producer ready ✅  
**Next**: Add event publishing to routers  
**After**: Create microservices to consume events
