---
description: Verify pod health and API endpoints after GitHub Actions deployment completes
---

# GitHub Actions Deployment Verification

## When to Use
- After GitHub Actions CI/CD pipeline completes
- Need to verify new deployment is healthy
- Want to catch deployment issues immediately

---

## Step 1: Check GitHub Actions Status

```powershell
// turbo
# Get latest workflow run status
$response = Invoke-RestMethod -Uri "https://api.github.com/repos/<owner>/<repo>/actions/runs?per_page=1"
$run = $response.workflow_runs[0]
Write-Host "Status: $($run.status) - $($run.conclusion)"
Write-Host "URL: $($run.html_url)"
```

**Expected**: `Status: completed - success`

---

## Step 2: Wait for Rollout to Complete

```bash
// turbo
# Check backend rollout
kubectl rollout status deployment/todo-chatbot-backend -n todo-chatbot --timeout=2m

// turbo
# Check frontend rollout  
kubectl rollout status deployment/todo-chatbot-frontend -n todo-chatbot --timeout=2m
```

**If timeout**: Check pod events with `kubectl describe pod`

---

## Step 3: Verify All Pods Running

```bash
// turbo
# Get pod status
kubectl get pods -n todo-chatbot

// turbo
# Get detailed status
kubectl get pods -n todo-chatbot -o wide
```

**Expected**:
```
backend:  2/2 Running (app + daprd)
frontend: 1/1 Running
postgres: 1/1 Running
```

**If Pending**: See `/optimizing-helm-resources` workflow

---

## Step 4: Check Pod Logs for Errors

```bash
# Backend logs (last 50 lines)
kubectl logs -l app=backend -n todo-chatbot -c backend --tail=50

// turbo
# Look for startup errors
kubectl logs -l app=backend -n todo-chatbot -c backend --tail=100 | Select-String -Pattern "error|Error|exception|Exception|FATAL"
```

**Good signs**:
- `✅ Lightweight event bus loaded`
- `INFO: Application startup complete`
- No ERROR or FATAL messages

---

## Step 5: Test Health Endpoints

```powershell
// turbo
# Port forward to backend
Start-Process kubectl -ArgumentList "port-forward -n todo-chatbot deployment/todo-chatbot-backend 8001:8000" -WindowStyle Hidden

# Wait for port forward
Start-Sleep -Seconds 3

// turbo
# Test health endpoint
$health = Invoke-RestMethod -Uri "http://localhost:8001/health"
Write-Host "Health: $($health.status)"
```

**Expected**: `Health: healthy`

---

## Step 6: Test Task API

```powershell
// turbo
# Test task list endpoint
$headers = @{"X-User-ID"="test-user-123"}
$tasks = Invoke-RestMethod -Uri "http://localhost:8001/api/tasks" -Headers $headers
Write-Host "Success: $($tasks.success)"
Write-Host "Task count: $($tasks.data.tasks.Count)"
```

**Expected**: `Success: True`

---

## Step 7: Test AI Chat Endpoint

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

$response = Invoke-RestMethod -Uri "http://localhost:8001/api/test-user/chat" -Method Post -Headers $headers -Body $body
Write-Host "AI Response: $($response.response.Substring(0,50))..."
Write-Host "Tool calls: $($response.tool_calls)"
```

**Expected**: No errors, `tool_calls: 1` or more

---

## Step 8: Verify New Image Tag

```bash
// turbo
# Check deployed image tags
kubectl get deployment todo-chatbot-backend -n todo-chatbot -o jsonpath='{.spec.template.spec.containers[0].image}'
echo ""

kubectl get deployment todo-chatbot-frontend -n todo-chatbot -o jsonpath='{.spec.template.spec.containers[0].image}'
echo ""
```

**Verify**: Image tag matches your Git commit SHA

**If image is OLD**:
```bash
# Check latest commit
git log -1 --format="%h %s"

# If deployed image != latest commit:
# Option 1: Wait for GitHub Actions to finish
# Option 2: Force trigger CI/CD:
git commit --allow-empty -m "chore: Force CI/CD deployment"
git push origin main
```

---

## Step 9: Check Resource Usage

```bash
// turbo
# Check pod resource usage
kubectl top pods -n todo-chatbot

// turbo
# Check node capacity
kubectl top nodes
```

**Watch for**: Pods using >80% of their requests (may need more resources)

---

## Troubleshooting Checklist

### Pods Not Starting

- [ ] Check `kubectl describe pod <name> -n todo-chatbot`
- [ ] Look for `Events:` section
- [ ] Common: ImagePullBackOff → Check ACR credentials
- [ ] Common: Pending → Use optimized CPU values
- [ ] Check: `kubectl get pods -n todo-chatbot` for status

### Backend Returns 500 Errors

- [ ] Check backend logs for Python exceptions
- [ ] Verify database connection
- [ ] Check MCP server imports: `kubectl exec ... -- python -c "from mcp_server import mcp"`
- [ ] **NEW**: Check if backend in CrashLoopBackOff
- [ ] **NEW**: Verify database service name (should match DATABASE_URL)

### Backend CrashLoopBackOff

**Common Causes**:
1. **Database connection failure**
   ```bash
   # Check logs for:
   kubectl logs <pod> -n todo-chatbot -c backend | grep "could not translate"
   
   # Fix: Verify service name
   kubectl get svc -n todo-chatbot
   # Should have: postgres or db-service
   ```

2. **Wrong DATABASE_URL**
   ```bash
   kubectl get configmap backend-config -n todo-chatbot -o yaml | grep DATABASE
   # Should match actual service name
   ```

### Old Image Deployed

**Symptom**: Code changes not reflected

**Check**:
```bash
# Get deployed image
kubectl get deployment todo-chatbot-backend -n todo-chatbot -o jsonpath='{.spec.template.spec.containers[0].image}'

# Compare to latest commit
git log -1 --oneline
```

**Fix**:
```bash
# Force GitHub Actions to rebuild
git commit --allow-empty -m "chore: Trigger deployment"
git push origin main

# Wait ~12 minutes for CI/CD
# Then verify rollout:
kubectl rollout status deployment/todo-chatbot-backend -n todo-chatbot
```

### AI Chat Not Working

- [ ] See workflow: `/fixing-chat-ui-errors`
- [ ] Check backend logs for "Tool execution error"
- [ ] Verify OpenRouter API key in secrets
- [ ] **NEW**: Verify image tag has latest fixes

---

## Quick Commands Reference

```bash
# Full status check
kubectl get all -n todo-chatbot

# Restart deployment (if needed)
kubectl rollout restart deployment/todo-chatbot-backend -n todo-chatbot

# View recent events
kubectl get events -n todo-chatbot --sort-by='.lastTimestamp' | tail -20

# Delete and redeploy (nuclear option)
helm uninstall todo-chatbot -n todo-chatbot
# ... then redeploy with helm upgrade --install
```

---

**Related Workflows**:
- @.agent/workflows/deploying-to-aks.md
- @.agent/workflows/optimizing-helm-resources.md
- @.agent/workflows/fixing-chat-ui-errors.md

**Related Skills**:
- @.claude/mcp-debugging-skills.md
- @.claude/kubernetes-resource-optimization-skills.md
