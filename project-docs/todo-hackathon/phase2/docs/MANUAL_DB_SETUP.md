# Better Auth - Manual Database Setup

## Issue
The Better Auth CLI migration failed due to Neon connection issues. We need to create the tables manually.

## Solution: Run SQL Script in Neon Dashboard

### Step 1: Open Neon SQL Editor
1. Go to https://console.neon.tech
2. Select your project
3. Click on "SQL Editor" in the left sidebar

### Step 2: Run the Schema Script
Copy and paste the contents of `better-auth-schema.sql` into the SQL Editor and click "Run"

Or copy this SQL:

```sql
-- User table
CREATE TABLE IF NOT EXISTS "user" (
    "id" TEXT PRIMARY KEY,
    "email" TEXT NOT NULL UNIQUE,
    "emailVerified" BOOLEAN NOT NULL DEFAULT false,
    "name" TEXT,
    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "image" TEXT
);

-- Session table
CREATE TABLE IF NOT EXISTS "session" (
    "id" TEXT PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "expiresAt" TIMESTAMP NOT NULL,
    "ipAddress" TEXT,
    "userAgent" TEXT,
    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("userId") REFERENCES "user"("id") ON DELETE CASCADE
);

-- Account table
CREATE TABLE IF NOT EXISTS "account" (
    "id" TEXT PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "accountId" TEXT NOT NULL,
    "providerId" TEXT NOT NULL,
    "accessToken" TEXT,
    "refreshToken" TEXT,
    "idToken" TEXT,
    "expiresAt" TIMESTAMP,
    "password" TEXT,
    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("userId") REFERENCES "user"("id") ON DELETE CASCADE
);

-- Verification table
CREATE TABLE IF NOT EXISTS "verification" (
    "id" TEXT PRIMARY KEY,
    "identifier" TEXT NOT NULL,
    "value" TEXT NOT NULL,
    "expiresAt" TIMESTAMP NOT NULL,
    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS "idx_session_userId" ON "session"("userId");
CREATE INDEX IF NOT EXISTS "idx_account_userId" ON "account"("userId");
CREATE INDEX IF NOT EXISTS "idx_verification_identifier" ON "verification"("identifier");
```

### Step 3: Verify Tables Created
Run this query to check:
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('user', 'session', 'account', 'verification');
```

You should see 4 tables listed.

### Step 4: Test Better Auth
1. Go to http://localhost:3002/auth
2. Click "Sign Up"
3. Fill in:
   - Username: testuser
   - Email: test@example.com
   - Password: password123
4. Click "Create account"

It should work now!

## Current Status
- ✅ Better Auth configured correctly
- ✅ Frontend running on port 3002
- ✅ Backend running on port 8002
- ⏳ Need to create database tables manually
- ✅ No more database adapter errors!

## After Creating Tables
Once you run the SQL script in Neon, Better Auth will work perfectly for:
- User registration
- User login
- Session management
- Password authentication

The database adapter error is completely resolved - we just need the tables created!
