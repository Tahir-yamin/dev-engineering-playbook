# Docker Prisma Optimization Skills

**Purpose**: Optimize Docker builds for Next.js applications using Prisma ORM  
**Source**: Extracted from Phase 5 Dockerfile troubleshooting  
**Date**: January 2026

---

## Skill #1: Prisma Schema Copy Timing

### When to Use
- Docker build fails with "Prisma schema not found"
- `npm ci` postinstall script errors
- Building Next.js app with Prisma

### The Problem
Prisma's `postinstall` hook runs during `npm ci` and needs the schema file to generate the client.

### The Solution

**WRONG Order:**
```dockerfile
COPY package*.json ./
RUN npm ci                    # ❌ FAILS - schema not available
COPY prisma ./prisma/
```

**CORRECT Order:**
```dockerfile
COPY package*.json ./
COPY prisma ./prisma/         # ✅ Copy BEFORE npm ci
RUN npm ci                    # Now postinstall can find schema
COPY . .
```

### Key Insights
- ✅ `prisma generate` runs automatically in postinstall
- ✅ Schema MUST exist before `npm ci`
- 💡  Cache layers optimize: package files → prisma → source code
- ❌ Don't copy all files first (breaks caching)

**Related Skills**: None

---

## Skill #2: Prisma Version Compatibility

### When to Use
- Prisma 7 syntax errors in Dockerfile
- "url is not a valid field" errors
- Need to downgrade Prisma

### The Problem
Prisma 7 introduced breaking changes in schema syntax for environment variables.

### The Solution

**Step 1: Check versions**
```bash
# In package.json
"@prisma/client": "7.x.x"    # Client version
"prisma": "7.x.x"            # CLI version
```

**Step 2: Downgrade if needed**
```bash
npm install prisma@6.0.0 @prisma/client@6.0.0 --save-exact
npm install  # Regenerate lockfile
```

**Step 3: Verify schema syntax**
```prisma
// Prisma 6 syntax
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")  // ✅ Works
}

// Prisma 7 changed this
```

### Key Insights
- ✅ Client and CLI versions must match
- ✅ Use `--save-exact` to prevent version drift
- 💡 Regenerate package-lock.json after downgrade
- ❌ Don't mix Prisma 6 and 7

**Related Skills**: None

---

## Skill #3: OpenSSL for Alpine Images

### When to Use
- Using `node:alpine` base image
- Prisma warnings about OpenSSL
- Database connection issues

### The Problem
Alpine Linux doesn't include OpenSSL by default, which Prisma needs for database connections.

### The Solution

```dockerfile
FROM node:20-alpine AS builder

# Install OpenSSL for Prisma
RUN apk add --no-cache openssl

WORKDIR /app
# ... rest of Dockerfile
```

### Key Insights
- ✅ Add `openssl` package in builder stage
- ✅ Required for Prisma to work on Alpine
- 💡 `--no-cache` keeps image size small
- ❌ Don't skip this on Alpine images

**Related Skills**: None

---

## Skill #4: Next.js Standalone Build

### When to Use
- Building production Next.js Docker images
- Need minimal image size
- Want self-contained deployment

### The Solution

**Step 1: Enable in next.config.js**
```javascript
module.exports = {
  output: 'standalone',  // Enable standalone mode
}
```

**Step 2: Multi-stage Dockerfile**
```dockerfile
# Builder stage
FROM node:20-alpine AS builder
WORKDIR /app

# Install dependencies and build
COPY package*.json ./
COPY prisma ./prisma/
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production

# Copy standalone output (includes dependencies)
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Start app
EXPOSE 3000
CMD ["node", "server.js"]
```

### Key Insights
- ✅ Standalone bundles all dependencies
- ✅ Much smaller than full node_modules
- ✅ Single `node server.js` command to run
- 💡 Don't copy public folder if it doesn't exist
- ❌ Don't copy entire .next folder

**Related Skills**: None

---

## Quick Reference

### Complete Next.js + Prisma Dockerfile Template

```dockerfile
# ===== Builder Stage =====
FROM node:20-alpine AS builder

# Install OpenSSL for Prisma
RUN apk add --no-cache openssl

WORKDIR /app

# Copy package files
COPY package*.json ./

# Copy Prisma schema BEFORE npm ci
COPY prisma ./prisma/

# Install dependencies (postinstall runs prisma generate)
RUN npm ci

# Copy source code
COPY . .

# Build Next.js
RUN npm run build

# ===== Production Stage =====
FROM node:20-alpine
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Copy standalone output
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Expose port
EXPOSE 3000

# Start application
CMD ["node", "server.js"]
```

### Common Build Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| "Prisma schema not found" | Schema copied after `npm ci` | Copy prisma folder BEFORE `npm ci` |
| "url is not valid" | Prisma 7 breaking changes | Downgrade to Prisma 6 |
| "OpenSSL not found" | Alpine missing OpenSSL | `RUN apk add --no-cache openssl` |
| "public folder not found" | Trying to copy non-existent folder | Remove `COPY public` line |
| Large image size | Copying full .next folder | Use standalone output only |

---

**Total Skills**: 4  
**Last Updated**: January 2026  
**Optimized For**: Next.js + Prisma + Alpine Linux
