# Sample Output: Code Reviewer Report

> This is a condensed sample from the code-reviewer agent.

---

## Code Reviewer Agent Activated

Analyzing 8 files in `src/auth/` for code quality...

### Summary

| Severity | Count |
|----------|-------|
| Critical | 2 |
| Warning | 5 |
| Info | 8 |

### Critical Issues

#### 1. Synchronous Password Hashing

**File:** `src/auth/password.js:34`

```javascript
// BAD: Blocks event loop
const hash = bcrypt.hashSync(password, 10);
```

**Impact:** Blocks the event loop during password hashing, causing latency spikes.

**Fix:**
```javascript
// GOOD: Async version
const hash = await bcrypt.hash(password, 10);
```

#### 2. Missing Error Handling

**File:** `src/auth/login.js:67`

```javascript
// BAD: Unhandled promise rejection
const user = await db.users.findOne({ email });
return generateToken(user.id);  // Crashes if user is null
```

**Fix:**
```javascript
const user = await db.users.findOne({ email });
if (!user) {
  throw new AuthError('Invalid credentials');
}
return generateToken(user.id);
```

### Warnings

1. **Inconsistent error messages** - `src/auth/login.js:45, 78, 92`
   - Some errors expose internal details, others are generic
   - Standardize to generic messages for security

2. **Magic numbers** - `src/auth/jwt.js:12`
   - Token expiry `86400` should be a named constant
   - `const TOKEN_EXPIRY_SECONDS = 86400; // 24 hours`

3. **Callback style in async code** - `src/auth/middleware.js:23`
   - Mixing callbacks with async/await
   - Convert to consistent async/await

4. **No input validation** - `src/auth/register.js:15`
   - Email format not validated before database query
   - Add validation layer

5. **Console.log in production** - `src/auth/jwt.js:78`
   - Debug logging left in code
   - Remove or use proper logger

### Positive Observations

- Good separation of concerns between modules
- Consistent file naming convention
- Proper use of environment variables for secrets
- Well-structured middleware pattern

### Recommendations

1. Add centralized error handling middleware
2. Create constants file for magic numbers
3. Add input validation layer (consider Joi or Zod)
4. Set up ESLint with stricter rules

---

*Code review complete. Returning to orchestrator.*
