# Authentication Skills - Better Auth & OAuth

**Topics**: Better Auth, OAuth, sessions, CSRF, password reset
**Version**: 1.0

---

## Skill #1: Better Auth Complete Setup

### When to Use
- Setting up authentication from scratch
- Migrating from another auth system
- Debugging authentication issues

### Prompt Template

```markdown
**ROLE**: Authentication security specialist

**SETUP**: Better Auth with [Email/Password + OAuth]
**DATABASE**: [PostgreSQL via Prisma]
**DEPLOYMENT**: [Docker / Vercel / Railway]

**CRITICAL ENVIRONMENT VARIABLES**:
```env
BETTER_AUTH_SECRET="min-32-chars-generate-with-openssl-rand"
BETTER_AUTH_URL="http://localhost:3000"  # Must match access URL!
TRUSTED_ORIGINS="http://localhost:3000"
DATABASE_URL="postgresql://...?sslmode=require&channel_binding=require"
```

**CONFIGURATION**:
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth"
import { prismaAdapter } from "better-auth/adapters/prisma"
import { prisma } from "@/lib/prisma"

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql"
  }),
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set true for production
  },
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }
  },
  trustedOrigins: process.env.TRUSTED_ORIGINS?.split(',') || [],
})
```

**DELIVERABLES**:
1. Complete auth.ts configuration
2. API route: app/api/auth/[...all]/route.ts
3. Client setup with useSession
4. Login/signup components
5. Protected route middleware
```

### Lessons Learned:
- ✅ BETTER_AUTH_SECRET **must** be 32+ characters
- ✅ BETTER_AUTH_URL must match exactly (protocol + domain + port)
- ✅ TRUSTED_ORIGINS prevents CSRF attacks
- ✅ DATABASE_URL needs SSL for NeonDB (`sslmode=require&channel_binding=require`)
- ❌ Common mistake: BETTER_AUTH_URL mismatch causes silent failures

---

## Skill #2: OAuth Flow Debugging

### When to Use
- OAuth redirect fails
- "Invalid client" errors
- Callback URL mismatch
- Missing user data

### Prompt Template

```markdown
**ROLE**: OAuth troubleshooting expert

**PROVIDER**: [GitHub / Google / Microsoft]
**ERROR**: [Paste error message]

**DEBUG CHECKLIST**:

1. **Provider Dashboard**:
   - Application name: [name]
   - Homepage URL: http://localhost:3000 (dev) or https://yourdomain.com (prod)
   - Callback URL: http://localhost:3000/api/auth/callback/github
   - ⚠️ **EXACT MATCH required** - including trailing slash!

2. **Environment Variables**:
   ```env
   GITHUB_CLIENT_ID="Ov23liL..." 
   GITHUB_CLIENT_SECRET="45b1a25..."
   BETTER_AUTH_URL="http://localhost:3000"  # No trailing slash
   ```

3. **Common Issues**:
   - Callback URL mismatch (check for http vs https)
   - Client ID/secret typo
   - Missing scopes (add "user:email" for GitHub)
   - HTTPS required in production

**TEST FLOW**:
1. Click "Sign in with GitHub"
2. Redirects to GitHub authorization
3. User authorizes
4. Redirects to callback URL
5. Creates/updates user in database
6. Sets session cookie

**DELIVERABLES**:
- Corrected OAuth configuration
- Updated provider settings
- Test checklist
```

### Common OAuth Errors:

| Error | Cause | Fix |
|-------|-------|-----|
| "redirect_uri_mismatch" | Callback URL doesn't match | Update provider dashboard |
| "invalid_client" | Wrong client ID/secret | Check environment variables |
| "access_denied" | User cancelled | Normal - handle gracefully |
| "Email not returned" | Missing scope | Add "user:email" scope |

---

## Skill #3: Session Management

### When to Use
- Users getting logged out
- Sessions not persisting
- "Session not found" errors

### Prompt Template

```markdown
**ROLE**: Session management specialist

**PROBLEM**: [Sessions not persisting / Users logged out / etc]

**SESSION CONFIGURATION**:
```typescript
// In betterAuth config
session: {
  expiresIn: 60 * 60 * 24 * 7, // 7 days
  updateAge: 60 * 60 * 24,      // Update every day
  cookieCache: {
    enabled: true,
    maxAge: 60 * 5 // 5 minutes
  }
}
```

**COOKIE SETTINGS**:
```typescript
advanced: {
  cookieOptions: {
    httpOnly: true,      // Prevent JS access (security)
    secure: process.env.NODE_ENV === 'production', // HTTPS only in prod
    sameSite: 'lax',     // CSRF protection
    path: '/',           // Available everywhere
  }
}
```

**CLIENT USAGE**:
```typescript
'use client'
import { useSession } from "@/lib/auth-client"

export function ProtectedComponent() {
  const { data: session, isPending } = useSession()
  
  if (isPending) return <Loading />
  if (!session) return <LoginPrompt />
  
  return <div>Hello {session.user.email}</div>
}
```

**DELIVERABLES**:
- Session configuration
- Cookie settings explanation
- Client-side session hooks
- Server-side session validation
```

### Session Debugging:
1. Check browser DevTools → Application → Cookies
2. Look for `better-auth.session_token` cookie
3. Verify `httpOnly`, `secure`, `sameSite` flags
4. Check expiration date

---

## Skill #4: Password Reset Flow

### When to Use
- Implementing forgot password
- Email verification
- Account recovery

### Prompt Template

```markdown
**ROLE**: Authentication flow specialist

**FEATURE**: Password reset via email

**EMAIL SERVICE**: [Resend / SendGrid / Mailgun]

**IMPLEMENTATION**:

1. **Request Reset**:
```typescript
// Client-side
const { sendResetPassword } = useAuth()
await sendResetPassword({ email: "user@example.com" })
```

2. **Email Configuration**:
```typescript
// In betterAuth config
emailAndPassword: {
  sendResetPassword: async ({ user, url }) => {
    await sendEmail({
      to: user.email,
      subject: "Reset your password",
      html: `Click here to reset: <a href="${url}">${url}</a>`
    })
  }
}
```

3. **Reset Page**:
```typescript
// app/reset-password/page.tsx
const { resetPassword } = useAuth()
await resetPassword({
  newPassword: password,
  token: searchParams.get('token')!
})
```

**DELIVERABLES**:
- Reset request handler
- Email template
- Reset page component
- Token validation
- Security considerations
```

### Security Best Practices:
- Tokens expire after 1 hour
- One-time use tokens
- Rate limit reset requests
- Don't reveal if email exists
- Use HTTPS for reset links

---

## Quick Reference

### Environment Variables Checklist
```bash
# Required (minimum)
BETTER_AUTH_SECRET="32+-characters-here"
BETTER_AUTH_URL="http://localhost:3000"
DATABASE_URL="postgresql://..."
TRUSTED_ORIGINS="http://localhost:3000"

# OAuth (if using)
GITHUB_CLIENT_ID="..."
GITHUB_CLIENT_SECRET="..."
GOOGLE_CLIENT_ID="..."
GOOGLE_CLIENT_SECRET="..."

# Email (if using)
RESEND_API_KEY="..."
EMAIL_FROM="noreply@yourdomain.com"
```

### Generate BETTER_AUTH_SECRET
```bash
# Mac/Linux
openssl rand -base64 32

# Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

### Common Auth Errors

| Error | Solution |
|-------|----------|
| "CSRF token mismatch" | Check BETTER_AUTH_URL and TRUSTED_ORIGINS |
| "Session not found" | Verify cookie settings and DATABASE_URL |
| "Invalid credentials" | User doesn't exist or wrong password |
| "OAuth redirect failed" | Check callback URL in provider |

---

## Testing Checklist

### Email/Password Auth
- [ ] Sign up creates user in database
- [ ] Password is hashed (not plain text)
- [ ] Login works with correct credentials
- [ ] Login fails with wrong password
- [ ] Session persists across page reloads
- [ ] Logout clears session
- [ ] Protected routes redirect to login

### OAuth Auth
- [ ] OAuth button redirects to provider
- [ ] Successful auth creates/updates user
- [ ] Email is captured correctly
- [ ] Session is created
- [ ] User can log out
- [ ] Works with existing email/password users

### Security
- [ ] Passwords are hashed
- [ ] Cookies have httpOnly flag
- [ ] HTTPS in production
- [ ] CSRF protection enabled
- [ ] Rate limiting on auth endpoints

---

## Lessons from This Project

1. **Better Auth URL Matching is Critical**
   - Set BETTER_AUTH_URL to exact access URL
   - Include protocol (http/https)
   - No trailing slash
   - Must match what browser shows

2. **TRUSTED_ORIGINS Prevents Issues**
   - Add all your frontend URLs
   - Separate with commas
   - Include development and production

3. **Database Connection**
   - NeonDB requires specific parameters
   - SSL must be enabled
   - Channel binding for NeonDB

4. **OAuth Setup**
   - Callback URL must match exactly
   - HTTPS required in production
   - Some providers need specific scopes

5. **Session Cookies**
   - httpOnly for security
   - secure in production only
   - sameSite for CSRF protection

---

## Related Skills
- Environment Skills: Managing auth secrets
- Database Skills: User table design
- Frontend Skills: Protected routes
- Backend Skills: API authentication

**Authentication is security-critical - take time to get it right!**
