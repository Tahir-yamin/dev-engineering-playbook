# Environment Variables Skills - For Claude AI

**Purpose**: Security setup, secret management, and validation
**Version**: 1.0
**Last Updated**: December 28, 2025

Full guides available in artifacts:
- `env_security_guide.md` - Comprehensive security best practices
- `env_quick_setup.md` - Quick 5-minute setup guide

---

## Skill #1: Environment Variables Security Setup

### When to Use
- Setting up new Docker project
- Fixing authentication issues
- Managing secrets properly
- CORS/security configuration

### Prompt Template

```markdown
**ROLE**: Security-conscious DevOps engineer

**PROJECT TYPE**: [Full-Stack / Backend API / Frontend App]

**REQUIRED VARS**:
- Database: [PostgreSQL / MySQL / MongoDB]
- Authentication: [Better Auth / NextAuth / JWT]
- External APIs: [OpenAI / Stripe / etc]
- CORS: [Frontend URL, allowed origins]

**DELIVERABLES**:
1. `.env.example` file with descriptions
2. `docker-compose.yml` environment section
3. Security best practices (what to commit vs ignore)
4. Validation script to check all vars present

**SPECIFIC REQUIREMENTS**:
- Better Auth needs 32+ character secret
- Database URL must include SSL params
- CORS must allow specific origins
```

---

## Skill #2: Secret Rotation Procedure

### When to Use
- Secret was committed to git
- Team member leaves
- Regular maintenance (every 90 days)
- Security breach suspected

### Prompt Template

```markdown
**ROLE**: Security specialist

**SECRET TO ROTATE**: [BETTER_AUTH_SECRET / DATABASE_URL / API_KEY]

**PROVIDE**:
1. How to generate new secret
2. Where to update it (all locations)
3. Impact on users/services
4. Verification steps
5. How to safely dispose of old secret

**URGENCY**: [Immediate / Scheduled / Routine]
```

---

## Skill #3: Database Connection String Validator

### When to Use
- Database connection failures
- SSL negotiation errors
- Cloud database setup (NeonDB, Supabase, etc)

### Prompt Template

```markdown
**ROLE**: Database connectivity specialist

**DATABASE**: [NeonDB / Supabase / RDS / etc]
**ORM**: [Prisma / TypeORM / SQLAlchemy]

**CURRENT CONNECTION STRING**:
```
[PASTE SANITIZED - remove password]
```

**ERROR**:
```
[PASTE ERROR MESSAGE]
```

**VALIDATE**:
1. Basic format (protocol, user, password, host, database)
2. SSL/TLS parameters (sslmode, channel_binding)
3. Docker-specific issues (host accessibility)

**PROVIDE**:
- Corrected connection string
- Required query parameters
- Test command to verify
- Troubleshooting steps
```

---

## Skill #4: Better Auth Docker Integration

### When to Use
- Setting up Better Auth in Docker
- CSRF token errors
- Session not persisting

### Prompt Template

```markdown
**ROLE**: Authentication and security specialist

**PROBLEM**: [Login fails / Session lost / CSRF error]

**CURRENT CONFIG**:
```env
BETTER_AUTH_SECRET=[length: X characters]
BETTER_AUTH_URL=[URL]
TRUSTED_ORIGINS=[origins]
DATABASE_URL=[sanitized]
```

**VERIFY**:
1. BETTER_AUTH_SECRET is 32+ characters
2. BETTER_AUTH_URL matches access URL
3. TRUSTED_ORIGINS includes all client origins
4. DATABASE_URL has proper SSL mode
5. Container networking is correct

**DELIVERABLES**:
- Corrected environment variables
- Fixed auth configuration code
- docker-compose.yml updates if needed
- Testing steps
```

---

## Quick Reference

### Essential Environment Variables

```bash
# Database (NeonDB)
DATABASE_URL=postgresql://user:pass@host.neon.tech/db?sslmode=require&channel_binding=require

# Authentication
BETTER_AUTH_SECRET=$(openssl rand -base64 32)  # Min 32 chars
BETTER_AUTH_URL=http://localhost:3000
TRUSTED_ORIGINS=http://localhost:3000

# APIs
OPENAI_API_KEY=sk-...
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Generate Secrets

```bash
# Mac/Linux
openssl rand -base64 32

# Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

### Security Checklist

- [ ] No hardcoded secrets in code
- [ ] `.env*` files in `.gitignore`
- [ ] Production secrets different from dev
- [ ] HTTPS in production URLs
- [ ] `sslmode=require` in DATABASE_URL
- [ ] `channel_binding=require` for NeonDB

---

## Validation Commands

```powershell
# Windows
.\scripts\validate-env.ps1

# Mac/Linux
chmod +x scripts/validate-env.sh
./scripts/validate-env.sh
```

---

**See Also**:
- Security guide (`env_security_guide.md`) in artifacts
- Quick setup guide (`env_quick_setup.md`) in artifacts
- Docker skills in `.claude/docker-skills.md`
