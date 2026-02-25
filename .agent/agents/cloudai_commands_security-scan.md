---
description: Security-focused code scan. Checks for hardcoded secrets, vulnerable dependencies, and common security issues.
---

# Security Scan

Security-focused code scanning. Run before commits and PRs to catch vulnerabilities.

## Phase 1: Secret Detection

Scan for hardcoded credentials:

```bash
# Common secret patterns
grep -rn "password\s*[=:]\s*['\"]" --include="*.{js,ts,py,go,java,rb}" . 2>/dev/null | grep -v node_modules | grep -v ".git"
grep -rn "api[_-]?key\s*[=:]\s*['\"]" --include="*.{js,ts,py,go,java,rb}" . 2>/dev/null | grep -v node_modules
grep -rn "secret\s*[=:]\s*['\"]" --include="*.{js,ts,py,go,java,rb}" . 2>/dev/null | grep -v node_modules
grep -rn "token\s*[=:]\s*['\"]" --include="*.{js,ts,py,go,java,rb}" . 2>/dev/null | grep -v node_modules

# AWS keys
grep -rn "AKIA[0-9A-Z]{16}" . 2>/dev/null | grep -v node_modules

# Private keys
find . -name "*.pem" -o -name "*.key" -o -name "id_rsa" 2>/dev/null | grep -v node_modules
```

## Phase 2: Dependency Audit

Check for vulnerable dependencies:

### Node.js
```bash
npm audit --json 2>/dev/null | head -100
# or
yarn audit --json 2>/dev/null | head -100
```

### Python
```bash
pip-audit 2>/dev/null || safety check 2>/dev/null
```

### Go
```bash
govulncheck ./... 2>/dev/null
```

### Rust
```bash
cargo audit 2>/dev/null
```

## Phase 3: Code Pattern Analysis

Check for dangerous patterns:

### SQL Injection
- String concatenation in SQL queries
- Unparameterized queries
- Dynamic table/column names from user input

### Command Injection
- Shell execution with user input (`exec`, `system`, `subprocess`)
- Unsanitized path construction

### XSS Vulnerabilities
- `innerHTML` with user data
- `dangerouslySetInnerHTML` without sanitization
- Unescaped template variables

### Path Traversal
- User input in file paths without sanitization
- Missing `..` checks

## Phase 4: Configuration Check

Verify security settings:
- [ ] Debug mode disabled in production configs
- [ ] HTTPS enforced (no HTTP URLs in prod)
- [ ] CORS properly configured
- [ ] Security headers present (CSP, X-Frame-Options, etc.)
- [ ] No default/weak passwords in configs

## Output Format

```
## Security Scan: [PASS/FAIL/WARNINGS]

### Secrets Detected: [count]
1. **CRITICAL** - `file:line`
   - Type: [API key/password/token/private key]
   - Action: Remove immediately and rotate credential

### Vulnerable Dependencies: [count]
1. **[package@version]** - Severity: [Critical/High/Medium/Low]
   - CVE: [CVE number if available]
   - Fixed in: [version]
   - Action: Update to [version]

### Code Vulnerabilities: [count]
1. **[Vulnerability Type]** - `file:line`
   - Risk: [description]
   - Fix: [remediation steps]

### Configuration Issues: [count]
1. **[Issue]**
   - Current: [state]
   - Recommended: [secure state]

### Recommendations
1. [Prioritized action items]
```

## NEVER Commit If

- Secrets detected in code (rotate and remove)
- Critical CVEs in dependencies (update first)
- Obvious injection vulnerabilities (fix first)

## Usage

Copy to your project:
```bash
cp templates/subagents/security-scan.md .claude/commands/
```

Invoke with: `/project:security-scan`
