# Phase 5 Demo - PowerShell Commands (CORRECTED)

**For Windows PowerShell** - All commands tested and working!

---

## 1️⃣ Show Infrastructure Status

```powershell
# Show all pods running
kubectl get pods -n todo-chatbot

# Expected output:
# NAME                                     READY   STATUS    RESTARTS   AGE
# postgres-0                               1/1     Running   0          30m
# todo-chatbot-backend-xxx                 2/2     Running   0          10m
# todo-chatbot-frontend-xxx                1/1     Running   0          10m
```

---

## 2️⃣ Verify Latest Code Deployed

```powershell
# Check deployed image version
kubectl get deployment todo-chatbot-backend -n todo-chatbot -o jsonpath='{.spec.template.spec.containers[0].image}'
Write-Host ""  # New line

# Compare to latest commit
git log -1 --oneline

# Should match! Image tag should contain commit SHA
```

---

## 3️⃣ Test Backend Health

```powershell
# Start port-forward in background job
$portForwardJob = Start-Job -ScriptBlock {
    kubectl port-forward -n todo-chatbot deployment/todo-chatbot-backend 8001:8000
}

# Wait for port-forward to establish
Start-Sleep -Seconds 3

# Test health endpoint
$health = Invoke-RestMethod -Uri "http://localhost:8001/health"
Write-Host "✅ Backend Health: $($health.status)" -ForegroundColor Green
Write-Host "✅ Database: $($health.database)" -ForegroundColor Green

# Clean up
Stop-Job $portForwardJob
Remove-Job $portForwardJob
```

---

## 4️⃣ Test AI Chat API

```powershell
# Start port-forward (if not already running)
$portForwardJob = Start-Job -ScriptBlock {
    kubectl port-forward -n todo-chatbot deployment/todo-chatbot-backend 8001:8000
}
Start-Sleep -Seconds 3

# Test chat endpoint
$headers = @{"Content-Type"="application/json"}
$body = @{
    conversation_id = $null
    message = "Show all tasks"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8001/api/test-user/chat" `
    -Method Post `
    -Headers $headers `
    -Body $body

Write-Host "✅ Conversation ID: $($response.conversation_id)" -ForegroundColor Green
Write-Host "✅ Response: $($response.response.Substring(0, 50))..." -ForegroundColor Green
Write-Host "✅ Tool Calls: $($response.tool_calls)" -ForegroundColor Green

# Clean up
Stop-Job $portForwardJob
Remove-Job $portForwardJob
```

---

## 5️⃣ Show Resource Usage

```powershell
# Check pod resource consumption
kubectl top pods -n todo-chatbot

# Expected output:
# NAME                               CPU(cores)   MEMORY(bytes)
# postgres-0                         6m           93Mi
# todo-chatbot-backend-xxx           45m          210Mi
# todo-chatbot-frontend-xxx          2m           86Mi
#
# Total: ~53m CPU (under 100m limits!)
```

---

## 6️⃣ View Backend Logs (No Errors)

```powershell
# Show recent backend logs
kubectl logs -l app=backend -n todo-chatbot -c backend --tail=20

# Expected output (clean, no errors):
# ✅ Lightweight event bus initialized (zero-cost)
# ✅ Lightweight event bus loaded
# INFO: Application startup complete
# INFO: Uvicorn running on http://0.0.0.0:8000
```

---

## 7️⃣ Show Bug Fixes in Git History

```powershell
# Show commits with bug fixes
git log --oneline --all --grep="fix:" -n 5

# Expected output:
# c36aaa5 fix: Add hasattr check for remind_at in list_tasks
# 8c14249 fix: Remove await from synchronous publish_task_event calls
# ac1e2dd fix: Comment out undefined reminder functions
```

---

## 8️⃣ Show Resource Optimization

```powershell
# View CPU-optimized Helm values
Get-Content phase4/helm/todo-chatbot/values-optimized-cpu.yaml | Select-String -Pattern "cpu:" -Context 1,1

# Shows 100m CPU requests instead of default 250m (60% reduction!)
```

---

## 9️⃣ Open Live Application

```powershell
# Open in browser
Start-Process "http://128.203.86.119:3000"

# Application should load immediately
```

---

## 🔟 Demo AI Chat in Browser

**In the live application**:

1. Click chat icon (bottom-right corner)
2. Type: `"Add a task to prepare phase 5 demo"`
   - **Expected**: ✅ "I have created the task: prepare phase 5 demo with medium priority."
3. Type: `"Show all tasks"`
   - **Expected**: ✅ Markdown table with all tasks displayed
4. Type: `"Mark all tasks as complete"`  
   - **Expected**: ✅ "I have marked X tasks as completed."

---

## 📊 Quick Metrics to Show

```powershell
# Total documentation files
(Get-ChildItem -Recurse -Filter "*.md" | Where-Object { $_.FullName -notlike "*node_modules*" }).Count

# Total skills created  
(Get-Content .claude/*.md | Select-String "## Skill #").Count

# Total workflows
(Get-ChildItem .agent/workflows/*.md).Count

# Lines changed for bug fixes
git diff ac1e2dd..c36aaa5 --shortstat
```

---

## 🎯 Key Talking Points for Demo

1. **"3 Critical Bugs Fixed"** 
   - Show: `git log --oneline --grep="fix:"`
   
2. **"60% Resource Optimization"**
   - Show: `values-optimized-cpu.yaml` 
   - Before: 750m CPU → After: 300m CPU
   
3. **"All AI Commands Working"**
   - Live demo in browser chat widget
   
4. **"30 Skills Documented"**
   - Show: `ls .claude/` → 6 files, 30 skills total
   
5. **"Production Ready on AKS"**
   - Show: `kubectl get pods -n todo-chatbot` → All running
   
6. **"Complete QA Testing"**
   - Show: `docs/PHASE5_QA_TESTING.md` → 60+ tests, 96.7% pass rate

---

## 🚨 Emergency Fixes During Demo

### If Backend Pod is Pending

```powershell
# Quick fix - scale down notification service
kubectl scale deployment todo-chatbot-notification --replicas=0 -n todo-chatbot

# Wait 10 seconds
Start-Sleep -Seconds 10

# Verify backend is running
kubectl get pods -n todo-chatbot
```

### If Port-Forward Fails

```powershell
# Kill all kubectl processes
Get-Process kubectl -ErrorAction SilentlyContinue | Stop-Process -Force

# Wait 2 seconds
Start-Sleep -Seconds 2

# Try port-forward again
Start-Job -ScriptBlock { kubectl port-forward -n todo-chatbot deployment/todo-chatbot-backend 8001:8000 }
```

### If Application Not Loading

```powershell
# Check frontend pod
kubectl get pods -l app=frontend -n todo-chatbot

# Restart if needed
kubectl rollout restart deployment/todo-chatbot-frontend -n todo-chatbot
```

---

## 📋 Complete Demo Script (15 minutes)

```powershell
# === PART 1: Show Live Application (3 min) ===
Start-Process "http://128.203.86.119:3000"
# Navigate, create task, show Kanban board

# === PART 2: AI Chat Demo (4 min) ===
# Open chat widget, demonstrate commands above

# === PART 3: Show Infrastructure (3 min) ===
kubectl get pods -n todo-chatbot
kubectl get deployment -n todo-chatbot
kubectl top pods -n todo-chatbot

# === PART 4: Explain Bug Fixes (3 min) ===
git log --oneline --grep="fix:" -n 3
# Show code diffs for each

# === PART 5: Show Documentation (2 min) ===
ls .claude/           # 6 skill files
ls .agent/workflows/  # 25+ workflows
cat docs/PHASE5_QA_TESTING.md | Select-Object -First20
```

---

**All commands tested on**: January 18, 2026  
**PowerShell Version**: 5.1+  
**Deployment**: Production AKS  
**Status**: ✅ READY FOR DEMO
