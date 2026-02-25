# Cloud-Native Orchestration Mastery

**Purpose**: Definitive guide for Containerization, Orchestration, and Sidecar Runtimes (Docker, Kubernetes, Dapr).
**Unified From**: `docker-skills.md`, `kubernetes-resource-management-skills.md`, `kubernetes-resource-optimization-skills.md`, `dapr-configuration-skills.md`, `dapr-integration-skills.md`.

---

## 🏗️ PART 1: DOCKER ARCHITECTURE & DEBUGGING

### Skill #1: Optimized Multi-Stage Builds
**Objective**: Minimal image size (<200MB) with separation of concerns.

```dockerfile
# Use node:20-slim for production-grade security and size
FROM node:20-slim AS deps
WORKDIR /app
COPY package*.json ./
RUN npm install

FROM node:20-slim AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Proactive Prisma generation
RUN npx prisma generate && npm run build

FROM node:20-slim AS runner
WORKDIR /app
COPY --from=builder /app/package.json .
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
CMD ["node", "server.js"]
```

### Skill #2: Container Debugging Workflow
1. **Logs**: `docker logs -f <container>`
2. **Inspection**: `docker inspect <container>` (Check env vars and network)
3. **Execution**: `docker exec -it <container> sh`
4. **Health Check**: Define `healthcheck` in `docker-compose.yml` to prevent dependent services from starting too early.

---

## ☸️ PART 2: KUBERNETES RESOURCE GOVERNANCE

### Skill #3: Request vs Limit Precision
- **Requests**: Guarateed minimum (used for scheduling).
- **Limits**: Hard ceiling (enforced at runtime).
| Load Type | Request | Limit | Note |
| :--- | :--- | :--- | :--- |
| **Stable** | Actual Usage | 1.5x Request | Baseline production |
| **Bursty** | Baseline | 3-4x Request | Allow spikes |
| **Critical** | High | Same as Request | Guaranteed QoS |

### Skill #4: Small Cluster Optimization (AKS/Dev)
Default K8s requests are often too high for 2-core / 4GB nodes.
- **Minimal Config**: `requests: {cpu: 50m, memory: 64Mi}` | `limits: {cpu: 200m, memory: 256Mi}`
- **AKS Reservation Awareness**: A 2-vCPU node has ~100m CPU reserved. Factor in Dapr (~500m) and System Pods (~200m). **Total Allocatable is often < 60% of capacity.**

---

## 🌌 PART 3: DAPR SIDECAR INTEGRATION (THE SOVEREIGN RUNTIME)

### Skill #5: Sidecar Injection & Efficiency
Enable Dapr via annotations in your Deployment:
```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "my-service"
  dapr.io/app-port: "8000"
  dapr.io/sidecar-cpu-request: "100m" # Reduced from default
  dapr.io/sidecar-cpu-limit: ""       # Dapr recommends NO CPU LIMIT to allow bursting
```

### Skill #6: Pub/Sub & State Abstraction
Use Dapr to abstract Kafka and PostgreSQL.
- **Publish (FastAPI)**: `POST http://localhost:3500/v1.0/publish/kafka-pubsub/task-events`
- **Subscribe**: Must implement `GET /dapr/subscribe` returning `{pubsubname, topic, route}`.
- **Benefits**: Swap storage/messaging providers via YAML components without changing app code.

---

## 🛠️ MASTER DIAGNOSTIC CHEAT SHEET

| Problem | Step 1 | Step 2 |
| :--- | :--- | :--- |
| **Pod Pending** | `kubectl describe pod` | Check `Insufficient cpu/memory` events |
| **1/2 Ready** | `kubectl logs <pod> -c daprd` | Check if sidecar component failed to load |
| **OOMKilled** | `kubectl top pods` | Increase `limits.memory` |
| **Slow Performance** | `kubectl top nodes` | Check for CPU throttling (Invisible in logs) |

---
**Last Updated**: February 2026
**Ecosystem status**: Production-Hardened (Phase 5 Logic)
