# Microsoft Agent Framework & Foundry Skills

**Topics**: Azure AI Foundry, Microsoft Agent Framework, Persistent Agents, Multi-Tool Integration
**Source**: [Microsoft Agent Skills](https://microsoft.github.io/skills/)
**Version**: 1.0 (2026 Update)

---

## Skill #1: Building Persistent Agents with Azure AI Foundry

### When to Use
- Creating agents that require long-running conversation threads and persistent state.
- Integrating with Azure-hosted tools (Code Interpreter, File Search).

### Implementation Pattern (Python):
```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

client = AIProjectClient.from_connection_string(
    conn_str=PROJECT_CONNECTION_STRING,
    credential=DefaultAzureCredential()
)

# Using ImageBasedHostedAgentDefinition for container-based agents
# Using PersistentAgentsClient for thread management
```

---

## Skill #2: Multi-Tool Orchestration (Azure Agent Framework)

### When to Use
- Complex workflows requiring multiple specialized tools (e.g., SQL + Doc Intelligence + Web Search).

### Triggers:
- `AgentApplication`: Root of the multi-tool routing.
- `TurnContext`: Manages the state of the current interaction.
- `CloudAdapter`: Handles communication across channels (Teams, M365, Copilot).

---

## Skill #3: "Invisible Scaffolding" Integration

### When to Use
- Designing the UX where AI suggests Bicep infrastructure or Azure resource configurations.

### Best Practice:
- Use `azd-deployment` patterns to bundle infrastructure-as-code (Bicep) with the agent logic.
- Implement "Review -> Verify -> Deploy" cycle for all Azure resource mutations.

---

Related Skills:
- @[aks-troubleshooting-skills.md]
- @[azure-deployment-preflight]
- @[kubernetes-resource-management-skills.md]
