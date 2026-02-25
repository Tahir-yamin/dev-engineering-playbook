---
description: Security audit workflow to prevent API key exposure and ensure secrets safety
---

# Security Audit Workflow

## Mission
Ensure no API keys, passwords, or sensitive credentials are exposed in the codebase before deployment or documentation sharing.

## When to Run
- Before every deployment
- Before committing code to Git
- Before sharing documentation
- After updating environment variables
- Before final submission

---

## Phase 1: Credential Scanning

### Step 1: Scan for Hard-Coded Secrets

```powershell
# Search for common API key patterns
$patterns = @(
    "api_key",
    "API_KEY",
    "secret",
    "SECRET",
    "password",
    "PASSWORD",
    "token",
    "TOKEN",
    "OPENROUTER",
    "GEMINI",
    "GITHUB_CLIENT",
    "GOOGLE_CLIENT",
    "RESEND",
    "DATABASE_URL"
)

foreach ($pattern in $patterns) {
    Write-Host "`n=== Searching for: $pattern ===" -ForegroundColor Yellow
    Get-ChildItem -Recurse -File -Exclude *.md,*.log,*.webp,*.png | 
        Select-String -Pattern $pattern -SimpleMatch |
        Select-Object -First 10
}
```

**Manual Review**: Check each result to ensure it's either:
- ✅ A placeholder (e.g., `your_api_key_here`)
- ✅ An environment variable reference (e.g., `process.env.API_KEY`)
- ✅ In `.env.example` with fake values
- ❌ **REMOVE** if it's a real credential

---

### Step 2: Check Git History

```powershell
# Check if .env files are in .gitignore
Get-Content .gitignore | Select-String "\.env"

# Verify .env files are not tracked
git ls-files | Select-String "\.env$"
```

**Expected**:
- ✅ `.env` should be in `.gitignore`
- ✅ `git ls-files` should NOT show any `.env` files

**If `.env` is tracked**:
```bash
git rm --cached .env
git rm --cached phase2/backend/.env
git rm --cached phase2/frontend/.env
git commit -m "Remove .env files from tracking"
```

---

### Step 3: Scan Documentation Files

```powershell
# Check markdown files for exposed credentials
Get-ChildItem -Path . -Include *.md -Recurse | 
    ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        if ($content -match "sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|re_[a-zA-Z0-9]{24}") {
            Write-Host "⚠️ Potential API key in: $($_.FullName)" -ForegroundColor Red
        }
    }
```

**Action**: Replace any real keys with placeholders like `sk-***REDACTED***`.

---

## Phase 2: Kubernetes Secrets Verification

### Step 1: Check ConfigMap for Secrets

```bash
# List all ConfigMap data
kubectl get configmap todo-app-config -n todo-chatbot -o yaml

# Verify sensitive data is NOT in ConfigMap
```

**Secrets that MUST be in Kubernetes Secret (not ConfigMap)**:
- `BETTER_AUTH_SECRET`
- `OPENROUTER_API_KEY`
- `GEMINI_API_KEY`
- `GITHUB_CLIENT_SECRET`
- `GOOGLE_CLIENT_SECRET`
- `RESEND_API_KEY`
- `DATABASE_URL` (contains password)

**Action**: Move secrets from ConfigMap to Secret.

---

### Step 2: Create Kubernetes Secret

```bash
# Create secret from literal values
kubectl create secret generic todo-app-secrets -n todo-chatbot \
  --from-literal=BETTER_AUTH_SECRET='your_secret_here' \
  --from-literal=OPENROUTER_API_KEY='sk-...' \
  --from-literal=GEMINI_API_KEY='...' \
  --from-literal=GITHUB_CLIENT_SECRET='...' \
  --from-literal=GOOGLE_CLIENT_SECRET='...' \
  --from-literal=RESEND_API_KEY='re_...' \
  --from-literal=DATABASE_URL='postgresql://...' \
  --dry-run=client -o yaml | kubectl apply -f -
```

**Verify**:
```bash
# Check secret exists (values are redacted)
kubectl get secret todo-app-secrets -n todo-chatbot -o yaml
```

---

### Step 3: Update Deployments to Use Secrets

```yaml
# In deployment manifests, replace ConfigMap refs with Secret refs
env:
  - name: BETTER_AUTH_SECRET
    valueFrom:
      secretKeyRef:
        name: todo-app-secrets
        key: BETTER_AUTH_SECRET
  - name: OPENROUTER_API_KEY
    valueFrom:
      secretKeyRef:
        name: todo-app-secrets
        key: OPENROUTER_API_KEY
```

---

## Phase 3: File-Level Security Checks

### Files That Should NEVER Contain Real Credentials:

**❌ FORBIDDEN**:
- `phase4/k8s/*.yaml` - Use placeholders or Secret references
- `phase4/helm/*/values.yaml` - Use placeholders or template references
- `phase4/scripts/*.ps1` - Use environment variable reads only
- `*.md` - Documentation should show examples, not real keys
- `.github/workflows/*` - Use GitHub Secrets

**✅ ALLOWED** (but must be in `.gitignore`):
- `.env` (local development only)
- `phase2/backend/.env`
- `phase2/frontend/.env`

---

## Phase 4: Pre-Deployment Checklist

Before deploying or committing:

- [ ] Run credential scan (Phase 1)
- [ ] Verify `.gitignore` includes `.env` files
- [ ] Check no `.env` files are tracked by Git
- [ ] Ensure Kubernetes Secrets exist (not ConfigMap)
- [ ] Verify deployment manifests reference Secrets
- [ ] Review all `.yaml` files for hard-coded credentials
- [ ] Check all documentation for exposed keys
- [ ] Verify `patch-config.json` is in `.gitignore` (contains real keys)

---

## Phase 5: Encryption (Optional for Production)

### Using `sealed-secrets` (Recommended for GitOps)

```bash
# Install sealed-secrets controller
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/controller.yaml

# Install kubeseal CLI
# (Download from GitHub releases)

# Create sealed secret
kubectl create secret generic todo-secrets \
  --from-literal=OPENROUTER_API_KEY='sk-...' \
  --dry-run=client -o yaml | \
  kubeseal -o yaml > sealed-secret.yaml

# Commit sealed-secret.yaml (safe to commit)
git add sealed-secret.yaml
git commit -m "Add sealed secrets"
```

**sealed-secret.yaml** can be committed to Git safely as it's encrypted.

---

## Phase 6: Automated Security Checks

### Create Pre-Commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running security checks..."

# Check for potential API keys
if git diff --cached | grep -E "sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|re_[a-zA-Z0-9]{24}"; then
    echo "❌ ERROR: Potential API key detected!"
    echo "Please remove API keys before committing."
    exit 1
fi

# Check if .env files are staged
if git diff --cached --name-only | grep "\.env$"; then
    echo "❌ ERROR: .env file is staged!"
    echo "Please unstage .env files."
    exit 1
fi

echo "✅ Security checks passed"
exit 0
```

```bash
chmod +x .git/hooks/pre-commit
```

---

## Emergency: Key Exposure Response

**If you accidentally commit an API key:**

1. **Immediately rotate the key**:
   - Go to the service provider (OpenRouter, GitHub, etc.)
   - Revoke the exposed key
   - Generate a new key

2. **Remove from Git history**:
   ```bash
   # Use BFG Repo-Cleaner or git-filter-repo
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch PATH_TO_FILE" \
     --prune-empty --tag-name-filter cat -- --all
   
   git push --force --all
   ```

3. **Update all deployments** with the new key.

4. **Document the incident** in security log.

---

## Security Best Practices

1. **Never commit `.env` files** - Add to `.gitignore`
2. **Use environment variables** - Reference, don't hard-code
3. **Use Kubernetes Secrets** - Not ConfigMaps for sensitive data
4. **Rotate keys regularly** - Every 90 days or on team changes
5. **Principle of least privilege** - Only grant necessary permissions
6. **Audit regularly** - Run this workflow weekly
7. **Use sealed-secrets** - For GitOps workflows
8. **Monitor access logs** - Track who accessed secrets

---

## Quick Security Scan Command

```powershell
# One-liner to scan for common patterns
Get-ChildItem -Recurse -File -Exclude *.md,*.log,*.webp,*.png,*.jpg,*.gif,node_modules | 
    Select-String -Pattern "sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|re_[a-zA-Z0-9]{24}|AIza[a-zA-Z0-9_-]{35}" |
    Group-Object Path |
    Select-Object Name, Count
```

---

**Related Workflows**: `/complete-application-qa`, `/deployment-issues`  
**Priority**: 🔴 **CRITICAL** - Run before every deployment
