---
description: Fix "Access to fetch blocked by CORS policy" errors when frontend can't reach backend
---

# CORS Errors Workflow

## When to Use
- "Access to fetch blocked by CORS policy"
- Frontend can't reach backend
- API calls fail with CORS error

---

## Step 1: Identify the Error

Browser Console Error:
```
Access to fetch at 'http://localhost:8000/api/tasks' from origin 
'http://localhost:3000' has been blocked by CORS policy: No 
'Access-Control-Allow-Origin' header is present
```

---

## Step 2: Check Backend CORS Configuration

```python
# In backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Must match frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Step 3: Common CORS Fixes

### Frontend URL Not in allow_origins

```python
# Add your frontend URL
allow_origins=[
    "http://localhost:3000",      # Local dev
    "https://yourdomain.com",     # Production
]
```

### Using Environment Variable

```python
import os

origins = os.getenv("CORS_ORIGINS", '["http://localhost:3000"]')
origins = eval(origins)  # Parse JSON string

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Credentials Issue

```python
# If using cookies/auth
allow_credentials=True  # Must be True

# And never use:
# allow_origins=["*"]  # Doesn't work with credentials
```

---

## Step 4: Verify Backend is Running

// turbo
```bash
# Check backend is accessible
curl http://localhost:8000/health

# Should return: {"status": "healthy"}
```

---

## Step 5: Test CORS

```javascript
# From browser console
fetch('http://localhost:8000/api/tasks', {
  credentials: 'include'
})
.then(r => r.json())
.then(console.log)

# Should not show CORS error
```

---

## Step 6: Restart Backend

// turbo
```bash
# After changing CORS config
cd phase4/docker
docker-compose restart backend

# Or local dev
# Ctrl+C to stop
uvicorn main:app --reload
```

---

**Reference**: @.claude/backend-skills.md Skill #3
