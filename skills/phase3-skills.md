# Phase 3 Skills - Advanced Features

**Phase**: 3 - Advanced Implementation  
**Topics**: Better Auth, OAuth, AI integration, real-time features, advanced UI
**Version**: 1.0

---

## Skill #1: Better Auth Integration

### When to Use
- Setting up authentication system
- Implementing email/password auth
- Configuring OAuth providers

### Prompt Template

```markdown
**ROLE**: Authentication security specialist

**AUTH LIBRARY**: Better Auth
**DATABASE**: [PostgreSQL / MySQL]
**DEPLOYMENT**: [Docker / Vercel / etc]

**REQUIREMENTS**:
- Email/password authentication
- OAuth providers: [GitHub / Google / etc]
- Session management
- Password reset functionality

**CURRENT ISSUE** (if any):
[CSRF token mismatch / Session not persisting / etc]

**SETUP REQUIRED**:
1. Better Auth configuration:
   ```typescript
   // lib/auth.ts
   export const auth = betterAuth({
     database: ...,
     emailAndPassword: {...},
     socialProviders: {...}
   })
   ```

2. Environment variables:
   - BETTER_AUTH_SECRET (32+ chars)
   - BETTER_AUTH_URL
   - DATABASE_URL
   - OAuth client IDs/secrets

3. API routes:
   - /api/auth/[...all]

**DELIVERABLES**:
- Complete auth configuration
- Environment variables list
- Login/signup components
- Protected route middleware
- Session hooks
```

---

## Skill #2: OAuth Provider Setup (GitHub/Google)

### When to Use
- Adding social login
- Configuring OAuth apps
- Debugging OAuth flows

### Prompt Template

```markdown
**ROLE**: OAuth integration specialist

**PROVIDER**: [GitHub / Google / Microsoft]
**APPLICATION TYPE**: [Web app / SaaS]

**SETUP STEPS NEEDED**:
1. Create OAuth app in provider dashboard:
   - Application name
   - Homepage URL
   - Callback URL

2. Configure Better Auth:
   ```typescript
   socialProviders: {
     github: {
       clientId: process.env.GITHUB_CLIENT_ID!,
       clientSecret: process.env.GITHUB_CLIENT_SECRET!
     }
   }
   ```

3. Handle OAuth errors:
   - Mismatched redirect URI
   - Invalid client ID
   - Scope issues

**COMMON ISSUES**:
- Callback URL mismatch
- HTTPS required in production
- Email not returned (scope issue)

**DELIVERABLES**:
- OAuth app configuration guide
- Better Auth setup code
- Error handling
- Testing checklist
```

---

## Skill #3: AI Chat Integration (OpenAI/OpenRouter)

### When to Use
- Adding AI-powered chat
- Implementing task suggestions
- Integrating LLM APIs

### Prompt Template

```markdown
**ROLE**: AI integration engineer

**AI PROVIDER**: [OpenAI / OpenRouter / Anthropic]
**MODEL**: [GPT-4 / DeepSeek / Claude]
**USE CASE**: [Chat assistant / Task suggestions / etc]

**IMPLEMENTATION REQUIRED**:
1. Backend endpoint:
   ```python
   @router.post("/chat")
   async def chat(message: str):
       # Call AI API
       # Return response
   ```

2. Frontend component:
   - Chat widget
   - Message history
   - Streaming responses (optional)
   - Loading states

3. Features:
   - Context awareness (pass task data)
   - Rate limiting
   - Error handling
   - Cost optimization

**DELIVERABLES**:
- AI API integration code
- Chat UI component
- Prompt engineering examples
- Error handling
- Cost estimates
```

---

## Skill #4: Real-Time Features (WebSockets)

### When to Use
- Live task updates
- Collaborative features
- Notifications

### Prompt Template

```markdown
**ROLE**: Real-time systems engineer

**TECHNOLOGY**: [WebSockets / Server-Sent Events / Polling]
**FRAMEWORK**: 
- Backend: [FastAPI WebSockets / Socket.io]
- Frontend: [Native WebSocket / Socket.io client]

**USE CASE**: [Live task updates / Notifications / etc]

**IMPLEMENT**:
1. Backend WebSocket endpoint
2. Connection management
3. Message broadcasting
4. Authentication over WebSocket
5. Reconnection logic

**DELIVERABLES**:
- WebSocket server setup
- Client connection code
- Message protocol
- Error handling
- Testing guide
```

---

## Skill #5: File Upload & Storage

### When to Use
- Uploading task attachments
- Profile pictures
- Document management

### Prompt Template

```markdown
**ROLE**: File handling specialist

**STORAGE**: [Local / S3 / Cloudinary / Supabase Storage]
**FILE TYPES**: [Images / PDFs / Any]
**MAX SIZE**: [e.g., 10MB]

**REQUIREMENTS**:
1. Upload endpoint:
   - Validation (type, size)
   - Secure filename generation
   - Storage path

2. Frontend:
   - File input component
   - Preview (for images)
   - Progress indicator
   - Drag & drop

3. Security:
   - Validate file types
   - Scan for malware (production)
   - Access control

**DELIVERABLES**:
- Upload API endpoint
- Frontend upload component
- File validation
- Storage configuration
- URL generation for downloads
```

---

## Skill #6: Email Integration (Resend/SendGrid)

### When to Use
- Sending verification emails
- Password reset emails
- Notifications

### Prompt Template

```markdown
**ROLE**: Email integration specialist

**EMAIL SERVICE**: [Resend / SendGrid / Mailgun]
**EMAIL TYPES NEEDED**:
- Verification emails
- Password reset
- [Other types]

**SETUP**:
1. Email service configuration:
   - API key
   - Sender domain
   - Templates

2. Better Auth email config:
   ```typescript
   emailAndPassword: {
     sendResetPassword: async ({ user, url }) => {
       // Send email
     }
   }
   ```

3. Email templates:
   - HTML design
   - Plain text fallback
   - Dynamic content

**DELIVERABLES**:
- Email service setup
- Template designs
- Sending functions
- Error handling
- Testing approach
```

---

## Skill #7: Advanced UI Patterns

### When to Use
- Implementing modals
- Toast notifications
- Drag & drop
- Complex interactions

### Prompt Template

```markdown
**ROLE**: UI/UX engineer

**PATTERN NEEDED**: [Modal / Toast / Drag-drop / etc]
**LIBRARY**: [Headless UI / Radix / Custom]

**REQUIREMENTS**:
[Describe specific requirements]

**IMPLEMENT**:
1. Component structure
2. Accessibility (ARIA labels, keyboard nav)
3. Animations
4. State management
5. Mobile responsiveness

**DELIVERABLES**:
- Component implementation
- Accessibility testing
- Animation configuration
- Usage examples
- Mobile considerations
```

---

## Skill #8: Performance Optimization

### When to Use
- Slow page loads
- Laggy interactions
- High memory usage

### Prompt Template

```markdown
**ROLE**: Performance optimization specialist

**CURRENT PROBLEM**:
[Describe performance issue]

**METRICS**:
- Page load time: [X seconds]
- Time to Interactive: [X seconds]
- Bundle size: [X KB]

**ANALYZE**:
1. Next.js bundle analysis
2. Component re-renders
3. API call optimization
4. Image optimization
5. Code splitting opportunities

**OPTIMIZE**:
- Use React.memo strategically
- Implement virtualization for long lists
- Lazy load components
- Optimize images
- Cache API responses

**DELIVERABLES**:
- Performance audit
- Optimization recommendations
- Implementation plan
- Before/after metrics
```

---

## Skill #9: Dark Mode Implementation

### When to Use
- Adding theme switching
- Supporting system preference
- Maintaining theme state

### Prompt Template

```markdown
**ROLE**: Theme implementation specialist

**FRAMEWORK**: Next.js + TailwindCSS
**REQUIREMENTS**:
- Light/dark modes
- System preference detection
- Persistent user choice

**IMPLEMENT**:
1. Tailwind dark mode configuration:
   ```js
   // tailwind.config.js
   module.exports = {
     darkMode: 'class',
     // or 'media' for system preference
   }
   ```

2. Theme provider:
   - Context for theme state
   - Toggle function
   - localStorage persistence

3. Component styling:
   - dark: classes in Tailwind
   - CSS variables approach
   - Consistent color scheme

**DELIVERABLES**:
- Theme provider setup
- Toggle component
- Dark mode styles
- System preference detection
```

---

## Skill #10: Testing Strategy

### When to Use
- Setting up testing infrastructure
- Writing component tests
- API endpoint testing

### Prompt Template

```markdown
**ROLE**: QA and testing specialist

**TESTING STACK**:
- Unit: [Jest / Vitest]
- Integration: [Testing Library / Playwright]
- E2E: [Cypress / Playwright]

**WHAT TO TEST**:
- Critical user flows: [Login, Create task, etc]
- Edge cases: [Empty states, errors]
- Accessibility

**SETUP REQUIRED**:
1. Test environment configuration
2. Mock data and factories
3. API mocking strategy
4. CI/CD integration

**DELIVERABLES**:
- Test setup configuration
- Example test suites
- CI pipeline configuration
- Coverage goals
```

---

## Phase 3 Lessons Learned

### Better Auth
1. **BETTER_AUTH_SECRET must be 32+ characters** - Common issue
2. **BETTER_AUTH_URL must match access URL** - Including protocol
3. **TRUSTED_ORIGINS critical** - Prevents CORS/CSRF issues
4. **Database SSL required** - Especially for NeonDB
5. **Session cookies need proper settings** - httpOnly, secure, sameSite

### AI Integration
1. **Stream responses for better UX** - Don't wait for full completion
2. **Context matters** - Include relevant task data in prompts
3. **Handle rate limits** - OpenAI/OpenRouter have limits
4. **Cost monitoring** - Track API usage
5. **Fallback for failures** - AI APIs can be unreliable

### OAuth
1. **Callback URL must match exactly** - Including trailing slash
2. **Test with real providers early** - Localhost limitations
3. **Handle missing email** - Some providers don't always send it
4. **Scope carefully** - Request only needed permissions
5. **HTTPS required in production** - OAuth providers enforce this

### Performance
1. **Measure before optimizing** - Use Chrome DevTools
2. **Images are often the culprit** - Use Next.js Image
3. **Code splitting helps** - Dynamic imports for large components
4. **API response caching** - React Query / SWR
5. **Virtual scrolling for lists** - 100+ items

---

## Common Phase 3 Issues

### "CSRF token mismatch" (Better Auth)
- Check BETTER_AUTH_URL matches
- Verify TRUSTED_ORIGINS includes frontend URL
- Ensure cookies are being sent

### OAuth redirect fails
- Verify callback URL in provider dashboard
- Check for typos in client ID/secret
- Ensure HTTPS in production

### AI responses timeout
- Implement streaming
- Set appropriate timeout values
- Handle partial responses

### Dark mode flashing
- Use next-themes for proper SSR
- Set initial theme in HTML
- Prevent hydration mismatch

---

## Related Skills

- **Auth Skills**: Deep dive into Better Auth
- **AI Skills**: Advanced AI integration patterns
- **Frontend Skills**: Advanced React patterns
- **Database Skills**: Session storage optimization

---

**Phase 3 adds polish and advanced features. Take time to get auth and security right!**
