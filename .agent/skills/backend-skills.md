# Backend Skills - FastAPI & Python

**Topics**: FastAPI, Python, API design, async operations, error handling
**Version**: 1.0

---

## Skill #1: FastAPI Project Structure

### When to Use
- Starting FastAPI backend
- Organizing API code
- Scaling backend architecture

### Prompt Template

```markdown
**ROLE**: FastAPI architect

**PROJECT**: [TODO API / SaaS backend / etc]

**RECOMMENDED STRUCTURE**:
```
backend/
├── main.py                 # FastAPI app & CORS
├── requirements.txt        # Dependencies
├── routers/
│   ├── __init__.py
│   ├── tasks.py           # Task endpoints
│   ├── users.py           # User endpoints
│   └── chat.py            # AI chat endpoints
├── models/
│   └── schemas.py         # Pydantic models
├── database.py            # DB connection
├── dependencies.py        # Shared dependencies
└── utils/
    └── helpers.py
```

**MAIN.PY SETUP**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import tasks, users, chat

app = FastAPI(title="TODO API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**DELIVERABLES**:
- Complete project structure
- FastAPI configuration
- Router setup
- CORS configuration
- Health check endpoint
```

### Best Practices:
- Separate routers by feature
- Use dependency injection
- Async/await for I/O operations
- Pydantic for validation
- Auto-generated OpenAPI docs

---

## Skill #2: Pydantic Schema Validation

### When to Use
- Validating request/response data
- Type safety in Python
- Auto-generating API docs

### Prompt Template

```markdown
**ROLE**: API schema designer

**ENDPOINT**: [POST /tasks / PUT /tasks/:id / etc]

**SCHEMAS**:
```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = Field("medium", regex="^(low|medium|high)$")
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    """Schema for creating a task"""
    pass

class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    priority: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskResponse(TaskBase):
    """Schema for task response"""
    id: str
    user_id: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # For ORM models

class TaskList(BaseModel):
    """Schema for paginated task list"""
    tasks: list[TaskResponse]
    total: int
    page: int
    per_page: int
```

**CUSTOM VALIDATORS**:
```python
class TaskCreate(TaskBase):
    @validator('due_date')
    def due_date_must_be_future(cls, v):
        if v and v < datetime.now():
            raise ValueError('Due date must be in the future')
        return v
```

**DELIVERABLES**:
- Request schemas
- Response schemas
- Custom validators
- Schema inheritance
```

### Pydantic Benefits:
- Automatic validation
- Clear error messages
- Type hints for IDEs
- JSON schema generation
- OpenAPI documentation

---

## Skill #3: CORS Configuration

### When to Use
- Frontend can't access API
- "CORS policy" errors in browser
- Setting up cross-origin requests

### Prompt Template

```markdown
**ROLE**: API security engineer

**PROBLEM**: CORS blocking requests from frontend

**ERROR IN BROWSER**:
```
Access to fetch at 'http://localhost:8000/api/tasks' from origin 
'http://localhost:3000' has been blocked by CORS policy
```

**SOLUTION**:
```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specific URL
    allow_credentials=True,     # Allow cookies/auth headers
    allow_methods=["*"],        # All HTTP methods
    allow_headers=["*"],        # All headers
)

# Production (more restrictive)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)
```

**ENVIRONMENT-BASED**:
```python
import os

ALLOWED_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    '["http://localhost:3000"]'
)
origins = eval(ALLOWED_ORIGINS)  # Parse JSON string

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**DELIVERABLES**:
- CORS middleware configuration
- Environment-based origins
- Security considerations
```

### CORS Security:
- Never use `allow_origins=["*"]` with `allow_credentials=True`
- List specific origins in production
- Use environment variables for configuration
- Consider API rate limiting

---

## Skill #4: Async Database Operations

### When to Use
- Database queries in FastAPI
- Improving API performance
- Handling concurrent requests

### Prompt Template

```markdown
**ROLE**: Async Python specialist

**DATABASE**: [PostgreSQL / MySQL / MongoDB]
**ORM/CLIENT**: [Prisma Client / SQLAlchemy / Motor]

**ASYNC PATTERNS**:

**Note**: For Prisma in Python, we use the Prisma Client Python library.

```python
from prisma import Prisma
from prisma.models import Task

# Initialize Prisma client
prisma = Prisma()

# Startup event
@app.on_event("startup")
async def startup():
    await prisma.connect()

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()

# CRUD operations
@router.get("/tasks")
async def get_tasks(user_id: str):
    tasks = await prisma.task.find_many(
        where={"user_id": user_id},
        order_by={"created_at": "desc"},
        include={"user": True}  # Include relations
    )
    return tasks

@router.post("/tasks")
async def create_task(task: TaskCreate, user_id: str):
    new_task = await prisma.task.create(
        data={
            "title": task.title,
            "description": task.description,
            "user_id": user_id,
        }
    )
    return new_task

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, user_id: str):
    # Check ownership
    task = await prisma.task.find_unique(
        where={"id": task_id}
    )
    if not task or task.user_id != user_id:
        raise HTTPException(404, "Task not found")
    
    await prisma.task.delete(where={"id": task_id})
    return {"message": "Task deleted"}
```

**DELIVERABLES**:
- Async database setup
- CRUD operations
- Error handling
- Connection management
```

### Async Best Practices:
- Always use `await` for I/O operations
- Don't mix sync/async database clients
- Handle connection pools properly
- Use transactions for complex operations

---

## Skill #5: Error Handling & Status Codes

### When to Use
- Implementing proper error responses
- Debugging API issues
- Following RESTful conventions

### Prompt Template

```markdown
**ROLE**: API design specialist

**IMPLEMENT**: Proper error handling and status codes

**HTTP STATUS CODES**:
```python
from fastapi import HTTPException, status

# 200 OK - Success
return {"message": "Task created", "id": task.id}

# 201 Created - Resource created
return Response(content=json.dumps(task), status_code=201)

# 400 Bad Request - Validation error
raise HTTPException(
    status_code=400,
    detail="Invalid task data"
)

# 401 Unauthorized - Not authenticated
raise HTTPException(
    status_code=401,
    detail="Authentication required"
)

# 403 Forbidden - Authenticated but no permission
raise HTTPException(
    status_code=403,
    detail="You don't have permission to delete this task"
)

# 404 Not Found - Resource doesn't exist
raise HTTPException(
    status_code=404,
    detail=f"Task with id {task_id} not found"
)

# 500 Internal Server Error - Server error
# Let FastAPI handle automatically or:
raise HTTPException(
    status_code=500,
    detail="Internal server error"
)
```

**CUSTOM EXCEPTION HANDLER**:
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if DEBUG else "An error occurred"
        }
    )
```

**VALIDATION ERRORS** (Pydantic):
```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
```

**DELIVERABLES**:
- Proper status codes
- Error response format
- Exception handlers
- Validation error handling
```

---

## Quick Reference

### FastAPI Essentials
```python
# Path parameters
@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    ...

# Query parameters
@app.get("/tasks")
async def list_tasks(page: int = 1, per_page: int = 10):
    ...

# Request body
@app.post("/tasks")
async def create_task(task: TaskCreate):
    ...

# Headers
@app.get("/tasks")
async def list_tasks(authorization: str = Header(None)):
    ...

# Dependencies
def get_current_user(token: str = Depends(oauth2_scheme)):
    ...

@app.get("/tasks")
async def list_tasks(user: User = Depends(get_current_user)):
    ...
```

### Running FastAPI
```bash
# Development (auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000

# With workers
uvicorn main:app --workers 4

# Access docs
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

---

## Lessons Learned

### FastAPI
1. Use async/await for I/O operations
2. Pydantic validation is powerful
3. Dependency injection is your friend
4. Auto-generated docs are amazing
5. Background tasks for long operations

### API Design
1. RESTful conventions matter
2. Proper status codes improve DX
3. Consistent error format helps debugging
4. Version your API (/v1/tasks)
5. Document expected responses

### Performance
1. Use connection pooling
2. Implement caching (Redis)
3. Async for concurrent requests
4. Pagination for large datasets
5. Background tasks for heavy work

### Security
1. Validate all inputs
2. Use environment variables for secrets
3. Implement rate limiting
4. Sanitize database queries
5. HTTPS in production

---

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "CORS policy" error | CORS not configured | Add CORSMiddleware |
| Sync function blocking | Using sync in async context | Make function async |
| "Module not found" | Missing dependency | pip install package |
| Slow endpoint | N+1 queries | Use includes/joins |
| 422 Unprocessable Entity | Pydantic validation failed | Check request schema |

---

## Related Skills
- Phase 2: API implementation
- Database Skills: Async operations
- Frontend Skills: API integration
- Docker Skills: Containerizing FastAPI

**FastAPI makes building APIs fast and enjoyable!**
