# Database Schema Specification

## Overview

This document defines the database schema for the Full-Stack Web Application using SQLModel. The schema includes tables for Users and Tasks with appropriate relationships and constraints.

## Technology Stack

- **Database**: PostgreSQL (via Neon DB)
- **ORM**: SQLModel (combines SQLAlchemy and Pydantic)
- **Database Type**: Serverless, auto-scaling

## Database Tables

### 1. Users Table

The Users table stores information about registered users.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

#### Fields Description

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier for the user |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Unique username for the user |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Unique email address for the user |
| hashed_password | VARCHAR(255) | NOT NULL | Hashed password using secure algorithm |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Timestamp when user was created |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Timestamp when user was last updated |
| is_active | BOOLEAN | DEFAULT TRUE | Flag indicating if user account is active |

#### Indexes
- `idx_users_email`: Index on email field for fast lookups
- `idx_users_username`: Index on username field for fast lookups

### 2. Tasks Table

The Tasks table stores information about user tasks.

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'medium',
    due_date TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### Fields Description

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier for the task |
| user_id | UUID | NOT NULL, FOREIGN KEY | Reference to the user who owns the task |
| title | VARCHAR(255) | NOT NULL | Title of the task |
| description | TEXT | | Detailed description of the task |
| status | VARCHAR(20) | DEFAULT 'pending' | Current status: 'pending', 'completed' |
| priority | VARCHAR(20) | DEFAULT 'medium' | Priority level: 'low', 'medium', 'high' |
| due_date | TIMESTAMP WITH TIME ZONE | | Deadline for the task |
| completed_at | TIMESTAMP WITH TIME ZONE | | Timestamp when task was completed |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Timestamp when task was created |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | Timestamp when task was last updated |

#### Indexes
- `idx_tasks_user_id`: Index on user_id for fast user-specific queries
- `idx_tasks_status`: Index on status for filtering by completion status
- `idx_tasks_priority`: Index on priority for sorting by priority
- `idx_tasks_due_date`: Index on due_date for sorting by deadline
- `idx_tasks_created_at`: Index on created_at for chronological ordering

#### Check Constraints
- `chk_priority`: Ensures priority is one of ('low', 'medium', 'high')
- `chk_status`: Ensures status is one of ('pending', 'completed')
- `chk_completed_at`: Ensures completed_at is only set when status is 'completed'

## SQLModel Pydantic Models

### User Model

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class UserBase(SQLModel):
    username: str = Field(min_length=3, max_length=50, unique=True)
    email: str = Field(regex=r'^[\w\.-]+@[\w\.-]+\.\w+$', unique=True)

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserUpdate(SQLModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[str] = Field(default=None, regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')

class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")

class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool
```

### Task Model

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: str = Field(default="medium", regex=r'^(low|medium|high)$')
    due_date: Optional[datetime] = Field(default=None)
    status: str = Field(default="pending", regex=r'^(pending|completed)$')

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[str] = Field(default=None, regex=r'^(low|medium|high)$')
    due_date: Optional[datetime] = Field(default=None)
    status: Optional[str] = Field(default=None, regex=r'^(pending|completed)$')

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    completed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: "User" = Relationship(back_populates="tasks")

class TaskPublic(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
```

## Database Relationships

### One-to-Many Relationship
- **Users to Tasks**: One user can have many tasks
- Implemented via `user_id` foreign key in the tasks table
- Cascading delete: When a user is deleted, all their tasks are also deleted

## Migration Strategy

### Initial Migration
1. Create users table
2. Create tasks table
3. Add indexes to both tables
4. Add check constraints to tasks table

### Future Migration Considerations
- Soft delete option for tasks (add `deleted_at` field)
- Task categories or tags (many-to-many relationship)
- Task sharing between users
- Recurring tasks

## Performance Considerations

### Indexes
- Proper indexing on frequently queried fields (user_id, status, priority)
- Composite indexes for common query patterns
- Regular monitoring of query performance

### Connection Pooling
- Use connection pooling with Neon DB
- Configure appropriate pool sizes based on expected load
- Implement retry logic for connection failures

## Security Considerations

### Data Encryption
- Database-level encryption for sensitive data
- Secure password hashing using bcrypt or similar
- Proper handling of connection credentials

### Access Control
- Database user with minimal required privileges
- Connection encryption (TLS/SSL)
- Audit logging for sensitive operations