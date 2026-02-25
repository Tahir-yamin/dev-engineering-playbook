---
description: Complete production deployment and troubleshooting workflow for AKS, Dapr, Kafka, and Helm.
---

# ☁️ ALPHA CLOUD DEPLOYMENT (SOVEREIGN INFRA)

**Unified Workflow**: `deploying-to-aks.md`, `deployment-issues.md`, `kubernetes-deployment-testing.md`, `phase5-troubleshooting.md`.

---

## 🛠️ PHASE 1: INFRASTRUCTURE INITIALIZATION

### 1. Dapr Setup
```bash
# Initialize Dapr in Kubernetes
dapr init -k --wait
# Verify
dapr status -k
```

### 2. Kafka (Strimzi) Setup
```bash
# Install Strimzi Operator
kubectl create namespace kafka
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
# Deploy Cluster
kubectl apply -f phase4/kafka/kafka-cluster.yaml -n kafka
kubectl wait kafka/kafka-cluster --for=condition=Ready --timeout=300s -n kafka
```

---

## 🚀 PHASE 2: APPLICATION ROLLOUT (HELM)

1. **Namespace & Secrets**:
   ```bash
   kubectl create namespace app-prod
   # Attach ACR
   az aks update -n <cluster> -g <rg> --attach-acr <acr-name>
   ```
2. **Components**:
   Apply Dapr components (Pub/Sub, State) to the **same** namespace as the app.
3. **Deployment**:
   ```bash
   # Use optimized-cpu values for single-node clusters
   helm upgrade --install my-app ./charts -n app-prod -f ./charts/values-optimized-cpu.yaml
   ```

---

## 🔍 PHASE 3: VERIFICATION GATES

- [ ] **Pod Readiness**: `kubectl get pods -n app-prod` (Backend should be 2/2 ready).
- [ ] **Dapr Connectivity**: `kubectl logs <pod> -c daprd` (Look for "component loaded").
- [ ] **Kafka Flow**: Test via `kafka-console-consumer` to ensure topics are receiving events.
- [ ] **Health API**: `curl localhost:8000/health` (via `kubectl exec`).

---

## 🆘 PHASE 4: THE TROUBLESHOOTING MATRIX

| Symptom | Probable Cause | Fix / Command |
| :--- | :--- | :--- |
| **ImagePullBackOff** | ACR Permission | `az aks update --attach-acr` |
| **1/2 Ready (daprd)** | Sidecar Error | `kubectl logs <pod> -c daprd` |
| **OOMKilled** | Memory limit too low | Increase `limits.memory` in Helm |
| **Pending Pods** | Resource Pressure | `kubectl describe pod` -> Reduce `requests` |
| **Kafka Not Ready** | Strimzi Operator | `kubectl logs deployment/strimzi-cluster-operator` |
| **500 Errors** | Dapr Misconfig | Add `dapr.io/log-level: debug` annotation |

---
**Standard**: Phase 5 Sovereign Logic
**Status**: Alpha Optimized
