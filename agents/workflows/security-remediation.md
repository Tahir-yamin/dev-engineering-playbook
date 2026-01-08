---
description: Workflow for checking and resolving GitHub security alerts (Code Scanning, Dependabot, Secrets)
---

# Security Remediation Workflow

## When to Use
- You receive a GitHub Security Alert
- Routine security audit (weekly/monthly)
- Before a major release
- "Dependabot alerts" notification

---

## Step 1: Perform Manual Security Audit (Local)

Before waiting for GitHub alerts, you can proactively scan your local codebase.

1. **Dependency Check**:
   ```bash
   # Frontend
   cd phase2/frontend
   npm audit

   # Backend (if using safety or pip-audit)
   pip install safety
   safety check
   ```

2. **Secret Scanning (Grep Check)**:
   Run these commands to find potential leaks:
   ```bash
   # Find potential API keys
   grep -r "API_KEY" . --exclude-dir={node_modules,venv,.git}
   
   # Find hardcoded passwords
   grep -r "password" . --exclude-dir={node_modules,venv,.git}
   ```
   *Verify that any matches are either in `.env.example` (placeholders) or test scripts (dummy data).*

3. **Code Pattern Scan**:
   Check for dangerous functions:
   ```bash
   # Frontend: Check for XSS risks
   grep -r "dangerouslySetInnerHTML" .
   
   # Backend: Check for SQL injection risks (f-strings in execute)
   grep -r "cursor.execute(f" .
   ```

---

## Step 2: Access Security Dashboard

1. Go to your GitHub Repository.
2. Click **Security** tab.
3. Review the overview dashboard.

---

## Step 3: Handle Dependabot Alerts (Dependencies)

**Goal**: Update vulnerable dependencies.

1. **Filter**: Go to **Dependabot alerts**.
2. **Prioritize**: Sort by "Critical" and "High" severity.
3. **Analyze**: Click an alert to see:
   - Vulnerable package
   - Patched version
   - Impact
4. **Remediate**:
   - **Option A (Automated)**: If Dependabot opened a PR, review the "Compatibility Score". If high, merge it.
   - **Option B (Manual)**:
     ```bash
     # Example: Update specific package
     npm install package-name@latest
     # or
     pip install --upgrade package-name
     ```
   - **Option C (False Positive)**: If the vulnerable code isn't used, you can dismiss the alert (Select "Vulnerable code is not actually used").

5. **Verify**: Run tests after updating.
   ```bash
   npm test
   # or
   pytest
   ```

---

## Step 4: Handle Code Scanning Alerts (CodeQL)

**Goal**: Fix security vulnerabilities in your code (SQLi, XSS, etc.).

1. **Filter**: Go to **Code scanning**.
2. **Analyze**: Click an alert.
   - View the **Data flow analysis** (Show paths).
   - Understand how untrusted input reaches a sensitive sink.
3. **Remediate**:
   - **Fix the code**: Apply input validation, output encoding, or use safe APIs.
   - **Example (SQL Injection)**:
     ```python
     # BAD
     cursor.execute(f"SELECT * FROM users WHERE id = {user_input}")
     
     # GOOD (Parameterized)
     cursor.execute("SELECT * FROM users WHERE id = %s", (user_input,))
     ```
4. **Commit**: Push the fix. CodeQL will automatically rescan and close the alert if fixed.

---

## Step 5: Handle Secret Scanning Alerts

**Goal**: Rotate exposed secrets immediately.

1. **Filter**: Go to **Secret scanning**.
2. **Analyze**: Identify the secret (API Key, Token, Password) and where it was committed.
3. **Remediate (CRITICAL)**:
   - **REVOKE** the exposed secret immediately in the service provider (AWS, OpenAI, etc.).
   - **Generate** a new secret.
   - **Update** your environment variables (e.g., GitHub Actions Secrets, `.env` on server).
   - **Remove** the secret from git history (optional but recommended using BFG or `git filter-repo`).
4. **Close**: Mark as "Revoked" in GitHub.

---

## Step 6: Routine Audit Checklist

- [ ] Check **Security** tab for new alerts.
- [ ] Verify **Dependabot** PRs are not stale.
- [ ] Review **Access** (Settings -> Collaborators): Remove inactive users.
- [ ] Rotate **Personal Access Tokens** (PATs) if nearing expiration.
- [ ] Check **Deploy Keys** and **Webhooks** for unused entries.

---

## Step 7: GitHub Post-Remediation

After resolving issues locally or via PRs:

1. **Verify Status**:
   - Go to **Security** tab.
   - Ensure "Dependabot alerts" count is 0 (or only low severity).
   - Ensure "Code scanning" alerts are closed.
   - Ensure "Secret scanning" shows no active secrets.

2. **Lock It Down**:
   - If you fixed a secret leak, ensure the old secret is **Revoked**.
   - If you fixed a dependency, ensure `package-lock.json` is committed.

3. **Enable Protections** (if not already):
   - **Settings** -> **Code security and analysis**:
     - Enable "Dependabot security updates" (Automated PRs).
     - Enable "Secret scanning" (Push protection).

---

**Related Workflows**: github-best-practices.md
