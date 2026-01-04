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

**Related Skills**: env-skills.md #2, debug-skills.md
