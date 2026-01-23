# CrewAI Complete Framework Integration Skills

## Overview

Complete integration of CrewAI framework capabilities into Antigravity as reusable intelligence patterns.

**Sources**:
- ✅ **Core Framework**: https://github.com/crewAIInc/crewAI
- ✅ **Examples**: https://github.com/crewAIInc/crewAI-examples  
- ⏳ **Cookbook**: https://github.com/crewAIInc/crewAI-cookbook (requires auth - add later)

**Version**: CrewAI 1.8.1  
**Location**: `d:\my-dev-knowledge-base\external-frameworks\`

---

## Core Concepts

### 1. Agents
**Role-based autonomous AI entities**

```python
from crewai import Agent

agent = Agent(
    role='Senior Market Analyst',
    goal='Conduct deep market analysis',
    backstory='Expert analyst with 10+ years experience',
    verbose=True,
    allow_delegation=False,
    tools=[SerperDevTool()]
)
```

**Key Properties**:
- `role`: What the agent does
- `goal`: What they aim to achieve
- `backstory`: Context for better responses
- `tools`: Available capabilities
- `allow_delegation`: Can delegate to other agents
- `memory`: Enable long-term memory

### 2. Tasks
**Specific assignments for agents**

```python
from crewai import Task

task = Task(
    description='Research {company} recent projects and culture',
    expected_output='Detailed company intelligence report',
    agent=analyst_agent,
    output_file='company_report.md'
)
```

**Key Properties**:
- `description`: What to do (supports variables)
- `expected_output`: What format/content to return
- `agent`: Who executes it
- `context`: Dependencies on other tasks
- `output_file`: Save results to file

### 3. Crews
**Teams of agents working together**

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.sequential,  # or Process.hierarchical
    verbose=True
)

result = crew.kickoff(inputs={'company': 'AECOM'})
```

**Process Types**:
- **Sequential**: Tasks execute in order
- **Hierarchical**: Manager agent delegates tasks

### 4. Flows
**Event-driven workflows with precise control**

```python
from crewai.flow.flow import Flow, listen, start, router

class JobResearchFlow(Flow):
    @start()
    def fetch_job_data(self):
        return {"url": "...", "company": "..."}
    
    @listen(fetch_job_data)
    def analyze_company(self, job_data):
        # Use crew here
        crew = Crew(agents=[...], tasks=[...])
        return crew.kickoff(inputs=job_data)
    
    @router(analyze_company)
    def decide_next_step(self):
        if self.state.confidence > 0.8:
            return "generate_application"
        return "request_more_data"
```

**Flow Features**:
- `@start()`: Entry point
- `@listen()`: React to events
- `@router()`: Conditional branching
- `or_()`, `and_()`: Combine conditions

---

## Available Example Crews

### 1. Job Application Crews

#### A. **Match Profile to Positions**
**Purpose**: Match CV to job openings

**Agents**:
- Profile Analyst
- Job Requirements Analyst
- Matcher

**Use Case**: Compare candidate against multiple roles

```python
# Location: external-frameworks/crewAI-examples/crews/match_profile_to_positions/
```

#### B. **Recruitment Crew**
**Purpose**: Automated recruitment process

**Agents**:
- Talent Sourcer
- Interviewer
- Coordinator

**Use Case**: Find and evaluate candidates

```python
# Location: external-frameworks/crewAI-examples/crews/recruitment/
```

### 2. Content Creation Crews

#### **Landing Page Generator**
**Purpose**: Create complete landing pages

**Agents**:
- Market Researcher
- Copywriter
- Developer

**Output**: HTML/CSS landing page

#### **Instagram Post Creator**
**Purpose**: Generate social media content

**Agents**:
- Content Strategist
- Copywriter
- Visual Designer

### 3. Research \u0026 Analysis Crews

#### **Stock Analysis**
**Purpose**: Financial market analysis

**Agents**:
- Financial Analyst
- Data Analyst
- Report Generator

#### **Trip Planner**
**Purpose**: Comprehensive travel planning

**Agents**:
- City Selector
- Local Expert
- Travel Concierge

### 4. Business Intelligence Crews

#### **Marketing Strategy**
**Purpose**: Develop marketing plans

**Agents**:
- Market Researcher
- Strategist
- Content Planner

#### **Game Builder**
**Purpose**: Design game concepts

**Agents**:
- Game Designer
- Developer
- Tester

---

## Integration Patterns for Job Applications

### Pattern 1: Company Intelligence Crew

```python
from crewai import Agent, Task, Crew, Process

# Define specialized agents
company_researcher = Agent(
    role='Company Intelligence Analyst',
    goal='Deep dive into company culture, recent projects, values',
    backstory='''Expert in corporate research with access to multiple 
    data sources. Known for uncovering insights about company culture 
    and strategic direction.''',
    verbose=True,
    tools=[SerperDevTool(), WebsiteSearchTool()]
)

tech_analyzer = Agent(
    role='Technology Stack Analyst',
    goal='Identify company\'s technology preferences and stack',
    backstory='''Senior tech analyst who understands how companies 
    choose and use technology. Expert at reading between the lines 
    of job postings.''',
    verbose=True
)

culture_expert = Agent(
    role='Workplace Culture Analyst',
    goal='Understand company values and work environment',
    backstory='''HR professional with deep insight into organizational 
    culture. Can identify culture fit indicators from public data.''',
    verbose=True
)

# Define tasks
research_company = Task(
    description='''Research {company} thoroughly:
    - Recent projects and news (last 6 months)
    - Company values and mission
    - Growth trajectory and market position
    - Employee reviews and culture signals
    
    Company website: {url}
    ''',
    expected_output='Comprehensive company intelligence report',
    agent=company_researcher
)

analyze_tech = Task(
    description='''Analyze {company}'s technology landscape:
    - Current technology stack
    - Preferred tools and methodologies
    - Technical culture indicators
    - Innovation focus areas
    ''',
    expected_output='Technology stack analysis',
    agent=tech_analyzer,
    context=[research_company]  # Depends on research
)

assess_culture = Task(
    description='''Evaluate {company}'s workplace culture:
    - Core values in action
    - Work-life balance indicators
    - Team collaboration style
    - Growth and development opportunities
    ''',
    expected_output='Culture assessment report',
    agent=culture_expert,
    context=[research_company]
)

# Create crew
intelligence_crew = Crew(
    agents=[company_researcher, tech_analyzer, culture_expert],
    tasks=[research_company, analyze_tech, assess_culture],
    process=Process.sequential,
    verbose=True
)

# Execute
result = intelligence_crew.kickoff(inputs={
    'company': 'AECOM',
    'url': 'https://careers.aecom.com'
})
```

### Pattern 2: Job Matching Crew

```python
job_analyzer = Agent(
    role='Job Requirements Analyst',
    goal='Extract and categorize job requirements',
    backstory='Expert at parsing job descriptions and identifying key requirements',
    verbose=True
)

profile_matcher = Agent(
    role='CV-to-Job Matcher',
    goal='Match candidate profile to job requirements',
    backstory='Experienced recruiter who understands skill transferability',
    verbose=True
)

application_strategist = Agent(
    role='Application Strategy Advisor',
    goal='Create winning application strategy',
    backstory='Career coach with proven success in job applications',
    verbose=True
)

# Tasks
analyze_job = Task(
    description='''Analyze the job posting at {url}:
    - Must-have requirements
    - Nice-to-have skills
    - Key responsibilities
    - Success metrics
    ''',
    expected_output='Structured job requirements breakdown',
    agent=job_analyzer
)

match_profile = Task(
    description='''Match candidate profile to job requirements:
    - Highlight relevant experience
    - Identify skill gaps
    - Find transferable skills
    - Calculate match percentage
    
    Candidate CV: {cv_path}
    ''',
    expected_output='Profile-to-job match analysis',
    agent=profile_matcher,
    context=[analyze_job]
)

create_strategy = Task(
    description='''Create tailored application strategy:
    - Key points to emphasize
    - How to address gaps
    - Customization recommendations
    - Cover letter angle
    ''',
    expected_output='Application strategy document',
    agent=application_strategist,
    context=[analyze_job, match_profile]
)

matching_crew = Crew(
    agents=[job_analyzer, profile_matcher, application_strategist],
    tasks=[analyze_job, match_profile, create_strategy],
    process=Process.sequential
)
```

### Pattern 3: Combined Flow (Intelligence + Matching)

```python
from crewai.flow.flow import Flow, listen, start

class JobApplicationFlow(Flow):
    @start()
    def collect_job_data(self):
        """Collect job posting details"""
        return {
            'company': 'AECOM',
            'url': 'https://aecom.jobs/...',
            'role': 'Project Controls Manager'
        }
    
    @listen(collect_job_data)
    def research_company(self, job_data):
        """Run company intelligence crew"""
        result = intelligence_crew.kickoff(inputs=job_data)
        self.state.company_intel = result
        return job_data
    
    @listen(research_company)
    def analyze_fit(self, job_data):
        """Run job matching crew"""
        job_data['cv_path'] = 'path/to/cv.pdf'
        result = matching_crew.kickoff(inputs=job_data)
        self.state.match_analysis = result
        return result
    
    @listen(analyze_fit)
    def generate_application(self, match_result):
        """Generate customized application"""
        # Use existing apply_job.py with research insights
        # Pass company_intel and match_analysis for better customization
        return "Application generated with deep research"

# Execute flow
flow = JobApplicationFlow()
result = flow.kickoff()
```

---

## Tools Available in CrewAI

### Built-in Tools
```python
from crewai_tools import (
    SerperDevTool,        # Google search
    WebsiteSearchTool,    # Scrape websites
    FileReadTool,         # Read files
    DirectoryReadTool,    # Read directories
    CodeInterpreterTool,  # Execute code
    PDFSearchTool,        # Search PDFs
    JSONSearchTool,       # Search JSON
    CSVSearchTool,        # Search CSV
)
```

### Custom Tools
```python
from crewai.tools import tool

@tool("Job Search Tool")
def search_jobs(query: str, location: str) -> str:
    """Search for jobs using custom logic"""
    # Your implementation
    return "Job results"

# Use in agent
agent = Agent(
    role="Job Searcher",
    tools=[search_jobs]
)
```

---

## Integration with Existing Workflow

### Enhanced Job Application Process

**Step 1: Search Jobs (Gemini)**
```bash
python gemini_job_searcher_simple.py
# Output: gemini_jobs.json with 5+ URLs
```

**Step 2: Deep Research (CrewAI)**
```bash
python crewai_job_research.py --input gemini_jobs.json
# Output: Detailed intelligence for each company
```

**Step 3: Generate Applications**
```bash
python apply_job.py --with-research
# Uses CrewAI research to tailor applications
```

---

## Configuration Files Pattern

### agents.yaml
```yaml
company_researcher:
  role: >
    Company Intelligence Analyst
  goal: >
    Research {company} deeply to understand culture and values
  backstory: >
    Expert corporate researcher with access to multiple data sources

job_analyst:
  role: >
    Job Requirements Analyst
  goal: >
    Extract key requirements from job posting at {url}
  backstory: >
    Experienced recruiter who identifies must-have vs nice-to-have skills
```

### tasks.yaml
```yaml
research_company:
  description: >
    Research {company} thoroughly including recent projects, 
    culture, and growth trajectory
  expected_output: >
    Comprehensive company intelligence report with actionable insights
  agent: company_researcher

analyze_job:
  description: >
    Analyze job posting at {url} and extract requirements
  expected_output: >
    Structured breakdown of job requirements
  agent: job_analyst
```

---

## Best Practices

### 1. Agent Design
- ✅ Give agents specific, focused roles
- ✅ Use rich backstories for better context
- ✅ Enable memory for complex workflows
- ✅ Choose tools relevant to role

### 2. Task Design
- ✅ Clear, detailed descriptions
- ✅ Specific expected outputs
- ✅ Use variable templates `{company}`
- ✅ Set context dependencies

### 3. Crew Orchestration
- ✅ Sequential for dependent tasks
- ✅ Hierarchical for complex delegation
- ✅ Verbose mode for debugging
- ✅ Save outputs to files

### 4. Flow Control
- ✅ Use flows for production workflows
- ✅ Maintain state between steps
- ✅ Implement error handling
- ✅ Use routers for branching

---

## Performance Optimization

### Faster Execution
- Use local models (Ollama) for development
- Cache intermediate results
- Parallelize independent tasks
- Use lighter models when possible

### Cost Optimization
- Use Gemini 3 Flash (free tier)
- Batch similar requests
- Implement result caching
- Use hierarchical process to reduce calls

---

## Example Use Cases for Knowledge Base

### 1. Job Application Enhancement
- Company research before applying
- Role requirement analysis
- Profile-to-job matching
- Application strategy

### 2. Content Creation
- Blog posts with research
- Technical documentation
- Marketing materials
- Social media content

### 3. Research Tasks
- Market analysis
- Competitive intelligence
- Technology assessment
- Trend analysis

### 4. Workflow Automation
- Multi-step processes
- Decision-making workflows
- Data processing pipelines
- Report generation

---

## Resources Cloned

```
d:\my-dev-knowledge-base\external-frameworks\
├── crewAI\                    # Core framework
│   ├── lib\crewai\           # Source code
│   ├── lib\crewai-tools\     # Built-in tools
│   └── docs\                 # Documentation
├── crewAI-examples\          # Practical examples
│   ├── crews\                # 16 example crews
│   └── flows\                # 6 flow examples
└── crewAI-cookbook\          # (pending auth)
```

---

## Next Actions

### Phase 2: Extract Specific Skills
- [ ] Create skill files for each example crew
- [ ] Document agent patterns
- [ ] Extract tool usage patterns
- [ ] Create workflow templates

### Phase 3: Integration Scripts
- [ ] `crewai_job_research.py`
- [ ] `crewai_content_creator.py`
- [ ] Integration with existing workflows

### Phase 4: Testing
- [ ] Test company research crew
- [ ] Test job matching crew
- [ ] Test combined flow
- [ ] Validate outputs

---

**Status**: Phase 1 Complete ✅  
**Next**: Extract specific patterns into individual skill files  
**Version**: 1.0  
**Last Updated**: 2026-01-21
