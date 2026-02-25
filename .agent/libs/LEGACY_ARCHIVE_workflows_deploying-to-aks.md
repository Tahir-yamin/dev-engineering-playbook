---
description: Complete workflow for deploying applications to Azure Kubernetes Service with Dapr and Kafka
---

# Deploying to AKS with Dapr and Kafka

## When to Use
- Deploying Phase 5 todo app to production
- Setting up event-driven architecture on AKS
- Need complete AKS + Dapr + Kafka deployment

---

## Prerequisites

- [ ] Azure subscription with AKS cluster created
- [ ] `kubectl` configured to access cluster
- [ ] Docker images pushed to ACR
- [ ] Helm installed locally

---

## Step 1: Install Dapr on AKS

```bash
# Install Dapr CLI
powershell -Command "iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex"

// turbo
# Initialize Dapr in Kubernetes
dapr init -k --wait

// turbo
# Verify Dapr installation
dapr status -k
kubectl get pods -n dapr-system
```

**Expected**: 5 dapr-system pods running (dashboard, operator, placement, sentry, sidecar-injector)

---

## Step 2: Deploy Kafka with Strimzi

```bash
// turbo
# Create namespace
kubectl create namespace kafka

// turbo
# Install Strimzi operator
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

// turbo
# Wait for operator to be ready
kubectl wait deployment/strimzi-cluster-operator --for=condition=Available --timeout=300s -n kafka

// turbo
# Deploy Kafka cluster (from phase4/kafka/kafka-cluster.yaml)
kubectl apply -f phase4/kafka/kafka-cluster.yaml -n kafka

// turbo
# Wait for Kafka to be ready (takes 2-3 minutes)
kubectl wait kafka/kafka-cluster --for=condition=Ready --timeout=300s -n kafka
```

---

## Step 3: Create Kafka Topics

```bash
// turbo
# Apply topic configurations
kubectl apply -f phase4/kafka/topics/ -n kafka

// turbo
# Verify topics created
kubectl get kafkatopics -n kafka
```

Expected topics:
- `task-events`
- `task-updates`  
- `reminders`

---

## Step 4: Create Application Namespace

```bash
// turbo
# Create namespace
kubectl create namespace todo-chatbot

// turbo
# Create image pull secret for ACR
kubectl create secret docker-registry acr-secret \
  --docker-server=<your-acr>.azurecr.io \
  --docker-username=<acr-username> \
  --docker-password=<acr-password> \
  -n todo-chatbot
```

---

## Step 5: Apply Dapr Components

```bash
// turbo
# Apply Kafka Pub/Sub component
kubectl apply -f phase4/dapr-components/kafka-pubsub.yaml -n todo-chatbot

// turbo
# Verify component
kubectl get component -n todo-chatbot
```

---

## Step 6: Deploy Application with Helm

```bash
# For SINGLE-NODE cluster (use optimized values)
helm upgrade --install todo-chatbot ./phase4/helm/todo-chatbot \
  -n todo-chatbot \
  -f ./phase4/helm/todo-chatbot/values-optimized-cpu.yaml \
  --set backend.image.tag=<your-tag> \
  --set frontend.image.tag=<your-tag>

# For MULTI-NODE cluster (use standard values)
helm upgrade --install todo-chatbot ./phase4/helm/todo-chatbot \
  -n todo-chatbot \
  --set backend.image.tag=<your-tag> \
  --set frontend.image.tag=<your-tag>
```

---

## Step 7: Verify Deployment

```bash
// turbo
# Check all pods
kubectl get pods -n todo-chatbot

// turbo
# Check services
kubectl get svc -n todo-chatbot

// turbo
# Check backend health
kubectl exec -it deployment/todo-chatbot-backend -n todo-chatbot -c backend -- curl localhost:8000/health
```

**Expected**:
```
✅ postgres-0: 1/1 Running
✅ backend: 2/2 Running (app + daprd sidecar)
✅ frontend: 1/1 Running
```

---

## Step 8: Test AI Chat

```bash
# Port-forward to backend
kubectl port-forward -n todo-chatbot deployment/todo-chatbot-backend 8001:8000

# In another terminal, test chat endpoint
curl -X POST http://localhost:8001/api/test-user/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show all tasks"}'
```

**Expected**: JSON response with AI response and no errors

---

## Step 9: Access Frontend

```bash
// turbo
# Get frontend external IP (if LoadBalancer)
kubectl get svc todo-chatbot-frontend -n todo-chatbot

# OR port-forward
kubectl port-forward -n todo-chatbot deployment/todo-chatbot-frontend 3000:3000
```

Open browser: `http://localhost:3000` or external IP

---

## Troubleshooting

### Pods Stuck in Pending

**Check**:
```bash
kubectl describe pod <pod-name> -n todo-chatbot | grep Events -A 10
```

**Solution**: Use `values-optimized-cpu.yaml` for single-node clusters

---

### Dapr Sidecar 1/2 Ready

**Check daprd logs**:
```bash
kubectl logs <pod-name> -c daprd -n todo-chatbot
```

**Common fix**: Verify Dapr annotations in deployment

---

### Can't Connect to Kafka

**Verify Kafka is ready**:
```bash
kubectl get kafka -n kafka
```

**Check component**:
```bash
kubectl describe component kafka-pubsub -n todo-chatbot
```

---

## Cleanup (Optional)

```bash
# Delete application
helm uninstall todo-chatbot -n todo-chatbot

# Delete Kafka
kubectl delete -f phase4/kafka/ -n kafka
kubectl delete namespace kafka

# Uninstall Dapr
dapr uninstall -k
```

---

**Related Skills**:  
- @.claude/dapr-configuration-skills.md
- @.claude/kubernetes-resource-optimization-skills.md
- @.agent/workflows/github-actions-deployment-verification.md
