# 🚀 Phase V: Advanced Cloud Deployment Skills

**Goal**: Master Kafka, Dapr, and cloud Kubernetes deployment.
**Timeline**: January 2026

---

## 1. Kafka Event-Driven Architecture

### 🔬 Micro-Skills
1. **Topic Design**:
   - *Skill*: Knowing when to create one topic per event type vs one topic per service.
   - *Test*: Design topics for a notification system. Justify your choice.
2. **Consumer Groups**:
   - *Skill*: Understanding how Kafka partitions messages across consumers.
   - *Test*: Scale consumers from 1 to 3 and observe message distribution.
3. **Idempotency**:
   - *Skill*: Designing consumers that handle duplicate messages safely.
   - *Test*: Process the same "TaskCompleted" event twice. User should get XP only once.

### 🛠️ Workflow: Implement Kafka Pub/Sub
1. **Install Strimzi**: `kubectl apply -f strimzi-kafka.yaml`
2. **Create Topic**: Define `KafkaTopic` custom resource.
3. **Publish Event**: Use `aiokafka` or Dapr Pub/Sub to publish.
4. **Consume Event**: Create a FastAPI service that subscribes via Dapr.

### Recommended Repos
- `strimzi/strimzi-kafka-operator`
- `aio-libs/aiokafka`

---

## 2. Dapr Distributed Runtime

### 🔬 Micro-Skills
1. **Sidecar Debugging**:
   - *Skill*: Understanding how the app talks to the sidecar (localhost:3500).
   - *Test*: Use `curl` to call the Dapr sidecar's Pub/Sub API directly.
2. **Component Configuration**:
   - *Skill*: Writing YAML for Pub/Sub, State, and Secrets components.
   - *Test*: Swap Kafka for Redis Pub/Sub by changing only the YAML.
3. **Jobs API for Scheduling**:
   - *Skill*: Scheduling exact-time callbacks instead of cron polling.
   - *Test*: Schedule a reminder for 5 minutes from now and verify the callback.

### 🛠️ Workflow: Integrate Dapr with FastAPI
1. **Install Dapr**: `dapr init -k`
2. **Create Components**: `dapr-components/pubsub.yaml`, `statestore.yaml`
3. **Add Annotations**: `dapr.io/enabled: "true"` to your Deployment.
4. **Refactor Code**: Replace `aiokafka` with Dapr HTTP calls.

### Recommended Repos
- `dapr/dapr`
- `dapr/python-sdk`
- `dapr/quickstarts`

---

## 3. Azure AKS Deployment

### 🔬 Micro-Skills
1. **ACR Integration**:
   - *Skill*: Attaching Azure Container Registry to AKS for pull access.
   - *Test*: Push an image to ACR and deploy it to AKS without imagePullSecrets.
2. **GitHub Actions for K8s**:
   - *Skill*: Writing CI/CD workflows for build, push, and Helm deploy.
   - *Test*: Push to `main` and watch the entire pipeline complete automatically.
3. **Ingress Configuration**:
   - *Skill*: Exposing services with NGINX Ingress and TLS.
   - *Test*: Access your app via `https://todo.yourdomain.com`.

### 🛠️ Workflow: Deploy to Azure AKS
1. **Create Resources**: `az group create`, `az acr create`, `az aks create`
2. **Attach ACR**: `az aks update --attach-acr todohackathonacr`
3. **Configure kubectl**: `az aks get-credentials`
4. **Install Dapr**: `dapr init -k`
5. **Deploy with Helm**: `helm upgrade --install todo-chatbot ./helm/todo-chatbot`
6. **Set up GitHub Actions**: Create `.github/workflows/deploy-aks.yml`

### Recommended Repos
- `Azure/aks-github-actions`
- `Azure-Samples/azure-voting-app`

---

## 4. Recurring Tasks & Reminders

### 🔬 Micro-Skills
1. **PostgreSQL Recurrence Storage**:
   - *Skill*: Storing recurrence rules in JSONB, not individual occurrences.
   - *Test*: Create a "weekly on Monday" task. Verify only the rule is stored.
2. **Next Occurrence Calculation**:
   - *Skill*: Calculating `next_occurrence_at` after each trigger.
   - *Test*: Complete a daily task. Verify the next occurrence is 24h later.
3. **Timezone Handling**:
   - *Skill*: Storing in UTC, displaying in user's timezone.
   - *Test*: User in NYC creates a 9 AM reminder. Verify UTC storage is 14:00.

### 🛠️ Workflow: Implement Recurring Tasks
1. **Update Database Schema**: Add `recurrence_type`, `recurrence_details`, `next_occurrence_at`.
2. **Update MCP Tools**: `add_task` accepts recurrence parameters.
3. **Create Recurring Task Service**: Listens to `task-events`, creates next occurrence on completion.
4. **Use Dapr Jobs API**: Schedule reminders at exact time.

### Recommended Repos
- `agronholm/apscheduler`
- `procrastinate-org/procrastinate`

---

## Common Issues & Solutions

### Dapr
| Issue | Solution |
|-------|----------|
| Sidecar not injecting | Verify `dapr.io/enabled: "true"` annotation |
| Component not found | Check namespace matches, YAML syntax |
| 500 errors from Dapr | Enable debug logging: `dapr.io/log-level: debug` |

### Kafka/Strimzi
| Issue | Solution |
|-------|----------|
| Cluster Operator stuck | Restart operator, check K8s version |
| Topic not created | Check Topic Operator logs |
| Client can't connect | Verify listener config, network policies |

### Azure AKS
| Issue | Solution |
|-------|----------|
| ACR pull fails | `az aks update --attach-acr` |
| Pod OOMKilled | Increase memory limits |
| Ingress not working | Install NGINX Ingress controller |
