---
description: Step-by-step guide to implementing a Corrective RAG (CRAG) system
---

# Implement Agentic RAG System

## When to Use
- You need higher accuracy than standard RAG.
- You want the system to self-correct when retrieval fails.
- You are building a complex Q&A system.

---

## Step 1: Framework Setup

Initialize the project with LangGraph and Qdrant.

```bash
# Install dependencies
pip install langchain langgraph qdrant-client tavily-python anthropic openai
```

---

## Step 2: Define the Graph State

Create `src/rag_graph.py` and define the state.

```python
from typing import TypedDict, List, Dict

class GraphState(TypedDict):
    """
    Represents the state of our RAG graph.
    """
    keys: Dict[str, any]
    question: str
    documents: List[str]
    runnable: bool
```

---

## Step 3: Implement Core Nodes

Implement the `retrieve`, `grade_documents`, and `transform_query` functions.

**Reference Skill**: `@[skills/agentic-rag-mastery.md]`

1. **Retrieve**: Connect to Qdrant and query embeddings.
2. **Grade**: Use Claude 3.5/4.5 to score document relevance (Yes/No).
3. **Web Search**: If Grade is "No", use Tavily API to find better context.

---

## Step 4: Build the Graph

Connect the nodes in LangGraph.

```python
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("transform_query", transform_query)
workflow.add_node("web_search", web_search)
workflow.add_node("generate", generate)

# Add Edges
workflow.add_edge("retrieve", "grade_documents")
# ... add conditional edges based on 'runnable' state ...
```

---

## Step 5: Verification

Run a test query that requires web search (e.g., current events) vs one that requires internal docs.

```bash
python src/rag_graph.py --query "What is the latest feature of LangGraph?"
```

---

**Related Skills**: `agentic-rag-mastery.md`
