---
description: Integrate Gemini CLI into GitHub workflows for autonomous code review and bug fixing
---

# Gemini CLI GitHub Integration

## When to Use
- Want automated code reviews on every PR
- Need autonomous bug fixing
- Automate issue triage
- Build custom CI/CD with AI

---

## Prerequisites

```bash
# GitHub account with admin access to repository
# Gemini API key (get from https://makersuite.google.com/app/apikey)
```

---

## Step 1: Set Up GitHub Secrets

### Add Gemini API Key

1. **Navigate to repository settings**:
   ```
   Your Repo → Settings → Secrets and variables → Actions
   ```

2. **Create new secret**:
   - Name: `GEMINI_API_KEY`
   - Value: Your Gemini API key
   - Click "Add secret"

---

## Step 2: Create Automated PR Review Workflow

### Basic Setup

Create `.github/workflows/ai-code-review.yml`:

```yaml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Get full history for better context

      - name: Run Gemini Code Review
        uses: google-gemini/gemini-cli-github-actions@v1
        with:
          task: 'review'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          focus: 'security,performance,best-practices'
          comment-on-pr: true
```

### Advanced Configuration

```yaml
name: Comprehensive AI Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      issues: write
    
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Security Review
        uses: google-gemini/gemini-cli-github-actions@v1
        with:
          task: 'review'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          focus: 'security'
          severity-threshold: 'medium'
          fail-on-issues: true
      
      - name: Performance Review
        uses: google-gemini/gemini-cli-github-actions@v1
        with:
          task: 'review'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          focus: 'performance'
          comment-on-pr: true
          
      - name: Best Practices Check
        uses: google-gemini/gemini-cli-github-actions@v1
        with:
          task: 'review'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          focus: 'best-practices,maintainability'
          generate-report: true
          report-path: './review-report.md'
      
      - name: Upload Review Report
        uses: actions/upload-artifact@v3
        with:
          name: code-review-report
          path: ./review-report.md
```

---

## Step 3: Enable Autonomous Bug Fixing

### Issue Auto-Fix Workflow

Create `.github/workflows/ai-bug-fix.yml`:

```yaml
name: AI Bug Fixer

on:
  issues:
    types: [labeled]
  issue_comment:
    types: [created]

jobs:
  auto-fix:
    if: contains(github.event.issue.labels.*.name, 'bug') || contains(github.event.comment.body, '@gemini-cli fix')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Fix Bug Autonomously
        uses: google-gemini/gemini-cli-github-actions@v1
        with:
          task: 'fix-bug'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          issue-number: ${{ github.event.issue.number }}
          create-pr: true
          branch-name: 'ai-fix-${{ github.event.issue.number }}'
          commit-message: 'fix: resolve issue #${{ github.event.issue.number }}'
      
      - name: Request Review
        if: success()
        run: gh pr create-review-request -a human-reviewer
        env:
          GH_TOKEN: ${{ github.token }}
```

### Usage

```markdown
# In any GitHub issue labeled "bug", comment:
@gemini-cli fix this bug

# Gemini will:
1. Analyze the issue description
2. Locate the problematic code
3. Generate a fix
4. Create a pull request
5. Request human review
```

---

## Step 4: Automated Issue Triage

### Issue Triage Workflow

Create `.github/workflows/ai-issue-triage.yml`:

```yaml
name: AI Issue Triage

on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    
    steps:
      - name: Analyze and Label Issue
        uses: google-gemini/gemini-cli-github-actions@v1
        with:
          task: 'triage'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          issue-number: ${{ github.event.issue.number }}
          labels-to-apply: 'auto-priority,auto-type,auto-urgency'
          
      - name: Add Priority Comment
        uses: google-gemini/gemini-cli-github-actions@v1
        with:
          task: 'comment'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          issue-number: ${{ github.event.issue.number }}
          comment-template: |
            ## AI Triage Analysis
            
            **Priority**: {priority}
            **Type**: {type}
            **Estimated Complexity**: {complexity}
            **Suggested Owner**: {owner}
            
            **Analysis**:
            {analysis}
```

### Labels Created

| Label | When Applied |
|-------|--------------|
| `priority:critical` | Security issues, production bugs |
| `priority:high` | Feature regressions, major bugs |
| `priority:medium` | Enhancement requests |
| `priority:low` | Documentation, minor improvements |
| `type:bug` | Bug reports |
| `type:feature` | Feature requests |
| `type:docs` | Documentation updates |

---

## Step 5: Custom AI Workflows

### Generate Release Notes

Create `.github/workflows/ai-release-notes.yml`:

```yaml
name: AI Release Notes

on:
  release:
    types: [created]

jobs:
  generate-notes:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Generate Release Notes
        uses: google-gemini/gemini-cli-github-actions@v1
        with:
          task: 'generate-release-notes'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          from-tag: ${{ github.event.release.tag_name }}
          output-file: 'RELEASE_NOTES.md'
      
      - name: Update Release Description
        run: |
          gh release edit ${{ github.event.release.tag_name }} \
            --notes-file RELEASE_NOTES.md
        env:
          GH_TOKEN: ${{ github.token }}
```

---

### Automated Documentation Updates

```yaml
name: AI Documentation Sync

on:
  push:
    branches: [main]
    paths:
      - 'src/**/*.ts'
      - 'src/**/*.tsx'

jobs:
  update-docs:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Generate API Documentation
        uses: google-gemini/gemini-cli-github-actions@v1
        with:
          task: 'generate-docs'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
          source-dir: './src'
          output-dir: './docs/api'
          format: 'markdown'
      
      - name: Commit Documentation
        run: |
          git config user.name 'AI Documentation Bot'
          git config user.email 'ai-bot@example.com'
          git add docs/api/
          git commit -m 'docs: auto-update API documentation' || exit 0
          git push
```

---

## Verification & Testing

### Test the Integration

// turbo
```bash
# Test locally before deploying
gh workflow run ai-code-review.yml

# Check workflow status
gh run list --workflow=ai-code-review.yml

# View logs
gh run view --log
```

### Monitor AI Actions

```bash
# View all workflow runs
gh run list

# See AI-generated PRs
gh pr list --author "github-actions[bot]"

# Check AI comments
gh api repos/:owner/:repo/issues/comments | jq '.[] | select(.user.login == "github-actions[bot]")'
```

---

## Best Practices

### DO:
✅ Always require human review for AI-generated code  
✅ Set up branch protection rules  
✅ Monitor AI accuracy and adjust thresholds  
✅ Use specific focus areas (security, performance)  
✅ Review AI comments before merging

### DON'T:
❌ Auto-merge AI-generated fixes without review  
❌ Give AI write access to production branches  
❌ Ignore false positives (refine prompts)  
❌ Skip testing AI-generated code  
❌ Use in repositories with sensitive data without audit

---

## Troubleshooting

### Workflow Fails with "API Key Invalid"

```yaml
# Verify secret is set correctly
gh secret list

# Update secret
gh secret set GEMINI_API_KEY < api-key.txt
```

### AI Not Creating PRs

```yaml
# Ensure permissions are set
permissions:
  contents: write
  pull-requests: write
  
# Enable fork creation if needed
with:
  create-fork: true
```

### Rate Limiting

```yaml
# Add rate limit handling
with:
  gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
  rate-limit-delay: 1000  # ms between requests
  max-retries: 3
```

---

## Advanced: Multi-Agent Workflow

```yaml
name: Multi-Agent Code Pipeline

on:
  pull_request:
    types: [opened]

jobs:
  security-agent:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: google-gemini/gemini-cli-github-actions@v1
        with:
          task: 'security-audit'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
  
  performance-agent:
    runs-on: ubuntu-latest
    needs: security-agent
    steps:
      - uses: actions/checkout@v3
      - uses: google-gemini/gemini-cli-github-actions@v1
        with:
          task: 'performance-analysis'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
  
  documentation-agent:
    runs-on: ubuntu-latest
    needs: performance-agent
    steps:
      - uses: actions/checkout@v3
      - uses: google-gemini/gemini-cli-github-actions@v1
        with:
          task: 'update-docs'
          gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
```

---

## Related Workflows
- [Setting Up Vercel Agent Skills](setting-up-vercel-agent-skills.md)
- [Code Review Testing](code-review-testing.md)
- [GitHub Best Practices](github-best-practices.md)

---

## Resources

- **GitHub Actions**: https://github.com/google-gemini/gemini-cli-github-actions
- **Documentation**: https://geminicli.com/github-actions
- **Examples**: https://github.com/google-gemini/gemini-cli-github-actions/tree/main/examples

---

**Autonomous AI in your CI/CD pipeline - code reviews while you sleep!** 🤖
