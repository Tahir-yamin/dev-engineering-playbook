# OpenAI AgentKit & Responses API Skills

**Topics**: OpenAI Agents, AgentKit, Responses API, Multi-Agent Workflows  
**Version**: 1.0  
**Source**: OpenAI Platform (January 2026)  
**Last Updated**: 2026-01-19

**IMPORTANT**: Assistants API is deprecated - migrate to Responses API by Aug 26, 2026

---

## Overview

OpenAI has transitioned from the Assistants API to a new architecture: **Responses API** + **AgentKit** + **Agents SDK**. This enables more flexible, performant multi-agent workflows for business automation.

---

## Skill #1: OpenAI Responses API

### When to Use
- Building new AI agents (replacement for Assistants API)
- Need faster, more flexible agent workflows
- Multi-step tool calling
- Persistent conversations

### Migration from Assistants API
**Deprecated**: Assistants API (sunset Aug 26, 2026)  
**New**: Responses API

### Setup

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

# Single HTTP request for complete workflow
response = client.responses.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Analyze this data and create a report"}
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "fetch_data",
                "description": "Fetch data from database",
                "parameters": {...}
            }
        }
    ],
    stream=True  # Stream tool calls and responses
)
```

### Key Features
- ✅ Single HTTP request for chat + tool call + result
- ✅ Streaming support for real-time responses
- ✅ Persistent threads and memory
- ✅ Built-in code interpreter
- ✅ Compatible with all current/future models

### Advantages Over Assistants API
- **Faster**: Streamlined architecture
- **More Control**: Fine-grained workflow management
- **Better Performance**: Optimized for production
- **Future-Proof**: Designed for new models

---

## Skill #2: OpenAI AgentKit

### When to Use
- Building business automation workflows
- Visual agent design (no code)
- Integrating with business systems
- Embedding agents in products

### Components

**1. Agent Builder**
- Visual workflow creation
- Drag-and-drop interface
- No coding required

**2. Connector Registry**
- Secure integration with business systems
- Pre-built connectors for:
  - CRM (Salesforce, HubSpot)
  - Email (Gmail, Outlook)
  - Databases
  - Internal tools

**3. ChatKit Modules**
- Embed agents into product UIs
- Customizable chat interfaces
- Brand-consistent design

### Setup

```javascript
import { AgentBuilder } from '@openai/agentkit';

const agent = new AgentBuilder()
  .setName("Customer Support Agent")
  .addConnector("salesforce")
  .addConnector("zendesk")
  .addWorkflow({
    trigger: "new_ticket",
    actions: [
      "fetch_customer_history",
      "categorize_issue",
      "suggest_solution",
      "update_ticket"
    ]
  })
  .build();

agent.deploy();
```

### Use Cases
- Customer support automation
- Data entry automation
- Report generation
- Workflow orchestration

---

## Skill #3: OpenAI Agents SDK

### When to Use
- Complex multi-agent orchestration
- Need guardrails and validation
- Python/Node development environments
- Production-grade agent systems

### Setup

```python
from openai.agents import Agent, Workflow, Guardrail

# Define agents with roles
researcher = Agent(
    name="Researcher",
    model="gpt-4-turbo",
    instructions="Research topics thoroughly",
    tools=["web_search", "document_reader"]
)

writer = Agent(
    name="Writer",
    model="gpt-4-turbo",
    instructions="Create engaging content",
    tools=["text_generator"]
)

# Define workflow with guardrails
workflow = Workflow()
workflow.add_agent(researcher)
workflow.add_agent(writer)
workflow.add_guardrail(
    Guardrail.input_validation(
        schema={"type": "object", "properties": {...}}
    )
)

# Execute with handoffs
result = workflow.execute(
    input="Research and write about AI agents",
    handoff_strategy="sequential"
)
```

### Key Features
- **Handoffs**: Delegate between agents
- **Guardrails**: Input/output validation
- **Orchestration**: Multi-agent coordination
- **Retries**: Automatic error handling

---

## Skill #4: Custom GPT Actions Evolution

### Background
Custom GPT actions (deprecated 2024) evolved into full AI agents with:
- Multi-step task execution
- Web browsing
- File creation
- Recurring workflows

### Modern Approach

**Instead of Custom Actions**:
```javascript
// Old way (deprecated)
GPT.addAction("fetch_data", apiSchema);

// New way - Full agent
const agent = new Agent({
  name: "Data Analyst",
  capabilities: [
    "web_browsing",
    "file_handling",
    "code_execution",
    "api_calling"
  ]
});
```

### Integration with GitHub

**Connect ChatGPT to GitHub**:
```python
from openai import OpenAI

client = OpenAI()

# Connect to GitHub repo
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{
        "role": "system",
        "content": "You have access to the GitHub repo: user/my-repo"
    }],
    tools=[{
        "type": "function",
        "function": {
            "name": "github_api",
            "description": "Interact with GitHub",
            "parameters": {...}
        }
    }]
)
```

---

## Skill #5: VS Code Custom Agents

### When to Use
- Team-specific workflows
- Custom coding assistance
- Organization standards enforcement

### Setup

Create `.github/agents/` folder in workspace:

**Example: Code Review Agent**
```yaml
# .github/agents/code-reviewer.yml
name: Code Reviewer
description: Reviews code for security and performance
triggers:
  - pull_request
  - manual

capabilities:
  - code_analysis
  - security_scanning
  - performance_profiling

rules:
  - Check for SQL injection
  - Verify input validation
  - Analyze time complexity
  - Check code coverage

output:
  format: markdown
  include_suggestions: true
```

**Usage**:
In VS Code, type `@code-reviewer check this PR`

---

## Quick Reference

### API Comparison

| Feature | Assistants API (OLD) | Responses API (NEW) |
|---------|---------------------|---------------------|
| Status | Deprecated | Active |
| Sunset | Aug 26, 2026 | N/A |
| Speed | Slower | Faster |
| Flexibility | Limited | High |
| Streaming | Basic | Advanced |
| Tool Calling | Sequential | Parallel |

### Migration Checklist

- [ ] Review current Assistants API usage
- [ ] Test Responses API implementation
- [ ] Update tool calling logic
- [ ] Test streaming functionality
- [ ] Update error handling
- [ ] Deploy before Aug 26, 2026

---

## Integration Examples

### Agent-to-Agent Communication

```python
from openai.agents import Agent, AgentTeam

# Define team
sales_agent = Agent(name="Sales", model="gpt-4-turbo")
support_agent = Agent(name="Support", model="gpt-4-turbo")

team = AgentTeam([sales_agent, support_agent])

# Agents collaborate
result = team.collaborate(
    task="Handle customer inquiry about refund",
    strategy="handoff"  # Sales → Support when needed
)
```

### ChatGPT in Browser

```javascript
// AgentGPT - Deploy autonomous agents
import { AutoAgent } from 'reworkd-agentgpt';

const agent = new AutoAgent({
  goal: "Research competitors and create comparison table",
  max_iterations: 5,
  tools: ["web_search", "data_extraction"]
});

agent.run();
```

---

## Best Practices

### DO:
✅ Migrate from Assistants API before deadline  
✅ Use Responses API for new projects  
✅ Implement guardrails for production  
✅ Test agent workflows thoroughly  
✅ Use AgentKit for business automation

### DON'T:
❌ Build new features on Assistants API  
❌ Skip input validation  
❌ Deploy without error handling  
❌ Ignore rate limits  
❌ Mix old and new APIs

---

## Related Skills
- Claude Agent Skills (claude-healthcare-skills.md)
- Gemini Agent Skills (gemini-agent-skills.md)
- Agent Frameworks Guide (agent-frameworks-guide.md)

---

## Resources

### Official Documentation
- Responses API: https://platform.openai.com/docs/api-reference/responses
- AgentKit: https://platform.openai.com/docs/agentkit
- Agents SDK: https://github.com/openai/agents-sdk
- Migration Guide: https://platform.openai.com/docs/migration

### GitHub Repositories
- openai/agents-sdk
- reworkd/AgentGPT
- flo-bit/chat_agents

### Community
- OpenAI Developer Forum
- Reddit: r/OpenAI

---

**OpenAI's agent platform is evolving - stay current with Responses API + AgentKit!** 🚀
