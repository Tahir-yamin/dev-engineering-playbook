# Gemini Agent & CLI Skills

**Topics**: Google Gemini, GitHub Integration, Agent Orchestration, CLI Automation  
**Version**: 1.0  
**Source**: Google Gemini CLI & Enterprise Platform (January 2026)  
**Last Updated**: 2026-01-19

---

## Overview

Google Gemini provides advanced AI agent capabilities with direct GitHub integration, CLI-based automation, and enterprise-grade orchestration features. These skills enable autonomous code reviews, workflow automation, and multi-agent collaboration.

---

## Skill #1: Gemini CLI GitHub Actions Integration

### When to Use
- Automating pull request reviews
- Bug fixing via GitHub issues
- Issue triage and prioritization
- Custom CI/CD workflows

### Setup

**Prerequisites**:
```bash
# Install Gemini CLI
npm install -g @google/gemini-cli

# Configure API key
export GEMINI_API_KEY="your-api-key"

# Verify installation
gemini --version
```

**GitHub Actions Setup**:
```yaml
# .github/workflows/ai-code-review.yml
name: AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: google-gemini/gemini-cli-github-actions@v1
        with:
          task: 'review'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
```

### Usage Patterns

**1. Automated PR Review**:
```yaml
# Review every pull request
on: pull_request
  - uses: google-gemini/gemini-cli-github-actions@v1
    with:
      task: 'review'
      focus: 'security,performance,best-practices'
```

**2. Bug Fixing on Demand**:
```markdown
# In GitHub issue, mention:
@gemini-cli please fix the bug described above

# Gemini will:
1. Analyze the issue
2. Locate the problematic code
3. Create a fix
4. Open a pull request
```

**3. Issue Triage**:
```yaml
# Automatically prioritize issues
on:
  issues:
    types: [opened]
    
- uses: google-gemini/gemini-cli-github-actions@v1
  with:
    task: 'triage'
    labels-to-apply: 'auto'
```

### Key Features
- ✅ Autonomous bug fixing
- ✅ Automated code review with security focus
- ✅ Issue prioritization based on content
- ✅ Multi-step reasoning for complex tasks
- ✅ Tool-calling for extended capabilities

### Best Practices
- ✅ Always review AI-generated fixes before merging
- ✅ Use focused reviews (security, performance, etc.)
- ✅ Set up branch protection rules
- ✅ Monitor AI decisions in workflow logs

---

## Skill #2: Gemini Agent Skills Framework

### When to Use
- Building specialized AI capabilities
- Creating reusable agent workflows
- Extending Gemini with custom expertise

### Implementation

**Create Agent Skill**:
```bash
# Directory structure
.agent/skills/security-audit/
├── SKILL.md           # Skill definition
├── scripts/           # Automation scripts
└── resources/         # Reference materials
```

**SKILL.md Template**:
```markdown
# Security Audit Skill

## Purpose
Perform comprehensive security audits on codebases

## Activation
Keywords: "security audit", "vulnerability scan", "code security"

## Instructions
1. Scan for SQL injection vulnerabilities
2. Check for XSS attack vectors
3. Review authentication implementation
4. Analyze dependency vulnerabilities
5. Check for sensitive data exposure

## Tools Required
- npm audit
- OWASP dep-check
- Bandit (Python)

## Output Format
- Vulnerability report (JSON)
- Remediation recommendations
- Risk severity ratings
```

**Activate Skill**:
```bash
# Gemini automatically loads when relevant
gemini "Run a security audit on this repository"

# Or explicitly
gemini --skill security-audit "Analyze ./src"
```

### Skill Categories

| Category | Example Skills | Use Cases |
|----------|---------------|-----------|
| **Development** | Code generation, refactoring | Feature implementation |
| **Security** | Vulnerability scanning, compliance | Security audits |
| **DevOps** | CI/CD setup, deployment | Infrastructure automation |
| **Documentation** | API docs, README generation | Project documentation |
| **Testing** | Test generation, coverage | Quality assurance |

### Advanced: Skill Chaining
```bash
# Create production line of skills
gemini chain \
  --skill code-generation \
  --skill security-audit \
  --skill test-generation \
  --skill documentation \
  "Build a new REST AP endpoint"
```

---

## Skill #3: Gemini CLI for Development Workflows

### When to Use
- Terminal-based AI assistance
- File manipulation and codebase understanding
- Command execution with AI oversight

### Core Commands

**File Operations**:
```bash
# Understand codebase
gemini "Explain the architecture of this project"

# File editing
gemini "Refactor ./src/api/users.ts to use async/await"

# File creation
gemini "Create a new React component for user profiles"
```

**Code Understanding**:
```bash
# Analyze specific file
gemini "What does ./utils/auth.ts do?"

# Find code patterns
gemini "Find all database queries in this project"

# Explain error
gemini "Why is this failing?" < error.log
```

**Debugging**: ```bash
# Debug with context
gemini --context ./logs/error.log "Fix the authentication bug"

# Trace execution
gemini "Add logging to track user session flow"
```

### Tool Integration
```bash
# Execute commands safely
gemini "Install dependencies for this project"
# Gemini will: analyze package.json → run npm install

# Git operations
gemini "Create a feature branch for user authentication"
# Gemini will: git checkout -b feature/auth
```

---

## Skill #4: Gemini Enterprise - Gem Teams

### When to Use
- Building collaborative AI agent teams
- Automating complex business workflows  
- Multi-step task orchestration

### Gem Team Architecture

**Example: Content Production Team**:
```javascript
{
  "team_name": "ContentProductionLine",
  "gems": [
    {
      "name": "Researcher",
      "role": "Gather information from web and docs",
      "skills": ["web-search", "document-analysis"]
    },
    {
      "name": "Writer",
      "role": "Create content from research",
      "skills": ["content-generation", "seo-optimization"],
      "input_from": "Researcher"
    },
    {
      "name": "Editor",
      "role": "Review and polish content",
      "skills": ["grammar-check", "tone-adjustment"],
      "input_from": "Writer"
    }
  ]
}
```

**Usage**:
```bash
gemini team run ContentProductionLine \
  --input "Create a blog post about AI coding assistants" \
  --output ./blog/new-post.md
```

### Workflow Patterns

**1. Research → Analysis → Report**:
```
GemResearcher → GemAnalyst → GemReporter
```

**2. Code → Test → Deploy**:
```
GemCoder → GemTester → GemDeployer
```

**3. Support Ticket → Resolution → Documentation**:
```
GemTriager → GemResolver → GemDocumenter
```

---

## Skill #5: Gemini Auto Browse

### When to Use
- Autonomous web navigation
- Information extraction from websites
- Complete browsing sessions without human input

### Implementation

**Enable Auto Browse**:
```javascript
const gemini = require('@google/generative-ai');

const model = gemini.getGenerativeModel({
  model: "gemini-2.0-pro",
  tools: [{
    name: "auto_browse",
    config: {
      browser: "chrome",
      headless: true
    }
  }]
});
```

**Usage Examples**:

**1. Research Task**:
```javascript
const prompt = `
Visit the following websites and extract pricing information:
1. competitor-a.com
2. competitor-b.com
3. competitor-c.com

Create a comparison table.
`;

const result = await model.generateContent(prompt);
```

**2. Form Submission**:
```javascript
const prompt = `
Navigate to example.com/signup and fill out the form with:
- Name: Test User
- Email: test@example.com
- Company: Acme Corp

Submit the form and capture the confirmation message.
`;
```

**3. Monitoring**:
```javascript
const prompt = `
Every hour, visit status.example.com and check if 
all services show as "Operational". Alert if any issues.
`;
```

### Safety Features
- ✅ Respects robots.txt
- ✅ Rate limiting to prevent abuse
- ✅ CAPTCHA detection (manual intervention required)
- ✅ Session recording for audit

---

## Quick Reference

### Gemini CLI Commands
```bash
# Basic usage
gemini "your prompt here"

# With context
gemini --context ./file.txt "analyze this"

# With skill
gemini --skill security-audit "scan codebase"

# GitHub integration
gemini github review --pr 123

# Team execution
gemini team run TeamName --input "task description"

# Auto browse
gemini browse "research topic X and summarize"
```

### Configuration
```bash
# Set API key
export GEMINI_API_KEY="your-key"

# Configure default model
gemini config set model gemini-2.0-pro

# Enable experimental features
gemini config set experimental true

# Set skill directory
gemini config set skills-dir ~/.agent/skills
```

---

## Integration Examples

### Node.js Integration
```javascript
const { GoogleGenerativeAI } = require("@google/generative-ai");

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

async function runCodeReview(code) {
  const model = genAI.getGenerativeModel({ model: "gemini-2.0-pro" });
  
  const prompt = `
  Review this code for security and performance issues:
  ${code}
  `;
  
  const result = await model.generateContent(prompt);
  return result.response.text();
}
```

### Python Integration
```python
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel('gemini-2.0-pro')

def analyze_logs(log_file):
    with open(log_file, 'r') as f:
        logs = f.read()
    
    response = model.generate_content(
        f"Analyze these logs and identify errors:\n{logs}"
    )
    return response.text
```

---

## Related Skills
- GitHub Integration Skills (github-skills.md)
- CLI Automation Skills (cli-skills.md)
- Agent Orchestration (agent-orchestration-guide.md)

---

## Resources

### Official Documentation
- Gemini CLI: https://geminicli.com
- GitHub Actions: https://github.com/google-gemini/gemini-cli-github-actions
- Agent Skills: https://geminicli.com/skills

### GitHub Repositories
- google-gemini/gemini-cli
- google-gemini/gemini-cli-github-actions

### Community
- Gemini Developers Discord
- Reddit: r/GoogleGemini

---

**Gemini brings AI directly into your development workflow - embrace autonomous assistance!** 🚀
