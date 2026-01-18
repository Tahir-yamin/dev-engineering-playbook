---
description: Continuous monitoring of GitHub Actions and pod status with automated issue resolution
---

# Post-Deployment Continuous Monitoring

## When to Use
- After pushing code to trigger CI/CD
- Waiting for deployment to complete
- Need automated checking of deployment health
- Want to catch and fix issues automatically

---

## Quick Monitor (One-Time Check)

```powershell
// turbo
# Check GitHub Actions latest run
Write-Host "🔍 Checking GitHub Actions..." -ForegroundColor Cyan
Start-Process "https://github.com/Tahir-yamin/todo_hackathon_phase2/actions"

// turbo
# Check pod status
kubectl get pods -n todo-chatbot
```

---

## Continuous Monitor Script

Save this as `monitor-deployment.ps1`:

```powershell
# ========================================
# Continuous Deployment Monitor
# ========================================
# Monitors GitHub Actions and Pod status
# Auto-resolves common issues
# ========================================

param(
    [int]$IntervalSeconds = 30,
    [int]$MaxChecks = 20
)

$namespace = "todo-chatbot"
$checkCount = 0

Write-Host "🚀 Starting deployment monitor..." -ForegroundColor Green
Write-Host "Namespace: $namespace" -ForegroundColor Yellow
Write-Host "Check interval: $IntervalSeconds seconds" -ForegroundColor Yellow
Write-Host "Max checks: $MaxChecks"
Write-Host "`n" + ("="*60) + "`n"

while ($checkCount -lt $MaxChecks) {
    $checkCount++
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    Write-Host "[$timestamp] Check #$checkCount/$MaxChecks" -ForegroundColor Cyan
    
    # ==================== POD STATUS ====================
    Write-Host "`n📦 Pod Status:" -ForegroundColor Yellow
    $pods = kubectl get pods -n $namespace -o json | ConvertFrom-Json
    
    $allHealthy = $true
    foreach ($pod in $pods.items) {
        $name = $pod.metadata.name
        $phase = $pod.status.phase
        $ready = "$($pod.status.containerStatuses.Count)/$($pod.status.containerStatuses.Count)"
        
        # Check if pod is healthy
        $isHealthy = $phase -eq "Running"
        foreach ($container in $pod.status.containerStatuses) {
            if (-not $container.ready) {
                $isHealthy = $false
            }
        }
        
        if ($isHealthy) {
            Write-Host "  ✅ $name - $phase" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $name - $phase" -ForegroundColor Red
            $allHealthy = $false
            
            # Check for common issues
            if ($phase -eq "Pending") {
                Write-Host "    🔍 Checking pending reason..." -ForegroundColor Yellow
                $events = kubectl describe pod $name -n $namespace | Select-String "Events:" -Context 0,5
                Write-Host $events
                
                # Auto-fix: If CPU issue, scale down notification
                if ($events -match "Insufficient cpu") {
                    Write-Host "    🔧 AUTO-FIX: Scaling down notification service" -ForegroundColor Cyan
                    kubectl scale deployment todo-chatbot-notification --replicas=0 -n $namespace
                }
            }
            
            if ($phase -eq "CrashLoopBackOff") {
                Write-Host "    🔍 Checking crash logs..." -ForegroundColor Yellow
                kubectl logs $name -n $namespace --tail=20
            }
        }
    }
    
    # ==================== DEPLOYMENT STATUS ====================
    Write-Host "`n🚢 Deployment Status:" -ForegroundColor Yellow
    $deployments = kubectl get deployment -n $namespace -o json | ConvertFrom-Json
    
    foreach ($deploy in $deployments.items) {
        $name = $deploy.metadata.name
        $ready = $deploy.status.readyReplicas
        $desired = $deploy.spec.replicas
        
        if ($ready -eq $desired) {
            Write-Host "  ✅ $name - $ready/$desired ready" -ForegroundColor Green
        } else {
            Write-Host "  ⏳ $name - $ready/$desired ready" -ForegroundColor Yellow
        }
    }
    
    # ==================== IMAGE VERSIONS ====================
    Write-Host "`n🏷️  Image Versions:" -ForegroundColor Yellow
    $backendImage = kubectl get deployment todo-chatbot-backend -n $namespace -o jsonpath='{.spec.template.spec.containers[0].image}'
    $frontendImage = kubectl get deployment todo-chatbot-frontend -n $namespace -o jsonpath='{.spec.template.spec.containers[0].image}'
    
    Write-Host "  Backend:  $backendImage"
    Write-Host "  Frontend: $frontendImage"
    
    # Check if image matches latest commit
    $latestCommit = git log -1 --format="%h"
    if ($backendImage -match $latestCommit) {
        Write-Host "  ✅ Backend image is up-to-date" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Backend image may be outdated (latest commit: $latestCommit)" -ForegroundColor Yellow
    }
    
    # ==================== HEALTH CHECK ====================
    if ($allHealthy) {
        Write-Host "`n✅ All systems healthy!" -ForegroundColor Green
        Write-Host "🎯 Testing backend health endpoint..." -ForegroundColor Cyan
        
        # Port-forward and test
        $job = Start-Job -ScriptBlock {
            kubectl port-forward -n todo-chatbot deployment/todo-chatbot-backend 8001:8000
        }
        Start-Sleep -Seconds 3
        
        try {
            $health = Invoke-RestMethod -Uri "http://localhost:8001/health" -TimeoutSec 5
            if ($health.status -eq "healthy") {
                Write-Host "✅ Backend health check PASSED" -ForegroundColor Green
                Write-Host "`n🎉 DEPLOYMENT SUCCESSFUL - All checks passed!" -ForegroundColor Green
                Stop-Job $job
                break
            }
        } catch {
            Write-Host "⚠️  Health check failed: $_" -ForegroundColor Yellow
        } finally {
            Stop-Job $job -ErrorAction SilentlyContinue
        }
    }
    
    Write-Host "`n" + ("="*60) + "`n"
    
    if ($checkCount -lt $MaxChecks) {
        Write-Host "⏳ Waiting $IntervalSeconds seconds before next check...`n" -ForegroundColor Gray
        Start-Sleep -Seconds $IntervalSeconds
    }
}

if ($checkCount -eq $MaxChecks) {
    Write-Host "⚠️  Reached maximum checks ($MaxChecks)" -ForegroundColor Yellow
    Write-Host "Deployment may still be in progress. Check manually:" -ForegroundColor Yellow
    Write-Host "  kubectl get pods -n $namespace" -ForegroundColor Cyan
}
```

---

## Usage

### Basic Monitoring
```powershell
# Run with defaults (30s interval, 20 checks = 10 minutes)
./monitor-deployment.ps1
```

### Custom Intervals
```powershell
# Check every 15 seconds, maximum 40 checks
./monitor-deployment.ps1 -IntervalSeconds 15 -MaxChecks 40

# Quick check every 10 seconds, only 10 times
./monitor-deployment.ps1 -IntervalSeconds 10 -MaxChecks 10
```

---

## Auto-Fix Features

### 1. CPU Constraints (Pending Pods)
**Detects**: `Insufficient cpu` in pod events  
**Action**: Scales down notification service to 0 replicas

### 2. CrashLoopBackOff
**Detects**: Pod phase = CrashLoopBackOff  
**Action**: Shows last 20 log lines for debugging

### 3. Old Image Deployed
**Detects**: Image tag doesn't match latest commit  
**Action**: Warns user, suggests triggering CI/CD

---

## Manual Interventions

### If Pod Stuck Pending
```powershell
# Check node resources
kubectl top nodes

# Check pod events
kubectl describe pod <pod-name> -n todo-chatbot | Select-String "Events:" -Context 0,10

# Force using optimized values
helm upgrade todo-chatbot ./phase4/helm/todo-chatbot -n todo-chatbot `
  -f ./phase4/helm/todo-chatbot/values-optimized-cpu.yaml
```

### If CrashLoopBackOff
```powershell
# Get detailed logs
kubectl logs <pod-name> -n todo-chatbot --tail=100

# Check for database connection
kubectl logs <pod-name> -n todo-chatbot | Select-String "database|connection"

# Verify secrets
kubectl get secrets -n todo-chatbot
```

### If Old Image
```powershell
# Force CI/CD trigger
git commit --allow-empty -m "chore: Force deployment"
git push origin main

# Wait 2 minutes then run monitor again
```

---

## GitHub Actions Monitoring

### Check Latest Run Programmatically
```powershell
# Using GitHub CLI (requires: winget install GitHub.cli)
gh run list --limit 1

# Get status
gh run view

# Watch live
gh run watch
```

### Browser Check
```powershell
Start-Process "https://github.com/Tahir-yamin/todo_hackathon_phase2/actions"
```

---

## Complete Deployment Flow

```powershell
# 1. Make code changes
git add .
git commit -m "fix: Your fix description"
git push origin main

# 2. Start monitoring
Write-Host "⏳ Waiting 1 minute for GitHub Actions to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 60

# 3. Run monitor
./monitor-deployment.ps1 -IntervalSeconds 30 -MaxChecks 25

# 4. If successful, test application
Start-Process "http://128.203.86.119:3000"
```

---

## Success Criteria

Monitor will exit successfully when:
- ✅ All pods: **Running**
- ✅ All deployments: **Ready**
- ✅ Backend health check: **Passed**
- ✅ Image tags: **Match latest commit**

---

## Troubleshooting

### Monitor Script Won't Run
```powershell
# Set execution policy
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Run again
./monitor-deployment.ps1
```

### Port-Forward Fails
- Another process may be using port 8001
- Kill existing port-forwards: `Get-Process kubectl | Stop-Process`

### Health Check Always Fails
- Backend may not be ready yet
- Check logs: `kubectl logs -l app=backend -n todo-chatbot -c backend`

---

## Related Workflows
- @.agent/workflows/github-actions-deployment-verification.md
- @.agent/workflows/fixing-chat-ui-errors.md
- @.agent/workflows/deploying-to-aks.md

---

**Monitor Duration**: ~10 minutes (default)  
**Auto-Fixes**: 3 common issues  
**Exit Conditions**: All healthy OR max checks reached
