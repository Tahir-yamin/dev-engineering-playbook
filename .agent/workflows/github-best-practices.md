---
description: Best practices for GitHub repository management, security, and environment handling
---

# GitHub Best Practices Workflow

## When to Use
- Setting up a new repository
- Auditing an existing repository
- Configuring security features
- Managing secrets and environment variables

---

## Step 1: Repository Configuration

### Visibility
- **Private**: Default for any project with proprietary code or business logic.
- **Public**: Only for open source libraries or portfolios (ensure NO secrets are present).

### Branch Protection (Settings -> Branches)
- Require pull request reviews before merging.
- Require status checks to pass before merging (CI/CD).
- **Crucial**: "Do not allow bypassing the above settings" (even for admins).

---

## Step 2: The Critical .gitignore

**Never** rely on manual exclusion. Your `.gitignore` must be robust.

// turbo
```bash
# Create or update .gitignore
echo "node_modules/" >> .gitignore
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
echo "!.env.example" >> .gitignore
echo ".DS_Store" >> .gitignore
echo "coverage/" >> .gitignore
echo ".vscode/" >> .gitignore
```

**Verification**:
```bash
git check-ignore -v .env
# Should output: .gitignore:X:.env
```

---

## Step 3: Secret Management

### 1. Environment Variables
- **NEVER** commit `.env` files.
- **ALWAYS** provide `.env.example` with dummy values.
- **Use** `scripts/validate-env.ps1` (if available) to check local env.

### 2. GitHub Secrets (Settings -> Secrets and variables -> Actions)
- Store production secrets here (e.g., `DATABASE_URL`, `AWS_KEYS`).
- Never print secrets in CI logs.

### 3. Secret Scanning (Settings -> Security & analysis)
- Enable **Secret scanning**: GitHub will alert you if you push a known secret format.
- Enable **Push protection**: Blocks commits containing secrets.

---

## Step 4: Vulnerability Management

### Dependabot (Settings -> Security & analysis)
- Enable **Dependabot alerts**.
- Enable **Dependabot security updates**.
- **Configuration** (`.github/dependabot.yml`):
```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

---

## Step 5: Pre-Commit Hooks (Prevention)

Prevent accidental commits of secrets or bad code.

```bash
# Install Husky
npm install --save-dev husky
npx husky init

# Add pre-commit hook
echo "npm test" > .husky/pre-commit
```

**Recommended**: Use `git-secrets` or similar tools in pre-commit to scan for keys.

---

## Step 6: Audit Existing Repo

If you suspect secrets were committed in the past:

1. **Scan history**:
   ```bash
   # using trufflehog (install first)
   trufflehog git file://. --only-verified
   ```

2. **Remove secrets**:
   - If found, **ROTATE THE SECRET IMMEDIATELY**.
   - Use `BFG Repo-Cleaner` or `git filter-repo` to remove file from history.
   - **Warning**: Changing history breaks forks/clones.

---

## Step 7: Security Policy

Create `SECURITY.md` in root:
- Instructions on how to report vulnerabilities.
- Supported versions.

---

## Step 8: License

- Add a `LICENSE` file (MIT, Apache 2.0, etc.) to clearly define usage rights.

---

## Step 9: Routine Security Audits

For handling alerts (Code Scanning, Dependabot, Secrets), follow the **[Security Remediation Workflow](./security-remediation.md)**.

---

## Step 10: Handling Large Files & Git Push Failures

### When This Section Applies
- `git push` fails with "Resolving deltas" error
- "remote rejected" errors during push
- Large binary files in repository (>10MB)
- Repository has complex history/conflicts

### Common Symptoms
- Push fails at "Resolving deltas" phase
- Error: "failed to push some refs"
- Error: "remote rejected main -> main"
- Large files causing timeout/memory issues

---

### Step 10.1: Identify Large Files

Before committing, check for large files:

```powershell
# turbo
# Find files larger than 10MB
Get-ChildItem -Recurse -File | Where-Object {$_.Length -gt 10MB} | 
  Select-Object FullName, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB,2)}} |
  Sort-Object "Size(MB)" -Descending

# Check what's being tracked by git
git ls-files --cached | ForEach-Object { Get-Item $_ -ErrorAction SilentlyContinue } | 
  Where-Object { $_.Length -gt 10MB }
```

**GitHub Limits**:
- File size limit: 100MB (hard limit)
- Recommended: Keep files under 10MB
- Use Git LFS for legitimate large files (datasets, models)

---

### Step 10.2: Enhance .gitignore for Large Files

Add these patterns to exclude common large files:

```bash
# turbo
# Append to .gitignore
cat >> .gitignore << 'EOF'

# Large binary files
*.zip
*.exe
*.dll
*.so
*.dylib
*.tar.gz
*.rar
*.7z

# Data and temp files
data/
logs/
*.log
*.tmp
*_extracted/
*_backup/

# Build outputs
*.min.js
*.map
build/
dist/
EOF
```

**Verify exclusions**:
```powershell
# Check if specific file is ignored
git check-ignore -v large_file.zip
# Should output: .gitignore:X:*.zip

# See all ignored files
git status --ignored
```

---

### Step 10.3: Remove Large Files from Git Tracking

If you've already committed large files:

```powershell
# Remove single file (keeps on disk)
git rm --cached filename.zip

# Remove directory (keeps on disk)
git rm --cached -r data/ -f

# Remove multiple files matching pattern
git rm --cached *.exe

# Verify removal
git status
# Files should appear as untracked (red), not deleted
```

**Then update .gitignore and commit**:
```powershell
git add .gitignore
git commit -m "chore: Remove large files from git tracking and update .gitignore"
```

---

### Step 10.4: Sync with Remote (Fix Push Conflicts)

If push fails due to diverged history:

```powershell
# Fetch latest remote state
git fetch origin

# Option A: Merge (safer, keeps full history)
git pull origin main --no-rebase

# Option B: Rebase (cleaner linear history)
git pull origin main --rebase

# Option C: Hard reset (⚠️ loses local changes)
git reset --hard origin/main
```

**Choose based on situation**:
- ✅ Use **merge** if multiple people working on repo
- ✅ Use **rebase** for personal repos/clean history
- ⚠️ Use **hard reset** only if you're sure local changes don't matter

---

### Step 10.5: Alternative - Dedicated Folder Strategy

If standard push still fails due to complex conflicts:

```powershell
# Create isolated folder for new code
New-Item -ItemType Directory -Path "phase5" -Force

# Copy only essential files (NO binaries)
Copy-Item "source/*.py" "phase5/" -Recurse -Exclude *.zip,*.exe

# Add and push ONLY the new folder
git add phase5/
git commit -m "feat(Phase 5): Add new implementation in isolated folder"
git push origin main
```

**Advantages**:
- ✅ Avoids conflicts with existing structure
- ✅ Clean separation of concerns
- ✅ Smaller, focused commits
- ✅ Easier code review
- ✅ Can be deleted/archived independently

---

### Step 10.6: Verify Push Success

```powershell
# Check local status
git status

# Verify remote has commit
git log origin/main --oneline -5

# Compare local and remote
git log origin/main..HEAD
# Should show nothing (all pushed)
```

**Visit GitHub**: Check repository to confirm files are there

---

### Step 10.7: Git LFS for Legitimate Large Files

If you MUST track large files (models, datasets):

```bash
# Install Git LFS
git lfs install

# Track specific file types
git lfs track "*.psd"
git lfs track "*.zip"
git lfs track "data/*.csv"

# Add .gitattributes (created by git lfs track)
git add .gitattributes

# Now add large files
git add large_model.psd
git commit -m "Add large files via Git LFS"
git push origin main
```

**Git LFS Benefits**:
- Replaces large files with text pointers in Git
- Actual files stored on LFS server
- Much faster cloning and operations

---

### Common Push Failure Troubleshooting

#### Error: "Resolving deltas" hangs
**Cause**: Large binaries timing out  
**Solution**: Remove binaries, use .gitignore, try dedicated folder approach

#### Error: "remote rejected"  
**Cause**: Local/remote history diverged  
**Solution**: `git fetch origin`, then `git pull origin main`

#### Error: "file size exceeds 100MB"
**Cause**: GitHub hard limit hit  
**Solution**: Remove file, use Git LFS, or host file elsewhere

#### Push succeeds but takes 10+ minutes
**Cause**: Large repository or slow connection  
**Solution**: Use .gitignore more aggressively, consider monorepo alternatives

---

### Emergency: Accidentally Pushed Large File

```powershell
# 1. Remove from latest commit (before anyone pulls)
git reset HEAD~1
git rm --cached large_file.zip
git commit -m "chore: Remove large file"
git push --force-with-lease origin main

# 2. Already pushed and others pulled? Use BFG Repo-Cleaner
# Download from: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files large_file.zip
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force --all

# ⚠️ WARNING: Force push notifies all collaborators to re-clone
```

---

### Best Practices Summary

**Prevention**:
1. ✅ Set up comprehensive .gitignore BEFORE first commit
2. ✅ Run `git check-ignore` to verify exclusions work
3. ✅ Check file sizes before `git add` (use workflow Step 10.1)
4. ✅ Use Git LFS for legitimate large files
5. ✅ Commit small, focused changes frequently

**If Push Fails**:
1. ✅ Don't panic - nothing is broken locally
2. ✅ Identify large files (Step 10.1)
3. ✅ Remove from git cache (Step 10.3)
4. ✅ Update .gitignore (Step 10.2)
5. ✅ Sync with remote (Step 10.4)
6. ✅ Try dedicated folder if still failing (Step 10.5)

**Web Search Template**:
- "git push failed Resolving deltas error solution 2026"
- "github large file error fix"
- "git remove file from history"

---

**Related Workflows**: `/security-audit` - Check for secrets before push  
**Related Skills**: `.claude/git-large-files-skills.md`, `.claude/github-best-practices-skills.md`
