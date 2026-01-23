# MCP Server Configuration Guide for Antigravity

## 🎯 Fixing the "EOF" Error

The `Error: calling "initialize": EOF` error means the MCP server script exited immediately instead of staying running. 

I've created a **new MCP-compatible server**: `tools_mcp.py`

---

## 📝 Step-by-Step Configuration

### Step 1: Find Your Python Path

Open PowerShell and run:
```powershell
where python
```

Copy the FIRST path (usually something like):
- `C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe`
-OR `C:\Python311\python.exe`
- OR wherever Python is installed

### Step 2: Update MCP Config

1. Open Antigravity Settings → MCP Servers
2. Find or create "EvolutionToolHub" server
3. Update the configuration:

```json
{
  "mcpServers": {
    "EvolutionToolHub": {
      "command": "C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
      "args": [
        "D:/Hackathon phase 1 TODO App/todo_hackathon_phase1/phase2/backend/tools_mcp.py"
      ],
      "env": {}
    }
  }
}
```

**IMPORTANT**: Replace the `command` path with YOUR actual Python path from Step 1!

### Step 3: Enable Non-Workspace File Access

1. Go to Antigravity Settings → Agent → File Access
2. Toggle **ON**: "Allow Agent Non-Workspace File Access"
3. **Restart Antigravity** (critical to clear EOF cache)

### Step 4: Test the Server

Before configuring in Antigravity, test it manually:

```powershell
cd "D:\Hackathon phase 1 TODO App\todo_hackathon_phase1"

# Test the server
python phase2/backend/tools_mcp.py
```

**Expected behavior**: 
- You should see debug messages in the terminal
- The script should NOT exit immediately
- It should wait for input (press Ctrl+C to stop)

If you see errors:
- `ModuleNotFoundError`: Install missing packages
- Immediate exit: Check the script for syntax errors

### Step 5: Verify Connection

After updating the MCP config and restarting Antigravity:

1. Look for a green dot (●) next to "EvolutionToolHub" in MCP settings
2. If you see a red dot (●) or error, click to see the error message
3. Check the logs for details

### Step 6: Test in Chat

Once connected (green dot ●):

1. Open Antigravity chat
2. Ask: "What tools are available from EvolutionToolHub?"
3. Or ask: "Check the status of the Kubernetes cluster"

Expected response: The agent should list tools like `k8s_cluster_status`, `scale_deployment`, etc.

---

## 🔍 Troubleshooting Guide

### Error: "Python not found"
**Fix**: Use absolute path to python.exe in the `command` field

### Error: "ModuleNotFoundError: No module named 'kubectl'"
**Fix**: The script doesn't need external modules, it calls kubectl via shell

### Error: Still getting EOF
**Fix**: 
1. Delete the MCP server entry completely
2. Restart Antigravity
3. Re-add the server with correct paths
4. Restart Antigravity again

### Error: "Access denied" or "Permission error"
**Fix**: 
1. Run Antigravity as Administrator
2. Or move the script to a non-UAC protected location

---

## ✅ Success Indicators

You know it's working when:

- ✅ Green dot (●) in MCP Servers list
- ✅ Agent can list tools when asked
- ✅ Agent can execute kubectl commands
- ✅ No EOF errors in logs

---

## 📊 Available Tools

Once connected, the agent has access to:

1. **k8s_cluster_status** - View all pods
2. **scale_deployment** - Scale frontend/backend (0-5 replicas)
3. **analyze_pod_logs** - Get pod logs
4. **get_service_endpoints** - List all services
5. **health_check_full** - Comprehensive health check

---

## 🎯 Example Agent Commands

Try these once connected:

- "Show me the cluster status"
- "Scale the frontend to 3 replicas"
- "Get the logs from the backend pod"
- "List all service endpoints"
- "Run a full health check"

---

## 📝 Quick Reference

**MCP Server File**: `phase2/backend/tools_mcp.py`  
**Config File**: `C:\Users\Administrator\.gemini\antigravity\mcp_config.json`  
**Restart Required**: Yes, after every config change  

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-26  
**Status**: Ready for configuration
