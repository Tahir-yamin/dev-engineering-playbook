# 💻 Path 0: Core Stack Upgrade (Web Development Expert)

**Goal**: Master the advanced patterns of the tools you already use (Next.js, FastAPI, Postgres).
**Timeline**: 2025 Q1

---

## 1. Next.js 15 & Server Actions
Move beyond basic API routes to a fully server-integrated application.

- **Tools**: Next.js 15, React Server Components (RSC)

### 🔬 Micro-Skills
1.  **Server Actions vs API Routes**:
    -   *Skill*: Knowing when to use `use server` (mutations) vs Route Handlers (webhooks/external APIs).
    -   *Test*: Build a form that works without JavaScript enabled.
2.  **Cache Revalidation**:
    -   *Skill*: Using `revalidatePath` vs `revalidateTag` for surgical cache updates.
    -   *Test*: Update a Todo title and see it reflect instantly on the dashboard without a page reload.
3.  **Streaming UI**:
    -   *Skill*: Wrapping slow components in `<Suspense>` boundaries.
    -   *Test*: Artificial 3s delay on the "Todo List" component, but show the "Add Todo" form instantly.

### 🛠️ Workflow: Refactor to Server Actions
1.  **Identify**: Find a `useEffect` that fetches data or an `onSubmit` that calls `fetch()`.
2.  **Create Action**: Make a `actions.ts` file with `use server`.
3.  **Migrate Logic**: Move the DB call from the API route to the Action.
4.  **Bind**: Use the `action={createTodo}` prop on the `<form>`.
5.  **Optimistic**: Wrap the UI state with `useOptimistic` for instant feedback.

### Recommended Repos
- `vercel/next.js` (examples/server-actions-upload)

---

## 2. Advanced FastAPI Patterns
Write Python backends that scale like Go.

- **Tools**: FastAPI, Pydantic v2, SQLAlchemy 2.0

### 🔬 Micro-Skills
1.  **Advanced Dependency Injection**:
    -   *Skill*: Creating "Yield Dependencies" for database sessions that auto-close.
    -   *Test*: Create a `get_current_active_user` dependency that reuses `get_current_user`.
2.  **Pydantic v2 Optimization**:
    -   *Skill*: Using `model_validator` for complex cross-field validation.
    -   *Test*: Validate that `due_date` is not in the past only if `status` is "pending".
3.  **Async Database Patterns**:
    -   *Skill*: Avoiding "Implicit IO" blocking the event loop.
    -   *Test*: Run 100 concurrent requests and ensure latency doesn't spike.

### 🛠️ Workflow: Async Performance Tuning
1.  **Profile**: Use `py-spy` to find blocking calls.
2.  **Refactor DB**: Switch `session.query()` (sync) to `await session.execute(select())` (async).
3.  **Middleware**: Ensure middleware isn't blocking (use `BaseHTTPMiddleware` carefully).
4.  **Worker Config**: Tune `uvicorn` workers based on CPU cores.

### Recommended Repos
- `tiangolo/full-stack-fastapi-template`

---

## 3. PostgreSQL Performance
Stop treating the DB like a black box.

- **Tools**: PostgreSQL 16, pgvector
- **Key Concepts**:
    - **Indexing**: B-Tree vs GIN vs HNSW (for vector search).
    - **JSONB**: Using Postgres as a NoSQL store (hybrid data).
    - **Explain Analyze**: Reading query plans to find bottlenecks.

### Learning Project
1. **Analyze**: Run `EXPLAIN ANALYZE` on the "Get Todos" query.
2. **Search**: Add a GIN index to the `todos` table for full-text search.

### Recommended Repos
- `supabase/supabase`
