---
description: Troubleshoot and resolve git push failures with large files and repository conflicts
---

# Git Push Failures with Large Files Workflow

## When to Use
- `git push` fails with "Resolving deltas" error
- "remote rejected" errors during push
- Large binary files in repository (>10MB)
- Repository has complex history/conflicts

---

## The Problem

**Symptoms**:
- Push fails at "Resolving deltas" phase
- Error: "failed to push some refs"
- Error: "remote rejected main -> main"
- Large files causing timeout/memory issues

**Common Causes**:
1. Large binary files (*.zip, *.exe, data folders)
2. Local/remote history divergence
3. .gitignore missing essential entries
4. Repository corruption or conflicts

---

## Step 1: Identify Large Files

```powershell
# Find files larger than 10MB
Get-ChildItem -Recurse -File | Where-Object {$_.Length -gt 10MB} | Select-Object FullName, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB,2)}}

# Check what's being tracked by git
git ls-files --cached | ForEach-Object { Get-Item $_ -ErrorAction SilentlyContinue } | Where-Object { $_.Length -gt 10MB }
```

**Expected Output**: List of large files that shouldn't be in repo

---

## Step 2: Update .gitignore (GitHub Best Practices)

```powershell
# turbo
# Add comprehensive .gitignore entries
Add-Content -Path .gitignore -Value @"

# Large binary files
*.zip
*.exe
*.dll
*.so
*.dylib

# Build artifacts
*_extracted/
data/
dist/
build/

# Dependencies
node_modules/
venv/
.venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
"@
```

**Verification**:
```powershell
# Check if .env is ignored
git check-ignore -v .env
# Should output: .gitignore:X:.env
```

---

## Step 3: Remove Large Files from Git Cache

```powershell
# Remove specific large files
git rm --cached file1.zip file2.exe -f

# Remove entire directories
git rm --cached -r data/ extracted_folders/ -f

# Verify removal
git status --short
```

**Important**: Files are removed from git tracking but remain on disk

---

## Step 4: Sync with Remote

```powershell
# Fetch latest remote state
git fetch origin

# Option A: Merge (if you want to keep both histories)
git pull origin main --no-rebase

# Option B: Rebase (for cleaner history)
git pull origin main --rebase

# Option C: Hard reset (if local changes can be discarded)
git reset --hard origin/main
```

---

## Step 5: Create Clean Commit

```powershell
# Stage .gitignore update
git add .gitignore

# Create commit with descriptive message
git commit -m "chore: Update .gitignore to exclude large binaries

- Exclude *.zip, *.exe, data/ per GitHub best practices
- Remove large files from git tracking
- Fix push failures caused by binary files

Resolves git push 'Resolving deltas' errors"

# Push to remote
git push origin main
```

---

## Alternative Solution: Dedicated Folder Approach

If push still fails due to conflicts with existing structure:

```powershell
# Create new isolated folder (e.g., phase5/)
New-Item -ItemType Directory -Path "phase5" -Force

# Copy only essential code files (no binaries)
Copy-Item "source/code.py" "phase5/code.py"

# Add, commit, and push ONLY the new folder
git add phase5/
git commit -m "feat: Add phase5 implementation"
git push origin main
```

**Advantages**:
- ✅ Avoids conflicts with existing repo structure
- ✅ Clean separation of concerns
- ✅ Smaller, focused commits
- ✅ Easier to troubleshoot

---

## Step 6: Verify Success

```powershell
# Check push status
git status

# Verify remote has your commit
git log origin/main --oneline -5

# Check GitHub (visit your repo URL)
```

**Success Indicators**:
- "Your branch is up to date with 'origin/main'"
- Latest commit visible on GitHub
- No error messages

---

## Common Pitfalls

### ❌ Don't Do This:
```powershell
# Committing large binaries
git add *.zip          # These should be in .gitignore!

# Force pushing without checking
git push --force       # Can destroy others' work!

# Ignoring .gitignore warnings
```

### ✅ Do This Instead:
```powershell
# Check what you're adding
git add -p             # Interactive staging

# Use safer force push
git push --force-with-lease   # Safer than --force

# Verify .gitignore works
git check-ignore file.zip
```

---

## Web Search Solutions Used

**Search Query**: "git push failed Resolving deltas error large files solution"

**Key Findings**:
1. **Git LFS** - For repositories that MUST track large files
2. **.gitignore** - Exclude files BEFORE they're committed
3. **git rm --cached** - Remove from tracking, keep on disk
4. **Dedicated folders** - Isolate new code from conflicts

---

## Lessons Learned

### ✅ What Worked:
1. **Dedicated folder approach** - phase5/ avoided all conflicts
2. **Comprehensive .gitignore** - Excluded all binary types
3. **git rm --cached** - Removed files without deleting locally
4. **Web search first** - Saved time vs trial-and-error

### ❌ What Didn't Work:
1. **Force push on conflicts** - Failed at "Resolving deltas"
2. **Rebase without removing binaries** - Still too large
3. **Multiple conflicting strategies** - Made things worse
4. **Assuming files were ignored** - Always verify with git check-ignore

### 💡 Best Practices:
1. **Set up .gitignore FIRST** - Before any commits
2. **Check file sizes** - Before git add
3. **Use Git LFS** - For legitimate large files
4. **Verify exclusions** - git check-ignore before committing
5. **Commit frequently** - Smaller commits = easier troubleshooting

---

## Related Skills

- `.claude/github-best-practices-skills.md` - Skill #1: .gitignore configuration
- `.claude/git-troubleshooting-skills.md` - Skill #2: Resolving push failures
- `.agent/workflows/github-best-practices.md` - Secret management

---

## Quick Reference

```powershell
# Find large files
Get-ChildItem -Recurse -File | Where-Object {$_.Length -gt 10MB}

# Update .gitignore
Add-Content .gitignore "*.zip`n*.exe`ndata/"

# Remove from git (keep locally)
git rm --cached -r large_folder/

# Sync and push
git fetch origin
git pull origin main
git push origin main
```

---

**Created**: January 2026  
**Source**: Phase 5 Dapr Integration Deployment  
**Success Rate**: ✅ 100% (after applying dedicated folder approach)
