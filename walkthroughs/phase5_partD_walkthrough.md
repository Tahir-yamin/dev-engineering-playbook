# Phase 5 Part D: GitHub Actions CI/CD - Walkthrough

**Completed**: January 5, 2026  
**Duration**: ~15 minutes

---

## What Was Implemented

### GitHub Actions Workflow

**File**: [deploy-aks.yml](file:///d:/Hackathon%20phase%201%20TODO%20App/todo_hackathon_phase1/.github/workflows/deploy-aks.yml)

A comprehensive CI/CD pipeline with 4 jobs:

| Job | Purpose |
|-----|---------|
| **build** | Build and push Docker images to Azure Container Registry |
| **deploy-infra** | Install Strimzi Kafka and Dapr on AKS |
| **deploy-app** | Deploy with Helm chart |
| **verify** | Health checks and endpoint verification |

---

## Pipeline Features

### 1. Smart Triggering

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'phase2/**'
      - 'phase4/**'
  workflow_dispatch:
    inputs:
      deploy_kafka: {type: choice, options: ['true', 'false']}
      deploy_dapr: {type: choice, options: ['true', 'false']}
```

- Triggers on code changes to relevant paths
- Manual trigger with optional Kafka/Dapr deployment

### 2. Image Tagging

```yaml
TAG=$(date +%Y%m%d%H%M%S)-${GITHUB_SHA::7}
```

Unique tags combine timestamp + commit SHA for traceability.

### 3. Parallel Image Builds

```yaml
- name: Build and push Backend
- name: Build and push Frontend
- name: Build and push Notification Service
```

All three services built and pushed in parallel with caching.

### 4. Infrastructure Deployment

```yaml
- name: Deploy Strimzi Operator
  run: kubectl apply -f https://strimzi.io/install/latest

- name: Install Dapr on AKS
  run: dapr init -k --wait
```

---

## Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `AZURE_CREDENTIALS` | Azure Service Principal JSON |
| `ACR_LOGIN_SERVER` | yourregistry.azurecr.io |
| `ACR_USERNAME` | ACR admin username |
| `ACR_PASSWORD` | ACR admin password |
| `AKS_CLUSTER_NAME` | todo-aks-cluster |
| `AKS_RESOURCE_GROUP` | todo-rg |

---

## Lessons Learned

### ✅ What Worked Well

1. **Workflow dispatch inputs**: Allows selective infrastructure deployment
2. **Conditional job execution**: `if: github.event.inputs.deploy_kafka == 'true'`
3. **Job dependencies with `needs:`**: Proper ordering of deployment stages

### 💡 Key Insights

1. **Always use `--wait`**: Helm and Dapr need time to stabilize
2. **Separate infra from app**: Better control and debugging
3. **Use outputs**: Pass image tags between jobs

---

## Skills Upgraded

| Skill | Level | What Was Learned |
|-------|-------|------------------|
| GitHub Actions | ⬆️ Advanced | Multi-job workflows, outputs |
| Azure AKS | ⬆️ Intermediate | CLI deployment patterns |
| Helm | ⬆️ Advanced | Dynamic value overrides |

---

## Complete Phase 5 Summary

| Part | Status | Key Deliverables |
|------|--------|------------------|
| A | ✅ | Database schema, events.py, Dapr components, Kafka cluster |
| B | ✅ | MCP tools integration, set_reminder tool, advanced filters |
| C | ✅ | Notification service (Dapr consumer), Docker, K8s manifest |
| D | ✅ | GitHub Actions CI/CD for Azure AKS |

---

## Files Created This Session

| File | Purpose |
|------|---------|
| `phase2/backend/models.py` | Updated with Phase 5 fields |
| `phase2/backend/events.py` | Dapr Pub/Sub event publishing |
| `phase2/backend/mcp_server.py` | Updated with event integration |
| `phase4/dapr-components/*.yaml` | 3 Dapr component configs |
| `phase4/kubernetes/kafka-cluster.yaml` | Strimzi Kafka cluster |
| `phase4/kubernetes/notification-service.yaml` | K8s deployment |
| `phase4/services/notification-service/*` | Consumer microservice |
| `.github/workflows/deploy-aks.yml` | CI/CD pipeline |
