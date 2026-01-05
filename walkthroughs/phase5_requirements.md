# Phase V: Advanced Cloud Deployment - Requirements Analysis

**Due Date**: January 18, 2026  
**Points**: 300 (highest of all phases)

---

## 📋 Overview

Phase V is the culmination of the hackathon. It requires implementing **advanced features**, **event-driven architecture**, and deploying to a **production-grade cloud Kubernetes cluster**.

---

## 🎯 Three Parts of Phase V

### Part A: Advanced Features (New Code)
| Feature | Description | Complexity |
|---------|-------------|------------|
| **Recurring Tasks** | Auto-reschedule repeating tasks (e.g., "weekly meeting") | High |
| **Due Dates & Reminders** | Set deadlines, browser notifications | Medium |
| **Priorities** | High/Medium/Low levels | Low |
| **Tags/Categories** | Labels (work/home) | Low |
| **Search & Filter** | Search by keyword, filter by status/priority/date | Medium |
| **Sort Tasks** | Reorder by due date, priority, alphabetically | Low |

### Part B: Local Deployment (Minikube)
| Requirement | Tool |
|-------------|------|
| Deploy to Minikube | `minikube start` |
| Deploy Dapr on Minikube | `dapr init -k` |
| Full Dapr features | Pub/Sub, State, Bindings (cron), Secrets, Service Invocation |

### Part C: Cloud Deployment (Production)
| Requirement | Options |
|-------------|---------|
| Cloud Provider | **Azure AKS** (recommended) / Google GKE / Oracle OKE |
| Kafka | Redpanda Cloud (free) / Strimzi (self-hosted) |
| CI/CD Pipeline | GitHub Actions |
| Monitoring & Logging | Configure observability |

---

## 🏗️ Technology Stack

| Component | Technology |
|-----------|------------|
| Orchestration | Azure AKS / Google GKE / Oracle OKE |
| Event Streaming | Apache Kafka (via Redpanda or Strimzi) |
| Distributed Runtime | Dapr (Distributed Application Runtime) |
| CI/CD | GitHub Actions |
| Package Manager | Helm Charts |

---

## 📡 Kafka Integration (Event-Driven Architecture)

### Kafka Topics
| Topic | Producer | Consumer | Purpose |
|-------|----------|----------|---------|
| `task-events` | Chat API (MCP Tools) | Recurring Task Service, Audit Service | All task CRUD operations |
| `reminders` | Chat API (due date set) | Notification Service | Scheduled reminder triggers |
| `task-updates` | Chat API | WebSocket Service | Real-time client sync |

### Use Cases
1. **Reminder/Notification System**: Publish reminder events → Notification service sends alerts
2. **Recurring Task Engine**: Task completed → Auto-create next occurrence
3. **Activity/Audit Log**: All operations logged via Kafka
4. **Real-time Sync**: Changes broadcast to all connected clients

---

## 🔧 Dapr Building Blocks

| Building Block | Use Case |
|----------------|----------|
| **Pub/Sub** | Kafka abstraction - no kafka-python library needed |
| **State Management** | Conversation state storage (PostgreSQL backend) |
| **Service Invocation** | Frontend → Backend with retries, mTLS |
| **Bindings (Jobs API)** | Scheduled reminders at exact time (not cron polling) |
| **Secrets Management** | API keys, DB credentials |

### Without Dapr vs With Dapr
| Without Dapr | With Dapr |
|--------------|-----------|
| Import Kafka, Redis, Postgres libraries | Single HTTP API for all |
| Connection strings in code | Dapr components (YAML config) |
| Manual retry logic | Built-in retries, circuit breakers |
| Service URLs hardcoded | Automatic service discovery |
| Vendor lock-in | Swap Kafka for RabbitMQ via config |

---

## 📁 Deliverables

### 1. GitHub Repository
- All source code for Phase V
- `/specs` folder with all specifications
- `CLAUDE.md` with Claude Code instructions
- `README.md` with comprehensive documentation
- Dapr component YAML files
- Helm charts for cloud deployment

### 2. Deployed Application Links
- **Local**: Instructions for Minikube + Dapr setup
- **Cloud**: Azure AKS / Google GKE / Oracle OKE URL

### 3. Demo Video (90 seconds max)
- Show recurring tasks in action
- Demonstrate Kafka event flow
- Show cloud deployment

---

## 💰 Cloud Provider Credits

| Provider | Free Credits | Duration |
|----------|--------------|----------|
| **Azure** | $200 | 30 days + 12 months free services |
| **Oracle (Recommended)** | Always Free (4 OCPUs, 24GB RAM) | Forever |
| **Google Cloud** | $300 | 90 days |

---

## 🚀 Implementation Approach

### Step 1: Implement Advanced Features
1. Add `due_date`, `priority`, `tags`, `recurrence` fields to Task model
2. Update MCP tools to handle new fields
3. Add filtering/sorting to `list_tasks` tool

### Step 2: Add Kafka Event Publishing
1. Install kafka-python or use Dapr Pub/Sub
2. Publish events on task CRUD operations
3. Create Notification Service (consumer)

### Step 3: Integrate Dapr
1. Install Dapr: `dapr init -k`
2. Create Dapr component YAML files
3. Refactor backend to use Dapr HTTP API

### Step 4: Deploy to Cloud
1. Create AKS/GKE/OKE cluster
2. Deploy Dapr to cluster
3. Deploy Kafka (Strimzi or connect to Redpanda Cloud)
4. Deploy application via Helm
5. Set up GitHub Actions CI/CD

---

## ⏱️ Timeline Estimate

| Task | Duration |
|------|----------|
| Advanced features (Tasks, Filters) | 2-3 days |
| Kafka integration | 1-2 days |
| Dapr integration | 1-2 days |
| Local testing (Minikube) | 1 day |
| Cloud deployment | 2-3 days |
| CI/CD + Documentation | 1 day |
| **Total** | **8-12 days** |

---

## 🔑 Key Success Criteria

1. ✅ All Advanced + Intermediate features working
2. ✅ Kafka event-driven architecture implemented
3. ✅ Dapr Pub/Sub, State, and Jobs API used
4. ✅ Running on Minikube locally
5. ✅ Deployed to cloud Kubernetes (AKS/GKE/OKE)
6. ✅ CI/CD pipeline via GitHub Actions
7. ✅ 90-second demo video
