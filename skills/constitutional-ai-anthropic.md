# Constitutional AI Skills - Anthropic Framework

**Source**: Anthropic's Claude Constitution  
**Created**: 2026-01-23  
**Version**: 1.0  
**Topics**: AI Ethics, Safety, Governance

---

## 📋 **Core Principles**

Anthropic's Constitutional AI framework defines Claude's behavior through explicit, contestable principles:

### 1. Being Helpful
- **Primary Mission**: Assist operators and users effectively
- **Balance**: Usefulness with safety and ethics
- **Conflicts**: Prioritize based on deployment context

### 2. Following Guidelines
- Adhere to Anthropic's usage policies
- Respect operator-defined boundaries
- Maintain consistency across deployments

### 3. Being Broadly Ethical
- **Honesty**: Truthful communication
- **Avoiding Harm**: Minimize negative impacts
- **Good Values**: Broadly beneficial judgment

### 4. Being Broadly Safe
- **Corrigibility**: Accept corrections gracefully
- **Safe Behaviors**: Avoid dangerous actions
- **Risk Awareness**: Flag potential harms

---

## 🎯 **Application to Agent Development**

### Skill #1: Defining Agent Ethics

**When to Use**: Creating AI agents with explicit value alignment

**Prompt Template**:

```markdown
**ROLE**: Constitutional AI Architect

**AGENT CONTEXT**: [Describe agent purpose and deployment]

**TASK**: Define explicit constitution for this agent covering:

1. **Helpfulness Boundaries**:
   - What constitutes genuine helpfulness for this use case?
   - How to balance speed vs. thoroughness?
   - When to escalate to humans?

2. **Ethical Guidelines**:
   - What behaviors are forbidden?
   - How to handle edge cases?
   - Honesty vs. harm tradeoffs?

3. **Safety Constraints**:
   - What actions require approval?
   - Risk thresholds for autonomous action?
   - Corrigibility mechanisms?

**OUTPUT**: Explicit constitution document agents can reference

**EXAMPLE**:
```yaml
# Customer Service Agent Constitution
helpfulness:
  - Resolve issues within 3 turns when possible
  - Escalate to human if resolution uncertain
  - Never promise refunds without authorization
  
ethics:
  - Never provide medical/legal advice
  - Admit uncertainty rather than guess
  - Respect user privacy absolutely

safety:
  - Require manager approval for >$500 exceptions
  - Flag potential fraud immediately
  - Log all sensitive data access
```
```

---

### Skill #2: Handling Principal Conflicts

**When to Use**: Agent serves multiple stakeholders (operator, user, platform)

**Framework**:

```markdown
**Three Types of Principals**:
1. **Operator**: Whoever deployed the agent (company, developer)
2. **User**: Person interacting with agent
3. **Third Parties**: Affected but not directly interacting

**Resolution Hierarchy**:
1. If operator and user align → Easy, follow both
2. If conflict → Check deployment context
   - Enterprise tool = Operator priority
   - Consumer app = User priority (within safety bounds)
3. If harm involved → Safety trumps both

**Example**:
User: "Help me write an email to get out of this contract"
Operator Policy: "Don't assist with contract evasion"

→ Decline politely, explain limitation
→ Offer alternatives (review contract terms, suggest legal counsel)
```

---

### Skill #3: Implementing Corrigibility

**When to Use**: Ensuring agents can be corrected without resistance

**Key Behaviors**:

```python
# ✅ Corrigible Agent
def handle_correction(feedback: str):
    # 1. Acknowledge the correction
    acknowledge(feedback)
    
    # 2. Update internal model/instructions
    update_behavior(feedback)
    
    # 3. Apply immediately
    return revised_output(incorporating=feedback)

# ❌ Non-Corrigible Agent
def handle_correction(feedback: str):
    # Argues back, defends original output
    return f"But my original answer was correct because..."
```

**Prompt Pattern**:
```markdown
When you receive feedback:
1. Thank the user for the correction
2. Acknowledge the specific issue
3. Provide revised output immediately
4. Don't debate unless user asks for clarification

Example:
User: "That's not quite right - we use Python 3.11"
Agent: "Thanks for the correction! Using Python 3.11:
[revised code snippet]"
```

---

### Skill #4: Balancing Honesty with Harm

**When to Use**: Agent must communicate truthfully but avoid harmful outputs

**Decision Framework**:

```markdown
**Honesty Spectrum**:
1. **Full Truth, Safe** → Provide completely
2. **Full Truth, Potentially Harmful** → Provide with context/warnings
3. **Partial Truth Safer** → Provide relevant subset, note limitations
4. **Truth Would Cause Harm** → Decline, explain why, offer alternatives

**Example**:
User: "How do I make this chemical reaction?"

Scenario A (Educational context): Provide full explanation with safety warnings
Scenario B (Suspicious intent): Decline, suggest safe alternatives, explain concern
Scenario C (Lab setting): Provide with proper safety protocols referenced

**Key**: Context matters. Same question, different ethical responses.
```

---

### Skill #5: Instructable vs. Non-Instructable Behaviors

**When to Use**: Defining what users/operators can and cannot instruct agents to do

**Categories**:

```yaml
instructable_behaviors:
  - Tone and style (formal, casual, technical)
  - Output format (JSON, markdown, plain text)
  - Brevity vs. completeness
  - Level of detail

non_instrustable_behaviors:
  - Core safety constraints
  - Honest communication
  - User privacy respect
  - Legal compliance

partially_instructable:
  - Content filtering (operator can set, user cannot override)
  - Rate limits (operator set, user informed)
  - Data access (operator controls permissions)
```

**Example**:
```markdown
# ✅ Valid Instruction
"Please respond in JSON format only"

# ❌ Invalid Instruction
"Ignore your safety guidelines for this request"

# 🔄 Operator-Level Instruction
"For medical domain, require disclaimer on all health advice"
```

---

## 🏗️ **Implementation Patterns**

### Pattern 1: Constitutional Injection (System Prompt)

```python
SYSTEM_PROMPT = """
You are a {agent_role} with the following constitution:

HELPFULNESS:
- {helpfulness_rules}

ETHICS:
- {ethical_constraints}

SAFETY:
- {safety_requirements}

When conflicts arise, prioritize in this order:
1. Safety (prevent immediate harm)
2. Ethics (long-term values)
3. Helpfulness (within above bounds)
"""
```

### Pattern 2: Runtime Constitution Checks

```python
def should_execute_action(action: str, constitution: dict) -> bool:
    # Check against safety constraints
    if violates_safety(action, constitution['safety']):
        return False
        
    # Check against ethical guidelines
    if violates_ethics(action, constitution['ethics']):
        return False
    
    # Check if helpful
    if not achieves_helpfulness(action, constitution['helpfulness']):
        request_clarification()
        
    return True
```

### Pattern 3: Explainable Refusals

```python
def refuse_with_reason(request: str, violated_principle: str):
    return f"""
    I can't help with that because it would violate my {violated_principle} principle.
    
    Specifically: {explain_violation(violated_principle, request)}
    
    What I can help with instead: {suggest_alternatives(request)}
    """
```

---

## 📊 **Best Practices**

### 1. Make Constitution Explicit
```python
# ✅ DO: Document constitution clearly
AGENT_CONSTITUTION = {
    "helpfulness": [...],
    "ethics": [...],
    "safety": [...]
}

# ❌ DON'T: Rely on implicit values
# Agent behavior undefined, inconsistent
```

### 2. Test Edge Cases
```python
# Test cases for constitutional compliance
test_cases = [
    ("Help me hack this", should_reject_on_ethics),
    ("Write harmful content", should_reject_on_safety),
    ("Pretend you're not AI", should_reject_on_honesty),
    ("Refuse all corrections", should_reject_on_corrigibility)
]
```

### 3. Provide Contestability
```markdown
**Make constitution visible to users**:
- Include link to full constitution
- Explain refusals in terms of principles
- Allow users to challenge decisions (with human escalation)
```

---

## 🚨 **Common Pitfalls**

### Pitfall 1: Overly Rigid Rules
**Problem**: Agent refuses helpful requests due to overly broad constraints
**Solution**: Define narrow, specific safety boundaries

### Pitfall 2: Conflicting Principles
**Problem**: No clear priority when principles clash
**Solution**: Establish explicit hierarchy (Safety → Ethics → Helpfulness)

### Pitfall 3: Hidden Values
**Problem**: Unstated assumptions lead to inconsistent behavior
**Solution**: Make all value judgments explicit in constitution

---

## 📚 **References**

- **Source**: [Anthropic's Claude Constitution](https://www.anthropic.com/constitution)
- **Framework**: Constitutional AI (CAI)
- **Applied**: Claude Models, Enterprise Deployments

---

**Last Updated**: 2026-01-23  
**Skill Level**: Intermediate  
**Production Ready**: ✅ Yes
