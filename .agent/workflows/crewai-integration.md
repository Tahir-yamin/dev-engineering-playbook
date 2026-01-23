---
description: Integrate CrewAI framework into Antigravity as reusable intelligence
---

# CrewAI Integration Workflow

## When to Use
- Before starting complex research tasks
- When multiple perspectives needed
- For job application deep research
- For content creation
- For market analysis

**Time Required**: 3 hours (full setup) OR 30 minutes (quick start)

---

## Quick Start (If Already Installed)

```bash
# Job research with CrewAI
python job-application\scripts\crewai_job_research.py \
  --company "AECOM" \
  --role "Project Controls Manager"

# Content creation with CrewAI
python scripts\crewai_content_creator.py \
  --topic "Your Topic" \
  --type "blog_post"
```

---

## Full Setup (First Time)

### Step 1: Install CrewAI

// turbo
```powershell
# Create directory
New-Item -Path "d:\my-dev-knowledge-base\external-frameworks" -ItemType Directory -Force

# Clone repositories
cd d:\my-dev-knowledge-base\external-frameworks
git clone https://github.com/crewAIInc/crewAI-examples.git
git clone https://github.com/crewAIInc/crewAI.git

# Install CrewAI
pip install crewai
pip install 'crewai[tools]'
```

---

### Step 2: Extract Industry Agents as Skills

**Create these skill files**:

#### A. Market Research Skills
**File**: `skills/crewai-market-research-skills.md`

Agents:
- Market Analyst
- Technology Expert  
- Business Consultant

#### B. Content Creation Skills
**File**: `skills/crewai-content-creation-skills.md`

Agents:
- Content Strategist
- Content Writer
- SEO Specialist

#### C. Job Application Research Skills
**File**: `skills/crewai-job-application-skills.md`

Agents:
- Company Intelligence Analyst
- Role Requirements Analyst
- Application Strategy Advisor

---

### Step 3: Create Workflow Files

#### A. Company Research Workflow
**File**: `.agent/workflows/crewai-company-research.md`

Sequential workflow:
1. Market Analyst researches company
2. Tech Expert analyzes tech stack
3. Consultant generates recommendations

#### B. Job Application Research Workflow
**File**: `.agent/workflows/crewai-job-research.md`

Multi-agent workflow:
1. Company Intelligence Agent → Company report
2. Role Analyst → Requirements breakdown
3. Application Strategist → Tailored strategy

---

### Step 4: Create Integration Scripts

#### A. Job Research Script
**File**: `job-application/scripts/crewai_job_research.py`

```python
from crewai import Agent, Task, Crew

# Company researcher agent
company_agent = Agent(
    role='Company Intelligence Analyst',
    goal='Deep research on company culture, values, projects',
    backstory='Expert corporate researcher',
    verbose=True
)

# Job analyst agent
job_agent = Agent(
    role='Job Requirements Analyst',
    goal='Extract key requirements and skills',
    backstory='Experienced HR professional',
    verbose=True
)

# Application strategist
strategy_agent = Agent(
    role='Application Strategy Advisor',
    goal='Create tailored application approach',
    backstory='Career coach with 10+ years experience',
    verbose=True
)

# Create crew and execute
crew = Crew(
    agents=[company_agent, job_agent, strategy_agent],
    tasks=[research_task, analysis_task, strategy_task],
    verbose=True
)

result = crew.kickoff()
```

#### B. Content Creator Script
**File**: `scripts/crewai_content_creator.py`

Similar multi-agent pattern for content creation.

---

### Step 5: Update Existing Workflows

#### Update apply-for-jobs.md

Add Option 4:

```markdown
### Option 4: CrewAI Deep Research (Advanced) 🤖

**Multi-agent company & role analysis**

```bash
python job-application\scripts\crewai_job_research.py \
  --company "Company Name" \
  --role "Role Title" \
  --url "job-url"
```

**Output**:
- Company intelligence report
- Role requirements breakdown
- Application strategy
- Research-backed CV customization
```

---

### Step 6: Add to AI Ecosystem Monitoring

Update `.agent/workflows/ai-ecosystem-monitoring.md`

Add CrewAI monitoring section:

```markdown
## Step 3B: Search CrewAI Updates

```
"CrewAI new agents crews workflows January 2026 site:github.com"
```

**Key repositories**:
- crewAIInc/crewAI
- crewAIInc/crewAI-examples
- Community crew templates
```

---

## Integration Points

### With Gemini Job Search:
```bash
# 1. Search with Gemini
python gemini_job_searcher_simple.py

# 2. Deep research with CrewAI
python crewai_job_research.py --url "job-url-from-gemini"

# 3. Generate application
python apply_job.py --with-research
```

### With Current Workflow:
```bash
# Enhanced workflow
1. Gemini → Find jobs
2. CrewAI → Research companies
3. apply_job.py → Generate applications
```

---

## Available Crews (After Setup)

### 1. Market Research Crew
- **Agents**: 3 (Analyst, Tech Expert, Consultant)
- **Output**: Market analysis report
- **Use**: Company research, industry analysis

### 2. Content Creation Crew
- **Agents**: 3 (Strategist, Writer, SEO)
- **Output**: Optimized content
- **Use**: Blog posts, documentation, marketing

### 3. Job Application Crew (NEW)
- **Agents**: 3 (Company Intel, Role Analyst, Strategist)
- **Output**: Research report + strategy
- **Use**: Tailored job applications

### 4. Financial Analysis Crew
- **Agents**: 3 (Analyst, Data Analyst, Reporter)
- **Output**: Financial report
- **Use**: Company financial health

---

## System Rules to Add

**In Antigravity Customizations → Rules**:

### Rule 1: Multi-Agent Collaboration
```
When a task requires multiple perspectives:
1. Identify distinct roles needed
2. Execute agents sequentially or parallel
3. Synthesize findings
4. Present unified recommendation

Reference: @skills/crewai-orchestration-patterns.md
```

### Rule 2: Role-Based Prompting
```
When adopting an agent role:
- Start with role definition
- Include goal and backstory
- Maintain role throughout task
- Provide role-specific output
```

---

## Success Metrics

After setup, you should have:

- [x] CrewAI installed and working
- [x] 3-4 skill files created
- [x] 2-3 workflow files created
- [x] 1-2 integration scripts working
- [x] Existing workflows updated
- [x] AI monitoring updated

---

## Testing the Integration

### Test 1: Company Research
```bash
python crewai_job_research.py \
  --company "AECOM" \
  --url "https://aecom.jobs/..."
```

Expected output: 3-part report (company intel, requirements, strategy)

### Test 2: Content Creation
```bash
python crewai_content_creator.py \
  --topic "AI Job Search" \
  --type "blog_post"
```

Expected output: SEO-optimized blog post

---

## Maintenance

### Weekly:
- Check for CrewAI updates: `pip install --upgrade crewai`
- Review new crew templates in crewAI-examples repo
- Update skills with new patterns

### Monthly:
- Add new industry agents as skills
- Create new crew combinations
- Update integration scripts

---

## Related Workflows

- [@ai-ecosystem-monitoring](ai-ecosystem-monitoring.md) - Includes CrewAI monitoring
- [@workflow-orchestrator](workflow-orchestrator.md) - Orchestrate CrewAI workflows
- [@apply-for-jobs](apply-for-jobs.md) - Enhanced with CrewAI research

---

## Next Steps After Setup

1. Test job application research crew
2. Create custom crews for your needs
3. Document successful patterns as skills
4. Share crew templates

---

**Created**: 2026-01-21  
**Version**: 1.0  
**Impact**: Transforms Antigravity into multi-agent platform
