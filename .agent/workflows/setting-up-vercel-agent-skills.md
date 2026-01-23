---
description: Set up and use Vercel Agent Skills for AI coding assistants
---

# Setting Up Vercel Agent Skills

## When to Use
- Want to add industry best practices to AI coding assistants
- Using Claude Code, GitHub Copilot, or similar tools
- Need standardized code optimization rules
- Want to improve AI-generated code quality

---

## Overview

Vercel Agent Skills is an open-source "NPM for AI agents" that provides curated skills for AI coding assistants. It integrates best practices directly into tools like Claude Code.

**Official Repository**: https://github.com/vercel-labs/agent-skills

---

## Step 1: Install Vercel Agent Skills

### Prerequisites
```bash
# Ensure you have Node.js installed
node --version  # Should be v18 or higher
npm --version
```

### Installation

// turbo
```bash
# Install the agent skills package
npx add-skill vercel-labs/agent-skills

# This will:
# 1. Clone the skills repository
# 2. Set up configuration
# 3. Make skills available to AI assistants
```

**Expected Output**:
```
✓ Cloning vercel-labs/agent-skills
✓ Installing dependencies
✓ Configuring skills
✓ 3 skills added successfully
  - react-best-practices
  - web-design-guidelines
  - vercel-deploy-claimable
```

---

## Step 2: Available Skills

### 1. React Best Practices
**Purpose**: Optimize React and Next.js code for performance

**What it does**:
- Suggests Server Components vs Client Components
- Recommends proper data fetching patterns
- Identifies unnecessary re-renders
- Optimizes bundle size

**Activation**:
- Automatically detected when working with React/Next.js files
- Or explicitly: "Apply React best practices to this component"

**Example**:
```jsx
// Before
"use client"
export default function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(setUser);
  }, [userId]);
  
  return <div>{user?.name}</div>;
}

// After (with React best practices skill)
// Server Component - no client-side fetching
export default async function UserProfile({ userId }) {
  const user = await getUser(userId);
  return <div>{user.name}</div>;
}
```

---

### 2. Web Design Guidelines
**Purpose**: Review UI code against design best practices

**What it does**:
- Checks accessibility (ARIA labels, semantic HTML)
- Validates responsive design
- Suggests color contrast improvements
- Recommends loading states

**Activation**:
- Detected when working with UI components
- Or: "Review this for web design best practices"

**Example**:
```jsx
// AI will suggest improvements like:
// ❌ Missing alt text
<img src="/avatar.jpg" />

// ✅ Accessible image
<img src="/avatar.jpg" alt="User avatar" />

// ❌ Poor contrast
<button className="text-gray-400 bg-gray-300">Click</button>

// ✅ Better contrast
<button className="text-white bg-blue-600">Click</button>
```

---

### 3. Vercel Deploy Claimable
**Purpose**: Automate Vercel deployments from AI conversations

**What it does**:
- Deploys directly to Vercel
- Manages preview deployments
- Handles environment variables
- Monitors deployment status

**Activation**:
- "Deploy this to Vercel"
- "Create a preview deployment"

**Example**:
```markdown
Me: "Deploy the current branch to Vercel as a preview"

Claude (with skill):
1. Detecting Git branch: feature/new-dashboard
2. Creating deployment...
3. ✓ Deployed to: https://my-app-abc123.vercel.app
4. Preview URL ready for testing
```

---

## Step 3: Configure Claude Code to Use Skills

### Enable in Claude Desktop App

1. **Open Claude Settings**:
   - macOS: Claude → Settings
   - Windows: File → Settings

2. **Enable Code Execution**:
   ```
   Settings → Code execution and file creation → ON
   ```

3. **Configure Skills Path**:
   ```bash
   # Point Claude to your skills directory
   ~/.agent-skills/vercel-labs/
   ```

### Verify Installation

```markdown
Ask Claude: "What agent skills do you have available?"

Expected response:
I have access to the following Vercel Agent Skills:
1. react-best-practices - Optimize React/Next.js code
2. web-design-guidelines - UI/UX best practices
3. vercel-deploy-claimable - Automated Vercel deployments
```

---

## Step 4: Use Skills in Practice

### Example Workflow 1: React Component Optimization

```markdown
Me: "Create a user dashboard component and optimize it"

Claude (automatically applies react-best-practices):
```tsx
// Optimized Server Component
import { Suspense } from 'react';

async function UserDashboard() {
  const data = await fetchDashboardData();
  
  return (
    <div>
      <Suspense fallback={<DashboardSkeleton />}>
        <DataGrid data={data} />
      </Suspense>
    </div>
  );
}

export default UserDashboard;
```

✓ Used Server Component (no client bundle)
✓ Implemented Suspense for streaming
✓ Added loading state
✓ Optimized for performance
```

---

### Example Workflow 2: Accessible Form

```markdown
Me: "Build a contact form with web design best practices"

Claude (applies web-design-guidelines):
```tsx
<form aria-label="Contact Form">
  <div>
    <label htmlFor="name">Name</label>
    <input 
      id="name"
      type="text"
      required
      aria-required="true"
      aria-describedby="name-help"
    />
    <span id="name-help" className="text-sm text-gray-600">
      Enter your full name
    </span>
  </div>
  
  <button 
    type="submit"
    className="bg-blue-600 text-white px-4 py-2 rounded
               hover:bg-blue-700 focus:ring-2 focus:ring-blue-500"
    aria-label="Submit contact form"
  >
    Send Message
  </button>
</form>
```

✓ Semantic HTML with proper labels
✓ ARIA attributes for accessibility
✓ High contrast colors
✓ Focus states for keyboard navigation
```

---

### Example Workflow 3: Deployment

```markdown
Me: "Deploy this to Vercel and share the preview URL"

Claude (uses vercel-deploy-claimable):
Deploying to Vercel...
✓ Build completed successfully
✓ Deployment live at: https://my-app-git-feature-username.vercel.app
✓ Production deployment ready

Preview URL: https://my-app-git-feature-username.vercel.app
Production: Will deploy on merge to main
```

---

## Step 5: Create Custom Skills (Advanced)

### Custom Skill Structure

```bash
# Create your own skill
mkdir -p ~/.agent-skills/custom/security-audit

# Create skill definition
cat > ~/.agent-skills/custom/security-audit/skill.json << EOF
{
  "name": "security-audit",
  "version": "1.0.0",
  "description": "Security best practices for Node.js apps",
  "activation_keywords": ["security", "audit", "vulnerabilities"],
  "rules": [
    "Check for SQL injection vulnerabilities",
    "Validate all user inputs",
    "Use parameterized queries",
    "Implement rate limiting",
    "Add CSRF protection"
  ]
}
EOF
```

### Register Custom Skill

```bash
# Add to Claude's configuration
npx add-skill ~/.agent-skills/custom/security-audit
```

---

## Troubleshooting

### Skill Not Detected

```bash
# Check skill installation
ls -la ~/.agent-skills/vercel-labs/

# Reinstall if needed
rm -rf ~/.agent-skills
npx add-skill vercel-labs/agent-skills
```

### Claude Not Using Skills

1. **Verify code execution is enabled**:
   - Settings → Code execution and file creation → ON

2. **Check skill path**:
   ```bash
   # Should output skill directory
   echo $CLAUDE_SKILLS_PATH
   ```

3. **Explicitly request skill**:
   ```markdown
   "Use the react-best-practices skill to optimize this code"
   ```

### Deployment Skill Fails

```bash
# Ensure Vercel CLI is installed
npm install -g vercel

# Login to Vercel
vercel login

# Verify authentication
vercel whoami
```

---

## Integration with Other Tools

### GitHub Copilot
```bash
# Copilot can also use Vercel Agent Skills
# Add to .github/.copilot-instructions.md
Use Vercel Agent Skills for:
- React optimization (react-best-practices)
- Accessibility (web-design-guidelines)
- Deployment (vercel-deploy-claimable)
```

### VS Code
```json
// .vscode/settings.json
{
  "ai.skills.enabled": true,
  "ai.skills.path": "~/.agent-skills/vercel-labs/"
}
```

---

## Best Practices

### DO:
✅ Let skills activate automatically when relevant  
✅ Review AI suggestions before applying  
✅ Combine multiple skills for comprehensive optimization  
✅ Create custom skills for your specific needs  
✅ Keep skills updated with `npx update-skill`

### DON'T:
❌ Override skill recommendations without understanding  
❌ Disable skills globally (configure per-project)  
❌ Ignore accessibility suggestions  
❌ Deploy without reviewing changes  
❌ Use deprecated skill patterns

---

## Next Steps

1. **Explore More Skills**:
   ```bash
   npx browse-skills vercel-labs
   ```

2. **Create Team Skills**:
   - Document coding standards as skills
   - Share across team via Git

3. **Monitor Skill Usage**:
   ```bash
   npx skill-stats
   # Shows which skills are most used
   ```

---

## Related Workflows
- [Code Review Testing](code-review-testing.md)
- [Adding New Features](adding-new-feature.md)
- [Performance Optimization](performance-problems.md)

---

## Resources

- **GitHub**: https://github.com/vercel-labs/agent-skills
- **Documentation**: https://vercel.com/docs/agent-skills
- **Community**: Vercel Discord #agent-skills channel

---

**Agent Skills make your AI coding assistant smarter - install once, benefit forever!** 🎯
