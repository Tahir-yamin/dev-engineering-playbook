# Sample Output: Security Auditor Report

> This is a condensed sample from the security-auditor agent.

---

## Security Auditor Agent Activated

Running OWASP Top 10 security scan on `src/auth/`...

### Vulnerability Summary

| Severity | Count | Status |
|----------|-------|--------|
| High | 1 | Must fix |
| Medium | 2 | Should fix |
| Low | 3 | Consider |

### High Severity

#### A03:2021 - Injection

**File:** `src/auth/login.js:52`

```javascript
// VULNERABLE: SQL Injection
const query = `SELECT * FROM users WHERE email = '${email}'`;
const user = await db.raw(query);
```

**Attack Vector:**
```
email: "admin'--"
```

**Impact:** Full database access, data exfiltration, privilege escalation.

**Remediation:**
```javascript
// SECURE: Parameterized query
const user = await db('users').where({ email }).first();
```

**CVSS Score:** 9.8 (Critical)

### Medium Severity

#### A02:2021 - Cryptographic Failures

**File:** `src/auth/jwt.js:8`

```javascript
// WEAK: Hardcoded secret
const JWT_SECRET = 'my-super-secret-key';
```

**Impact:** If secret is compromised, all tokens can be forged.

**Remediation:**
```javascript
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) {
  throw new Error('JWT_SECRET must be set');
}
```

#### A07:2021 - Identification and Authentication Failures

**File:** `src/auth/login.js:89`

```javascript
// WEAK: No rate limiting
app.post('/login', async (req, res) => {
  // No protection against brute force
});
```

**Impact:** Brute force attacks on user accounts.

**Remediation:**
```javascript
const rateLimit = require('express-rate-limit');
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts'
});
app.post('/login', loginLimiter, async (req, res) => { ... });
```

### Low Severity

1. **Verbose error messages** - `src/auth/login.js:95`
   - "User not found" vs "Invalid credentials" reveals user existence

2. **Missing security headers** - `src/auth/middleware.js`
   - No helmet middleware for security headers

3. **Session not invalidated** - `src/auth/logout.js:12`
   - Logout doesn't invalidate server-side session

### OWASP Top 10 Coverage

| Category | Status |
|----------|--------|
| A01 Broken Access Control | Not reviewed (out of scope) |
| A02 Cryptographic Failures | 1 finding |
| A03 Injection | 1 finding (critical) |
| A04 Insecure Design | Pass |
| A05 Security Misconfiguration | Pass |
| A06 Vulnerable Components | Not checked |
| A07 Auth Failures | 1 finding |
| A08 Data Integrity | Pass |
| A09 Logging Failures | Pass |
| A10 SSRF | Not applicable |

### Recommended Actions

**Immediate (before merge):**
1. Fix SQL injection vulnerability
2. Move JWT secret to environment variable

**Short-term (this sprint):**
3. Implement rate limiting on auth endpoints
4. Add helmet for security headers

**Long-term:**
5. Security audit of all database queries
6. Implement proper session management
7. Add dependency vulnerability scanning

---

*Security audit complete. Returning to orchestrator.*
