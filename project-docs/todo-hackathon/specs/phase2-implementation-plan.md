# Phase II Implementation Plan - Better Auth Integration

## Goal

Implement Better Auth with JWT tokens to enable secure, multi-user todo application with proper user isolation.

## Current State Analysis

### What's Working ✅
- Backend FastAPI with basic JWT auth
- Frontend Next.js with task UI
- Neon PostgreSQL database
- Task CRUD operations
- Basic API client (`frontend/src/lib/api.ts`)

### What's Broken ❌
- `better-auth` package installed but not configured
- No Better Auth API routes in frontend
- Frontend trying to access `/api/auth/[...all]` (doesn't exist)
- PostgreSQL connection timeouts from Better Auth
- No JWT verification in backend
- No user isolation (all users see all tasks)

## Implementation Steps

### Step 1: Configure Better Auth in Frontend

#### 1.1 Create Auth Configuration
**File**: `frontend/src/lib/auth.ts` (NEW)

```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  database: {
    provider: "postgres",
    url: process.env.DATABASE_URL!,
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Disable for hackathon
  },
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET!,
      expiresIn: "7d",
    }),
  ],
  trustedOrigins: [
    "http://localhost:3000",
    "http://localhost:3001",
    process.env.NEXT_PUBLIC_APP_URL || "",
  ],
});

export type Session = typeof auth.$Infer.Session;
```

#### 1.2 Create API Route Handler
**File**: `frontend/src/app/api/auth/[...all]/route.ts` (NEW)

```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

#### 1.3 Update Environment Variables
**File**: `frontend/.env.local` (UPDATE)

```env
DATABASE_URL=<your-neon-db-url>
BETTER_AUTH_SECRET=<generate-random-32-char-string>
NEXT_PUBLIC_APP_URL=http://localhost:3001
```

#### 1.4 Create Auth Client
**File**: `frontend/src/lib/auth-client.ts` (NEW)

```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3001",
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

### Step 2: Update Frontend Auth Page

#### 2.1 Modify Auth Page to Use Better Auth
**File**: `frontend/src/app/auth/page.tsx` (MODIFY)

Replace current implementation with Better Auth hooks:

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { signIn, signUp } from '@/lib/auth-client';

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isLogin) {
        const result = await signIn.email({
          email,
          password,
        });
        
        if (result.error) {
          setError(result.error.message);
          return;
        }
      } else {
        const result = await signUp.email({
          email,
          password,
          name: username,
        });
        
        if (result.error) {
          setError(result.error.message);
          return;
        }
      }

      router.push('/');
      router.refresh();
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  // ... rest of UI code remains same
}
```

### Step 3: Update API Client with JWT

#### 3.1 Modify API Client to Use Better Auth Session
**File**: `frontend/src/lib/api.ts` (MODIFY)

```typescript
import { authClient } from './auth-client';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

// Get JWT token from Better Auth session
const getAuthToken = async () => {
  const session = await authClient.getSession();
  return session?.data?.session?.token;
};

// Helper function to add auth headers
const getAuthHeaders = async () => {
  const token = await getAuthToken();
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
  };
};

export const api = {
  getTasks: async (userId: string) => {
    const res = await fetch(`${API_URL}/api/${userId}/tasks`, {
      headers: await getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch tasks');
    return res.json();
  },

  createTask: async (userId: string, taskData: any) => {
    const res = await fetch(`${API_URL}/api/${userId}/tasks`, {
      method: 'POST',
      headers: await getAuthHeaders(),
      body: JSON.stringify(taskData),
    });
    if (!res.ok) throw new Error('Failed to create task');
    return res.json();
  },

  // ... other methods with userId parameter
};
```

### Step 4: Update Backend JWT Verification

#### 4.1 Update Auth Module
**File**: `backend/auth.py` (MODIFY)

```python
import os
import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from backend.db import get_session
from backend.models import User

# Use same secret as Better Auth
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable must be set")

ALGORITHM = "HS256"

security = HTTPBearer()

def verify_jwt_token(token: str) -> dict:
    """Verify JWT token from Better Auth."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """Get current user from JWT token."""
    token = credentials.credentials
    payload = verify_jwt_token(token)
    
    # Better Auth JWT payload structure
    user_id: str = payload.get("sub") or payload.get("userId")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

def verify_user_access(user_id: str, current_user: User):
    """Verify that the current user can access the requested user_id."""
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources",
        )
```

#### 4.2 Update Task Routes
**File**: `backend/routers/tasks.py` (MODIFY)

Add user_id parameter and verification to all endpoints:

```python
from backend.auth import get_current_user, verify_user_access

@router.get("/{user_id}/tasks", response_model=dict)
def list_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    # ... other parameters
):
    """List tasks for authenticated user only."""
    # Verify user can access this user_id
    verify_user_access(user_id, current_user)
    
    # Query only this user's tasks
    query = select(Task).where(Task.user_id == current_user.id)
    # ... rest of implementation

@router.post("/{user_id}/tasks", response_model=dict)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create task for authenticated user."""
    verify_user_access(user_id, current_user)
    
    task = Task(
        **task_data.dict(),
        user_id=current_user.id  # Force user_id from token
    )
    # ... rest of implementation
```

### Step 5: Update Frontend to Use Session

#### 5.1 Modify Main Page
**File**: `frontend/src/app/page.tsx` (MODIFY)

```typescript
'use client';

import { useSession } from '@/lib/auth-client';
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

export default function Home() {
  const { data: session, isPending } = useSession();
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    if (session?.user?.id) {
      fetchTasks();
    }
  }, [session]);

  const fetchTasks = async () => {
    if (!session?.user?.id) return;
    
    try {
      const response = await api.getTasks(session.user.id);
      setTasks(response.data.tasks || []);
    } catch (err) {
      console.error('Error fetching tasks:', err);
    }
  };

  if (isPending) {
    return <div>Loading...</div>;
  }

  if (!session) {
    return <div>Please log in</div>;
  }

  // ... rest of component
}
```

### Step 6: Environment Variables Setup

#### Frontend `.env.local`
```env
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=your-32-char-secret-here
NEXT_PUBLIC_APP_URL=http://localhost:3001
NEXT_PUBLIC_API_URL=http://localhost:8001
```

#### Backend `.env`
```env
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=your-32-char-secret-here
```

**CRITICAL**: Both must use the SAME `BETTER_AUTH_SECRET`

## Testing Plan

### 1. Sign Up Flow
```
1. Navigate to /auth
2. Fill in username, email, password
3. Click "Create account"
4. Verify redirect to /
5. Verify tasks page loads
6. Check browser localStorage for session
```

### 2. User Isolation
```
1. Sign up as User A
2. Create 3 tasks
3. Log out
4. Sign up as User B
5. Verify User B sees 0 tasks (not User A's tasks)
6. Create 2 tasks for User B
7. Log out, log in as User A
8. Verify User A still sees only their 3 tasks
```

### 3. Token Verification
```
1. Log in
2. Open DevTools → Network
3. Create a task
4. Verify request has "Authorization: Bearer <token>" header
5. Verify backend accepts the token
6. Manually modify token in localStorage
7. Try to fetch tasks
8. Verify receives 401 Unauthorized
```

## Deployment Checklist

- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Railway/Render
- [ ] Environment variables set in both platforms
- [ ] BETTER_AUTH_SECRET matches on both
- [ ] DATABASE_URL points to Neon DB
- [ ] CORS configured for production URLs
- [ ] Test signup/login on production
- [ ] Test user isolation on production

## Success Criteria

- ✅ Users can sign up and log in
- ✅ JWT tokens are issued and verified
- ✅ Users only see their own tasks
- ✅ Attempting to access other user's data returns 403
- ✅ No PostgreSQL timeout errors
- ✅ Application works on localhost and production
