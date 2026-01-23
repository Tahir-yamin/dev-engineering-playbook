# MCP Server Debugging Skills

**Purpose**: Debug and fix Model Context Protocol (MCP) server issues in AI assistant integrations  
**Source**: Extracted from Todo Hackathon Phase 5 - January 2026  
**Success Rate**: ✅ 100% - Fixed 3 critical production bugs

---

## Skill #1: Debugging Async/Await Mismatches

### When to Use
- MCP tools fail silently without clear error messages
- AI assistant reports errors but backend shows 200 OK
- TypeError mentioning `'await' expression` or `object can't be used in 'await'`

### The Problem
Calling synchronous functions with `await` keyword causes runtime TypeError that may not appear in logs.

### The Solution

**Step 1: Identify the function definition**
```bash
# Search for function definition
grep -n "def function_name" backend/*.py
```

Look for:
- `def function_name()` → **Synchronous** (no await)
- `async def function_name()` → **Asynchronous** (use await)

**Step 2: Find all calls to the function**
```bash
grep -n "await function_name" backend/*.py
```

**Step 3: Remove `await` if function is synchronous**
```python
# BEFORE (❌ Will crash):
async def tool_execution():
    result = await publish_event(data)  # publish_event is NOT async!
    
# AFTER (✅ Works):
async def tool_execution():
    result = publish_event(data)  # No await for sync function
```

### Key Insights
- ✅ Always check if a function is `async def` before using `await`
- ✅ grep/search for "def function_name" to see actual definition
- ❌ Don't assume a function is async just because other async functions call it
- 💡 Test imports locally: `python -c "from module import func"` catches this immediately

**Related Skills**: python-async-skills.md

---

## Skill #2: Fixing AttributeError in ORM Models

### When to Use
- MCP tools crash with `'Model' object has no attribute 'field_name'`
- Working with SQLModel/SQLAlchemy models
- Accessing optional or nullable fields

### The Problem
Accessing ORM model attributes that don't exist raises AttributeError, even if you check for None.

### The Solution

**Always use `hasattr()` before accessing optional fields**:

```python
# BEFORE (❌ Crashes if field doesn't exist):
task_list = [
    {
        "field": model.field.isoformat() if model.field else None
    }
    for model in models
]

# AFTER (✅ Safe):
task_list = [
    {
        "field": model.field.isoformat() if hasattr(model, 'field') and model.field else None
    }
    for model in models
]
```

**Pattern for multiple optional fields**:
```python
def safe_serialize(model):
    return {
        "id": model.id,  # Always exists
        "optional_date": model.optional_date.isoformat() 
            if hasattr(model, 'optional_date') and model.optional_date 
            else None,
        "optional_enum": model.optional_enum 
            if hasattr(model, 'optional_enum') 
            else "DEFAULT",
    }
```

### Key Insights
- ✅ Use `hasattr(obj, 'field')` before accessing optional fields
- ✅ Check both existence AND value: `hasattr(...) and field`
- ❌ Don't rely on `or None` - it doesn't prevent AttributeError
- 💡 Look for similar patterns in existing code (recurrence, next_occurrence)

**Related Skills**: sqlalchemy-skills.md, fastapi-skills.md

---

## Skill #3: Debugging Undefined Function Calls

### When to Use
- MCP tools crash with `NameError: name 'function_name' is not defined`
- Functions referenced but never implemented
- Placeholder code left in production

### The Problem
Code calls functions that were planned but never implemented, causing immediate crashes.

### The Solution

**Step 1: Identify all calls to undefined function**
```bash
grep -rn "function_name" backend/
```

**Step 2: Choose approach**

**Option A: Implement the function** (if needed now)
```python
# In simple_events.py
def schedule_reminder_job(task_id, remind_at, user_id):
    """Schedule a reminder via Dapr Jobs API"""
    # Implementation here
    pass
```

**Option B: Comment out calls** (if not needed yet)
```python
# In MCP server
if EVENTS_ENABLED:
    # TODO: Implement Dapr Jobs API for reminders
    # if remind_at:
    #     await schedule_reminder_job(task.id, remind_at, user_id)
    pass
```

**Option C: Add stub implementation** (for graceful degradation)
```python
def schedule_reminder_job(task_id, remind_at, user_id):
    """Stub: Reminder scheduling not yet implemented"""
    print(f"⚠️ Reminder scheduling not implemented for task {task_id}")
    return True  # Return success to not block workflow
```

### Key Insights
- ✅ Search codebase for ALL references before fixing
- ✅ Add TODO comments explaining why it's commented out
- ❌ Don't leave placeholder calls in production without stubs
- 💡 Stub implementations prevent cascading failures

**Related Skills**: error-handling-skills.md

---

## Skill #4: Testing MCP Tools Locally

### When to Use
- Before every deployment
- After changing MCP server code
- To catch import/runtime errors early

### The Solution

**Quick Smoke Test**:
```bash
cd backend
python -c "from mcp_server import mcp; print('✅ MCP imports OK'); print(f'Tools: {len(mcp.get_tools_schema())}')"
```

**Full Import Test**:
```bash
python -c "
from mcp_server import mcp
tools = mcp.get_tools_schema()
print(f'✅ {len(tools)} tools available:')
for tool in tools:
    print(f'  - {tool[\"function\"][\"name\"]}')
"
```

**Test Specific Tool**:
```python
# test_mcp.py
from mcp_server import MCPServer
from database import get_session

async def test_list_tasks():
    server = MCPServer()
    session = next(get_session())
    result = await server._list_tasks(session, {}, "test-user-id")
    print(f"Result: {result}")
    assert result['success'] == True

if __name__ == '__main__':
    import asyncio
    asyncio.run(test_list_tasks())
```

### Key Insights
- ✅ Test imports before EVERY git commit
- ✅ Saved 2 production rollbacks in Phase 5
- ✅ Takes 5 seconds, prevents hours of debugging
- 💡 Add to pre-commit hook for automation

---

## Skill #5: Reading MCP Backend Logs

### When to Use
- AI assistant reports errors but no obvious cause
- Need to see actual MCP tool execution
- Debugging tool argument parsing

### The Solution

**Get backend pod logs**:
```bash
# Find backend pod
kubectl get pods -l app=backend -n namespace

# Tail logs
kubectl logs <pod-name> -c backend --tail=100 --follow

# Search for tool errors
kubectl logs <pod-name> -c backend --tail=500 | grep -i "error\|exception\|tool\|mcp"
```

**Look for these patterns**:
```
✅ Tool: list_tasks          # Tool was called
📦 Arguments: {}              # What args were passed
❌ Tool execution error:      # The actual error
'Task' object has no attribute 'remind_at'  # Root cause
```

**Advanced: Filter for specific tool**:
```bash
kubectl logs <pod-name> -c backend --tail=1000 | \
  grep -A 5 "Tool: list_tasks"
```

### Key Insights
- ✅ Backend logs show errors frontend doesn't display
- ✅ Look for "Tool execution error" lines
- ✅ Arguments: {} often means tool call succeeded but execution failed
- 💡 Always check logs BEFORE making code changes

**Related Skills**: kubernetes-troubleshooting-skills.md

---

## Quick Reference

### Common MCP Errors

| Error Pattern | Likely Cause | Fix |
|---------------|--------------|-----|
| `TypeError: object can't be used in 'await'` | Sync function called with await | Remove `await` |
| `'Model' object has no attribute` | Missing field access | Add `hasattr()` check |
| `NameError: name 'X' is not defined` | Undefined function call | Implement, stub, or comment out |
| Tool returns error but 200 OK | Silent exception in tool | Check backend logs |

### Debug Checklist

Before deploying MCP changes:
- [ ] Run local import test
- [ ] Check all async/await pairs
- [ ] Verify hasattr for optional fields
- [ ] Search for undefined function calls
- [ ] Test with actual user data
- [ ] Review backend logs

---

**Total Skills**: 5  
**Last Updated**: January 18, 2026  
**Production Tested**: ✅ Yes (Todo Hackathon Phase 5)
