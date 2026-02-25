# INFRASTRUCTURE SPECIFICATION: MINIKUBE

**Specification**: K8s-Local-Standard-v1  
**Provider**: Minikube (Docker Driver)  
**Protocol**: AgentSkills + MCP

---

## 🎯 Cluster Parameters

### Core Configuration
- **Provider**: Minikube
- **Driver**: Docker
- **Kubernetes Version**: v1.28.3
- **CPUs**: 4 cores
- **Memory**: 4096MB (4GB)

### Enabled Features
- **Ingress Controller**: Nginx (via `minikube addons`)
- **Metrics Server**: For resource monitoring (`kubectl top`)
- **Dashboard**: Visual cluster management

---

## 🔌 Required Addons

### 1. Ingress (Nginx)
**Purpose**: HTTP/HTTPS routing for external access

**Namespace**: `ingress-nginx`

**Key Components**:
- `ingress-nginx-controller` - Main routing controller
- `ingress-nginx-admission` - Webhook for validation

**Verification**:
```bash
kubectl get pods -n ingress-nginx
# Should show: ingress-nginx-controller-xxx Running
```

**Agent Skill**: `check_ingress_status`
```
If Frontend shows "Connection Refused":
1. Check: kubectl get pods -n ingress-nginx
2. If not running: minikube addons enable ingress
3. Wait: kubectl wait --for=condition=ready pod -l app.kubernetes.io/component=controller -n ingress-nginx
4. Verify: Check pod is Running
```

---

### 2. Metrics Server
**Purpose**: Resource usage monitoring (CPU, RAM)

**Namespace**: `kube-system`

**Key Components**:
- `metrics-server` - Aggregates resource metrics

**Verification**:
```bash
kubectl top nodes
# Should show: CPU% and Memory% usage
```

**Agent Skill**: `monitor_resource_usage`
```
To check cluster health:
1. Run: kubectl top nodes
2. Run: kubectl top pods -n todo-chatbot
3. Alert if CPU > 80% or Memory > 80%
```

---

### 3. Dashboard
**Purpose**: Visual Kubernetes management UI

**Namespace**: `kubernetes-dashboard`

**Access**:
```bash
minikube dashboard
# Opens browser with cluster visualization
```

**Agent Skill**: `provide_dashboard_access`
```
If user asks "Show me the cluster":
1. Execute: minikube dashboard
2. Provide URL for browser access
```

---

## 🔄 Agent Workflow Patterns

### Workflow 1: Infrastructure Health Check

**Trigger**: User reports connectivity issues

**Agent Steps**:
```
<thought>
User can't access the application. I should check the infrastructure layer.
</thought>

1. Check Minikube status:
   minikube status
   
2. Check Ingress controller:
   kubectl get pods -n ingress-nginx
   
3. Check Metrics server:
   kubectl get deployment metrics-server -n kube-system
   
4. If any fail:
   - Ingress: minikube addons enable ingress
   - Metrics: minikube addons enable metrics-server
   
5. Verify recovery:
   kubectl wait --for=condition=ready pod -l app=<component>
```

---

### Workflow 2: Resource Monitoring

**Trigger**: User reports slow performance

**Agent Steps**:
```
<thought>
Slow performance could be resource exhaustion. I'll check metrics.
</thought>

1. Check node resources:
   kubectl top nodes
   
2. Check pod resources:
   kubectl top pods -n todo-chatbot
   
3. If resources high (>80%):
   - Suggest scaling down non-critical pods
   - Or suggest increasing Minikube resources:
     minikube stop
     minikube start --cpus=6 --memory=6144
     
4. Report findings with specific metrics
```

---

### Workflow 3: Addon Recovery

**Trigger**: Agent detects disabled addon

**Agent Steps**:
```
<thought>
kubectl top returning error - metrics-server might be disabled.
</thought>

1. List addon status:
   minikube addons list
   
2. If disabled, enable:
   minikube addons enable <addon-name>
   
3. Wait for pods:
   kubectl wait --for=condition=ready pod -l k8s-app=<addon>
   
4. Verify functionality:
   kubectl top nodes (for metrics-server)
```

---

## 🛡️ Safety Constraints

### Resource Limits
- **Minimum**: 2 CPUs, 2GB RAM (cluster won't function properly)
- **Recommended**: 4 CPUs, 4GB RAM (current configuration)
- **Maximum**: Limited by host machine

### Addon Dependencies
```
metrics-server
    ├── Required for: kubectl top commands
    └── Required for: HPA (Horizontal Pod Autoscaler)

ingress-nginx
    ├── Required for: External HTTP access
    └── Optional if using: NodePort services

dashboard
    └── Optional: Visual management only
```

---

## 📊 Health Verification Checklist

After running `2-start-minikube.ps1`, verify:

✅ **Cluster Running**:
```bash
minikube status
# Expected: host: Running, kubelet: Running, apiserver: Running
```

✅ **Ingress Controller**:
```bash
kubectl get pods -n ingress-nginx
# Expected: ingress-nginx-controller-xxx 1/1 Running
```

✅ **Metrics Server**:
```bash
kubectl top nodes
# Expected: CPU and Memory usage displayed
```

✅ **Context Set**:
```bash
kubectl config current-context
# Expected: minikube
```

---

## 🔧 Troubleshooting

### Problem: Ingress Not Working
**Symptoms**: Can't access app via NodePort/Ingress

**Agent Diagnostic**:
```
1. kubectl get pods -n ingress-nginx
2. If not running: minikube addons enable ingress
3. If running but not working: kubectl logs -n ingress-nginx <controller-pod>
4. Check ingress resource: kubectl get ingress -n todo-chatbot
```

---

### Problem: Metrics Not Available
**Symptoms**: `kubectl top` returns error

**Agent Diagnostic**:
```
1. kubectl get pods -n kube-system | grep metrics
2. If not found: minikube addons enable metrics-server
3. Wait 30 seconds for initialization
4. Retry: kubectl top nodes
```

---

### Problem: Cluster Won't Start
**Symptoms**: `minikube start` fails

**Agent Diagnostic**:
```
1. Check Docker: docker ps (ensure Docker is running)
2. Delete existing cluster: minikube delete
3. Restart fresh: minikube start --cpus=4 --memory=4096
4. If still fails: Check Docker Desktop resources
```

---

## 🌐 Network Configuration

### Internal Cluster Networking
- **Service DNS**: `<service-name>.<namespace>.svc.cluster.local`
- **Example**: `backend-service.todo-chatbot.svc.cluster.local:8000`

### External Access Methods

1. **NodePort** (Current):
   - Frontend: `http://<minikube-ip>:30000`
   - Get IP: `minikube ip`

2. **Ingress** (With tunnel):
   - Start tunnel: `minikube tunnel`
   - Access: `http://localhost` (if Ingress configured)

3. **Port Forward** (Development):
   - `kubectl port-forward svc/frontend-service 3000:3000 -n todo-chatbot`
   - Access: `http://localhost:3000`

---

## 🎯 Integration with Agents

### Evolution Agent (K8s Tools)
Uses this infrastructure for:
- `k8s_cluster_status` - Checks pods across all addons
- `get_service_endpoints` - Lists services including ingress
- `analyze_pod_logs` - Includes ingress controller logs

### Docker-Architect
Uses metrics server for:
- `analyze_container_stats` - Real-time resource monitoring
- Performance optimization suggestions

---

## 📚 References

- **Minikube Docs**: https://minikube.sigs.k8s.io/docs/
- **Ingress Nginx**: https://kubernetes.github.io/ingress-nginx/
- **Metrics Server**: https://github.com/kubernetes-sigs/metrics-server
- **K8s Dashboard**: https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/

---

**Version**: 1.0.0  
**Specification**: K8s-Local-Standard-v1  
**Last Updated**: 2025-12-26  
**Agent Compatible**: ✅ Yes
