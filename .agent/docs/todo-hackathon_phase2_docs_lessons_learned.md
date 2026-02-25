# 📚 Lessons Learned: Better Auth & Task Management Integration
**Date:** December 12, 2025
**Project:** Ultimate Todoist Clone (Hackathon Phase II)

This document records the critical technical challenges, debugging insights, and solutions discovered during the implementation of Better Auth and Task Management.

---

## 🔐 Authentication (Better Auth)

### 1. The "Hybrid Auth" Pattern
*   **Challenge**: Validating Better Auth sessions on a Python backend is complex because the `better-auth` library is primarily designed for Node.js/TypeScript. Direct database verification or JWT decoding proved unreliable due to secret key mismatches and library limitations.
*   **Lesson**: When mixing a Next.js frontend (using Better Auth) with a Python backend, a **Hybrid Approach** is most effective for hackathons:
    *   **Frontend**: Use the official `better-auth/react` client for all user interactions (login, signup, session).
    *   **Backend**: Trust the `X-User-ID` header sent by the frontend *after* verifying the user exists in the database.
*   **Solution**: We bypassed complex token validation by having the frontend send the user ID explicitly, which the backend validates against the `user` table.

### 2. Database Schema Mismatches
*   **Challenge**: Better Auth creates tables automatically with specific types (e.g., `id` as `TEXT`). Our initial backend models expected `UUID` types.
*   **Error**: `DataError: invalid input syntax for type uuid`
*   **Lesson**: Always check the *actual* database schema created by third-party tools before defining backend models.
*   **Solution**: Changed backend model fields from `uuid.UUID` to `str` to match Better Auth's text-based IDs.

---

## 🐍 Backend (FastAPI & SQLModel)

### 3. The Trailing Slash & CORS
*   **Challenge**: Frontend requests to `http://localhost:8002/api/tasks` were failing with CORS errors, while requests to `.../tasks/` (with slash) worked.
*   **Root Cause**: FastAPI redirects URLs without trailing slashes. This redirect (307 Temporary Redirect) often triggers CORS preflight failures in browsers.
*   **Lesson**: **Always use trailing slashes** in API definitions and frontend calls to avoid unnecessary redirects.
*   **Solution**: Updated all frontend API calls to append `/` (e.g., `/api/tasks/`).

### 4. Environment Variables in Subdirectories
*   **Challenge**: Running `python -m backend.main` from the root directory caused `DATABASE_URL not set` errors.
*   **Root Cause**: `load_dotenv()` looks for `.env` in the *current working directory* by default. Our `.env` was inside the `backend/` folder.
*   **Lesson**: Explicitly define the path to `.env` when your entry point is different from your configuration location.
*   **Solution**: Used `pathlib` to find the `.env` file relative to the `db.py` file:
    ```python
    backend_dir = pathlib.Path(__file__).parent
    load_dotenv(backend_dir / ".env")
    ```

### 5. UUID vs. String Type Safety
*   **Challenge**: Update and Delete operations failed with `500 Internal Server Error`.
*   **Root Cause**: The Pydantic models used `str` for IDs, but the FastAPI router parameters were typed as `id: uuid.UUID`. FastAPI tried to convert the string IDs to UUID objects, causing validation failures.
*   **Lesson**: Ensure type consistency across the entire stack: Database Column -> SQLModel -> Pydantic Schema -> API Router Parameter.
*   **Solution**: Updated all router parameters to `id: str`.

---

## ⚛️ Frontend (Next.js & React)

### 6. Undefined IDs in Event Handlers
*   **Challenge**: Deleting a task failed with `404 Not Found` because the API was called with `undefined`.
*   **Root Cause**: The `deleteTask` function signature in `TaskList.tsx` expected `(userId, taskId)`, but was called with just `(taskId)`.
*   **Lesson**: Simplify function signatures. If a value (like `userId`) is available globally or not needed, remove it from the component handler arguments.
*   **Solution**: Refactored `deleteTask` to only require `taskId`.

### 7. Optional Fields & Validation
*   **Challenge**: Creating a task without a due date failed.
*   **Root Cause**: The form was sending an empty string `""` for the date field. The backend expected either a valid ISO date string or `null`.
*   **Lesson**: Frontend forms often treat empty inputs as empty strings. APIs usually expect `null` for optional fields.
*   **Solution**: Transformed the payload before sending:
    ```javascript
    due_date: formData.due_date ? new Date(formData.due_date).toISOString() : null
    ```

---

## 🛠️ Tools & Debugging Strategy

### 8. The "Check Database" Script
*   **Strategy**: When in doubt about table names or column types, don't guess.
*   **Action**: We wrote a simple script (`check-task-table.js`) to inspect the actual database schema.
*   **Result**: This immediately revealed that our table was named `"Task"` (case-sensitive) and `user_id` was `TEXT`, saving hours of debugging.

### 9. Browser Console is King
*   **Strategy**: The "Network" tab in Chrome DevTools provided the exact error details (e.g., `422 Unprocessable Entity`, `500 Internal Server Error`) that were hidden by generic frontend error messages.
*   **Lesson**: Always look at the *Response* tab of the failed network request to see the backend's specific error message.
