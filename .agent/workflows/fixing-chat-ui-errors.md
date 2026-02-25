---
description: Debug and fix AI chat widget errors systematically
---

# Fixing Chat UI Errors

## When to Use
- AI chat showing "error while trying to fetch tasks"
- Chat widget returns errors but API works manually
- MCP tools failing silently

---

## Step 1: Verify Backend API Works

```powershell
// turbo
# Port-forward to backend
kubectl port-forward -n todo-chatbot deployment/todo-chatbot-backend 8001:8000 &

// turbo
# Test health endpoint
Start-Sleep -Seconds 2
Invoke-RestMethod -Uri "http://localhost:8001/health"
```

**Expected**: `{status: "healthy"}`

**If fails**: Backend pod not ready, check `/github-actions-deployment-verification`

---

## Step 2: Test Task API Directly

```powershell
// turbo
# Test task list endpoint
$headers = @{"X-User-ID"="test-user-123"}
$response = Invoke-RestMethod -Uri "http://localhost:8001/api/tasks" -Headers $headers
Write-Host "Success: $($response.success)"
```

**Expected**: `Success: True`

**If fails**: Database connection issue or backend crash

---

## Step 3: Verify Backend Image Version

```bash
# Check deployed image tag
kubectl get deployment todo-chatbot-backend -n todo-chatbot -o jsonpath='{.spec.template.spec.containers[0].image}'

# Check latest commit with fix
git log --oneline | grep -E "remind_at|async|await" | head -3
```

**Expected**: Image tag should contain commit SHA with your fix

**If OLD image deployed**:
- GitHub Actions may still be building
- Or CI/CD didn't trigger
- Force trigger: `git commit --allow-empty -m "chore: Deploy" && git push`

---

## Step 4: Check Backend Logs for MCP Errors

```bash
# Get backend pod name
POD=$(kubectl get pods -l app=backend -n todo-chatbot -o jsonpath='{.items[0].metadata.name}')

# Check for MCP tool errors
kubectl logs $POD -n todo-chatbot -c backend --tail=200 | grep -i "tool\|error\|exception"
```

**Look for**:
- `Tool execution error: ...` → Actual error message
- `AttributeError` → Missing field (see fix below)
- `TypeError: object can't be used in 'await'` → Async/await issue
- `could not translate host name` → Database connection issue

---

## Step 5: Test Chat Endpoint Directly

```powershell
// turbo
# Test chat endpoint
$headers = @{
    "Content-Type"="application/json"
    "X-User-ID"="test-user"
}
$body = @{
    conversation_id=$null
    message="Show all tasks"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8001/api/test-user/chat" \
    -Method Post \
    -Headers $headers \
    -Body $body

Write-Host "AI Response: $($response.response)"
Write-Host "Tool calls: $($response.tool_calls)"
```

**Expected**: 
- Response contains task list or formatted output
- No error messages in response

**If "error while trying to fetch"**:
- Check Step 5 (MCP tool bugs)

---

## Step 6: Common MCP Tool Bugs

### Bug: AttributeError on Optional Fields

**Symptom**: `'Task' object has no attribute 'remind_at'`

**Fix**:
```python
# In mcp_server.py, use hasattr check
"remind_at": t.remind_at.isoformat() if hasattr(t, 'remind_at') and t.remind_at else None
```

**See**: `@.claude/mcp-debugging-skills.md` Skill #2

---

### Bug: Async/Await Mismatch

**Symptom**: `TypeError: object bool can't be used in 'await' expression`

**Fix**:
```python
# Check if function is actually async
def publish_event(data):  # NOT async!
    return True

# Don't use await
publish_event(data)  # Correct

# Instead of
await publish_event(data)  # Wrong!
```

**See**: `@.claude/mcp-debugging-skills.md` Skill #1

---

### Bug: Undefined Functions

**Symptom**: `NameError: name 'schedule_reminder_job' is not defined`

**Fix**:
```python
# Comment out call if not implemented
# TODO: Implement Dapr Jobs API
# if remind_at:
#     schedule_reminder_job(task_id, remind_at, user_id)
```

**See**: `@.claude/mcp-debugging-skills.md` Skill #3

---

## Step 7: Test Locally Before Deploying

```bash
# Navigate to backend
cd phase2/backend

# Test MCP imports
python -c "from mcp_server import mcp; print('✅ MCP OK'); print(f'Tools: {len(mcp.get_tools_schema())}')"
```

**Expected**: `✅ MCP OK` with tool count

**If import fails**: Fix Python errors before deploying

---

## Step 8: Verify Markdown Rendering (Frontend)

If tasks show as raw markdown instead of formatted tables:

**Check**: `ChatWidget.tsx` has `ReactMarkdown` with `remarkGfm`

```typescript
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

// In render
<ReactMarkdown remarkPlugins={[remarkGfm]}>
  {msg.content}
</ReactMarkdown>
```

**If missing**: Install dependencies
```bash
npm install react-markdown remark-gfm
```

---

## Step 9: Check OpenRouter API Key

If chat completely fails:

```bash
# Exec into backend pod
kubectl exec -it deployment/todo-chatbot-backend -n todo-chatbot -c backend -- sh

# Check API key is loaded
echo $OPENROUTER_API_KEY
```

**Should start with**: `sk-or-v1-`

**If empty**: Secret not mounted, see `/deploying-to-aks` Step 4

---

## Quick Diagnostic Flowchart

```
Chat Error
  ↓
Backend API works? → NO → Check pod status, logs
  ↓ YES
Chat endpoint works? → NO → Check OpenRouter API key
  ↓ YES
Tool execution error in logs? → YES → Fix MCP bugs (Step 5)
  ↓ NO
Markdown not rendering? → YES → Check ReactMarkdown (Step 7)
  ↓
✅ Should be working now
```

---

## Related Workflows
- @.agent/workflows/github-actions-deployment-verification.md
- @.agent/workflows/deploying-to-aks.md

## Related Skills
- @.claude/mcp-debugging-skills.md
- @.claude/openrouter-api-skills.md
