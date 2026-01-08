---
description: Guide for systematically upgrading skills using the 2025 roadmap
---

# Skill Upgrade Workflow

This workflow guides you through the process of upgrading your skills from "Cloud-Native Practitioner" to "Enterprise Architect" using the curated roadmap and resources.

## Prerequisites

- [ ] Review the skill path for your chosen area:
    - `docs/misc/SKILL_PATH_0_CORE_STACK.md`
    - `docs/misc/SKILL_PATH_A_DEVOPS.md`
    - `docs/misc/SKILL_PATH_B_AI_ENGINEERING.md`
    - `docs/misc/SKILL_PATH_C_ARCHITECTURE.md`
- [ ] Review `docs/misc/RECOMMENDED_REPOS.md`
- [ ] Select **ONE** path to focus on

## Step 1: Choose Your Path

Decide which area you want to tackle first. **Do not try to do all at once.**

- **Path 0: Core Stack Upgrade** (Next.js 15, FastAPI, Postgres) - *Recommended Start*
- **Path A: Advanced DevOps** (GitOps, Observability)
- **Path B: AI Engineering** (RAG, Agents)
- **Path C: Enterprise Architecture** (Event-Driven, Dapr)

## Step 2: Study the "Deep Dive" Repos

For your chosen path, clone and study the recommended repositories found in `docs/misc/RECOMMENDED_REPOS.md`.

1. **Clone the repo**: `git clone <repo-url>`
2. **Read the code**: Focus on the specific directories mentioned in the guide.
3. **Run the project**: Try to get it running locally to understand the developer experience.

## Step 3: Implement a "Learning Project"

Apply what you've learned to the current Todo App (or a new project).

### If Path 0 (Core Stack):
- Refactor one API route to a **Server Action**.
- Implement **Optimistic Updates** for a toggle feature.
- Add a **GIN index** to Postgres.

### If Path A (DevOps):
- Install **ArgoCD** on your local K8s cluster.
- Create an **Application** manifest for the Todo App.
- Add a **Grafana** dashboard for pod metrics.

### If Path B (AI Engineering):
- Create a simple **RAG** pipeline using LangChain/LlamaIndex.
- Index your project's `docs/` folder.
- Allow the chatbot to answer questions about the project structure.

### If Path C (Architecture):
- Install **Dapr** on your cluster.
- Refactor the backend to use Dapr for **State Management**.
- Implement a simple **Pub/Sub** event (e.g., "TaskCompleted").

## Step 4: Document Your Learning

1. Create a new file: `docs/learning/<path-name>-notes.md`.
2. Document what you built.
3. Note down any "gotchas" or challenges.
4. (Optional) Create a PR to the main repo with your improvements.

## Troubleshooting

- **"I don't understand this code"**: Use the AI assistant to explain specific files in the recommended repos.
- **"It won't run locally"**: Check the repo's `CONTRIBUTING.md` or `README.md` for prerequisites.
- **"I'm overwhelmed"**: Stop. Pick just **ONE** concept (e.g., "Server Actions") and master that before moving on.
