---
description: Troubleshooting workflow for Phase V deployment issues (Kafka, Dapr, AKS)
---

# Phase V Deployment Troubleshooting

This workflow covers common issues with Kafka, Dapr, and Azure AKS deployment.

## Prerequisites

- [ ] Dapr is installed: `dapr version`
- [ ] kubectl is configured: `kubectl cluster-info`
- [ ] Helm is installed: `helm version`

---

## Dapr Issues

### 1. Sidecar Not Injecting

**Symptoms**: Pod runs but no Dapr sidecar container.

**Checks**:
// turbo
```bash
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'
```

**Fix**:
1. Verify annotation: `dapr.io/enabled: "true"`
2. Verify app-id: `dapr.io/app-id: "backend"`
3. Verify app-port: `dapr.io/app-port: "8000"`
4. Restart deployment: `kubectl rollout restart deployment backend`

### 2. Component Not Found

**Symptoms**: Error `component X cannot be found`

**Checks**:
// turbo
```bash
kubectl get components -A
```

**Fix**:
1. Check component namespace matches app namespace
2. Verify YAML syntax
3. Check component scoping (if using `scopes:` in component YAML)

### 3. 500 Errors from Dapr

**Fix**:
1. Enable debug logging: Add `dapr.io/log-level: debug` annotation
2. Check sidecar logs: `kubectl logs <pod> -c daprd`

---

## Kafka/Strimzi Issues

### 1. Cluster Operator Stuck

**Symptoms**: Kafka pods don't appear, operator shows "reconciliation in progress"

**Checks**:
// turbo
```bash
kubectl get strimzipodsets -n kafka
kubectl logs -n kafka deployment/strimzi-cluster-operator --tail=50
```

**Fix**:
1. Restart operator: `kubectl rollout restart deployment strimzi-cluster-operator -n kafka`
2. Check K8s version compatibility (Strimzi 0.39+ for K8s 1.33+)

### 2. Topic Not Created

**Symptoms**: KafkaTopic resource created but topic doesn't exist in Kafka

**Checks**:
// turbo
```bash
kubectl get kafkatopics -n kafka
kubectl logs -n kafka deployment/todo-kafka-entity-operator --tail=50
```

**Fix**:
1. Verify Topic Operator is running
2. Check ZooKeeper connectivity
3. Verify topic name doesn't conflict

### 3. Client Can't Connect

**Symptoms**: Producer/consumer fails to connect to brokers

**Checks**:
// turbo
```bash
kubectl get svc -n kafka
kubectl exec -it todo-kafka-0 -n kafka -- bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

**Fix**:
1. Check listener configuration
2. Verify network policies don't block traffic
3. Check service name and port

---

## Azure AKS Issues

### 1. ACR Pull Fails

**Symptoms**: `ImagePullBackOff` or `ErrImagePull`

**Checks**:
// turbo
```bash
kubectl describe pod <pod-name>
```

**Fix**:
```bash
az aks update -n todo-aks-cluster -g todo-hackathon-rg --attach-acr todohackathonacr
```

### 2. Pod OOMKilled

**Symptoms**: Pod restarts with reason `OOMKilled`

**Fix**:
1. Increase memory limits in Helm values
2. Check Dapr sidecar memory limits: `dapr.io/sidecar-memory-limit`

### 3. Ingress Not Working

**Symptoms**: External IP is `<pending>` or requests timeout

**Checks**:
// turbo
```bash
kubectl get ingress -A
kubectl get svc -n ingress-nginx
```

**Fix**:
1. Install NGINX Ingress: `helm install nginx-ingress ingress-nginx/ingress-nginx`
2. Check ingress class in Ingress resource
3. Verify DNS pointing to Load Balancer IP

---

## GitHub Actions CI/CD Issues

### 1. Azure Login Fails

**Symptoms**: `AZURE_CREDENTIALS` error

**Fix**:
1. Verify secret is set in GitHub
2. Check service principal has correct permissions
3. Regenerate credentials: `az ad sp create-for-rbac --sdk-auth`

### 2. Helm Deploy Fails

**Symptoms**: `Release not found` or values not applied

**Fix**:
1. Use `helm upgrade --install` instead of just `helm install`
2. Verify values.yaml path is correct
3. Check kubectl context is set to correct cluster

---

## Related Workflows

- [Kubernetes Deployment Testing](./kubernetes-deployment-testing.md)
- [Security Audit](./security-audit.md)
- [Docker Container Problems](./docker-container-problems.md)
