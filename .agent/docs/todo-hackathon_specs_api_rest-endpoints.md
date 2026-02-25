# REST API Endpoints Specification

## Overview

This document defines the REST API endpoints for the Full-Stack Web Application. The API will be built using FastAPI and will follow RESTful principles for task management operations.

## Base URL

All API endpoints are prefixed with `/api/v1/` to allow for future versioning.

Base URL: `https://your-backend-domain.com/api/v1/`

## Authentication

All endpoints (except user registration and login) require authentication via JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

## Endpoints

### User Authentication Endpoints

#### POST /auth/register
Register a new user account

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "username": "username"
}
```

**Response:**
- 201 Created: User successfully registered
- 400 Bad Request: Invalid input data
- 409 Conflict: User with email already exists

#### POST /auth/login
Authenticate user and return JWT token

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
- 200 OK: Authentication successful, returns JWT token
- 401 Unauthorized: Invalid credentials

#### POST /auth/logout
Logout user (invalidate token)

**Response:**
- 200 OK: Successfully logged out

### Task Management Endpoints

#### GET /tasks
Retrieve all tasks for the authenticated user

**Query Parameters:**
- `status`: Filter by task status (all, pending, completed) - default: all
- `priority`: Filter by priority (all, low, medium, high) - default: all
- `search`: Search in task title and description
- `page`: Page number for pagination - default: 1
- `limit`: Number of items per page - default: 10, max: 100
- `sort`: Sort by field (created_at, due_date, priority) - default: created_at
- `order`: Sort order (asc, desc) - default: desc

**Response:**
- 200 OK: Successfully retrieved tasks
```json
{
  "success": true,
  "data": {
    "tasks": [...],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25,
      "total_pages": 3
    }
  }
}
```
- 401 Unauthorized: User not authenticated

#### GET /tasks/{id}
Retrieve a specific task by ID

**Path Parameters:**
- `id`: Task ID

**Response:**
- 200 OK: Task found and returned
- 401 Unauthorized: User not authenticated
- 403 Forbidden: User doesn't own this task
- 404 Not Found: Task not found

#### POST /tasks
Create a new task

**Request Body:**
```json
{
  "title": "Task title",
  "description": "Task description (optional)",
  "priority": "high|medium|low (optional, default: medium)",
  "due_date": "2023-12-31T23:59:59Z (optional)",
  "completed": false (optional, default: false)
}
```

**Response:**
- 201 Created: Task successfully created
- 400 Bad Request: Invalid input data
- 401 Unauthorized: User not authenticated

#### PUT /tasks/{id}
Update an existing task

**Path Parameters:**
- `id`: Task ID

**Request Body:**
```json
{
  "title": "Updated task title (optional)",
  "description": "Updated task description (optional)",
  "priority": "high|medium|low (optional)",
  "due_date": "2023-12-31T23:59:59Z (optional)",
  "completed": false (optional)
}
```

**Response:**
- 200 OK: Task successfully updated
- 400 Bad Request: Invalid input data
- 401 Unauthorized: User not authenticated
- 403 Forbidden: User doesn't own this task
- 404 Not Found: Task not found

#### PATCH /tasks/{id}/complete
Toggle task completion status

**Path Parameters:**
- `id`: Task ID

**Request Body:**
```json
{
  "completed": true|false
}
```

**Response:**
- 200 OK: Task completion status updated
- 401 Unauthorized: User not authenticated
- 403 Forbidden: User doesn't own this task
- 404 Not Found: Task not found

#### DELETE /tasks/{id}
Delete a specific task

**Path Parameters:**
- `id`: Task ID

**Response:**
- 200 OK: Task successfully deleted
- 401 Unauthorized: User not authenticated
- 403 Forbidden: User doesn't own this task
- 404 Not Found: Task not found

### User Profile Endpoints

#### GET /profile
Retrieve authenticated user's profile information

**Response:**
- 200 OK: User profile returned
- 401 Unauthorized: User not authenticated

#### PUT /profile
Update authenticated user's profile information

**Request Body:**
```json
{
  "username": "new_username (optional)",
  "email": "new_email@example.com (optional)"
}
```

**Response:**
- 200 OK: Profile successfully updated
- 400 Bad Request: Invalid input data
- 401 Unauthorized: User not authenticated
- 409 Conflict: Email already exists

## Error Codes

- `AUTH_REQUIRED`: Authentication required
- `FORBIDDEN`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `VALIDATION_ERROR`: Request validation failed
- `DUPLICATE_RESOURCE`: Resource already exists
- `INTERNAL_ERROR`: Internal server error occurred
- `BAD_REQUEST`: Malformed request

## Rate Limiting

- API endpoints are rate-limited to 1000 requests per hour per user
- Exceeding the limit returns HTTP 429 Too Many Requests

## Content Type

All requests and responses use `application/json` content type.