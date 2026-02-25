# Agentic RAG Mastery & Implementation

**Topics**: RAG, LangGraph, Architectures, Vector search, CRAG
**Version**: 1.0
**Source**: `awesome-llm-apps/rag_tutorials/corrective_rag`

---

## Skill #1: Corrective RAG (CRAG) Implementation

### Context
CRAG improves RAG by adding a self-corrective layer. If retrieved documents are irrelevant, it transforms the query and falls back to web search.

### The Architecture
1. **Retrieve**: Fetch top-k docs from Vector DB (e.g., Qdrant).
2. **Grade Relevance**: LLM (Claude/GPT-4) scores each doc as `relevant` or `irrelevant`.
3. **Decide**:
   - If *all* irrelevant -> **Transform Query** -> **Web Search** (Tavily).
   - If *some* relevant -> **Filter** -> **Generate**.
4. **Generate**: Final answer Synthesis.

### Implementation Pattern (LangGraph)

```python
# State Definition
class GraphState(TypedDict):
    keys: Dict[str, any]
    question: str
    documents: List[str]
    runnable: bool

# Nodes
def retrieve(state):
    # Call Qdrant/Chroma
    return {"documents": retrieved_docs}

def grade_documents(state):
    # LLM Binary Score: "yes" or "no"
    # Filter out "no" docs
    if not relevant_docs:
        return {"runnable": False} # Trigger web search
    return {"documents": relevant_docs, "runnable": True}

def transform_query(state):
    # LLM rewrite query for better search
    return {"question": new_question}

def web_search(state):
    # Tavily API call
    return {"documents": web_results}
```

### Critical Components
- **Grader Prompt**: "You are a grader assessing relevance of a retrieved document to a user question. If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant."
- **Fallback**: Always have a `web_search` tool for "unknown" domains.

---

## Skill #2: Self-RAG Pattern

### Context
Self-RAG adds a "Critic" agent that critiques the generation for hallucinations and relevance.

### Workflow
1. **Retrieve** based on query.
2. **Generate** initial response.
3. **Critique**:
   - Is it supported by docs? (Hallucination check)
   - Is it useful? (Relevance check)
4. **Refine**: If critique fails, regenerate or retrieve more context.

---

## Quick Reference: Tools
- **Orchestration**: LangGraph, CrewAI
- **Vector DB**: Qdrant, Chroma, Pinecone
- **Search API**: Tavily, Serper

---

## Related Skills
- `backend-specialist` (Python/FastAPI)
- `multi-agent-patterns-google-adk`
