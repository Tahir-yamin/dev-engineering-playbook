# DevOps Auto-Run Commands Policy

**Purpose**: Define which commands are safe to auto-run without user approval  
**Status**: Active Memory Profile  
**Last Updated**: January 8, 2026

---

## 🎯 Auto-Run Policy

Commands marked with `SafeToAutoRun: true` should meet ALL criteria:
1. **Read-only** or have **NO destructive side-effects**
2. **Fast execution** (< 5 seconds typically)
3. **No external dependencies** that might fail
4. **No system modifications** (no installs, no deletions)
5. **No network calls** to external services (internal K8s OK)

---

## ✅ SAFE Auto-Run Commands

### Git Operations (Read-Only)
```powershell
# Always safe
git status
git log --oneline -5
git log origin/main..HEAD
git diff origin/main
git branch
git remote -v
git check-ignore -v <file>
git ls-files

# Safe with parameters
git log --graph --oneline -10
git show <commit>
```

### File System (Read-Only)
```powershell
# Always safe
Get-ChildItem
Get-Content <file>
Test-Path <path>
ls, dir, cat  # Aliases

# Safe searches
Get-ChildItem -Recurse -File | Where-Object {$_.Length -gt 10MB}
find, grep patterns (read-only)
```

### Kubernetes (Read-Only)
```bash
# Always safe
kubectl get pods
kubectl get services
kubectl get deployments
kubectl get nodes
kubectl describe pod <name>
kubectl logs <pod>
kubectl get events

# Safe with namespace
kubectl get all -n <namespace>
kubectl get components -n <namespace>
```

### Docker (Read-Only)
```bash
# Always safe
docker ps
docker images
docker inspect <container>
docker logs <container>
```

### Package Managers (Info Only)
```bash
# npm (read-only)
npm list
npm outdated
npm version

# pip (read-only)
pip list
pip show <package>
```

### Azure CLI (Read-Only)
```bash
# Safe queries
az aks list
az aks show --name <cluster> --resource-group <rg>
az acr list
az account show
```

---

## ⚠️ REQUIRE APPROVAL

### Git Operations (Write)
```powershell
# Always require approval
git add
git commit
git push
git reset
git revert
git merge
git rebase
git rm
git checkout
git branch -d
```

### File System (Write)
```powershell
# Always require approval
New-Item
Remove-Item
Move-Item
Copy-Item
Set-Content
Add-Content
Out-File
```

### Kubernetes (Write/Destructive)
```bash
# Always require approval
kubectl apply
kubectl delete
kubectl create
kubectl scale
kubectl rollout
kubectl exec
kubectl port-forward  # Opens network connection
```

### Docker (Write/Destructive)
```bash
# Always require approval
docker build
docker push
docker run
docker rm
docker rmi
docker-compose up
docker-compose down
```

### Package Managers (Installs)
```bash
# Always require approval
npm install
npm uninstall
pip install
pip uninstall
helm install
helm upgrade
```

---

## 🔧 Special Cases

### Conditional Auto-Run

**Safe IF preceded by approval in same workflow**:
```powershell
# Workflow with // turbo annotation
// turbo
git add .
git commit -m "message"
git push origin main
```

**Safe IF in .agent/workflows/ with // turbo**:
- Workflow files can mark specific steps as auto-run
- Only those specific steps in that context
- User has approved the workflow by running it

**Safe IF testing/verification**:
```bash
# After deployment (read-only verification)
curl http://localhost:8000/health
kubectl get pods -n <namespace>  # Verify deployment
```

---

## 📋 Decision Matrix

| Command Type | Auto-Run? | Reason |
|--------------|-----------|--------|
| `git status` | ✅ Yes | Read-only, no side-effects |
| `git add` | ❌ No | Modifies staging area |
| `kubectl get` | ✅ Yes | Read-only query |
| `kubectl apply` | ❌ No | Modifies cluster state |
| `Get-Content` | ✅ Yes | Read-only file access |
| `Set-Content` | ❌ No | Modifies files |
| `npm list` | ✅ Yes | Read-only package info |
| `npm install` | ❌ No | Modifies dependencies |
| `docker ps` | ✅ Yes | Read-only container list |
| `docker build` | ❌ No | Creates images, uses resources |
| `curl <URL>` | ✅ Yes | Read-only HTTP GET |
| `curl -X POST` | ❌ No | Modifies remote state |

---

## 🎯 Implementation Guidelines

### In Code
```python
# Auto-run example
run_command(
    CommandLine="git status",
    SafeToAutoRun=true,  # ✅ Safe
    WaitMsBeforeAsync=1000
)

# Requires approval example
run_command(
    CommandLine="git push origin main",
    SafeToAutoRun=false,  # ❌ Requires approval
    WaitMsBeforeAsync=5000
)
```

### In Workflows
```markdown
// turbo
```bash
# This specific command is safe to auto-run in this workflow
kubectl get pods -n todo-chatbot
```
```

---

## 🔐 Security Considerations

**Never Auto-Run**:
1. Commands that delete data
2. Commands that expose secrets
3. Commands that make network calls to external services
4. Commands that install software
5. Commands that modify system configuration
6. Commands that cost money (cloud resources)

**Always Verify Before Auto-Run**:
- Command doesn't access sensitive files
- Command doesn't transmit data externally
- Command execution time is predictable
- Command won't hang or block

---

## 📊 Statistics

**Current Policy**:
- ✅ Safe auto-run commands: ~40
- ❌ Require approval: ~60
- ⚠️ Conditional/context-dependent: ~10

**Coverage**:
- Git operations: 15 safe / 20 total
- Kubernetes: 20 safe / 35 total  
- File operations: 10 safe / 25 total
- Package managers: 5 safe / 15 total

---

## 🔄 Update Protocol

**When to update this policy**:
1. New safe command patterns discovered
2. Security incident related to auto-run
3. User feedback on approval fatigue
4. New tools/technologies added

**How to update**:
1. Edit this file in `.claude/` directory
2. Test new auto-run command thoroughly
3. Document rationale for auto-run approval
4. Commit with clear message

---

**Policy Version**: 1.0  
**Last Review**: January 8, 2026  
**Next Review**: February 8, 2026  
**Owner**: DevOps AI Agent
