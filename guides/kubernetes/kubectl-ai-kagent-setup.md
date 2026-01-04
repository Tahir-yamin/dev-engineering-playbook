# kubectl-ai and kagent Setup Guide (Optional Enhancements)

**Purpose**: Install and configure AI-assisted Kubernetes tools for Phase IV bonus credibility  
**Time Required**: 2-4 hours total  
**Bonus Value**: Demonstrates AI

Ops mastery, enhances presentation

---

## Overview

**kubectl-ai** and **kagent** are AI-powered tools that allow natural language interaction with Kubernetes clusters. While not strictly required for Phase IV, they demonstrate advanced AIOps capabilities and can earn bonus points.

**Benefits**:
- Natural language cluster management
- Faster troubleshooting
- Impressive demo for judges
- Real-world AIOps experience

---

## Part 1: kubectl-ai Installation & Setup

### What is kubectl-ai?

kubectl-ai is a kubectl plugin that translates natural language commands into Kubernetes operations using AI (OpenAI GPT models).

**Example Usage**:
```bash
kubectl-ai "show me all pods that are not running in todo-chatbot namespace"
kubectl-ai "scale the frontend deployment to 3 replicas"
kubectl-ai "why are my pods crashing?"
```

---

### Installation (Windows - PowerShell)

#### Prerequisites
- kubectl installed and working
- OpenAI API key (can use existing from project)
- Go 1.19+ (for building from source)

#### Method 1: Install via krew (Recommended)

```powershell
# Install krew (kubectl plugin manager)
# Visit: https://krew.sigs.k8s.io/docs/user-guide/setup/install/

# After krew is installed:
kubectl krew install kubectl-ai
```

#### Method 2: Build from Source

```powershell
# Clone repository
git clone https://github.com/sozercan/kubectl-ai.git
cd kubectl-ai

# Build
go build -o kubectl-ai cmd/kubectl-ai/kubectl-ai.go

# Move to PATH
mv kubectl-ai $env:USERPROFILE\bin\kubectl-ai.exe
# OR add current directory to PATH
```

---

### Configuration

```powershell
# Set OpenAI API key
$env:OPENAI_API_KEY = "your-openai-api-key-here"

# Optional: Set preferred model
$env:OPENAI_DEPLOYMENT_NAME = "gpt-4"

# Test installation
kubectl ai "list all namespaces"
```

---

### Usage Examples for Todo App

#### Cluster Inspection

```powershell
# Basic status
kubectl ai "show me all resources in todo-chatbot namespace"

# Pod health
kubectl ai "which pods are not healthy in todo-chatbot"

# Resource usage
kubectl ai "show memory and CPU usage for frontend pods"
```

**Expected Output**:
```
Analyzing cluster...

Here's what I found:
- frontend pod: Running (2/2 ready)
- backend pod: Running (1/1 ready)
- All pods are healthy!

Memory usage:
- frontend-xyz: 128Mi / 256Mi (50%)
- backend-abc: 64Mi / 128Mi (50%)
```

#### Troubleshooting

```powershell
# Diagnose issues
kubectl ai "why is the backend pod crashing?"

# Check logs
kubectl ai "show me the last 50 lines of logs from the backend pod"

# Check events
kubectl ai "show me recent events that might indicate problems"
```

#### Deployment Operations

```powershell
# Scale deployment
kubectl ai "scale frontend to 3 replicas"

# Restart deployment
kubectl ai "restart the backend deployment"

# Update image
kubectl ai "update backend deployment to use image todo-backend:v2"
```

#### Configuration Inspection

```powershell
# Check ConfigMap
kubectl ai "show me all environment variables in todo-app-config"

# Check Secrets
kubectl ai "list all secrets in the todo-chatbot namespace"

# Check Services
kubectl ai "what ports are exposed by the frontend service?"
```

---

### Demo Script for Judges

**Scenario**: Live demonstration of AI-assisted Kubernetes management

```powershell
# 1. Show cluster status
kubectl ai "give me an overview of the todo-chatbot namespace"

# 2. Demonstrate troubleshooting
kubectl ai "are there any issues with the deployments?"

# 3. Show scaling
kubectl ai "how many replicas is the frontend running?"
kubectl ai "scale frontend to 3 replicas"
kubectl ai "verify the frontend now has 3 pods"

# 4. Log inspection
kubectl ai "show me if there are any errors in the backend logs"

# 5. Resource check
kubectl ai "what resources are the pods using?"
```

**Time**: 3-5 minutes of demo

---

## Part 2: kagent Installation & Setup

### What is kagent?

kagent (Kubernetes Agent) is an AI-powered Kubernetes co-pilot that provides intelligent cluster management, analysis, and recommendations.

**Features**:
- Cluster health analysis
- Performance optimization suggestions
- Security vulnerability scanning
- Resource utilization insights

---

### Installation (Windows - PowerShell)

#### Method 1: Install via Binary

```powershell
# Download latest release
$KAGENT_VERSION = "v0.3.0"  # Check latest version on GitHub
$url = "https://github.com/kubetoolsio/kagent/releases/download/$KAGENT_VERSION/kagent-windows-amd64.exe"

# Download
Invoke-WebRequest -Uri $url -OutFile "$env:USERPROFILE\bin\kagent.exe"

# Add to PATH if needed
$env:Path += ";$env:USERPROFILE\bin"
```

#### Method 2: Build from Source

```powershell
# Clone repository
git clone https://github.com/kubetoolsio/kagent.git
cd kagent

# Build
go build -o kagent.exe

# Move to PATH
mv kagent.exe $env:USERPROFILE\bin\
```

---

### Configuration

```powershell
# Initialize kagent
kagent init

# Configure OpenAI API
kagent config set openai-api-key "your-openai-api-key"

# Set default namespace
kagent config set namespace todo-chatbot

# Verify configuration
kagent config list
```

---

### Usage Examples for Todo App

#### Cluster Analysis

```powershell
# Comprehensive health check
kagent analyze cluster

# Deployment analysis
kagent analyze deployment todo-app-frontend

# Resource optimization
kagent optimize resources
```

**Expected Output**:
```
╔════════════════════════════════════════════════╗
║     Cluster Health Analysis                    ║
╠════════════════════════════════════════════════╣
║ Namespace: todo-chatbot                        ║
║ Deployments: 2 (All Healthy)                   ║
║ Pods: 3 (All Running)                          ║
║ Services: 2 (All Endpoints Ready)              ║
╚════════════════════════════════════════════════╝

Recommendations:
✓ All services healthy
⚠ Frontend could benefit from HPA (Horizontal Pod Autoscaler)
ℹ Consider adding resource limits to backend
```

#### Security Scanning

```powershell
# Security scan
kagent security scan

# Check for vulnerabilities
kagent security vulnerabilities

# Compliance check
kagent security compliance
```

#### Performance Optimization

```powershell
# Resource usage analysis
kagent performance resources

# Bottleneck detection
kagent performance bottlenecks

# Optimization suggestions
kagent performance optimize
```

---

### Demo Script for Judges

**Scenario**: Advanced cluster management with AI insights

```powershell
# 1. Cluster health overview
kagent analyze cluster --verbose

# 2. Security audit
kagent security scan --namespace todo-chatbot

# 3. Performance insights
kagent performance resources

# 4. Get recommendations
kagent recommend improvements

# 5. Troubleshoot if needed
kagent troubleshoot pods
```

**Time**: 5-7 minutes of demo

---

## Combined kubectl-ai + kagent Demo Flow

### 30-Second Power Demo

```powershell
# Quick status
kubectl ai "show me the health of todo-chatbot"

# Deep analysis
kagent analyze cluster

# Make a change
kubectl ai "scale frontend to 3 replicas"

# Verify with AI
kagent analyze deployment todo-app-frontend
```

---

## Integration with Phase IV Project

### Update workflows to include AI tools

**File**: `.agent/workflows/kubernetes-deployment-testing.md`

Add section:
```markdown
### AI-Assisted Troubleshooting

#### Using kubectl-ai
```bash
# Quick diagnosis
kubectl ai "diagnose issues in todo-chatbot namespace"
```

#### Using kagent
```bash
# Comprehensive analysis
kagent analyze deployment todo-app-backend
```
```

---

### Update README.md

Add to technologies section:
```markdown
### AIOps Tools (Phase IV Enhancement)
- **kubectl-ai**: Natural language Kubernetes operations
- **kagent**: AI-powered cluster analysis and optimization
```

---

### Update MANUAL-OPERATIONS-GUIDE.md

Add new section:
```markdown
## Part 6: AI-Assisted Operations (Optional)

### Using kubectl-ai for Natural Language Commands

Instead of remembering kubectl syntax, use natural language:

```bash
kubectl ai "show me all pods"
kubectl ai "scale frontend to 3 replicas"
kubectl ai "check backend logs for errors"
```

### Using kagent for Cluster Analysis

Get AI-powered insights:

```bash
kagent analyze cluster
kagent security scan
kagent recommend improvements
```
```

---

## Troubleshooting

### kubectl-ai Issues

#### Issue: "OpenAI API key not found"
**Fix**:
```powershell
$env:OPENAI_API_KEY = "your-key-here"
# Make persistent:
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'your-key-here', 'User')
```

#### Issue: "kubectl-ai command not found"
**Fix**:
```powershell
# Check if in PATH
where.exe kubectl-ai

# If not, add to PATH or use full path
C:\path\to\kubectl-ai.exe "your command"
```

### kagent Issues

#### Issue: "Cannot connect to cluster"
**Fix**:
```powershell
# Verify kubectl works first
kubectl get nodes

# Then try kagent
kagent config set kubeconfig $env:USERPROFILE\.kube\config
```

---

## Documentation for Submission

### Add to CLAUDE.md

```markdown
### AI-Assisted Operations

**kubectl-ai Usage**:
- Natural language cluster management
- Faster troubleshooting
- Demo: "kubectl ai 'scale frontend to 3 replicas'"

**kagent Usage**:
- Comprehensive cluster analysis
- Security scanning
- Performance optimization
- Demo: "kagent analyze cluster"
```

### Add to Demo Video Script

```
[30-45 seconds mark]
Narrator: "We've also integrated AI-powered operations tools"
[Show kubectl-ai command]
kubectl ai "show me the health of todo-chatbot"
[Show output]
[Show kagent command]
kagent analyze cluster
[Show analysis output]
Narrator: "This demonstrates our mastery of cutting-edge AIOps"
```

---

## Bonus Points Justification

### How This Earns Bonus Points

**Reusable Intelligence** (+200 potential):
- kubectl-ai and kagent are reusable across all K8s projects
- Document patterns in `.agent/workflows/`
- Share prompt examples

**Advanced AIOps Demonstration**:
- Shows understanding of modern DevOps practices
- Demonstrates AI integration beyond just chatbot
- Impresses judges with cutting-edge tools

---

## Time Investment vs. Reward

| Task | Time | Reward |
|------|------|---------|
| kubectl-ai install | 30 min | Demo credibility |
| kubectl-ai integration | 1 hour | Workflow enhancement |
| kagent install | 30 min | Advanced analysis |
| kagent integration | 1 hour | Security/performance insights |
| Documentation updates | 1 hour | Completeness |
| **TOTAL** | **4 hours** | **Significant bonus impression** |

---

## Alternative: If Time is Limited

### Minimal Implementation (1 hour)

1. **Install kubectl-ai only** (30 min)
2. **Run 3 demo commands** (10 min)
3. **Add to README** (10 min)
4. **Mention in demo video** (10 min)

**Result**: Still demonstrates AIOps awareness, lower time investment

---

## Conclusion

kubectl-ai and kagent are **optional enhancements** that can significantly improve your Phase IV submission:

✅ **Pros**:
- Impressive demo material
- Real-world AIOps skills
- Bonus points potential
- Future-proof learning

⚠️ **Cons**:
- Additional setup time
- Extra dependencies
- Not required for core points

**Recommendation**: 
- If you have **4+ hours**: Full implementation (both tools)
- If you have **2 hours**: kubectl-ai only
- If you have **< 1 hour**: Skip (focus on required documentation)

---

**Status**: Optional Enhancement Guide  
**Priority**: Medium (if time permits)  
**Updated**: December 30, 2025
