# Phase 2 Skills - Full-Stack Development

**Phase**: 2 - Core Implementation
**Topics**: Next.js, FastAPI, CRUD operations, API integration, UI components
**Version**: 1.0

---

## Skill #1: Next.js 14 App Router Setup

### When to Use
- Setting up Next.js with App Router
- Configuring for production
- Setting up layouts and routing

### Prompt Template

```markdown
**ROLE**: Next.js specialist

**REQUIREMENTS**:
- Next.js version: 14+
- Router: App Router (not Pages Router)
- Styling: [TailwindCSS / CSS Modules / Styled Components]
- Features needed: [List features]

**SETUP TASKS**:
1. Initialize Next.js project with App Router
2. Configure next.config.js for:
   - Standalone output (for Docker)
   - API URL configuration
   - Image optimization
3. Set up root layout with metadata
4. Create folder structure (app/, components/, lib/)
5. Configure TailwindCSS
6. Set up fonts and global styles

**DELIVERABLES**:
- Complete project structure
- Configured next.config.js
- Root layout with proper metadata
- Sample page to verify setup
```

---

## Skill #2: FastAPI Backend Architecture

### When to Use
- Setting up Python FastAPI backend
- Designing API routes
- Implementing CRUD operations

### Prompt Template

```markdown
**ROLE**: Backend architect specializing in FastAPI

**PROJECT**: [Project name]
**DATABASE**: [PostgreSQL / MySQL / MongoDB]
**ORM**: [Prisma / SQLAlchemy / Tortoise]

**ARCHITECTURE REQUIRED**:
1. Project structure:
   ```
   backend/
   ├── main.py          # FastAPI app
   ├── routers/         # API routes
   ├── models/          # Data models
   ├── schemas/         # Pydantic schemas
   └── database.py      # DB connection
   ```

2. Features to implement:
   - CORS configuration
   - Health check endpoint
   - Error handling middleware
   - Request validation
   - [Additional features]

**DELIVERABLES**:
- Complete FastAPI setup
- Router structure
- Pydantic models
- Database connection
- Example CRUD endpoints
```

---

## Skill #3: Prisma Schema & Migrations

### When to Use
- Defining database schema with Prisma
- Creating migrations
- Handling schema changes

### Prompt Template

```markdown
**ROLE**: Database engineer with Prisma expertise

**DATABASE**: [NeonDB / local PostgreSQL / etc]
**MODELS NEEDED**: [List models, e.g., User, Task, Category]

**CURRENT ISSUE** (if any): [Describe problem]

**TASKS**:
1. Design Prisma schema for:
   - [Model 1] with fields: [list]
   - [Model 2] with fields: [list]
   - Relationships between models
   
2. Set up:
   - Binary targets for Docker
   - Prisma Client generation
   - Connection pooling

3. Create migration strategy:
   - Development migrations
   - Production deployment

**DELIVERABLES**:
- Complete schema.prisma file
- Migration commands
- Seed data script (optional)
- Client usage examples
```

---

## Skill #4: API Route Implementation (Next.js)

### When to Use
- Creating API routes in Next.js
- Connecting frontend to FastAPI backend
- Handling API errors

### Prompt Template

```markdown
**ROLE**: Full-stack developer

**SCENARIO**: Next.js frontend needs to call FastAPI backend

**SETUP**:
- Frontend: Next.js 14 (App Router)
- Backend: FastAPI at ${NEXT_PUBLIC_API_URL}
- Auth: [Better Auth / NextAuth / None]

**IMPLEMENT**:
1. API utility functions in lib/api.ts:
   - GET, POST, PUT, DELETE helpers
   - Error handling
   - Token/session management

2. Example endpoints:
   ```typescript
   // GET /tasks
   // POST /tasks
   // PUT /tasks/:id
   // DELETE /tasks/:id
   ```

3. Type safety:
   - TypeScript interfaces
   - Zod validation (optional)

**DELIVERABLES**:
- Complete API client
- Type definitions
- Error handling
- Usage examples
```

---

## Skill #5: React Component Architecture

### When to Use
- Building reusable components
- Organizing component hierarchy
- Managing component state

### Prompt Template

```markdown
**ROLE**: React/Next.js component specialist

**APPLICATION**: [TODO app / Dashboard / etc]

**COMPONENTS NEEDED**:
- [TaskCard / UserProfile / etc]
- Props: [list expected props]
- State: [list state needs]
- Events: [list handlers]

**REQUIREMENTS**:
1. Component structure:
   - Functional components with hooks
   - TypeScript interfaces for props
   - Proper prop validation

2. Best practices:
   - Single responsibility
   - Reusability
   - Performance (memo, useCallback)

3. Styling approach:
   - [TailwindCSS / CSS Modules / etc]

**DELIVERABLES**:
- Component implementation
- TypeScript types
- Usage examples
- Storybook/documentation (optional)
```

---

## Skill #6: State Management Strategy

### When to Use
- Managing global state
- Sharing data between components
- Optimizing re-renders

### Prompt Template

```markdown
**ROLE**: State management architect

**APPLICATION COMPLEXITY**: [Simple / Medium / Complex]
**CURRENT PROBLEM**: [Describe state issues]

**STATE NEEDS**:
- User session/auth
- Task list
- UI state (modals, loading)
- [Other state]

**OPTIONS TO EVALUATE**:
1. React Context + useReducer (simple)
2. Zustand (medium)
3. Redux Toolkit (complex)
4. Server State: React Query / SWR

**RECOMMEND**:
- Best solution for this use case
- Implementation guide
- Migration path if changing

**DELIVERABLES**:
- State management setup
- Store/context structure
- Hook usage examples
```

---

## Skill #7: Form Handling & Validation

### When to Use
- Creating forms (create task, edit task, etc.)
- Adding validation
- Handling form submission

### Prompt Template

```markdown
**ROLE**: Form and UX specialist

**FORM**: [Login / Create Task / Edit Profile / etc]

**FIELDS**:
- [Field 1]: type, validation rules
- [Field 2]: type, validation rules
- [etc.]

**LIBRARY CHOICE**:
- React Hook Form (recommended)
- Formik
- Vanilla React state

**VALIDATION**:
- Client-side with Zod/Yup
- Server-side error display

**DELIVERABLES**:
- Complete form component
- Validation schema
- Error handling
- Submit handler
- Loading/success states
```

---

## Skill #8: TailwindCSS Component Styling

### When to Use
- Styling components with Tailwind
- Creating consistent design system
- Responsive design

### Prompt Template

```markdown
**ROLE**: UI/UX developer with Tailwind expertise

**COMPONENT**: [TaskCard / Button / Modal / etc]

**DESIGN REQUIREMENTS**:
- Style: [Modern / Minimal / Glassmorphism / etc]
- Colors: [Color scheme]
- Responsive: Mobile, tablet, desktop
- Dark mode support: [Yes / No]

**CURRENT ISSUE** (if any):
- [Describe styling problem]

**DELIVERABLES**:
1. Tailwind classes for component
2. Responsive breakpoints
3. Hover/active states
4. Dark mode variants (if needed)
5. Accessibility (focus states, etc.)

**AVOID**:
- Inline styles
- !important flags
- Overly specific classes
```

---

## Skill #9: API Error Handling

### When to Use
- Handling failed API requests
- Displaying error messages
- Retry logic

### Prompt Template

```markdown
**ROLE**: Error handling specialist

**SCENARIO**: [API call failing / Network error / etc]

**CURRENT IMPLEMENTATION**:
```typescript
[Paste current code]
```

**IMPROVE**:
1. Error types to handle:
   - Network errors (fetch failed)
   - HTTP errors (4xx, 5xx)
   - Validation errors
   - Timeout errors

2. User experience:
   - Toast notifications
   - Inline error messages
   - Retry buttons
   - Fallback UI

3. Logging:
   - Console for development
   - Sentry/logging service for production

**DELIVERABLES**:
- Error handling wrapper
- UI components for errors
- Retry logic
- User-friendly messages
```

---

## Skill #10: CORS Configuration

### When to Use
- Frontend can't reach backend
- CORS errors in browser console
- Configuring allowed origins

### Prompt Template

```markdown
**ROLE**: Backend security engineer

**PROBLEM**: CORS error blocking requests

**SETUP**:
- Frontend URL: [http://localhost:3000]
- Backend URL: [http://localhost:8000]
- Framework: [FastAPI / Express / etc]

**ERROR MESSAGE**:
```
[Paste CORS error]
```

**FIX REQUIRED**:
1. Configure CORS middleware
2. Set allowed origins
3. Allow credentials if needed
4. Set allowed methods/headers

**FOR FASTAPI**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[...],  # Configure this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**DELIVERABLES**:
- Correct CORS configuration
- Security considerations
- Testing commands
```

---

## Phase 2 Lessons Learned

### Frontend (Next.js)
1. **App Router is different** - Learn the new patterns
2. **Use server components** - Better performance
3. **Type everything** - TypeScript saves debugging time
4. **Optimize images** - Use Next.js Image component
5. **Error boundaries** - Catch React errors gracefully

### Backend (FastAPI)
1. **Pydantic is powerful** - Use for validation
2. **Async everything** - async/await for DB calls
3. **Document with OpenAPI** - FastAPI generates docs
4. **Handle CORS early** - Frontend integration blocker
5. **Health checks** - Essential for monitoring

### Database (Prisma)
1. **Schema first** - Design before coding
2. **Migrations carefully** - Can't easily undo
3. **Index performance fields** - Queries on filtered fields
4. **Binary targets for Docker** - Required for containers
5. **Connection pooling** - Especially for serverless

### General
1. **API contracts** - Define interfaces early
2. **Error handling** - Plan for failures
3. **Loading states** - Better UX
4. **Type sharing** - Share types between frontend/backend
5. **Test as you go** - Don't wait until the end

---

## Common Phase 2 Issues

### "Module not found" errors
- Check import paths
- Verify tsconfig paths configuration
- Restart dev server

### API calls fail with CORS
- Configure CORS in backend
- Check NEXT_PUBLIC_API_URL
- Verify backend is running

### Prisma Client not generated
- Run `npx prisma generate`
- Check binary targets in schema
- Rebuild Docker if in container

### Slow page loads
- Use React.lazy for code splitting
- Optimize images
- Check for unnecessary re-renders

---

## Related Skills

- **Phase 1**: Foundation and architecture
- **Phase 3**: Advanced features (auth, AI)
- **Frontend Skills**: Detailed Next.js patterns
- **Backend Skills**: Advanced FastAPI topics
- **Database Skills**: Prisma optimization

---

**This phase builds the core application. Get this solid before moving to Phase 3!**
