# Python Async/Await Patterns and Debugging

**Purpose**: Understand and debug async/await issues in FastAPI and Python  
**Source**: Phase 5 MCP async/await bugs  
**Date**: January 2026

---

## Skill #1: Identifying Async vs Sync Functions

### When to Use
- Getting TypeError about await expressions
- Unsure if function should be called with await
- Debugging async code

### The Problem
Python async/await errors can be subtle and misleading.

### The Solution

**Check function definition**:
```python
# Synchronous function
def sync_function():
    return "result"

# Asynchronous function
async def async_function():
    return "result"
```

**How to call**:
```python
# Sync function - NO await
result = sync_function()

# Async function - MUST await
result = await async_function()

# In non-async context
import asyncio
result = asyncio.run(async_function())
```

**Search for definition**:
```bash
# Find function definition
grep -n "def function_name" **/*.py
grep -n "async def function_name" **/*.py
```

### Key Insights
- ✅ Look for `async` keyword in definition
- ✅ Can't use `await` outside async functions
- ❌ Can't await synchronous functions
- 💡 IDE shows async functions with different color/icon

---

## Skill #2: Common Async/Await Errors

### When to Use
- Debugging TypeError or RuntimeError
- Understanding cryptic async error messages

### The Problem
Async errors have confusing messages.

### The Solution

**Error: "object X can't be used in 'await' expression"**
```python
# WRONG - sync function called with await
def sync_func():
    return True

await sync_func()  # ❌ TypeError
```

**Fix**: Remove `await`
```python
sync_func()  # ✅ Correct
```

---

**Error: "coroutine was never awaited"**
```python
# WRONG - async function called without await
async def async_func():
    return True

result = async_func()  # ❌ Returns coroutine object, not result
```

**Fix**: Add `await`
```python
result = await async_func()  # ✅ Correct
```

---

**Error: "await outside async function"**
```python
# WRONG - using await in sync function
def regular_function():
    result = await async_func()  # ❌ SyntaxError
```

**Fix**: Make function async
```python
async def regular_function():
    result = await async_func()  # ✅ Correct
```

### Key Insights
- ✅ Await only works inside async functions
- ✅ Async functions must be awaited (in async context)
- ✅ Mix sync/async carefully
- 💡 Use `asyncio.run()` at top level

---

## Skill #3: Async in FastAPI Routes

### When to Use
- Creating FastAPI endpoints
- Deciding between sync and async routes

### The Problem
FastAPI supports both sync and async, but choice matters for performance.

### The Solution

**Async route** (use for I/O operations):
```python
@app.get("/users")
async def get_users():
    # Can await here
    users = await db.fetch_all("SELECT * FROM users")
    return users
```

**Sync route** (use for CPU-bound or simple operations):
```python
@app.get("/calculate")
def calculate(x: int, y: int):
    # NO await
    result = x + y
    return {"result": result}
```

**Mixed approach**:
```python
@app.post("/task")
async def create_task(task: Task):
    # Async database call
    db_task = await session.add(task)
    
    # Sync event publishing (non-blocking)
    publish_event("task.created", db_task)  # No await!
    
    return db_task
```

### Key Insights
- ✅ Use async if you await anything inside
- ✅ Use sync for simple calculations
- ✅ Can call sync from async (but not vice versa in route)
- 💡 FastAPI runs sync routes in thread pool

---

## Skill #4: Debugging with Print Statements

### When to Use
- Understanding execution flow
- Finding where coroutine isn't awaited

### The Solution

**Check if function is being called**:
```python
async def my_function():
    print("✅ Function started")  # Will print if awaited
    result = await some_operation()
    print("✅ Function completed")  # Will print if completes
    return result

# If you only see returns coroutine in logs → not awaited
# If you see "started" but not "completed" → error during execution
```

**Check async/sync mix**:
```python
def sync_function():
    print("🔵 SYNC function called")
    return True

async def async_function():
    print("🔴 ASYNC function called")
    return True

# In your code
print(f"Type: {type(sync_function())}")   # <class 'bool'>
print(f"Type: {type(async_function())}")  # <class 'coroutine'>
```

### Key Insights
- ✅ Print helps identify sync/async issues
- ✅ Coroutine objects mean missing await
- ✅ Add prints at entry/exit of functions
- 💡 Use emojis to distinguish log types

---

## Skill #5: Async Best Practices

### When to Use
- Writing new async code
- Refactoring sync to async

### The Solution

**DO**:
```python
# ✅ Consistent async chain
async def route():
    result = await service_function()
    return result

async def service_function():
    data = await repository_function()
    return process(data)

async def repository_function():
    return await db.query("SELECT...")
```

**DON'T**:
```python
# ❌ Breaking async chain
async def route():
    result = sync_service()  # Lost async benefit
    return result

def sync_service():  # Not async!
    data = await repository()  # ❌ SyntaxError
```

**Mixed correctly**:
```python
async def route():
    # Async I/O
    db_data = await fetch_from_db()
    
    # Sync processing (CPU-bound)
    processed = process_data(db_data)  # No await needed
    
    # Async I/O again
    await save_to_cache(processed)
    
    return processed
```

### Key Insights
- ✅ Keep async chain for I/O operations
- ✅ Sync functions for pure calculations
- ✅ Don't await sync functions
- 💡 Async doesn't make code faster, just more efficient

---

## Quick Reference

### Decision Tree: Async or Sync?

```
Does function do I/O? (database, API, file)
  ↓ YES
  Is the I/O library async? (httpx, asyncpg, motor)
    ↓ YES  
    → Use async def + await
    ↓ NO
    → Use sync def (runs in thread pool)
  ↓ NO
  Is it just calculations/logic?
    ↓ YES
    → Use sync def
```

### Common Async Libraries

| Type | Sync | Async |
|------|------|-------|
| HTTP Client | requests | httpx, aiohttp |
| Database | psycopg2 | asyncpg |
| MongoDB | pymongo | motor |
| Redis | redis-py | aioredis |
| File I/O | open() | aiofiles |

### FastAPI Route Guidelines

```python
# I/O heavy → async
@app.get("/users")
async def get_users():
    return await db.fetch_all()

# CPU heavy → sync (thread pool)
@app.post("/calculate")
def calculate(data):
    return heavy_calculation(data)

# Mixed → async (for flexibility)
@app.post("/task")
async def create_task(task):
    result = await db.save(task)
    process_sync(result)  # Sync is fine
    return result
```

---

**Total Skills**: 5  
**Last Updated**: January 18, 2026  
**Production Tested**: ✅ Fixed 2 async bugs in Phase 5
