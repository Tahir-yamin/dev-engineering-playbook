# Phase II: Full-Stack Web App Specification

## Overview
This specification defines the requirements for the full-stack web application that will transition from the current CLI-based todo app to a web-based application with both frontend and backend components.

## API Endpoints

### Task Management Endpoints

#### GET /api/tasks
- **Description**: Retrieve all tasks with optional filtering
- **Method**: GET
- **Parameters**:
  - `status` (optional): Filter by task status (pending/completed)
  - `priority` (optional): Filter by task priority (Low/Medium/High)
  - `due_date` (optional): Filter by due date (YYYY-MM-DD)
- **Response**:
  - Status: 200 OK
  - Body: Array of Task objects

#### GET /api/tasks/{id}
- **Description**: Retrieve a specific task by ID
- **Method**: GET
- **Path Parameter**: `id` (task ID)
- **Response**:
  - Status: 200 OK (success) / 404 Not Found (task not found)
  - Body: Single Task object

#### POST /api/tasks
- **Description**: Create a new task
- **Method**: POST
- **Request Body**:
  ```json
  {
    "title": "Task title (required)",
    "description": "Task description (optional)",
    "priority": "Priority level (Low/Medium/High, default: Medium)",
    "due_date": "Due date (YYYY-MM-DD format, optional)",
    "status": "Task status (pending/completed, default: pending)"
  }
  ```
- **Response**:
  - Status: 201 Created (success) / 400 Bad Request (invalid input)
  - Body: Created Task object

#### PUT /api/tasks/{id}
- **Description**: Update an existing task
- **Method**: PUT
- **Path Parameter**: `id` (task ID)
- **Request Body** (all fields optional):
  ```json
  {
    "title": "New task title (optional)",
    "description": "New task description (optional)",
    "priority": "New priority level (Low/Medium/High, optional)",
    "due_date": "New due date (YYYY-MM-DD format, optional)",
    "status": "New task status (pending/completed, optional)"
  }
  ```
- **Response**:
  - Status: 200 OK (success) / 404 Not Found (task not found) / 400 Bad Request (invalid input)
  - Body: Updated Task object

#### DELETE /api/tasks/{id}
- **Description**: Delete a task by ID
- **Method**: DELETE
- **Path Parameter**: `id` (task ID)
- **Response**:
  - Status: 200 OK (success) / 404 Not Found (task not found)
  - Body: Confirmation message

## Database Schema

### Task Model
The Task model will be implemented using SQLAlchemy/SQLModel with the following fields:

#### Fields:
- `id`: Integer (Primary Key, Auto-increment)
- `title`: String (255 characters max, NOT NULL)
- `description`: Text (optional, nullable)
- `priority`: String (Enum: 'Low', 'Medium', 'High', default: 'Medium')
- `due_date`: Date (optional, nullable)
- `status`: String (Enum: 'pending', 'completed', default: 'pending')
- `created_at`: DateTime (default: current timestamp)
- `updated_at`: DateTime (default: current timestamp, updates on modification)

#### Example SQL Schema:
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(10) DEFAULT 'Medium' CHECK (priority IN ('Low', 'Medium', 'High')),
    due_date DATE,
    status VARCHAR(10) DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Frontend Pages

### 1. Task List Page (`/tasks` or `/`)
- **Purpose**: Display all tasks with filtering and sorting capabilities
- **Components**:
  - Task list with each task showing title, priority, due date, and status
  - Filter controls for priority, status, and due date
  - Search functionality
  - Add new task button/form
  - Edit/delete buttons for each task

- **Features**:
  - Display tasks in a clean, responsive layout
  - Visual indicators for priority (color coding)
  - Due date warnings for overdue tasks
  - Status toggle (completed/pending)
  - Pagination for large task lists

### 2. Add Task Form (`/tasks/new` or modal on main page)
- **Purpose**: Create new tasks with all required fields
- **Form Fields**:
  - Title (required, text input)
  - Description (optional, textarea)
  - Priority (required, dropdown: Low/Medium/High)
  - Due Date (optional, date picker)
  - Status (optional, default to 'pending')

- **Features**:
  - Form validation
  - Real-time feedback
  - Success/error messages
  - Redirect to task list after creation

### 3. Edit Task Form (`/tasks/{id}/edit` or modal)
- **Purpose**: Update existing tasks
- **Form Fields** (same as Add Task Form but pre-filled with existing values):
  - Title (text input)
  - Description (textarea)
  - Priority (dropdown: Low/Medium/High)
  - Due Date (date picker)
  - Status (dropdown: pending/completed)

- **Features**:
  - Pre-populate with existing task data
  - Form validation
  - Success/error messages
  - Redirect to task list after update

## Authentication & Authorization
- Basic authentication system (to be defined in future iteration)
- User-specific task isolation

## Error Handling
- 400 Bad Request: Invalid input data
- 404 Not Found: Resource not found
- 500 Internal Server Error: Server-side errors

## Validation Rules
- Title: Required, minimum 1 character, maximum 255 characters
- Description: Optional, maximum 1000 characters
- Priority: Must be one of 'Low', 'Medium', 'High'
- Due Date: Must be in YYYY-MM-DD format or null
- Status: Must be one of 'pending', 'completed'

## Frontend Technologies
- Next.js 14+ with App Router
- TypeScript
- Tailwind CSS for styling
- React Query or SWR for data fetching and caching

## Backend Technologies
- FastAPI for the API framework
- SQLAlchemy/SQLModel for ORM
- PostgreSQL for database (to be configured)
- Pydantic for data validation