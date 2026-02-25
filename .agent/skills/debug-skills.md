# Debug Skills - Troubleshooting & Problem Solving

**Topics**: Systematic debugging, common errors, log analysis, troubleshooting
**Version**: 1.0

---

## Skill #1: Systematic Error Analysis

### When to Use
- Any error or bug
- Unexpected behavior
- System not working

### Prompt Template

```markdown
**ROLE**: Debugging specialist

**PROBLEM**: [Describe issue]
**ERROR MESSAGE**: [Paste full error if available]

**SYSTEMATIC DEBUG PROCESS**:

1. **Reproduce**:
   - Can you consistently reproduce it?
   - What are the exact steps?
   - Does it happen always or intermittently?

2. **Isolate**:
   - When did it start working/failing?
   - What changed recently?
   - Does it work in different environment?

3. **Gather Information**:
   - Console logs (browser/server)
   - Network tab (if API related)
   - React DevTools (component state)
   - Database logs

4. **Form Hypothesis**:
   - What could cause this?
   - List 3 most likely causes

5. **Test**:
   - Test each hypothesis
   - Add logging/breakpoints
   - Verify assumptions

6. **Fix**:
   - Implement solution
   - Test fix thoroughly
   - Document what was wrong

**DELIVERABLES**:
- Root cause identification
- Fix implementation
- Prevention strategy
- Documentation
```

### Debug Checklist:
- [ ] Read error message completely
- [ ] Check console for all errors
- [ ] Verify environment variables
- [ ] Test with minimal reproduction
- [ ] Check recent changes (git diff)
- [ ] Search error online
- [ ] Ask for help if stuck >1 hour

---

## Skill #2: File Corruption Recovery

### When to Use
- File has duplicate code
- Syntax errors after editing
- Build fails mysteriously
- File won't parse

### Prompt Template

```markdown
**ROLE**: Code recovery specialist

**CORRUPTED FILE**: [file path]
**SYMPTOMS**:
- [ ] Duplicate code blocks
- [ ] Syntax errors
- [ ] Missing functions
- [ ] Build failures

**RECOVERY PROCESS**:

1. **Check Git**:
```bash
git status
git diff [file]
git checkout [file]  # Restore if corrupted
```

2. **If not in Git**:
- View entire file
- Identify duplicate/broken sections
- Rewrite file completely
- Use write_to_file with overwrite

3. **Verify Fix**:
```bash
# TypeScript/JavaScript
npm run build

# Python
python -m py_compile [file]

# Prisma
npx prisma validate
```

**PREVENTION**:
- Commit often
- Use version control
- Test after each change
- Review AI-generated edits

**DELIVERABLES**:
- Restored/rewritten file
- Verification that it works
- Git commit with fix
```

### Common Corruption Patterns:
- Function defined twice
- Missing closing braces
- Extra semicolons
- Incorrect indentation
- Mixed quote styles

---

##Skill #3: Network Debugging (CORS, SSL, Timeouts)

### When to Use
- API requests failing
- CORS errors
- SSL/TLS issues
- Connection timeouts

### Prompt Template

```markdown
**ROLE**: Network debugging expert

**ISSUE**: [CORS / SSL / Timeout / etc]
**ERROR**: [Paste error from browser console]

**CORS ERRORS**:
```
Access to fetch at 'http://localhost:8000' from origin 
'http://localhost:3000' has been blocked by CORS policy
```

**Fix**: Configure CORS middleware (see backend-skills.md #3)

**SSL/TLS ERRORS**:
```
SSL negotiation failed
channel_binding required
```

**Fix**: Add to DATABASE_URL:
```
?sslmode=require&channel_binding=require
```

**TIMEOUT ERRORS**:
```
TimeoutError: Request took longer than 30s
```

**Fix**:
```typescript
// Increase timeout
fetch('...', { 
  signal: AbortSignal.timeout(60000) // 60s
})

// Or use streaming for long operations
```

**DEBUG TOOLS**:
1. Browser DevTools → Network tab
2. Check request/response headers
3. Verify request payload
4. Check status code
5. Test with curl/Postman

**DELIVERABLES**:
- Root cause identified
- Configuration fix
- Testing commands
```

---

## Skill #4: Build Failure Diagnosis

### When to Use
- npm/docker build fails
- TypeScript errors
- Module not found
- Dependency issues

### Prompt Template

```markdown
**ROLE**: Build troubleshooting specialist

**BUILD TOOL**: [npm / Docker / Prisma / etc]
**ERROR**: [Paste build error]

**COMMON BUILD ERRORS**:

**1. Module Not Found**:
```
Error: Cannot find module '@/lib/utils'
```
**Check**:
- File exists at correct path
- tsconfig paths configuration
- Import statement syntax
- Case sensitivity (Linux)

**2. TypeScript Errors**:
```
Type 'string' is not assignable to type 'number'
```
**Fix**:
- Add proper types
- Use type assertions if needed
- Check interface definitions

**3. Dependency Issues**:
```
npm ERR! peer dependency
```
**Fix**:
```bash
rm -rf node_modules package-lock.json
npm install
```

**4. Docker Build Fails**:
```
COPY failed: file not found
```
**Fix**:
- Check build context
- Verify file paths in Dockerfile
- See docker-skills.md #1

**DELIVERABLES**:
- Identified error type
- Step-by-step fix
- Commands to rebuild
- Prevention tips
```

---

## Skill #5: Runtime Error Tracing

### When to Use
- App crashes at runtime
- Unexpected behavior
- State issues
- Memory leaks

### Prompt Template

```markdown
**ROLE**: Runtime debugging specialist

**ERROR**: [Paste error message]
**WHEN IT HAPPENS**: [User action / Page load / etc]

**DEBUGGING STEPS**:

1. **Check Browser Console**:
- Any red errors?
- Warnings before error?
- Network failures?

2. **Add Logging**:
```typescript
console.log('Before API call', { userId })
const result = await api.getTasks(userId)
console.log('After API call', { result })
```

3. **Use Debugger**:
```typescript
debugger; // Browser will pause here
const data = processData(input)
```

4. **React DevTools**:
- Check component props
- Verify state values
- Look for re-render loops

5. **Network Tab**:
- Check API responses
- Verify status codes
- Check response data

**COMMON RUNTIME ERRORS**:
- `Uncaught TypeError: Cannot read property 'X' of undefined`
  → Check if object exists before accessing
  
- `Maximum update depth exceeded`
  → Infinite re-render loop, check useEffect dependencies
  
- `Failed to fetch`
  → Network error, check backend is running

**DELIVERABLES**:
- Error cause identified
- Fix implemented
- Additional logging added
- Test cases updated
```

---

## Skill #6: Performance Profiling

### When to Use
- Slow page loads
- Laggy interactions
- High memory usage
- Poor user experience

### Prompt Template

```markdown
**ROLE**: Performance optimization specialist

**PROBLEM**: [Slow load / Laggy UI / etc]

**PROFILING PROCESS**:

1. **Measure First**:
```typescript
// Chrome DevTools → Performance tab
// Record while interacting
// Look for long tasks (>50ms)

// Or use performance API
const start = performance.now()
doExpensiveOperation()
const end = performance.now()
console.log(`Took ${end - start}ms`)
```

2. **React Profiler**:
```bash
# React DevTools → Profiler tab
# Start recording → Interact → Stop
# Look for:
# - Components rendering too often
# - Long render times
# - Unnecessary re-renders
```

3. **Network**:
```
# DevTools → Network tab
# Look for:
# - Large bundle sizes
# - Many requests
# - Slow responses
```

**COMMON FIXES**:

**Slow Initial Load**:
- Code split with dynamic imports
- Optimize images (use Next.js Image)
- Reduce bundle size
- Enable compression

**Slow Interactions**:
- Use React.memo
- Optimize useCallback/useMemo
- Virtual scrolling for long lists
- Debounce expensive operations

**Memory Leaks**:
- Clean up event listeners
- Cancel pending requests
- Clear intervals/timeouts
- Unsubscribe from observables

**DELIVERABLES**:
- Performance metrics (before/after)
- Bottlenecks identified
- Optimizations implemented
- User-perceivable improvement
```

---

## Quick Reference

### Essential Debug Commands

```bash
# Check logs
docker-compose logs -f frontend
docker-compose logs -f backend

# Check container status
docker-compose ps

# Restart service
docker-compose restart frontend

# Rebuild
docker-compose build --no-cache

# Check environment
docker-compose config

# Exec into container
docker-compose exec frontend sh
```

### Browser DevTools Shortcuts

| Tool | Chrome/Edge | Firefox |
|------|-------------|---------|
| Console | Cmd+Option+J / F12 | Cmd+Option+K |
| Network | Cmd+Option+I → Network | Cmd+Option+E |
| Elements | Cmd+Option+C | Cmd+Option+C |
| Debugger | Cmd+Option+I → Sources | Cmd+Option+S |

---

## Common Error Patterns

### Frontend Errors
| Error | Likely Cause | Quick Fix |
|-------|--------------|-----------|
| "Cannot read property" | Undefined object | Add null check |
| "Hydration failed" | Server/client mismatch | Move to client component |
| "Module not found" | Wrong import path | Check file location |
| "Maximum update depth" | Infinite loop | Check useEffect deps |

### Backend Errors
| Error | Likely Cause | Quick Fix |
|-------|--------------|-----------|
| "CORS policy" | CORS not configured | Add CORSMiddleware |
| "Connection refused" | Service not running | Start service |
| "422 Unprocessable" | Validation failed | Check request body |
| "500 Internal" | Server error | Check logs |

### Database Errors
| Error | Likely Cause | Quick Fix |
|-------|--------------|-----------|
| "Client not generated" | Prisma not generated | Run `npx prisma generate` |
| "SSL negotiation" | Missing SSL params | Add `sslmode=require` |
| "Connection timeout" | DB not accessible | Check connection string |
| "Migration failed" | SQL error | Review migration SQL |

---

## Debugging Mindset

### DO:
✅ Read error messages completely
✅ Reproduce consistently
✅ Test one change at a time
✅ Add logging strategically
✅ Take breaks if stuck
✅ Ask for help with context

### DON'T:
❌ Change multiple things at once
❌ Ignore warnings
❌ Skip reading documentation
❌ Debug without understanding
❌ Give up after 10 minutes
❌ Delete code randomly

---

## Lessons Learned

1. **Error messages are helpful** - Read them fully
2. **Console is your friend** - Check it always
3. **Git helps recovery** - Commit often
4. **Break it down** - Isolate the problem
5. **Document solutions** - Help future you
6. **Test fixes** - Verify they work
7. **Learn patterns** - Similar errors recur
8. **Stay systematic** - Don't guess randomly

---

## When to Ask for Help

Ask after you've:
1. Read the error message
2. Checked console/logs
3. Googled the error
4. Tried obvious fixes
5. Spent 30-60 minutes

Provide when asking:
- Full error message
- Code that's failing
- What you've tried
- Environment details
- Steps to reproduce

---

## Related Skills
- All other skill files
- Docker Skills: Container debugging
- Database Skills: Connection issues
- Frontend Skills: React debugging  
- Backend Skills: API troubleshooting

**Good debugging is a superpower - practice it!**
