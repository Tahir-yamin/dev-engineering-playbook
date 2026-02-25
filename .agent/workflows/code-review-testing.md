---
description: Comprehensive code review and testing checklist before deployment
---

# Code Review & Testing Workflow

## When to Use
- Before deploying
- Pull request review
- QA testing
- Pre-production verification

---

## Step 1: Code Review Checklist

### Code Quality
- [ ] No console.logs in production code
- [ ] Error handling present
- [ ] Types defined (TypeScript)
- [ ] Comments for complex logic
- [ ] No hardcoded values
- [ ] Environment variables used

### Security
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Authentication on protected routes

### Performance
- [ ] No N+1 queries
- [ ] Database indexes
- [ ] Images optimized
- [ ] Code split (if needed)
- [ ] Memoization (if needed)

---

## Step 2: Manual Testing

### Happy Path
- [ ] Feature works as expected
- [ ] UI looks correct
- [ ] Data persists
- [ ] Navigation works

### Edge Cases
- [ ] Empty states
- [ ] Error states
- [ ] Network failures
- [ ] Invalid inputs
- [ ] Concurrent operations

### Cross-Browser
- [ ] Chrome
- [ ] Firefox
- [ ] Safari (if Mac)
- [ ] Edge

---

## Step 3: Automated Testing (if implemented)

```bash
# Unit tests
npm test

# E2E tests
npm run test:e2e

# Coverage
npm run test:coverage
```

---

## Step 4: Performance Testing

Use @.claude/debug-skills.md Skill #6

1. Chrome DevTools → Performance
2. Record interaction
3. Check for:
   - Long tasks
   - Memory leaks
   - Bundle size

---

## Step 5: Security Testing

Check:
- Authentication works
- Authorization enforced
- Secrets not exposed
- CORS configured
- Rate limiting (if implemented)

---

## Step 6: Document Findings

Create list of:
- Issues found
- Suggestions
- Blockers
- Nice-to-haves

---

**Reference**: @.claude/debug-skills.md for systematic testing
