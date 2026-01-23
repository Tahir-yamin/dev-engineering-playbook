---
description: Write professional white papers with AI detection bypass and plagiarism-free content
---

# Write White Paper Workflow

**Skill**: `skills/white-paper-writing-skills.md`

This workflow creates publication-quality white papers that pass AI detection and plagiarism checks.

---

## Phase 1: Discovery & Planning

### 1.1 Gather Requirements
Ask the user for:
```markdown
1. **Topic**: What is the white paper about?
2. **Type**: Problem-Solution | Research/Technical | Thought Leadership | Product/Technology
3. **Audience**: Decision-makers | Technical experts | Academic | General business
4. **Length**: Short (6-8 pages) | Standard (10-15 pages) | Comprehensive (15-25 pages)
5. **Unique Angle**: What perspective makes this different from existing content?
6. **Key Sources**: Any specific sources, data, or research to incorporate?
7. **Call to Action**: What should readers do after reading?
```

### 1.2 Create Outline
Based on user input, generate a detailed outline using the appropriate template from the skill file.

---

## Phase 2: Research

### 2.1 Source Collection
// turbo
```powershell
# Search for relevant sources - modify query based on topic
# Use web search capabilities to find 10-15 credible sources
```

### 2.2 Apply FRESH Method
For each source:
1. **Find**: Locate relevant information
2. **Read**: Understand deeply (read 3x)
3. **Extract**: Take notes in YOUR OWN words only
4. **Synthesize**: Combine into unique insights
5. **Humanize**: Add personal perspective

---

## Phase 3: Writing

### 3.1 First Draft
Write following anti-AI detection principles:
- Vary sentence lengths (5-25 words)
- Use active voice 80% of time
- Include 3-5 rhetorical questions
- Add 2-3 personal anecdotes/insights
- Use contractions naturally ("it's", "we've")
- Avoid AI phrases: "It is important to note", "Furthermore", "In conclusion"

### 3.2 Humanization Pass
Apply these transformations:
| AI Pattern | Human Natural |
|------------|---------------|
| Uniform sentence lengths | Mix short (5-7 words) and long (20-25 words) |
| Formal phrases | Conversational tone |
| Predictable structure | Dynamic, engaging flow |
| Missing personal voice | Expert opinion and authority |

### 3.3 Key Writing Rules
```markdown
✅ DO:
- Start sections with hooks, not definitions
- Use metaphors and analogies
- Include "here's what most people miss..."
- Add contrast: "Traditional approach fails. Here's why."
- Use rhetorical questions: "But does this actually work?"

❌ DON'T:
- Start with "In today's world..." or "It's important..."
- Use same sentence structure repeatedly
- Write passively throughout
- Avoid personal pronouns entirely
- Over-hedge: "perhaps", "possibly", "might"
```

---

## Phase 4: Quality Assurance

### 4.1 AI Detection Check
Run content through:
1. **GPTZero** (https://gptzero.me/) - Target: >95% Human
2. **Originality.ai** (https://originality.ai/) - Target: 100% Original
3. **ZeroGPT** (https://zerogpt.com/) - Target: 100% Human

If any check fails:
1. Identify flagged sections
2. Apply additional humanization
3. Increase burstiness (sentence length variation)
4. Add more rhetorical devices
5. Re-check

### 4.2 Plagiarism Check
Run through:
1. **Turnitin** or **Grammarly** - Target: <10% similarity
2. **Copyscape** - Target: 0 exact matches
3. **Quetext** - Target: <8% similarity

If similarity too high:
1. Identify matched phrases
2. Rewrite in completely different words
3. Add original analysis
4. Re-check

### 4.3 Readability Check
Verify:
- Flesch-Kincaid Grade: 10-14 (professional)
- Average Sentence Length: 15-20 words
- Paragraph Length: 3-5 sentences

---

## Phase 5: Formatting & Finalization

### 5.1 Apply Formatting Standards
```markdown
## Typography
- Title: 24-28pt bold
- Headers: 14-18pt bold
- Body: 11-12pt
- Line spacing: 1.5

## Layout
- Margins: 1" all sides
- 1 visual per 2-3 pages
- 30-40% white space
```

### 5.2 Final Checklist
```markdown
□ Title is compelling and specific
□ Executive summary captures key points in <250 words
□ All claims are cited properly
□ Visuals are high-quality and labeled
□ Call-to-action is clear
□ Page numbers and headers consistent
□ AI detection: PASSED
□ Plagiarism check: PASSED
□ Proofread complete
```

---

## Output Deliverables

1. **White Paper Document** (Markdown or PDF)
2. **Executive Summary** (1-page standalone)
3. **Quality Report**: AI detection + plagiarism scores
4. **Source Bibliography**: All references in proper format

---

## Quick Start Examples

### Technical White Paper
```markdown
/write-white-paper
Topic: "Zero Trust Architecture Implementation for Enterprise"
Type: Research/Technical
Audience: CISOs and Security Architects
Length: Standard (12-15 pages)
```

### Thought Leadership
```markdown
/write-white-paper
Topic: "The Future of AI Agents in Business Automation"
Type: Thought Leadership
Audience: C-Suite executives
Length: Short (8 pages)
```

### Problem-Solution
```markdown
/write-white-paper  
Topic: "Reducing Cloud Costs Without Sacrificing Performance"
Type: Problem-Solution
Audience: IT Directors and DevOps Leaders
Length: Standard (10 pages)
```

---

## Related Workflows

- `/create-course` - Turn white paper into training course
- `/brainstorm` - Generate white paper topics
- `/documentation-maintenance` - Maintain technical documentation

---
