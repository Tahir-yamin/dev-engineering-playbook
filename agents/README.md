# Evolution Agent - Complete Architecture

## 📋 Overview

This directory contains the complete agentic architecture for the "Evolution of Todo" project, following the **agentskills** specification and **MCP (Model Context Protocol)**.

## 🏗️ Architecture Components

### 1. Backend Tool Hub (`phase2/backend/tools.py`)
The central execution engine that implements all agent capabilities:

- **7 Tools Total**: Cluster management, debugging, database checks
- **Async Execution**: All tools run asynchronously for performance
- **Safety Constraints**: Built-in limits (e.g., max 5 replicas)
- **Error Handling**: Comprehensive error handling with timestamps

### 2. Skills Manifest (`skills.json`)
The "contract" between the agent and execution environment:

- **Tool Definitions**: Name, parameters, descriptions
- **Risk Levels**: safe, moderate, destructive
- **Workflow Patterns**: Pre-defined automation sequences
- **Safety Rules**: Hard constraints on agent behavior

### 3. MCP API Endpoints (`phase2/backend/main.py`)
FastAPI endpoints that expose the tools:

- `GET /agent/tools` - Discovery endpoint (returns manifest)
- `POST /agent/execute` - Execution endpoint (runs tools)
- `GET /agent/health` - Health check for agent interface

### 4. Antigravity Instructions (`antigravity-instructions.md`)
Custom instructions for the Antigravity agent:

- **Persona**: Senior DevOps Architect
- **Workflow**: Think-Tool-Verify pattern
- **Examples**: Concrete usage scenarios
- **Safety**: Explicit rules and constraints

## 🚀 Usage

### For Developers

1. **Start the backend** with MCP endpoints:
   ```bash
   cd phase2/backend
   python main.py
   ```

2. **Discover available tools**:
   ```bash
   curl http://localhost:8000/agent/tools
   ```

3. **Execute a tool**:
   ```bash
   curl -X POST http://localhost:8000/agent/execute \
     -H "Content-Type: application/json" \
     -d '{"name": "k8s_cluster_status", "arguments": {}}'
   ```

### For Agents (Antigravity/Claude/etc.)

Load the `antigravity-instructions.md` as custom instructions, then interact naturally:

**User**: "Are all my pods healthy?"

**Agent**:
```
<thought>
I'll check the cluster status to see pod health.
</thought>

[Calls k8s_cluster_status via MCP]

✅ All 3 pods are running:
- frontend-xxx: Ready (1/1)
- backend-xxx: Ready (1/1)  
- postgres-xxx: Ready (1/1)
```

## 🔄 Workflow Patterns

### 1. Self-Healing Loop
```
Trigger: Pod crash detected
→ k8s_cluster_status (confirm crash)
→ analyze_pod_logs (find error)
→ [User confirms fix]
→ restart_deployment
```

### 2. Performance Debug
```
Trigger: User reports slowness
→ health_check_full (overall status)
→ db_query_stats (check latency)
→ k8s_cluster_status (check pods)
→ Provide diagnosis
```

### 3. Scale on Demand
```
Trigger: Need more capacity
→ k8s_cluster_status (current state)
→ scale_deployment (increase replicas)
→ Verify success
```

## 🛡️ Safety Features

1. **Replica Limit**: Max 5 replicas enforced at tool level
2. **Confirmation Required**: Destructive actions require user approval
3. **Logging**: All executions logged with timestamps
4. **Error Handling**: Graceful failures with detailed messages

## 📊 Tool Inventory

| Tool | Category | Risk | Description |
|------|----------|------|-------------|
| `k8s_cluster_status` | Cluster | Safe | View pod status |
| `scale_deployment` | Cluster | Moderate | Scale replicas (0-5) |
| `restart_deployment` | Cluster | Moderate | Rolling restart |
| `analyze_pod_logs` | Debug | Safe | Retrieve logs |
| `db_query_stats` | Database | Safe | Check DB health |
| `get_service_endpoints` | Network | Safe | List services |
| `health_check_full` | Monitor | Safe | Full health check |

## 🎯 Next Steps

### Phase 4A: Kubernetes Setup
1. Install Minikube
2. Deploy todo-chatbot namespace
3. Verify MCP endpoints are accessible from within cluster

### Phase 4B: kubectl-ai Integration
1. Install kubectl-ai in Minikube
2. Configure natural language access
3. Test agent-driven kubectl commands

### Phase 4C: Advanced Workflows
1. Implement automatic crash recovery
2. Add performance monitoring triggers
3. Create deployment approval workflows

## 📝 References

- **agentskills spec**: https://github.com/anthropics/skills
- **MCP Protocol**: https://modelcontextprotocol.io
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

**Version**: 1.0.0  
**Author**: Evolution Team  
**Last Updated**: 2025-12-26
