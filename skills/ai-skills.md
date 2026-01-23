# AI Integration Skills - OpenAI & LLMs

**Topics**: OpenAI, OpenRouter, DeepSeek, chat features, prompt engineering
**Version**: 1.0

---

## Skill #1: OpenAI/OpenRouter Setup

### When to Use
- Adding AI features to app
- Implementing chat assistant
- Task suggestions with AI

### Prompt Template

```markdown
**ROLE**: AI integration specialist

**PROVIDER**: [OpenAI / OpenRouter / Anthropic]
**MODEL**: [GPT-4 / DeepSeek / Claude]
**USE CASE**: [Chat assistant / Task generation / etc]

**SETUP (OpenRouter)**:
```python
import httpx
from typing import AsyncGenerator

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
AI_MODEL = "deepseek/deepseek-chat"  # Cost-effective!

async def chat_completion(
    messages: list[dict],
    stream: bool = False
) -> str | AsyncGenerator:
    """Call OpenRouter API"""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "TODO App"
            },
            json={
                "model": AI_MODEL,
                "messages": messages,
                "stream": stream,
                "temperature": 0.7,
                "max_tokens": 1000
            },
            timeout=30.0
        )
        
        if stream:
            return stream_response(response)
        else:
            data = response.json()
            return data["choices"][0]["message"]["content"]
```

**SETUP (OpenAI Direct)**:
```python
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def chat_completion(messages: list[dict]) -> str:
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content
```

**DELIVERABLES**:
- API client setup
- Chat completion function
- Error handling
- Cost consideration
```

### Cost Comparison:
- **OpenAI GPT-4**: ~$0.03 per 1K tokens
- **OpenRouter DeepSeek**: ~$0.0002 per 1K tokens (150x cheaper!)
- **OpenAI GPT-3.5**: ~$0.002 per 1K tokens

---

## Skill #2: Streaming Responses

### When to Use
- Real-time chat experience
- Long AI responses
- Better perceived performance

### Prompt Template

```markdown
**ROLE**: Streaming API specialist

**IMPLEMENT**: Server-Sent Events (SSE) for streaming AI responses

**BACKEND (FastAPI)**:
```python
from fastapi import StreamingResponse
from fastapi.responses import Response
import json

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def generate():
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    },
                    json={
                        "model": AI_MODEL,
                        "messages": request.messages,
                        "stream": True
                    }
                ) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]
                            if data == "[DONE]":
                                break
                            
                            try:
                                chunk = json.loads(data)
                                content = chunk["choices"][0]["delta"].get("content", "")
                                if content:
                                    yield f"data: {json.dumps({'content': content})}\n\n"
                            except:
                                continue
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

**FRONTEND (React)**:
```typescript
const [messages, setMessages] = useState<Message[]>([])
const [streaming, setStreaming] = useState(false)

async function sendMessage(content: string) {
  setStreaming(true)
  const newMessage = { role: 'assistant', content: '' }
  setMessages(prev => [...prev, newMessage])
  
  const response = await fetch('/api/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages: [...messages, { role: 'user', content }] })
  })
  
  const reader = response.body?.getReader()
  const decoder = new TextDecoder()
  
  while (true) {
    const { done, value } = await reader!.read()
    if (done) break
    
    const text = decoder.decode(value)
    const lines = text.split('\n').filter(line => line.startsWith('data: '))
    
    for (const line of lines) {
      const data = JSON.parse(line.slice(6))
      if (data.content) {
        setMessages(prev => {
          const updated = [...prev]
          updated[updated.length - 1].content += data.content
          return updated
        })
      }
    }
  }
  
  setStreaming(false)
}
```

**DELIVERABLES**:
- Streaming backend endpoint
- Frontend SSE client
- Loading states
- Error handling
```

### Benefits of Streaming:
- User sees response immediately
- Better perceived performance
- Can cancel long responses
- More interactive feel

---

## Skill #3: Context Management & Prompts

### When to Use
- Improving AI responses
- Adding app context
- Crafting effective prompts

### Prompt Template

```markdown
**ROLE**: Prompt engineering specialist

**USE CASE**: [Task suggestions / Chat assistant / etc]

**SYSTEM PROMPT**:
```python
SYSTEM_PROMPT = """You are a helpful AI assistant for a TODO task 
management application. You help users:

1. Create and organize tasks
2. Suggest priorities and deadlines
3. Break down large tasks into smaller ones
4. Provide productivity tips

Current context:
- User has {task_count} active tasks
- Most urgent task: {urgent_task}
- User's productivity pattern: {pattern}

Be concise, actionable, and friendly. Suggest specific next steps."""

# Example usage
async def chat_with_context(user_message: str, user_id: str):
    # Get user context
    tasks = await get_user_tasks(user_id)
    task_count = len(tasks)
    urgent_task = get_most_urgent(tasks)
    
    # Build context-aware system prompt
    system_prompt = SYSTEM_PROMPT.format(
        task_count=task_count,
        urgent_task=urgent_task.title if urgent_task else "None",
        pattern="morning person"  # Could be learned
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    return await chat_completion(messages)
```

**PROMPT TEMPLATES**:
```python
# Task creation from natural language
TASK_CREATION_PROMPT = """Extract a structured task from this message:
"{user_input}"

Return JSON:
{{
  "title": "Short task title",
  "description": "Detailed description",
  "priority": "low|medium|high",
  "estimated_time": "e.g., 30 minutes",
  "suggested_due_date": "YYYY-MM-DD or null"
}}"""

# Task breakdown
TASK_BREAKDOWN_PROMPT = """Break down this large task into smaller subtasks:
"{task_title}"

Return a numbered list of 3-5 actionable subtasks."""
```

**DELIVERABLES**:
- System prompt template
- Context injection logic
- Specific use-case prompts
- Response parsing
```

### Prompt Engineering Tips:
1. Be specific about desired format
2. Provide relevant context
3. Use examples (few-shot learning)
4. Set temperature (0.7 for creative, 0.2 for factual)
5. Limit max_tokens to control cost
6. Test and iterate prompts

---

## Skill #4: Rate Limiting & Cost Control

### When to Use
- Preventing API abuse
- Controlling costs
- Production deployment

### Prompt Template

```markdown
**ROLE**: AI cost optimization specialist

**IMPLEMENT**: Rate limiting and cost controls

**RATE LIMITING**:
```python
from fastapi import HTTPException
from collections import defaultdict
from datetime import datetime, timedelta

# Simple in-memory rate limiter
rate_limits = defaultdict(list)
MAX_REQUESTS_PER_HOUR = 100

async def check_rate_limit(user_id: str):
    now = datetime.now()
    hour_ago = now - timedelta(hours=1)
    
    # Clean old requests
    rate_limits[user_id] = [
        req_time for req_time in rate_limits[user_id]
        if req_time > hour_ago
    ]
    
    # Check limit
    if len(rate_limits[user_id]) >= MAX_REQUESTS_PER_HOUR:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )
    
    # Record request
    rate_limits[user_id].append(now)

@router.post("/chat")
async def chat(request: ChatRequest, user_id: str = Depends(get_user_id)):
    await check_rate_limit(user_id)
    # ... proceed with chat
```

**COST TRACKING**:
```python
import tiktoken

def estimate_cost(text: str, model: str = "gpt-4") -> float:
    """Estimate API cost before making request"""
    encoding = tiktoken.encoding_for_model(model)
    tokens = len(encoding.encode(text))
    
    # Pricing (example)
    costs = {
        "gpt-4": 0.03 / 1000,           # $0.03 per 1K tokens
        "gpt-3.5-turbo": 0.002 / 1000,  # $0.002 per 1K tokens
        "deepseek": 0.0002 / 1000        # $0.0002 per 1K tokens
    }
    
    return tokens * costs.get(model, 0.03)

# Log costs
import logging

async def chat_with_tracking(messages: list[dict]):
    input_text = " ".join([m["content"] for m in messages])
    estimated_cost = estimate_cost(input_text)
    
    logging.info(f"AI request - Estimated cost: ${estimated_cost:.4f}")
    
    response = await chat_completion(messages)
    return response
```

**CACHING**:
```python
from functools import lru_cache

# Cache common queries
@lru_cache(maxsize=100)
def get_cached_response(query: str) -> str | None:
    # Check if we've seen this exact query before
    # Could use Redis for distributed caching
    pass
```

**DELIVERABLES**:
- Rate limiting implementation
- Cost estimation
- Usage logging
- Caching strategy
```

### Cost Saving Strategies:
1. Use cheaper models (DeepSeek via OpenRouter)
2. Cache common responses
3. Limit max_tokens
4. Set rate limits per user
5. Use streaming to allow cancellation
6. Monitor usage with logging
7. Implement user tiers (free/paid)

---

## Quick Reference

### OpenRouter Models
```python
# Cost-effective
"deepseek/deepseek-chat"          # $0.0002/1K tokens
"meta-llama/llama-3-8b-instruct"  # $0.0001/1K tokens

# Balanced
"anthropic/claude-3-haiku"        # $0.003/1K tokens
"openai/gpt-3.5-turbo"            # $0.002/1K tokens

# Premium
"openai/gpt-4"                    # $0.03/1K tokens
"anthropic/claude-3-opus"         # $0.075/1K tokens
```

### Common Patterns
```python
# Simple completion
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Help me organize my tasks"}
]
response = await chat_completion(messages)

# Multi-turn conversation
conversation = []
conversation.append({"role": "user", "content": "First question"})
response1 = await chat_completion(conversation)
conversation.append({"role": "assistant", "content": response1})
conversation.append({"role": "user", "content": "Follow-up question"})
response2 = await chat_completion(conversation)

# With context
system_msg = f"User has {len(tasks)} tasks. Help them prioritize."
messages = [
    {"role": "system", "content": system_msg},
    {"role": "user", "content": user_question}
]
```

---

## Lessons Learned

### Provider Choice
1. **OpenRouter** is cost-effective (DeepSeek model)
2. **OpenAI** for best quality (GPT-4)
3. Test different models for your use case
4. Monitor costs in production
5. Have fallback providers

### Streaming
1. Much better UX than waiting
2. Users can see progress
3. Can cancel if going wrong
4. Slightly more complex to implement
5. Handle connection drops gracefully

### Prompt Engineering
1. Be specific about format
2. Include relevant context
3. Test prompts extensively
4. Iterate based on results
5. Use system messages for behavior

### Cost Control
1. Always implement rate limiting
2. Track usage per user
3. Set max_tokens wisely
4. Cache when possible
5. Use cheaper models for simple tasks

---

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Rate limit exceeded" | Too many requests | Implement rate limiting |
| Timeout errors | Long response | Increase timeout, use streaming |
| High costs | Inefficient prompts | Optimize prompts, use cheaper model |
| Poor quality responses | Bad prompts | Improve system message, add context |
| Inconsistent formatting | No format specification | Use JSON mode or strict prompts |

---

## Related Skills
- Phase 3: AI chat implementation
- Backend Skills: Async operations
- Frontend Skills: Streaming UI
- Debug Skills: API debugging

**AI features add magic - but manage costs carefully!**
