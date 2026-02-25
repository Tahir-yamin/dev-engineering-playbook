---
name: algolia-grounded-rag
description: Principles for building Grounded RAG applications using Algolia Agent Studio and InstantSearch.
skills:
  - id: 1
    description: Implementing Search-First Agent Prompting to prevent hallucinations.
    content: |
      ## Skill #1: Search-First Agent Prompting

      ### When to Use
      - Building AI agents that must adhere to strict knowledge bases (legal, compliance, technical).
      - Preventing "hallucinations" where the AI invents facts not in the index.

      ### Pattern
      Configure the Agent's System Prompt to **forbid** answering from general knowledge and **mandate** tool use.

      ```markdown
      **SYSTEM PROMPT TEMPLATE**:
      You are an expert consultant using the [Index Name] knowledge base.
      
      **CRITICAL RULES**:
      1. You MUST use the `search_index` tool for EVERY user query.
      2. You MUST NOT answer based on your internal training data.
      3. If the search tool returns no results, state "I cannot find verified information."
      4. Your final answer must cite the specific `objectID` or `source` field from the tool output.
      ```

  - id: 2
    description: Bridging Algolia Agent API with Frontend UI.
    content: |
      ## Skill #2: Agent-UI Hydra Pattern

      ### When to Use
      - Displaying "Non-Conversational" UI elements (cards, dashboards) driven by Agent logic.

      ### Pattern
      Instead of just streaming text, have the agent return structured JSON or specific "Signal" keywords that the frontend maps to UI components.
      
      **Frontend (Next.js)**:
      ```typescript
      // Call Agent via Proxy (to hide secrets)
      const response = await fetch('/api/agent/analyze', { body: { query } });
      const { thinking, signals } = await response.json();
      
      // Render dedicated components for signals
      {signals.map(s => <ComplianceCard data={s} />)}
      ```

  - id: 3
    description: Optimizing Algolia Index Structure for RAG.
    content: |
      ## Skill #3: RAG-Optimized Indexing

      ### Principles
      - **Chunking**: Don't index entire PDFs. Split content into "Knowledge Atoms" (e.g., individual Articles, FAQ pairs).
      - **Enrichment**: finding meaningful tags (e.g., `risk_level: critical`) to allow agents to filter pre-search.
      - **Attributes for Retrieval**: Ensure `content`, `title`, and `source_url` are set to `searchableAttributes`.
---
