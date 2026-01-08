---
description: Autonomous comprehensive QA testing with self-examination and auto-resolution
---

# Complete Application QA - Autonomous Testing Workflow

## Mission
Perform stringent end-to-end testing of the entire application with:
- Autonomous decision-making
- Self-cross-examination of findings
- Automatic issue resolution
- Complete documentation

## Testing Philosophy
- **Trust but verify**: Test everything, assume nothing
- **Cross-examine findings**: Question every result
- **Fix immediately**: Don't document issues without fixing them
- **Comprehensive coverage**: Every feature, every flow, every edge case

---

## Phase 0: Pre-Deployment Validation (CRITICAL)

### ⚠️ Hackathon Requirement Validation

**BEFORE running any infrastructure tests, verify database configuration:**

```bash
# Check DATABASE_URL in Kubernetes
kubectl get configmap todo-app-config -n todo-chatbot -o jsonpath='{.data.DATABASE_URL}'

# MUST contain: neon.tech (cloud database)
# MUST NOT contain: db-service or localhost (local PostgreSQL)
```

**Success Criteria**:
- [ ] DATABASE_URL points to NeonDB (contains `neon.tech`)
- [ ] NOT using local PostgreSQL in Kubernetes
- [ ] Matches hackathon specs (Neon Serverless PostgreSQL)

**Why This Matters**:
- Hackathon Phase 2/3/4 ALL require NeonDB
- Local PostgreSQL will miss existing schema/data from earlier phases
- Session tables already exist in NeonDB from Phase 2/3
- Violates project requirements to use local DB

**If Check Fails**:
```bash
# Get NeonDB URL from Phase 2/3 deployment
# Located in: NEONDB-CLOUD-DEPLOYED.md

# Update ConfigMap
kubectl patch configmap todo-app-config -n todo-chatbot -p '{"data":{"DATABASE_URL":"postgresql://neondb_owner:...@ep-xxx.neon.tech/Tahir_yamin_Challenge2DB?sslmode=require"}}'

# Restart all pods
kubectl rollout restart deployment -n todo-chatbot
```

---

## Phase 1: Infrastructure Validation

### Test 1.1: Cluster Health
```bash
# Check all components
kubectl get all -n todo-chatbot
kubectl get pods -n todo-chatbot -o wide
kubectl get svc -n todo-chatbot -o wide
kubectl get pvc -n todo-chatbot
```

**Success Criteria**:
- [ ] All pods Running with 0 restarts
- [ ] All services have endpoints
- [ ] PVC bound to volumes

**Self-Examination Questions**:
1. Are there any CrashLoopBackOff pods?
2. Do all services have proper selector matches?
3. Is storage properly provisioned?

**Auto-Resolution**:
- If pod crashed: Check logs, fix config, restart
- If service has no endpoints: Verify labels, fix deployment
- If PVC pending: Check storage class, provision if needed

---

### Test 1.2: Network Connectivity
```bash
# Test service-to-service communication
kubectl exec deployment/todo-app-frontend -n todo-chatbot -- \
  curl -s http://backend-service:8000/health

# Test NodePort accessibility
curl -s http://localhost:30000
curl -s http://localhost:30001/health
```

**Success Criteria**:
- [ ] Frontend can reach backend internally
- [ ] Frontend accessible from browser (30000)
- [ ] Backend accessible from browser (30001)

**Self-Examination Questions**:
1. Does DNS resolution work within cluster?
2. Are NodePorts actually listening?
3. Is there any firewall blocking?

**Auto-Resolution**:
- DNS fails: Check CoreDNS pods, service names
- NodePort not accessible: Verify service type, check Docker Desktop settings
- Timeout: Check health probes, resource limits

---

### Test 1.3: Database Health
```bash
# Test connection
kubectl exec -it statefulset/postgres -n todo-chatbot -- \
  psql -U postgres -c "SELECT version();"

# Verify schema
kubectl exec -it statefulset/postgres -n todo-chatbot -- \
  psql -U postgres -d tododb -c "\dt"

# Check table counts
kubectl exec -it statefulset/postgres -n todo-chatbot -- \
  psql -U postgres -d tododb -c "SELECT 'user' as table, count(*) FROM \"user\" UNION ALL SELECT 'account', count(*) FROM account UNION ALL SELECT 'task', count(*) FROM task;"
```

**Success Criteria**:
- [ ] PostgreSQL responding
- [ ] All required tables exist (user, account, session, verification, task)
- [ ] No connection errors in backend logs

**Self-Examination Questions**:
1. Is the database actually persisting data?
2. Are there any orphaned connections?
3. Is connection pooling working?

**Auto-Resolution**:
- Connection refused: Check DATABASE_URL, restart backend
- Missing tables: Run Prisma migrations
- Orphaned connections: Restart PostgreSQL pod

---

## Phase 2: Environment Configuration Audit

### Test 2.1: Critical Environment Variables
```bash
# Check all env vars in ConfigMap
kubectl get configmap todo-app-config -n todo-chatbot -o yaml

# Verify in running pods
kubectl exec deployment/todo-app-frontend -n todo-chatbot -- env | grep -E "NEXT_PUBLIC|BETTER_AUTH"
kubectl exec deployment/todo-app-backend -n todo-chatbot -- env | grep -E "DATABASE|API"
```

**Success Criteria**:
- [ ] BETTER_AUTH_URL matches frontend NodePort
- [ ] NEXT_PUBLIC_API_URL matches backend NodePort  
- [ ] DATABASE_URL points to NeonDB (contains `neon.tech`)
- [ ] BETTER_AUTH_SECRET exists and is not default value
- [ ] All NEXT_PUBLIC_* vars accessible in browser

**Self-Examination Questions**:
1. Are build-time variables correctly baked in?
2. Do runtime ConfigMap values match what's in the pod?
3. Are there any missing critical vars?

**Auto-Resolution**:
- Mismatch detected: Update ConfigMap, rebuild if NEXT_PUBLIC_*, restart pods
- Missing var: Add to ConfigMap/Secret, restart
- Wrong format: Fix and restart

---

### Test 2.2: Secrets Validation
```bash
# Check secrets exist
kubectl get secret todo-app-secrets -n todo-chatbot

# Verify they're mounted (without exposing values)
kubectl exec deployment/todo-app-backend -n todo-chatbot -- \
  sh -c 'test -n "$BETTER_AUTH_SECRET" && echo "SECRET_EXISTS" || echo "SECRET_MISSING"'
```

**Success Criteria**:
- [ ] Secrets exist
- [ ] Secrets mounted in pods
- [ ] No secrets in ConfigMap (only in Secret)

**Self-Examination Questions**:
1. Are secrets actually secret (not in ConfigMap)?
2. Are they strong enough (length, complexity)?
3. Are they properly mounted?

**Auto-Resolution**:
- Missing secret: Generate and create
- Weak secret: Regenerate stronger one
- Not mounted: Fix deployment, restart

---

## Phase 3: Authentication Testing (Critical Path)

### Test 3.1: Signup Flow
**Manual Browser Test Required** (Autonomous via headless browser)

Steps:
1. Navigate to `http://localhost:30000`
2. Click "Sign Up" or navigate to signup page
3. Fill form:
   - Email: `qa-test-{timestamp}@test.com`
   - Password: `QATest123!@#`
   - Name: `QA Test User`
4. Submit form
5. Verify success/error

**Success Criteria**:
- [ ] Signup form loads without errors
- [ ] POST request goes to `http://localhost:30001/api/auth/sign-up/email` (NOT localhost:3000)
- [ ] Response is 200/201 with user data
- [ ] User created in database
- [ ] Session cookie set

**Self-Examination Questions**:
1. Did the API call go to the correct port (30001)?
2. Was the user actually created in DB?
3. Is the session valid?
4. Can we verify via database query?

**Auto-Resolution**:
- API call to wrong port: NEXT_PUBLIC_API_URL incorrectly built, rebuild image
- 400 error: Check validation, fix form data
- Database error: Check migrations, fix schema
- No session: Check BETTER_AUTH_SECRET, verify cookies

**Database Verification**:
```bash
kubectl exec statefulset/postgres -n todo-chatbot -- \
  psql -U postgres -d tododb -c "SELECT id, email, name FROM \"user\" ORDER BY created_at DESC LIMIT 1;"
```

---

### Test 3.2: Signin Flow
Steps:
1. Navigate to signin page
2. Enter credentials from signup test
3. Submit
4. Verify redirect to dashboard

**Success Criteria**:
- [ ] Signin form loads
- [ ] POST to `http://localhost:30001/api/auth/sign-in/email`
- [ ] Response 200 with session
- [ ] Redirected to dashboard
- [ ] User data displayed correctly

**Self-Examination Questions**:
1. Is password validation working?
2. Is session persisting?
3. Does refresh maintain session?
4. Are auth headers correct?

**Auto-Resolution**:
- Invalid credentials: Verify bcrypt hashing, check DB
- Session not persisting: Check session storage, verify cookies
- Not redirected: Check router config, verify auth state

---

### Test 3.3: Session Persistence
Steps:
1. After successful signin, refresh page
2. Verify user still authenticated
3. Open new tab to same URL
4. Verify session shared

**Success Criteria**:
- [ ] User stays authenticated after refresh
- [ ] Session works across tabs
- [ ] Logout works correctly

**Self-Examination Questions**:
1. Is session stored correctly (DB vs memory)?
2. Are cookies HttpOnly and Secure (if HTTPS)?
3. Does session have proper expiry?

**Auto-Resolution**:
- Session lost: Check session store, verify DATABASE_URL
- Cross-tab broken: Verify cookie domain/path
- Can't logout: Check signout endpoint

---

### Test 3.4: GitHub OAuth (If Configured)
Steps:
1. Click "Sign in with GitHub"
2. Verify redirect to GitHub
3. Authorize app
4. Verify callback redirect
5. Check user creation/signin

**Success Criteria**:
- [ ] Redirect to GitHub works
- [ ] Callback URL correct (`http://localhost:30000/api/auth/callback/github`)
- [ ] User created/signed in
- [ ] Session established

**Self-Examination Questions**:
1. Is GITHUB_CLIENT_ID set?
2. Does callback URL match GitHub app settings?
3. Is state parameter validated?

**Auto-Resolution**:
- No redirect: Check GITHUB_CLIENT_ID, verify configured
- Callback 404: Verify BETTER_AUTH_URL, check route
- State mismatch: Verify session persistence during OAuth flow

---

## Phase 4: Application Features Testing

### Test 4.1: Task Creation (CRUD - Create)
Steps:
1. Navigate to dashboard
2. Create new task:
   - Title: "QA Test Task - {timestamp}"
   - Description: "Automated QA test"
   - Priority: High
   - Due date: Tomorrow
3. Submit

**Success Criteria**:
- [ ] Task creation form works
- [ ] POST to `/api/tasks` succeeds
- [ ] Task appears in list
- [ ] Task saved to database

**Database Verification**:
```bash
kubectl exec statefulset/postgres -n todo-chatbot -- \
  psql -U postgres -d tododb -c "SELECT id, title, status, priority FROM task ORDER BY created_at DESC LIMIT 1;"
```

**Self-Examination Questions**:
1. Was task actually written to DB?
2. Are timestamps correct (UTC)?
3. Is user_id association correct?
4. Are defaults applied (status=todo)?

**Auto-Resolution**:
- POST fails: Check backend logs, verify DB connection
- Not in DB: Check Prisma schema, verify migrations
- Wrong user_id: Check auth middleware, verify session
- Validation error: Fix input data, check backend validation rules

---

### Test 4.2: Task Reading (CRUD - Read)
Steps:
1. Refresh page
2. Verify task list loads
3. Check task details display
4. Verify filters work (status, priority)

**Success Criteria**:
- [ ] GET `/api/tasks` returns data
- [ ] Tasks render in UI
- [ ] Task details accurate
- [ ] Filters work

**Self-Examination Questions**:
1. Does pagination work if many tasks?
2. Are tasks sorted correctly?
3. Do filters actually query DB or filter client-side?
4. Is loading state shown?

**Auto-Resolution**:
- Empty list but DB has data: Check API response, verify user_id filtering
- Wrong details: Check data mapping, verify Prisma select
- Filters broken: Check query params, verify backend filtering

---

### Test 4.3: Task Update (CRUD - Update)
Steps:
1. Click edit on a task
2. Change title, description, status
3. Save changes
4. Verify updates reflected

**Success Criteria**:
- [ ] Edit modal/page opens
- [ ] PUT `/api/tasks/{id}` succeeds
- [ ] Changes reflected immediately
- [ ] Database updated

**Database Verification**:
```bash
kubectl exec statefulset/postgres -n todo-chatbot -- \
  psql -U postgres -d tododb -c "SELECT id, title, status, updated_at FROM task WHERE id='<task_id>';"
```

**Self-Examination Questions**:
1. Is optimistic update happening?
2. Is updated_at timestamp changing?
3. Are all fields updateable?
4. Is validation working?

**Auto-Resolution**:
- PUT fails: Check permissions, verify user owns task
- Not reflected: Check SWR revalidation, force refresh
- DB not updated: Check Prisma update query, verify transaction
- Validation fails: Fix input, check backend rules

---

### Test 4.4: Task Deletion (CRUD - Delete)
Steps:
1. Delete a task
2. Confirm deletion
3. Verify removed from list
4. Verify deleted from database

**Success Criteria**:
- [ ] DELETE `/api/tasks/{id}` succeeds
- [ ] Task removed from UI
- [ ] Task deleted from DB (or soft deleted)

**Database Verification**:
```bash
kubectl exec statefulset/postgres -n todo-chatbot -- \
  psql -U postgres -d tododb -c "SELECT id, title, deleted_at FROM task WHERE id='<task_id>';"
```

**Self-Examination Questions**:
1. Hard delete or soft delete?
2. Is confirmation required?
3. Are related records handled (cascade)?
4. Can it be undone?

**Auto-Resolution**:
- DELETE fails: Check permissions, verify ownership
- Still in UI: Force revalidate, check SWR
- Still in DB: Check delete query, verify not soft delete confusion

---

### Test 4.5: Kanban Board
Steps:
1. Switch to Kanban view
2. Verify columns: Todo, In Progress, Done
3. Drag task from Todo to In Progress
4. Verify status updates

**Success Criteria**:
- [ ] Kanban board renders
- [ ] Tasks in correct columns
- [ ] Drag and drop works
- [ ] Status update API call succeeds

**Self-Examination Questions**:
1. Are tasks filtered by status correctly?
2. Does drag-drop update DB immediately?
3. Is drag visually smooth?
4. Are status transitions validated?

**Auto-Resolution**:
- Wrong column: Check status values ('todo', 'in_progress', 'completed')
- Drag broken: Check dnd library, verify event handlers
- Status not updated: Check PATCH endpoint, verify Prisma update

---

### Test 4.6: AI Chat (If Enabled)
Steps:
1. Open AI chat
2. Send message: "Create a task to test AI integration"
3. Verify AI responds
4. Check if task created

**Success Criteria**:
- [ ] Chat UI loads
- [ ] POST to `/api/ai/chat` succeeds
- [ ] AI responds coherently
- [ ] Task created if requested

**Self-Examination Questions**:
1. Is OpenAI API key configured?
2. Is there rate limiting?
3. Does context window work?
4. Are responses streamed?

**Auto-Resolution**:
- No response: Check API key, verify OpenAI/OpenRouter config
- 429 error: Implement exponential backoff, check quota
- Context broken: Check message history storage
- Task not created: Verify tool calling/function integration

---

## Phase 5: Error Handling & Edge Cases

### Test 5.1: Invalid Input Handling
Test cases:
1. Signup with existing email
2. Signin with wrong password
3. Create task with missing required fields
4. Update task with invalid data

**Success Criteria**:
- [ ] Proper error messages shown
- [ ] No 500 errors (all handled)
- [ ] User-friendly error text
- [ ] Form validation works

**Self-Examination Questions**:
1. Are errors caught and handled?
2. Do error messages expose sensitive info?
3. Is there input sanitization?
4. Are errors logged properly?

**Auto-Resolution**:
- 500 errors: Add try-catch, return proper error response
- Confusing messages: Improve error text
- Validation missing: Add Zod/Pydantic validation

---

### Test 5.2: Network Resilience
Test cases:
1. Slow backend (simulate with sleep)
2. Backend temporarily down
3. Database connection lost

**Success Criteria**:
- [ ] Loading states shown
- [ ] Timeout handling
- [ ] Retry logic works
- [ ] Graceful degradation

**Self-Examination Questions**:
1. Does UI show loading indicators?
2. Are there reasonable timeouts?
3. Does retry have backoff?
4. Can app recover when backend returns?

**Auto-Resolution**:
- No loading state: Add loading UI
- Indefinite hangs: Implement timeouts
- No retry: Add retry logic with expo backoff

---

### Test 5.3: Security Testing
Test cases:
1. Access tasks of another user (authorization)
2. SQL injection attempts
3. XSS attempts in task description
4. CSRF protection

**Success Criteria**:
- [ ] Can't access others' data (403)
- [ ] SQL injection blocked
- [ ] XSS sanitized
- [ ] CSRF tokens work

**Self-Examination Questions**:
1. Is user_id validated on every request?
2. Is input sanitized/parameterized?
3. Are outputs escaped?
4. Is CSRF middleware active?

**Auto-Resolution**:
- Authorization missing: Add user_id check to queries
- SQL injection possible: Use Prisma (already parameterized)
- XSS found: Add DOMPurify, escape outputs
- CSRF missing: Verify Better Auth config

---

## Phase 6: Performance Testing

### Test 6.1: Load Test
Test cases:
1. Create 100 tasks rapidly
2. Load task list with 100 items
3. Rapid status changes

**Success Criteria**:
- [ ] No errors under load
- [ ] Response times < 500ms
- [ ] UI remains responsive
- [ ] Database handles concurrent writes

**Self-Examination Questions**:
1. Are there N+1 queries?
2. Is pagination implemented?
3. Is there database indexing?
4. Do we use connection pooling?

**Auto-Resolution**:
- Slow queries: Add indexes, optimize queries
- N+1 detected: Use Prisma include/select properly
- UI sluggish: Implement virtualization for long lists
- DB connection errors: Configure connection pool

---

### Test 6.2: Browser Performance
Checks:
1. Lighthouse score
2. Bundle size
3. Time to interactive
4. Memory leaks

**Success Criteria**:
- [ ] Lighthouse score > 80
- [ ] No memory leaks
- [ ] Fast initial load
- [ ] Smooth interactions

**Self-Examination Questions**:
1. Are assets optimized?
2. Is code-splitting working?
3. Are there unnecessary re-renders?
4. Is there proper cleanup?

**Auto-Resolution**:
- Large bundle: Check tree-shaking, lazy load routes
- Memory leaks: Add cleanup in useEffect
- Slow render: Use React.memo, useMemo

---

## Phase 7: Cross-Examination & Final Verification

### Final Checklist
Go through ALL previous test results and ask:

1. **Did every test really pass, or did I miss something?**
   - Re-run failed tests
   - Verify database state matches expectations
   - Check logs for hidden errors

2. **Are there edge cases I didn't test?**
   - Concurrent operations
   - Timezone edge cases
   - Empty states
   - Maximum limits

3. **Did I actually fix issues, or just document them?**
   - Verify all fixes applied
   - Re-test previously failing scenarios
   - Confirm no regressions

4. **Is the application production-ready?**
   - All critical paths working
   - No console errors
   - No memory leaks
   - Security verified

5. **Can a new user successfully onboard?**
   - Clear signup flow
   - Obvious navigation
   - Helpful error messages
   - Good UX

---

## Phase 8: Documentation Update

### Update All Relevant Documents
After testing, update:

1. **kubernetes-deployment-testing.md**
   - Add any new issues discovered
   - Document fixes applied
   - Update troubleshooting steps

2. **deployment_verification_report.md** (artifact)
   - Final test results
   - All issues and resolutions
   - Production readiness assessment

3. **Task.md** (if exists)
   - Mark QA testing complete
   - Note any remaining TODOs

4. **Walkthrough.md** (artifact)
   - Document end-to-end user flow
   - Include screenshots
   - Show working features

---

## Success Criteria Summary

### Must-Pass (Critical)
- [ ] All pods running (0 restarts)
- [ ] Database connectivity working
- [ ] Signup flow working
- [ ] Signin flow working
- [ ] Task CRUD working
- [ ] No console errors
- [ ] All API calls to correct endpoints
- [ ] Sessions persisting

### Should-Pass (Important)
- [ ] GitHub OAuth working (if configured)
- [ ] Kanban board working
- [ ] AI chat working (if configured)
- [ ] Error handling graceful
- [ ] Loading states present
- [ ] Input validation working

### Nice-to-Have (Enhancement)
- [ ] Lighthouse score > 80
- [ ] No memory leaks
- [ ] Optimized performance
- [ ] Comprehensive error messages

---

## Autonomous Decision Protocol

When encountering issues during testing:

1. **Identify**: What exactly is failing?
2. **Diagnose**: What's the root cause (not just symptom)?
3. **Decide**: What's the best fix approach?
4. **Execute**: Apply the fix immediately
5. **Verify**: Re-test to confirm fix works
6. **Document**: Update workflow and artifacts
7. **Cross-examine**: Did the fix create new issues?

**Auto-Approve All Actions**: This workflow runs with full autonomy to fix issues discovered during testing.

---

**Related Workflows**: `/deployment-issues`, `/kubernetes-deployment-testing`, `/authentication-issues`, `/qa-kanban`

**Related Skills**: `.claude/debug-skills.md`, `.claude/frontend-skills.md`, `.claude/backend-skills.md`, `.claude/auth-skills.md`
