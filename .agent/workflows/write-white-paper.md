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

## Phase 2: Research (Dream Team Mode)

### 2.1 Deploy Specialist Agents
// turbo
```powershell
# Deploy Researcher and Auditor for deep intel gathering
# Use templates from skills/soul-templates.md
```

### 2.2 Source Collection
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

### 3.1 First Draft (Operator Mode)
Follow `skills/autonomous-operator-directives.md` and anti-AI detection principles:
- **Autonomous Research**: If a fact is missing, the Operator MUST find it before proceeding.
- **FIO Protocol**: Resolve contradictions in sources independently.
- Vary sentence lengths (5-25 words)

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

---

## Phase 6: Distribution & Outreach

### 6.1 LinkedIn Article Publishing
Use the `linkedin-article-publisher.md` skill to distribute your white paper:
1. Run `parse_markdown.py` on your final white paper.
2. Follow the prompt template in the skill file to publish as a **DRAFT**.
3. Use the "Reverse Insertion" technique for high-fidelity image placement.

### 6.2 Cross-Platform Reach
- Adapt for Medium using `/medium-publish`.
- Share key insights as short-form posts linking to the long-form article.
```

---

## Output Deliverables

1. **White Paper Document** (Markdown or PDF)
2. **Executive Summary** (1-page standalone)
3. **Quality Report**: AI detection + plagiarism scores
4. **Source Bibliography**: All references in proper format
5. **LinkedIn Article**: Optimized for distribution via `linkedin-article-publisher.md`

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

- `/medium-publish` - Adapt for Medium publishing
- `/linkedin-publish` - Publish directly to LinkedIn Articles
- `/create-course` - Turn white paper into training course
- `/brainstorm` - Generate white paper topics
- `/documentation-maintenance` - Maintain technical documentation

---
