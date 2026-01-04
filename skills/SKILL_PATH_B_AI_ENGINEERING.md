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
