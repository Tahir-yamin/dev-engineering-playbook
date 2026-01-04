# 🗺️ Path A: Advanced DevOps (Cloud-Native Expert)

**Goal**: Master the "how" of deployment, operations, and scale.
**Timeline**: 2025 Q1-Q2

---

## 1. GitOps Mastery
Move beyond manual `helm install` to declarative, automated delivery.

- **Tools**: ArgoCD (Industry Standard), Flux CD (Kubernetes Native)

### 🔬 Micro-Skills
1.  **ApplicationSet Pattern**:
    -   *Skill*: Generating ArgoCD Applications dynamically from Git folders.
    -   *Test*: Add a new folder `apps/blog` to Git and see it auto-deploy without touching ArgoCD.
2.  **Sync Waves & Hooks**:
    -   *Skill*: Controlling deployment order (DB migration -> App update).
    -   *Test*: Ensure the `db-migrate` job completes *before* the `backend` pod restarts.
3.  **Secret Management**:
    -   *Skill*: Using `SealedSecrets` or `ExternalSecrets` with GitOps.
    -   *Test*: Commit an encrypted secret to Git and verify it's decrypted in the cluster.

### 🛠️ Workflow: Implement GitOps
1.  **Install**: `helm install argocd argo/argo-cd`.
2.  **Define App**: Create an `Application` manifest pointing to your `helm/` folder.
3.  **Sync Policy**: Enable `automated: { prune: true, selfHeal: true }`.
4.  **Image Updater**: Configure `argocd-image-updater` to watch Docker Hub and auto-commit new tags.

### Recommended Repos
- `argoproj/argo-cd`
- `fluxcd/flux2`

---

## 2. Observability (The "Missing Piece")
You have deployment, but can you see what's happening inside?

- **Tools**: Prometheus (Metrics), Grafana (Visualization), OpenTelemetry (Tracing)

### 🔬 Micro-Skills
1.  **PromQL Queries**:
    -   *Skill*: Writing queries like `rate(http_requests_total[5m])`.
    -   *Test*: Create an alert that fires if error rate > 1% for 5 minutes.
2.  **Span Context Propagation**:
    -   *Skill*: Passing `trace-id` headers from Frontend -> Backend -> DB.
    -   *Test*: View a single "Click" in Grafana Tempo and see the SQL query it triggered.
3.  **Golden Signals**:
    -   *Skill*: Building a dashboard with Latency, Traffic, Errors, and Saturation.
    -   *Test*: Load test the app and watch the "Saturation" (CPU/Memory) spike.

### 🛠️ Workflow: Full-Stack Observability
1.  **Deploy Stack**: `helm install kube-prometheus-stack`.
2.  **Instrument Code**: Add `opentelemetry-instrumentation-fastapi` to your backend.
3.  **Configure Exporter**: Point the OTLP exporter to the collector.
4.  **Visualize**: Import the "FastAPI Dashboard" ID into Grafana.

### Recommended Repos
- `prometheus-operator/kube-prometheus`

---

## 3. Infrastructure as Code (IaC)
Manage the cloud resources (NeonDB, Vercel) as code.

- **Tools**: Terraform (Universal), Crossplane (K8s Native)
- **Learning Project**: Use Terraform to provision a GitHub repository and secrets.
