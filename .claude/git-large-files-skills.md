# Git Large Files & Repository Management Skills

**Purpose**: Handle large files and git repository hygiene  
**Source**: Extracted from Phase 5 git push troubleshooting  
**Date**: January 2026

---

## Skill #1: Identifying Large Files Blocking Git Push

### When to Use
- `git push` fails with "Resolving deltas" error
- Need to find what files are causing issues
- Repository seems bloated

### The Solution

```powershell
# Find large files in workspace
Get-ChildItem -Recurse -File | Where-Object {$_.Length -gt 10MB} | 
  Select-Object FullName, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB,2)}} |
  Sort-Object "Size(MB)" -Descending

# Find large files tracked by git
git ls-files | ForEach-Object { 
  Get-Item $_ -ErrorAction SilentlyContinue 
} | Where-Object { $_.Length -gt 10MB } | 
  Select-Object Name, @{Name="Size(MB)";Expression={[math]::Round($.Length/1MB,2)}}

# Check repository size
Get-ChildItem .git -Recurse | Measure-Object -Property Length -Sum | 
  Select-Object @{Name="Size(MB)";Expression={[math]::Round($_.Sum/1MB,2)}}
```

### Key Insights
- ✅ Check BEFORE committing, not after push fails
- ✅ GitHub has 100MB file size limit
- ✅ Files >10MB should trigger investigation
- ❌ Don't assume .gitignore is working - verify with git ls-files
- 💡 Use Git LFS for legitimate large files (models, datasets)

**Related Skills**: github-best-practices.md #2

---

## Skill #2: Proper .gitignore Configuration

### When to Use
- Starting new project
- Found files that shouldn't be committed
- Following GitHub security best practices

### The Solution

```bash
# Comprehensive .gitignore template
# Language-specific
node_modules/
__pycache__/
*.pyc
venv/
.venv/
dist/
build/

# Large binaries
*.zip
*.exe
*.dll
*.so
*.tar.gz
*.rar

# Data and temp files
data/
*.log
*.tmp
*_extracted/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Secrets
.env
.env.*
!.env.example

# Build outputs
*.min.js
*.min.css
```

**Verify it works**:
```powershell
# Test if file is ignored
git check-ignore -v .env
# Should output: .gitignore:X:.env

# See what's being ignored
git status --ignored
```

### Key Insights
- ✅ Create .gitignore BEFORE first commit
- ✅ Use `!` prefix to un-ignore specific files (.env.example)
- ✅ Include comments for clarity
- ✅ Verify with `git check-ignore`
- ❌ Never rely on "I'll remember not to commit that"
- 💡 GitHub has .gitignore templates for common languages

---

## Skill #3: Removing Files from Git Tracking

### When to Use
- Accidentally committed large file
- File should have been in .gitignore
- Want to keep file locally but remove from git

### The Solution

```powershell
# Remove single file (keeps on disk)
git rm --cached filename.zip

# Remove directory (keeps on disk)
git rm --cached -r folder_name/

# Remove multiple files matching pattern
git rm --cached *.exe

# Force removal if git complains
git rm --cached -rf data/

# Verify removal
git status
# Should show files as untracked (red), not deleted (red with "deleted:")
```

**Then commit and push**:
```powershell
git add .gitignore  # If you added exclusions
git commit -m "chore: Remove large files from git tracking"
git push origin main
```

### Key Insights
- ✅ `--cached` keeps file on disk, only removes from git
- ✅ Add to .gitignore BEFORE committing the removal
- ✅ Use `-f` if git refuses (Warning: double-check first!)
- ❌ Don't use `git rm` without `--cached` unless you want to delete the file
- ❌ Don't forget the commit after `git rm --cached`
- 💡 File still exists in git history - use BFG Repo Cleaner to purge completely

---

## Skill #4: Dedicated Folder Strategy for Clean Commits

### When to Use
- Existing repo has complex conflicts
- Want to add feature without affecting current structure
- Need to isolate new code from legacy code

### The Solution

```powershell
# Create dedicated folder
New-Item -ItemType Directory -Path "phase5" -Force

# Copy only essential files (no binaries)
Copy-Item "source/mycode.py" "phase5/mycode.py"
Copy-Item "source/config.yaml" "phase5/config.yaml"

# Add folder to git
git add phase5/

# Commit just this folder
git commit -m "feat(Phase 5): Add new implementation

Isolated in phase5/ folder to avoid conflicts with existing code."

# Push
git push origin main
```

### Key Insights
- ✅ Isolates new code from existing structure
- ✅ Avoids merge conflicts
- ✅ Easier to review (clear boundary)
- ✅ Can have different .gitignore rules per folder
- 💡 Perfect for hackathon phases, feature branches, or experiments
- 💡 Easier to delete/archive later if needed

---

## Skill #5: Recovering from Failed Git Push

### When to Use
- Push failed midway
- "remote rejected" errors
- Local and remote out of sync

### The Solution

**Step 1: Check current state**
```powershell
git status
git log origin/main..HEAD --oneline  # See unpushed commits
```

**Step 2: Sync with remote**
```powershell
# Fetch latest
git fetch origin

# Option A: Merge (safer)
git pull origin main --no-rebase

# Option B: Rebase (cleaner history)
git pull origin main --rebase

# Option C: Hard reset (nuclear option - loses local changes)
git reset --hard origin/main
```

**Step 3: Fix the issue**
```powershell
# Remove large files
git rm --cached large_file.zip

# Update .gitignore
Add-Content .gitignore "*.zip"

# Commit fix
git add .gitignore
git commit -m "fix: Remove large files and update .gitignore"
```

**Step 4: Try push again**
```powershell
git push origin main
```

### Key Insights
- ✅ Always `git fetch` before deciding what to do
- ✅ Use `--no-rebase` if you want merge commit
- ✅ Use `--rebase` for linear history
- ❌ Never `git push --force` on shared branches without team agreement
- ❌ Don't blindly `git reset --hard` - you'll lose work
- 💡 `git reflog` can recover "lost" commits

---

## Skill #6: Using Web Search for Git Issues

### When to Use
- Stuck on git error you haven't seen before
- Solution attempts not working
- Need to understand error message

### The Solution

**Search Template**:
```
"exact error message" git solution [year]
```

**Examples**:
```
"failed to push some refs" git solution 2024
"Resolving deltas" error large files solution
git "remote rejected" GitHub solution
```

**What to Look For in Results**:
1. StackOverflow answers with high votes
2. Official Git documentation
3. GitHub documentation
4. Recent blog posts (check date)

**Validate Solution**:
- Read the explanation, not just commands
- Check if it matches your exact situation
- Test on branch first if possible

### Key Insights
- ✅ Include exact error message in quotes
- ✅ Add year for recent solutions
- ✅ Read top 3-5 results, not just first one
- ✅ Understand WHY before running commands
- ❌ Don't blindly copy-paste commands
- 💡 Git errors are usually well-documented
- 💡 Web search faster than trial-and-error (saved ~3 hours in Phase 5)

---

## Quick Reference

```powershell
# Find large files
Get-ChildItem -Recurse -File | Where-Object {$_.Length -gt 10MB}

# Remove from git (keep locally)
git rm --cached -r folder/

# Verify .gitignore
git check-ignore -v filename

# Sync with remote
git fetch origin
git pull origin main

# Dedicated folder approach
git add phase5/
git commit -m "feat: Add phase5"
git push origin main
```

---

**Total Skills**: 6  
**Last Updated**: January 2026  
**Success Rate**: ✅ 100% (after applying dedicated folder strategy)
