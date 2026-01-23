# Helm Chart Deployment Guide - Evolution Todo

## 📦 What is Helm?

Helm is the "package manager" for Kubernetes - like npm for Node.js or pip for Python, but for Kubernetes applications.

**Key Benefits:**
- **Single Command Deployment**: Install entire stack with one command
- **Version Control**: Track and rollback releases
- **Templating**: DRY principle - one values.yaml instead of 10+ YAML files
- **Lifecycle Management**: Install, upgrade, rollback, uninstall
- **Agent-Friendly**: Perfect for AI-driven infrastructure management

## 🏗️ Helm Chart Structure

```
phase4/helm/todo-chatbot/
├── Chart.yaml                    # Chart metadata
├── values.yaml                   # Configuration "control panel"
└── templates/
    ├── _helpers.tpl              # Template helper functions
    ├── configmap-secret.yaml     # Namespace, ConfigMap, Secrets
    ├── database.yaml             # PostgreSQL StatefulSet
    ├── backend.yaml              # FastAPI Deployment + Service
    └── frontend.yaml             # Next.js Deployment + Service
```

## 🚀 Deployment Commands

### Install (First Time)

```powershell
# Install the chart
helm install evolution-todo ./phase4/helm/todo-chatbot `
  --namespace todo-chatbot `
  --create-namespace

# Watch the deployment
kubectl get pods -n todo-chatbot -w
```

### Upgrade (Update Existing)

```powershell
# Upgrade with new values
helm upgrade evolution-todo ./phase4/helm/todo-chatbot `
  --namespace todo-chatbot

# Or use install with --install flag (idempotent)
helm upgrade --install evolution-todo ./phase4/helm/todo-chatbot `
  --namespace todo-chatbot `
  --create-namespace
```

### Uninstall

```powershell
# Remove the entire release
helm uninstall evolution-todo --namespace todo-chatbot

# Delete the namespace
kubectl delete namespace todo-chatbot
```

## ⚙️ Customizing Deployment

### Override Values at Deploy Time

```powershell
# Scale frontend to 3 replicas
helm upgrade --install evolution-todo ./phase4/helm/todo-chatbot `
  --namespace todo-chatbot `
  --set frontend.replicaCount=3

# Change multiple values
helm upgrade --install evolution-todo ./phase4/helm/todo-chatbot `
  --namespace todo-chatbot `
  --set frontend.replicaCount=3 `
  --set backend.replicaCount=2 `
  --set database.persistence.size=2Gi
```

### Use Custom Values File

```powershell
# Create custom values file
cp phase4/helm/todo-chatbot/values.yaml my-values.yaml

# Edit my-values.yaml as needed
# Deploy with custom values
helm upgrade --install evolution-todo ./phase4/helm/todo-chatbot `
  --namespace todo-chatbot `
  --values my-values.yaml
```

## 🔄 Release Management

### List Releases

```powershell
# List all releases in namespace
helm list -n todo-chatbot

# List all releases across all namespaces
helm list --all-namespaces
```

### View Release History

```powershell
# See all revisions
helm history evolution-todo -n todo-chatbot
```

### Rollback to Previous Version

```powershell
# Rollback to previous revision
helm rollback evolution-todo -n todo-chatbot

# Rollback to specific revision
helm rollback evolution-todo 1 -n todo-chatbot
```

### View Release Status

```powershell
# Get release status
helm status evolution-todo -n todo-chatbot

# Get all values (computed)
helm get values evolution-todo -n todo-chatbot

# Get manifest (rendered templates)
helm get manifest evolution-todo -n todo-chatbot
```

## 🔍 Debugging

### Dry Run (Preview Without Installing)

```powershell
# See what would be deployed
helm install evolution-todo ./phase4/helm/todo-chatbot `
  --namespace todo-chatbot `
  --dry-run --debug
```

### Template Rendering

```powershell
# Render templates locally
helm template evolution-todo ./phase4/helm/todo-chatbot `
  --namespace todo-chatbot

# Save rendered templates to file
helm template evolution-todo ./phase4/helm/todo-chatbot `
  --namespace todo-chatbot > rendered.yaml
```

### Validate Chart

```powershell
# Lint the chart
helm lint ./phase4/helm/todo-chatbot
```

## 🎯 Common Workflows

### Workflow 1: First Deployment

```powershell
# 1. Build images in Minikube
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
docker build -t todo-frontend:v1 -f phase4/docker/frontend.Dockerfile .
docker build -t todo-backend:v1 -f phase4/docker/backend.Dockerfile .

# 2. Install with Helm
helm install evolution-todo ./phase4/helm/todo-chatbot `
  --namespace todo-chatbot `
  --create-namespace

# 3. Wait for pods
kubectl wait --for=condition=ready pod -l app=postgres -n todo-chatbot --timeout=120s

# 4. Initialize database
kubectl port-forward pod/postgres-0 5432:5432 -n todo-chatbot
# In another terminal: cd phase2/frontend && npx prisma db push

# 5. Access application
minikube service frontend-service -n todo-chatbot
```

### Workflow 2: Update Frontend to v2

```powershell
# 1. Build new image
docker build -t todo-frontend:v2 -f phase4/docker/frontend.Dockerfile .

# 2. Upgrade with new tag
helm upgrade evolution-todo ./phase4/helm/todo-chatbot `
  --namespace todo-chatbot `
  --set frontend.image.tag=v2

# 3. Watch rollout
kubectl rollout status deployment/evolution-todo-frontend -n todo-chatbot
```

### Workflow 3: Disaster Recovery

```powershell
# Something broke after upgrade
# Check history
helm history evolution-todo -n todo-chatbot

# Example output:
# REVISION  STATUS      CHART              DESCRIPTION
# 1         superseded  todo-chatbot-1.0.0  Install complete
# 2         deployed    todo-chatbot-1.0.0  Upgrade complete

# Rollback to revision 1
helm rollback evolution-todo 1 -n todo-chatbot

# Verify
kubectl get pods -n todo-chatbot
```

### Workflow 4: Scale for High Load

```powershell
# Scale frontend and backend
helm upgrade evolution-todo ./phase4/helm/todo-chatbot `
  --namespace todo-chatbot `
  --set frontend.replicaCount=5 `
  --set backend.replicaCount=3 `
  --reuse-values

# Verify
kubectl get deployments -n todo-chatbot
```

## 🧠 Agent Integration

The Antigravity Agent can now manage releases via Helm tools:

### Agent Workflow: Deploy New Version

```
User: "Deploy frontend version 2"

Agent:
1. Calls helm_upgrade(release="evolution-todo", set=["frontend.image.tag=v2"])
2. Calls k8s_cluster_status() to monitor rollout
3. Reports: "✅ Frontend v2 deployed, 2/2 pods healthy"
```

### Agent Workflow: Auto-Rollback on Failure

```
User: "The app is broken after the upgrade!"

Agent:
1. Calls helm_history(release="evolution-todo")
2. Identifies last working revision (e.g., revision 3)
3. Asks: "Shall I rollback to revision 3?"
4. [User confirms]
5. Calls helm_rollback(release="evolution-todo", revision=3)
6. Verifies: k8s_cluster_status()
7. Reports: "✅ Rolled back to v1, all pods healthy"
```

## 📊 Values.yaml Sections

| Section | Purpose | Common Changes |
|---------|---------|----------------|
| `database` | PostgreSQL config | Storage size, credentials |
| `backend` | FastAPI config | Replicas, image tag |
| `frontend` | Next.js config | Replicas, image tag, NodePort |
| `config` | ConfigMap | API URLs, environment |
| `secrets` | Sensitive data | Auth secrets, API keys |
| `autoscaling` | HPA settings | Min/max replicas, CPU target |

## ⚠️ Important Notes

1. **Image Pull Policy**: Default is `Never` for Minikube. Change to `IfNotPresent` for production.

2. **Secrets**: Default secrets are base64-encoded placeholders. **NEVER use these in production.**

3. **Database Password**: Stored in plain values.yaml. Use external secret management in production (Vault, AWS Secrets Manager).

4. **NodePort**: Fixed to 30000 for local access. Use Ingress for production.

5. **Persistent Storage**: Default storage class is used. Specify `storageClass` for production.

## 🔐 Production Considerations

Before deploying to production:

1. **External Secrets**: Use Sealed Secrets, External Secrets Operator, or cloud provider secrets

2. **Ingress**: Replace NodePort with Ingress + cert-manager for HTTPS

3. **Resource Limits**: Adjust based on actual load testing

4. **Monitoring**: Enable Prometheus ServiceMonitor

5. **Backups**: Implement database backup strategy

6. **High Availability**: Increase replicas for all services

## 📚 References

- [Helm Documentation](https://helm.sh/docs/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Helm Template Guide](https://helm.sh/docs/chart_template_guide/)

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-26
