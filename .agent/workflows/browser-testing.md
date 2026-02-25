# Browser Testing Best Practices Workflow

## Critical Rules for Form Testing

### ⚠️ IMPORTANT: Always Clear Fields Before Typing

When testing forms (login, signup, any input fields), the browser agent MUST:

1. **ALWAYS use `ClearText: true`** when typing into input fields that may already contain text
2. **Clear the field BEFORE typing** to avoid text concatenation
3. **Never assume fields are empty** - even on first load, autofill may have populated them

### Example - Correct Login Testing

```
1. Navigate to login page
2. Type email with ClearText=true: browser_input(Index=1, Text="user@example.com", ClearText=true)
3. Type password with ClearText=true: browser_input(Index=2, Text="password123", ClearText=true)
4. Click submit button
```

### Common Mistakes to Avoid

❌ **WRONG** - Text gets appended:
```
browser_input(Index=1, Text="newuser@test.com")  // Will append to existing text!
```

✅ **CORRECT** - Text replaces existing:
```
browser_input(Index=1, Text="newuser@test.com", ClearText=true)
```

### When Retrying with Different Credentials

If login fails and you need to try different credentials:
1. Clear BOTH email and password fields before retyping
2. Use `ClearText: true` for every input attempt
3. Don't assume failed submission cleared the fields

### Form Testing Checklist

- [ ] Use `ClearText: true` for all input fields
- [ ] Wait for page to fully load before interacting
- [ ] Take screenshots after each major action
- [ ] Check for error messages after form submission
- [ ] Clear fields between multiple attempts
