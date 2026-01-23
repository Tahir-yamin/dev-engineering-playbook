# Multi-Agent Patterns - Google ADK Implementation Skills

**Source**: Google Developers Blog - ADK Framework  
**Created**: 2026-01-23  
**Version**: 1.0  
**Topics**: Multi-Agent Systems, Orchestration, Context Management

---

## 📋 **Pattern Overview**

Google ADK defines **8 core multi-agent patterns** for production systems:

| Pattern | Metaphor | Use Case | Complexity |
|---------|----------|----------|------------|
| **Sequential Pipeline** | Assembly Line | Data Processing | ⭐ |
| **Coordinator/Dispatcher** | Concierge | Intent Routing | ⭐⭐ |
| **Parallel Fan-Out/Gather** | Octopus | Speed Optimization | ⭐⭐ |
| **Hierarchical Decomposition** | Russian Doll | Complex Tasks | ⭐⭐⭐ |
| **Generator and Critic** | Editor's Desk | Quality Control | ⭐⭐⭐ |
| **Iterative Refinement** | Sculptor | Progressive Enhancement | ⭐⭐⭐ |
| **Human-in-the-Loop** | Safety Net | Risk Mitigation | ⭐⭐ |
| **Composite Patterns** | Mix-and-Match | Custom Workflows | ⭐⭐⭐⭐ |

---

## Pattern 1: Sequential Pipeline (Assembly Line)

### When to Use
- Linear data processing workflows
- Each step depends on previous output
- Deterministic, debuggable flow needed

### Architecture
```
Agent A → Agent B → Agent C → Result
```

### ADK Implementation

```python
# Step 1: Parse PDF
parser = LlmAgent(
    name="ParserAgent",
    instruction="Parse raw PDF and extract text.",
    tools=[PDFParser],
    output_key="raw_text"  # ← Writes to shared state
)

# Step 2: Extract structured data
extractor = LlmAgent(
    name="ExtractorAgent",
    instruction="Extract structured data from {raw_text}.",  # ← Reads from state
    tools=[RegexExtractor],
    output_key="structured_data"
)

# Step 3: Summarize
summarizer = LlmAgent(
    name="SummarizerAgent",
    instruction="Generate summary from {structured_data}.",
    tools=[SummaryEngine]
)

# Orchestrate
pipeline = SequentialAgent(
    name="PDFProcessingPipeline",
    sub_agents=[parser, extractor, summarizer]
)
```

### Key Concepts
- **State Management**: Use `output_key` to write results to shared `session.state`
- **Templating**: Use `{key}` syntax to read from previous steps
- **Debugging**: Linear flow makes failures easy to trace

---

## Pattern 2: Coordinator/Dispatcher (Concierge)

### When to Use
- Multiple specialist agents needed
- Dynamic routing based on user intent
- Customer service bots, multi-domain chatbots

### Architecture
```
User → Coordinator → [Billing | TechSupport | Sales]
```

### ADK Implementation

```python
# Define specialists
billing_specialist = LlmAgent(
    name="BillingSpecialist",
    description="Handles billing inquiries and invoices.",  # ← Used for routing
    tools=[BillingSystemDB]
)

tech_support = LlmAgent(
    name="TechSupportSpecialist",
    description="Troubleshoots technical issues.",
    tools=[DiagnosticTool]
)

# Central dispatcher
coordinator = LlmAgent(
    name="CoordinatorAgent",
    instruction="""
    Analyze user intent. 
    Route billing issues to BillingSpecialist.
    Route bugs to TechSupportSpecialist.
    """,
    sub_agents=[billing_specialist, tech_support]  # ← AutoFlow routes based on descriptions
)
```

### Key Concepts
- **LLM-Driven Delegation**: Coordinator uses descriptions to route intelligently
- **Auto Flow**: ADK handles transfer logic automatically
- **Scalability**: Easy to add new specialists without changing coordinator logic

---

## Pattern 3: Parallel Fan-Out/Gather (Octopus)

### When to Use
- Independent tasks can run simultaneously
- Need to aggregate diverse perspectives
- Speed optimization required

### Architecture
```
                    → Agent A →
Input → Spawner →   → Agent B → Gatherer → Result
                    → Agent C →
```

### ADK Implementation

```python
# Define parallel workers
security_scanner = LlmAgent(
    name="SecurityAuditor",
    instruction="Check for vulnerabilities like injection attacks.",
    output_key="security_report"  # ← Unique key prevents race conditions
)

style_checker = LlmAgent(
    name="StyleEnforcer",
    instruction="Check for PEP8 compliance.",
    output_key="style_report"
)

complexity_analyzer = LlmAgent(
    name="PerformanceAnalyst",
    instruction="Analyze time complexity.",
    output_key="performance_report"
)

# Fan-out
parallel_reviews = ParallelAgent(
    name="CodeReviewSwarm",
    sub_agents=[security_scanner, style_checker, complexity_analyzer]
)

# Gather/Synthesize
pr_summarizer = LlmAgent(
    name="PRSummarizer",
    instruction="""
    Create consolidated Pull Request review using:
    {security_report}, {style_report}, {performance_report}
    """
)

# Combine
workflow = SequentialAgent(
    sub_agents=[parallel_reviews, pr_summarizer]
)
```

### Key Concepts
- **Unique Output Keys**: Prevents race conditions in shared state
- **Latency Reduction**: Parallel execution cuts total time
- **Synthesis**: Final agent aggregates diverse perspectives

---

## Pattern 4: Hierarchical Decomposition (Russian Doll)

### When to Use
- Task too complex for single agent context
- Natural hierarchical breakdown exists
- Sub-tasks need specialized expertise

### Architecture
```
Top Agent
  └─ Mid-Level Agent
      ├─ Tool Agent 1
      └─ Tool Agent 2
```

### ADK Implementation

```python
# Level  3: Tool Agents
web_searcher = LlmAgent(
    name="WebSearchAgent",
    description="Searches web for facts."
)

summarizer = LlmAgent(
    name="SummarizerAgent",
    description="Condenses text."
)

# Level 2: Coordinator
research_assistant = LlmAgent(
    name="ResearchAssistant",
    description="Finds and summarizes info.",
    sub_agents=[web_searcher, summarizer]  # ← Manages tool agents
)

# Level 1: Top-Level Agent
report_writer = LlmAgent(
    name="ReportWriter",
    instruction="Write comprehensive report on AI trends. Use ResearchAssistant.",
    tools=[AgentTool(research_assistant)]  # ← Treat sub-agent as tool
)
```

### Key Concepts
- **AgentTool Wrapper**: Turns entire sub-agent workflow into single tool call
- **Context Management**: Each level operates within its own context window
- **Delegation**: Parent waits for child results before continuing

---

## Pattern 5: Generator and Critic (Editor's Desk)

### When to Use
- Output quality must meet specific criteria
- Code generation requiring syntax validation
- Content needing compliance review

### Architecture
```
Generator → Draft → Critic → [Pass → Done | Fail → Feedback Loop]
```

### ADK Implementation

```python
# The Generator
generator = LlmAgent(
    name="Generator",
    instruction="""
    Generate SQL query.
    If you receive {feedback}, fix errors and regenerate.
    """,
    output_key="draft"
)

# The Critic
critic = LlmAgent(
    name="Critic",
    instruction="""
    Check if {draft} is valid SQL.
    If correct, output 'PASS'.
    If not, output error details.
    """,
    output_key="feedback"
)

# The Loop Loop = LoopAgent(
    name="ValidationLoop",
    sub_agents=[generator, critic],
    condition_key="feedback",  # ← Checks this key
    exit_condition="PASS"       # ← Exits when feedback == "PASS"
)
```

### Key Concepts
- **Conditional Looping**: Continues until quality gate passes
- **Separation of Concerns**: Generator creates, Critic validates
- **Feedback Integration**: Generator receives specific improvement instructions

---

## Pattern 6: Iterative Refinement (Sculptor)

### When to Use
- Gradual improvement needed
- User feedback drives enhancement
- Quality improves with iterations

### Implementation Notes
Similar to Generator/Critic but driven by external feedback or metrics rather than binary pass/fail.

---

## Pattern 7: Human-in-the-Loop (Safety Net)

### When to Use
- High-risk decisions
- Legal/compliance review needed
- Actions require human approval

### Architecture
```
Agent → Proposal → Human Review → [Approve → Execute | Reject → Revise]
```

### Key Concepts
- Human becomes validation step in workflow
- Agent pauses and waits for approval
- Can combine with other patterns

---

## Pattern 8: Composite Patterns (Mix-and-Match)

### When to Use
- Complex workflows requiring multiple patterns
- Real-world production systems

### Example: Enterprise Code Review

```python
# Combines:
# - Hierarchical (top-level coordinator)
# - Parallel (multiple reviewers)
# - Generator/Critic (quality loops)
# - Human-in-Loop (final approval)

workflow = SequentialAgent(
    sub_agents=[
        # Step 1: Parallel analysis
        ParallelAgent(sub_agents=[security, style, performance]),
        
        # Step 2: Synthesize
        synthesis_agent,
        
        # Step 3: Human review
        human_approval_gate,
        
        # Step 4: Apply fixes (Generator/Critic loop)
        LoopAgent(sub_agents=[fixer, validator])
    ]
)
```

---

## 🏗️ **Context Architecture (Production-Scale)**

Google ADK uses a **tiered context model** to handle scaling:

### Tier 1: Working Context (Ephemeral)
- **What**: Prompt sent to LLM for this invocation
- **Contains**: System instructions, agent identity, selected history, tool outputs
- **Lifetime**: Single LLM call, then discarded
- **Key Insight**: Recomputed from durable state each time

### Tier 2: Session (Durable Log)
- **What**: Structured event stream of interaction
- **Contains**: Every message, tool call, result, error as typed Event objects
- **Lifetime**: Duration of conversation/workflow
- **Key Advantage**: Model-agnostic, supports time-travel debugging

### Tier 3: Memory (Long-term Knowledge)
- **What**: Searchable, persistent knowledge
- **Contains**: User preferences, past conversations, learned facts
- **Lifetime**: Outlives single sessions
- **Access**: Retrieved on-demand, not always in context

### Tier 4: Artifacts (Large Data)
- **What**: Files, logs, images
- **Lifetime**: Persistent
- **Access**: Referenced by name/version, not pasted into prompt

---

## 🔧 **Context Processing Pipeline**

ADK builds working context through **ordered processors**:

```python
# Example Flow Processors
self.request_processors += [
    basic.request_processor,           # Basic setup
    auth_preprocessor.request_processor,  # Authentication
    instructions.request_processor,    # System instructions
    identity.request_processor,        # Agent identity
    contents.request_processor,        # ← Session → Working Context
    context_cache_processor,           # Caching optimization
    planning.request_processor,        # Planning capabilities
    code_execution.request_processor,  # Tool execution
    output_schema_processor            # Structured output
]
```

### Key Concepts
- **Separation of Storage and Presentation**: Session stores full state, Working Context is computed view
- **Processor Pipeline**: Each step transforms context incrementally
- **Flexibility**: Add custom processors without rewriting entire system

---

## 📊 **Best Practices**

### 1. State Management
```python
# ✅ DO: Use unique output keys
agent_a = LlmAgent(output_key="agent_a_result")
agent_b = LlmAgent(output_key="agent_b_result")

# ❌ DON'T: Reuse keys in parallel agents
parallel_agent = ParallelAgent(sub_agents=[
    LlmAgent(output_key="result"),  # ← Race condition!
    LlmAgent(output_key="result")
])
```

### 2. Context Optimization
```python
# ✅ DO: Scope context to minimum needed
agent = LlmAgent(
    instruction="Use {relevant_data} only",  # ← Specific reference
    tools=[specific_tool]                     # ← Limited tool access
)

# ❌ DON'T: Flood context with everything
agent = LlmAgent(
    instruction=f"{entire_session_history}"  # ← Token waste
)
```

### 3. Error Handling
```python
# ✅ DO: Capture errors as structured events
try:
    result = agent.run()
except AgentError as e:
    session.add_event(ErrorEvent(error=str(e), agent=agent.name))
    
# ❌ DON'T: Let errors propagate silently
result = agent.run()  # ← No error handling
```

---

## 🚨 **Common Pitfalls**

### Pitfall 1: Over-Parallelization
**Problem**: Too many parallel agents create race conditions
**Solution**: Use ParallelAgent judiciously, ensure unique output keys

### Pitfall 2: Context Bloat
**Problem**: Appending everything to prompt causes cost/latency issues
**Solution**: Use tiered architecture, retrieve memory on-demand

### Pitfall 3: Rigid Hierarchies
**Problem**: Deep nesting makes debugging hard
**Solution**: Keep hierarchies shallow 2-3 levels), use Coordinator for routing

### Pitfall 4: No Human Oversight
**Problem**: Agents make high-risk decisions autonomously
**Solution**: Add Human-in-Loop for critical actions

---

## 📚 **References**

- **Source**: [Google Developers Blog - Multi-Agent Patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
- **Architecture**: [Context-Aware Multi-Agent Framework](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/)
- **Framework**: Google ADK (Agents Development Kit)

---

## 🎯 **When to Apply Each Pattern**

| Your Need | Pattern to Use |
|-----------|----------------|
| Process documents step-by-step | Sequential Pipeline |
| Route users to specialists | Coordinator/Dispatcher |
| Speed up independent tasks | Parallel Fan-Out/Gather |
| Break down complex goals | Hierarchical Decomposition |
| Ensure output quality | Generator and Critic |
| Improve over iterations | Iterative Refinement |
| Require human approval | Human-in-the-Loop |
| Complex real-world workflow | Composite Patterns |

---

**Last Updated**: 2026-01-23  
**Skill Level**: Advanced  
**Production Ready**: ✅ Yes (Google-validated patterns)
