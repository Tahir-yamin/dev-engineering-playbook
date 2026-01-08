# Sample Output: Test Architect Report

> This is a condensed sample from the test-architect agent.

---

## Test Architect Agent Activated

Analyzing test coverage for `src/auth/`...

### Coverage Summary

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Line Coverage | 45% | 80% | Below target |
| Branch Coverage | 32% | 70% | Below target |
| Function Coverage | 60% | 90% | Below target |

### Untested Code Paths

#### Critical (must test)

1. **Login failure scenarios** - `src/auth/login.js:60-85`
   - Invalid password handling
   - Account locked state
   - Rate limit exceeded

2. **Token validation edge cases** - `src/auth/jwt.js:45-78`
   - Expired token
   - Malformed token
   - Invalid signature

3. **Password reset flow** - `src/auth/password.js:90-145`
   - Entire flow untested
   - Token generation
   - Token validation
   - Password update

#### Important (should test)

4. **Registration validation** - `src/auth/register.js:20-45`
   - Email format validation
   - Password strength check
   - Duplicate user handling

5. **Middleware chain** - `src/auth/middleware.js:15-60`
   - Missing token
   - Invalid token format
   - Blacklisted token

### Recommended Test Cases

#### Unit Tests

```javascript
// src/auth/__tests__/login.test.js

describe('Login', () => {
  describe('successful login', () => {
    it('returns JWT token for valid credentials');
    it('sets correct token expiry');
    it('includes user ID in token payload');
  });

  describe('failed login', () => {
    it('returns 401 for invalid password');
    it('returns 401 for non-existent user');
    it('returns 429 after rate limit exceeded');
    it('does not reveal user existence in error');
  });

  describe('edge cases', () => {
    it('handles SQL injection attempts');
    it('handles extremely long passwords');
    it('handles unicode in email');
  });
});
```

#### Integration Tests

```javascript
// src/auth/__tests__/auth.integration.test.js

describe('Auth Flow', () => {
  it('registers, logs in, accesses protected route, logs out');
  it('cannot access protected route after logout');
  it('cannot reuse expired token');
  it('password reset invalidates old tokens');
});
```

### Test Infrastructure Recommendations

1. **Add test database**
   - Use in-memory SQLite for unit tests
   - Docker PostgreSQL for integration tests

2. **Mock external services**
   - Email service for password reset
   - Rate limiter for testing limits

3. **Add fixtures**
   ```javascript
   // test/fixtures/users.js
   export const validUser = {
     email: 'test@example.com',
     password: 'SecureP@ss123',
     // ...
   };
   ```

4. **CI integration**
   - Run tests on PR
   - Block merge if coverage drops
   - Generate coverage reports

### Priority Order

| Priority | Test | Effort | Impact |
|----------|------|--------|--------|
| 1 | Login failure scenarios | Medium | High |
| 2 | Token validation | Medium | High |
| 3 | Password reset flow | High | High |
| 4 | Registration validation | Low | Medium |
| 5 | Middleware chain | Medium | Medium |

### Estimated Effort

- **Unit tests:** 4-6 hours
- **Integration tests:** 3-4 hours
- **Infrastructure setup:** 2-3 hours
- **Total:** ~12 hours to reach 80% coverage

---

*Test analysis complete. Returning to orchestrator.*
