# Feature: Authentication with Better Auth + JWT

## Spec-Kit Status

**Phase**: Phase 2 - Full-Stack Web Application  
**Feature ID**: `authentication`  
**Last Updated**: 2025-12-18

### Implementation Status
- [x] Specified
- [x] Designed
- [x] Implemented
- [ ] Fully Tested
- [ ] Documented

### Hackathon Compliance
- [x] Requirements defined
- [x] Architecture documented
- [x] Security requirements specified
- [x] Better Auth configured
- [x] JWT verification implemented
- [ ] All security tests passing
- [ ] User documentation complete

---

## Overview

Implement user authentication using Better Auth on the frontend with JWT token integration to FastAPI backend. This ensures secure, stateless authentication where users can only access their own tasks.

## User Stories

- As a new user, I can sign up with username, email, and password
- As a registered user, I can log in with email and password
- As an authenticated user, I receive a JWT token for API access
- As an authenticated user, I can only see and manage my own tasks
- As a user, I can log out and my session is cleared

## Architecture

```
┌─────────────────┐     JWT Token      ┌──────────────────┐
│   Frontend      │ ←─────────────────→ │   Backend        │
│   (Next.js)     │                     │   (FastAPI)      │
│                 │                     │                  │
│  Better Auth    │                     │  JWT Verify      │
│  + JWT Plugin   │                     │  Middleware      │
└─────────────────┘                     └──────────────────┘
         │                                       │
         │                                       │
         ▼                                       ▼
  ┌─────────────┐                      ┌─────────────┐
  │ User Session│                      │ User Tasks  │
  │ (Browser)   │                      │ (Filtered)  │
  └─────────────┘                      └─────────────┘
```

## Technical Requirements

### Frontend (Better Auth Configuration)

1. **Install Better Auth**
   - Package: `better-auth@^1.4.5` (already installed)
   - JWT plugin for token generation

2. **Configuration File**: `frontend/src/lib/auth.ts`
   ```typescript
   import { betterAuth } from "better-auth"
   import { jwt } from "better-auth/plugins"
   
   export const auth = betterAuth({
     database: {
       provider: "postgres",
       url: process.env.DATABASE_URL
     },
     plugins: [
       jwt({
         secret: process.env.BETTER_AUTH_SECRET,
         expiresIn: "7d"
       })
     ]
   })
   ```

3. **API Route**: `frontend/src/app/api/auth/[...all]/route.ts`
   - Handle all Better Auth requests
   - Return JWT tokens on successful login/signup

4. **Environment Variables**:
   ```
   DATABASE_URL=<neon-db-connection-string>
   BETTER_AUTH_SECRET=<shared-secret-with-backend>
   ```

### Backend (FastAPI JWT Verification)

1. **Shared Secret**
   - Same `BETTER_AUTH_SECRET` as frontend
   - Used to verify JWT signatures

2. **JWT Verification Middleware**: `backend/auth.py`
   ```python
   import jwt
   from fastapi import HTTPException, Depends
   from fastapi.security import HTTPBearer
   
   SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
   
   def verify_jwt_token(token: str) -> dict:
       try:
           payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
           return payload
       except jwt.ExpiredSignatureError:
           raise HTTPException(401, "Token expired")
       except jwt.InvalidTokenError:
           raise HTTPException(401, "Invalid token")
   ```

3. **User Extraction**:
   - Extract user_id from JWT payload
   - Match with user_id in API endpoint path
   - Ensure users can only access their own data

### Database Schema

Better Auth will create its own tables:
- `user` - User accounts
- `session` - Session management
- `account` - OAuth accounts (if needed)

Our existing `tasks` table already has `user_id` foreign key.

## API Behavior Changes

### Before Authentication
```
GET /api/tasks → Returns all tasks (insecure)
```

### After Authentication
```
GET /api/{user_id}/tasks
Headers: Authorization: Bearer <jwt-token>

1. Extract JWT from header
2. Verify JWT signature
3. Extract user_id from JWT payload
4. Verify JWT user_id matches URL user_id
5. Return only tasks where task.user_id = user_id
```

## Security Requirements

1. **User Isolation**
   - Users can ONLY access their own tasks
   - Attempting to access another user's tasks returns 403 Forbidden

2. **Token Validation**
   - All API requests require valid JWT token
   - Expired tokens are rejected
   - Invalid signatures are rejected

3. **Password Security**
   - Passwords hashed with bcrypt (Better Auth default)
   - Minimum 6 characters (frontend validation)
   - Minimum 8 characters (backend validation)

4. **HTTPS in Production**
   - All authentication traffic over HTTPS
   - Secure cookie flags enabled

## Acceptance Criteria

### Sign Up
- [x] User can create account with username, email, password
- [x] Email must be unique
- [x] Password must be at least 6 characters
- [x] Successful signup returns JWT token
- [x] User is automatically logged in after signup

### Log In
- [x] User can log in with email and password
- [x] Incorrect credentials show error message
- [x] Successful login returns JWT token
- [x] Token is stored in localStorage

### Protected API Access
- [x] All task endpoints require JWT token
- [x] Requests without token receive 401 Unauthorized
- [x] Requests with invalid token receive 401 Unauthorized
- [x] Requests with expired token receive 401 Unauthorized

### User Isolation
- [x] User A cannot see User B's tasks
- [x] User A cannot modify User B's tasks
- [x] User A cannot delete User B's tasks
- [x] Attempting to access other user's data returns 403 Forbidden

### Log Out
- [x] User can log out
- [x] Token is removed from localStorage
- [x] User is redirected to login page
- [x] Subsequent API requests fail with 401

## Error Handling

| Scenario | Status Code | Message |
|----------|-------------|---------|
| No token provided | 401 | "Authentication required" |
| Invalid token | 401 | "Invalid token" |
| Expired token | 401 | "Token expired" |
| User mismatch | 403 | "Access denied" |
| Email already exists | 400 | "Email already registered" |
| Invalid credentials | 401 | "Invalid email or password" |

## Testing Scenarios

1. **Happy Path**
   - Sign up → Receive token → Access tasks → Log out

2. **User Isolation**
   - User A signs up → Creates tasks
   - User B signs up → Cannot see User A's tasks

3. **Token Expiry**
   - Log in → Wait 7 days → Token expires → Must log in again

4. **Invalid Access**
   - User A gets token
   - User A tries GET /api/user-b-id/tasks
   - Receives 403 Forbidden

## Implementation Notes

- Better Auth handles user table creation automatically
- JWT tokens are stateless (no server-side session storage)
- Frontend stores token in localStorage
- Backend verifies token on every request
- No need for session cookies or Redis

## References

- Better Auth Docs: https://better-auth.com
- JWT Plugin: https://better-auth.com/docs/plugins/jwt
- FastAPI JWT: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
