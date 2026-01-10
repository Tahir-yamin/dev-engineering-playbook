---
description: Best practices for GitHub repository management, security, and environment handling
---

# GitHub Best Practices & Repository Analysis Workflow Workflow

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

---

## Step 10: Comprehensive Repository Analysis & Bug-Fixing

**Purpose**: Systematic identification, prioritization, fixing, and documentation of ALL verifiable bugs, security vulnerabilities, and critical issues.

**When to Use**:
- Before major releases
- After inheriting a codebase
- During security audits
- When implementing quality improvements

**Reference**: See [comprehensive-bug-analysis.md](./comprehensive-bug-analysis.md) for full detailed workflow

### Quick Overview - 7 Phase Process:

#### Phase 1: Initial Repository Assessment
- Map complete project structure
- Identify technology stack and dependencies
- Document entry points and critical paths
- Analyze build configurations
- Review existing documentation

#### Phase 2: Systematic Bug Discovery
**Categories**:
- Critical: Security vulnerabilities, data corruption, crashes
- Functional: Logic errors, state management issues
- Integration: Database errors,API issues, network problems
- Edge Cases: Null handling, boundary conditions
- Code Quality: Dead code, deprecated APIs, bottlenecks

**Methods**:
- Static code analysis
- Dependency vulnerability scanning
- Code path analysis
- Configuration validation

#### Phase 3: Bug Documentation & Prioritization
- Document each bug with BUG-ID, severity, category
- Root cause analysis
- Impact assessment (user/system/business)
- Prioritization matrix (P0-P3)

#### Phase 4: Fix Implementation
- Create isolated branches for each fix
- Write failing test first (TDD)
- Implement minimal fixes
- Run regression tests

#### Phase 5: Testing & Validation
- Unit, integration, and regression tests
- Static analysis validation
- Performance benchmarks

#### Phase 6: Documentation & Reporting
- Update inline comments and API docs
- Create executive summary
- Generate reports (Markdown, JSON/YAML, CSV)

#### Phase 7: Continuous Improvement
- Identify common bug patterns
- Recommend preventive measures
- Propose process enhancements

### Quick Commands:

\\\ash
# Static Analysis
npm install -g eslint
eslint . --ext .js,.ts

# Security Scanning
npm audit
npm audit fix

# Dependency Vulnerabilities
safety check  # Python
./gradlew dependencyCheckAnalyze  # Java

# Coverage Analysis
npm test -- --coverage
pytest --cov=. --cov-report=html
\\\

### Bug Report Template:

\\\markdown
## BUG-[ID]: [Short Description]

**Severity**: Critical | High | Medium | Low
**Category**: Security | Functional | Integration | Edge Case
**Priority**: P0 | P1 | P2 | P3

### Location
- File(s): path/to/file.js:123
- Component: Module Name
- Function: functionName()

### Current vs Expected Behavior
[What happens vs what should happen]

### Root Cause
[Technical explanation]

### Impact
- User: [H/M/L] - [Details]
- System: [H/M/L] - [Details]
- Business: [H/M/L] - [Details]

### Fix Approach
[Solution strategy]
\\\

### Constraints:

-  Never compromise security for simplicity
-  Maintain audit trail of all changes
-  Follow semantic versioning for API changes
-  Document all assumptions
-  Respect rate limits and quotas

### Success Criteria:

-  All P0 (critical) bugs fixed
-  90%+ P1 (high priority) bugs fixed
-  Test coverage 80%
-  Zero high/critical security vulnerabilities
-  CI/CD pipeline passing
-  Preventive measures implemented

---

**For Full Details**: See [@comprehensive-bug-analysis.md](./comprehensive-bug-analysis.md)

---

**Related Skills**: security-audit.md, code-review-testing.md, security-remediation.md
**Last Updated**: 2026-01-09
