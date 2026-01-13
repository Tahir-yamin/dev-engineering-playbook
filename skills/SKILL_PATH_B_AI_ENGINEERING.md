# 🧠 Path B: AI Engineering (The "New" Full Stack)

**Goal**: Build the "brain" of applications using LLMs and Agents.
**Timeline**: 2025 Q2-Q3

---

## 1. RAG Systems (Retrieval-Augmented Generation)
Move beyond simple chatbots to systems that "know" your data.

- **Tools**: LangChain, LlamaIndex, RAGFlow

### 🔬 Micro-Skills
1.  **Chunking Strategies**:
    -   *Skill*: Knowing when to use "Fixed Size" vs "Recursive Character" vs "Semantic" chunking.
    -   *Test*: Split a 50-page PDF so that tables aren't broken in the middle.
2.  **Embedding Models**:
    -   *Skill*: Choosing between OpenAI `text-embedding-3-small` vs HuggingFace `all-MiniLM-L6-v2`.
    -   *Test*: Compare cosine similarity of "Apple" (fruit) vs "Apple" (company).
3.  **Vector Database Ops**:
    -   *Skill*: CRUD operations on `pgvector` or Pinecone.
    -   *Test*: Perform a "Hybrid Search" (Keyword + Semantic) query.

### 🛠️ Workflow: Build a RAG Pipeline
1.  **Ingest**: Write a script to read `docs/*.md`.
2.  **Chunk**: Use `RecursiveCharacterTextSplitter` (chunk_size=1000, overlap=200).
3.  **Embed**: Generate embeddings using a local model (save API costs).
4.  **Store**: Insert into Postgres `pgvector` table.
5.  **Retrieve**: On user query, fetch top 3 chunks.
6.  **Generate**: Pass chunks + query to LLM as "Context".

### Recommended Repos
- `run-llama/llama_index`
- `langchain-ai/langchain`

---

## 2. Agentic Workflows
Build systems that *do* things, not just *say* things.

- **Tools**: AutoGen (Multi-Agent), CrewAI, LangGraph

### 🔬 Micro-Skills
1.  **Prompt Engineering for Agents**:
    -   *Skill*: Writing "System Prompts" that define persona and constraints.
    -   *Test*: Make an agent that *refuses* to answer outside its domain.
2.  **Tool Definition (Function Calling)**:
    -   *Skill*: Defining JSON schemas for functions the AI can call.
    -   *Test*: Create a `get_weather(city)` tool and have the AI call it correctly.
3.  **Orchestration**:
    -   *Skill*: Managing the "Conversation State" between multiple agents.
    -   *Test*: Build a loop where Agent A writes code and Agent B reviews it until it passes.

### 🛠️ Workflow: Create a Multi-Agent System
1.  **Define Roles**: Create `UserProxyAgent` (Human) and `AssistantAgent` (AI).
2.  **Register Tools**: Give the Assistant a `write_file` function.
3.  **Initiate Chat**: User asks "Create a Python script to calculate pi".
4.  **Loop**:
    -   Assistant generates code.
    -   UserProxy executes code.
    -   If error -> UserProxy sends error back -> Assistant fixes.
    -   If success -> Terminate.

### Recommended Repos
- `microsoft/autogen`

---

## 3. LLM Ops (Production AI)
Treat AI like software engineering.

- **Tools**: LangSmith, Arize Phoenix, PromptFlow
- **Key Concepts**:
    - **Evaluation**: How do you know if the new prompt is better? (Ragas score).
    - **Tracing**: Seeing the full chain of thought and latency.
    - **Cost Tracking**: Monitoring token usage per user.

### Learning Project
1. **Trace**: Add tracing to your chatbot to see how long each step takes.
2. **Eval**: Create a dataset of 20 questions and automatically test your bot against them.

---

## 4. 2026 AI Trends & Emerging Skills

### Multi-Agent Orchestration (Agent Ops)
Build and coordinate teams of specialized AI agents.

- **Tools**: CrewAI, AutoGen, Microsoft Agent Framework, Google ADK

### 🔬 Micro-Skills
1.  **Agent Coordination**:
    -   *Skill*: Orchestrating multiple agents with different roles (research, write, review).
    -   *Test*: Create a 3-agent system where agents collaborate on a document.
2.  **Context Management**:
    -   *Skill*: Sharing state and context between agents efficiently.
    -   *Test*: Build a workflow where Agent A's output becomes Agent B's input.
3.  **Platform Selection**:
    -   *Skill*: Choosing the right orchestration framework for use case.
    -   *Test*: Compare CrewAI vs AutoGen for a specific multi-step workflow.

### 🛠️ Workflow: Build a Multi-Agent System
1.  **Define Roles**: Create Researcher, Writer, Editor agents.
2.  **Set Up Communication**: Configure inter-agent messaging.
3.  **Orchestrate**: Use CrewAI to coordinate sequential workflow.
4.  **Monitor**: Track performance and token usage.

### Recommended Frameworks
- `joaomdmoura/crewai` (most popular open source)
- `microsoft/autogen`
- Microsoft/Google/OpenAI enterprise platforms

---

## 5. AI Co-Workers & Collaboration Tools

### Desktop AI Agents
- **Claude Cowork** (macOS) - File management for non-technical users
- **Microsoft 365 Copilot** - Integrated into Office suite
- **Google Workspace Gemini** - Cross-app AI assistance

### Key Skills
- Prompt engineering for productivity tools
- AI tool stacking (connecting multiple AI tools)
- Designing human-agent collaboration workflows

---

## Critical 2026 Skills Summary

| Skill | Priority | Market Demand |
|-------|----------|---------------|
| **Prompt Engineering** | ⭐⭐⭐ | Foundational |
| **Agent Ops (Multi-Agent Orchestration)** | ⭐⭐⭐ | Emerging High |
| **RAG Systems** | ⭐⭐⭐ | Essential |
| **Agentic Workflows** | ⭐⭐ | Growing |
| **LLM Ops** | ⭐⭐ | Production |
| **Multimodal AI** | ⭐⭐ | Emerging |
| **AI Governance** | ⭐⭐ | Critical |

**Market Stats (2026)**:
- $8.5B AI agent market
- 40% of apps will embed agents
- 74% of B2B orgs deployed agents
- 90% using AI for development

**Updated**: 2026-01-13  
**Original Timeline**: 2025 Q2-Q3  
**Status**: Active and rapidly evolving
