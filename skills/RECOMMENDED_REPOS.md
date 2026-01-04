# 🏆 Recommended Repositories for Deep Learning

This document provides a "deep dive" into specific GitHub repositories that represent the gold standard for the skills outlined in the [Skill Upgrade Roadmap](./SKILL_UPGRADE_ROADMAP.md).

---

## 💻 Core Web Stack (Next.js, FastAPI, Postgres)

### 1. `vercel/next.js` (Official Examples)
**Why study this?** The source of truth for Next.js 15 patterns.
- **What to look for**:
    - `examples/app-dir-i18n-routing`: Advanced routing patterns.
    - `examples/server-actions-upload`: Handling file uploads with Server Actions (no API routes).
    - **Discussions Tab**: The "RFC" (Request for Comments) threads show *why* features exist.

### 2. `tiangolo/full-stack-fastapi-template`
**Why study this?** The creator of FastAPI's own production template.
- **What to look for**:
    - `backend/app/api/deps.py`: How to handle complex dependency injection for Auth.
    - `backend/app/core/security.py`: Production-grade JWT handling.
    - **Docker integration**: How to structure a multi-container app (FastAPI + Postgres + Traefik).

### 3. `supabase/supabase`
**Why study this?** The ultimate "Postgres as a Service" codebase.
- **What to look for**:
    - `studio/`: A massive Next.js app that manages Postgres.
    - **Postgres Extensions**: See how they package extensions like `pgvector` for AI.

---

## 🛠️ DevOps & Cloud-Native

### 1. `argoproj/argo-cd`
**Why study this?** It's the industry standard for GitOps.
- **What to look for**:
    - `manifests/install.yaml`: How they package their own application for K8s.
    - `server/`: The Go code that handles the API and UI.
    - `controller/`: The core logic that syncs Git to K8s (the "reconciliation loop").

### 2. `fluxcd/flux2`
**Why study this?** The "Kubernetes-native" way of doing GitOps.
- **What to look for**:
    - **Micro-controller architecture**: Flux is split into `source-controller`, `kustomize-controller`, `helm-controller`. Study how these interact.
    - **CRDs**: Look at `manifests/crds` to see how they extend the K8s API.

### 3. `prometheus-operator/kube-prometheus`
**Why study this?** The ultimate observability stack.
- **What to look for**:
    - **Jsonnet**: They use Jsonnet to generate thousands of lines of YAML. This is "Infrastructure as Code" at scale.
    - **AlertManager rules**: Study the default alerts to understand what "production-ready" monitoring looks like.

---

## 🧠 AI Engineering

### 1. `langchain-ai/langchain`
**Why study this?** The framework that started the LLM revolution.
- **What to look for**:
    - `libs/langchain/langchain/chains/`: How they abstract complex workflows (RetrievalQA, Summarization).
    - `libs/langchain/langchain/agents/`: The logic for "ReAct" agents and tool use.

### 2. `run-llama/llama_index`
**Why study this?** The best framework for RAG (Retrieval-Augmented Generation).
- **What to look for**:
    - `llama_index/indices/`: How they structure data (VectorStore, List, Tree).
    - `llama_index/query_engine/`: The logic for retrieving and synthesizing answers.

### 3. `microsoft/autogen`
**Why study this?** The future of multi-agent systems.
- **What to look for**:
    - `autogen/agentchat/`: How agents "talk" to each other.
    - `autogen/code_utils.py`: How the agents execute code (sandboxing).

---

## 🏗️ Enterprise Architecture

### 1. `dapr/dapr`
**Why study this?** It solves the "hard parts" of distributed systems.
- **What to look for**:
    - `pkg/components/`: How they abstract different state stores (Redis, CosmosDB) into a common API.
    - `pkg/injector/`: How the Dapr sidecar is injected into K8s pods.

### 2. `dotnet-architecture/eShopOnDapr`
**Why study this?** A reference implementation of a real-world microservices app.
- **What to look for**:
    - **Architecture**: See how `Ordering`, `Catalog`, and `Basket` services communicate via Dapr Pub/Sub.
    - **Helm Charts**: How a complex multi-service app is deployed.

### 3. `donnemartin/system-design-primer`
**Why study this?** The "bible" of system design interviews and knowledge.
- **What to look for**:
    - **Diagrams**: Study the visual representations of Load Balancing, Caching, and Sharding.
    - **Case Studies**: Read the "Design Twitter" and "Design Uber" sections.

---

## 🎓 How to Study a Repo

Don't just read the code. **Run it.**

1. **Clone it**: `git clone <repo>`
2. **Build it**: Try to run the build instructions.
3. **Break it**: Change a line of code and see what happens.
4. **Fix it**: Try to fix a "Good First Issue".
