# OpenRouter API Integration Skills

**Purpose**: Integrate and troubleshoot OpenRouter API for AI chat functionality  
**Source**: Todo Hackathon Phase 5 - AI assistant integration  
**Date**: January 2026

---

## Skill #1: Setting Up OpenRouter API

### When to Use
- Need free AI API access for development
- Want to avoid OpenAI API costs
- Testing AI chat functionality

### The Problem
OpenAI API requires payment, need free alternative for development/testing.

### The Solution

**Step 1: Get API key**
1. Visit: https://openrouter.ai
2. Sign up with GitHub
3. Navigate to "Keys" section
4. Create new API key
5. Copy key (starts with `sk-or-...`)

**Step 2: Store in Kubernetes Secret**
```bash
# Create secret
kubectl create secret generic openrouter-secret \
  --from-literal=api-key='sk-or-v1-YOUR-KEY-HERE' \
  -n todo-chatbot

# Verify
kubectl get secret openrouter-secret -n todo-chatbot
```

**Step 3: Reference in deployment**
```yaml
# In your deployment
env:
  - name: OPENROUTER_API_KEY
    valueFrom:
      secretKeyRef:
        name: openrouter-secret
        key: api-key
```

**Step 4: Use in FastAPI**
```python
import os
import httpx

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

async def call_ai(messages):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Todo Chatbot"
            },
            json={
                "model": "mistralai/devstral-2512:free",
                "messages": messages
            }
        )
        return response.json()
```

### Key Insights
- ✅ Free tier available: `mistralai/devstral-2512:free`
- ✅ Compatible with OpenAI SDK
- ✅ No credit card required
- 💡 Rate limits apply to free tier

---

## Skill #2: Choosing the Right Free Model

### When to Use
- Optimizing for cost/performance
- Understanding model capabilities
- Staying within rate limits

### The Problem
Different free models have different capabilities and limits.

### The Solution

**Free models on OpenRouter**:

| Model | Best For | Strengths | Limits |
|-------|----------|-----------|--------|
| `mistralai/devstral-2512:free` | Development | Good reasoning | 30 req/min |
| `google/gemini-flash-1.5:free` | Speed | Fast responses | 15 req/min |
| `meta-llama/llama-3.1-8b-instruct:free` | Balance | Open source | 20 req/min |

**How to switch models**:
```python
# In your code
MODEL = "mistralai/devstral-2512:free"  # Change this

response = await client.post(
    f"{OPENROUTER_BASE_URL}/chat/completions",
    json={"model": MODEL, "messages": messages}
)
```

**Via environment variable** (better):
```python
MODEL = os.getenv("AI_MODEL", "mistralai/devstral-2512:free")
```

### Key Insights
- ✅ Mistral: Best for task management reasoning
- ✅ Gemini Flash: Best for quick responses
- ✅ LLaMA: Good balance, open source
- 💡 Test locally before deploying to production

---

## Skill #3: Debugging OpenRouter API Errors

### When to Use
- Getting 500 errors from chat endpoint
- API key not working
- Rate limit issues

### The Problem
OpenRouter API errors can be cryptic or hidden in backend logs.

### The Solution

**Check API key is loaded**:
```bash
# Exec into backend pod
kubectl exec -it deployment/todo-chatbot-backend -n todo-chatbot -c backend -- /bin/sh

# Check env var
echo $OPENROUTER_API_KEY

# Should start with: sk-or-v1-
```

**Test API key directly**:
```bash
# From your machine
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer sk-or-v1-YOUR-KEY"

# Should return list of models
```

**Common errors and fixes**:

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Invalid API key | Regenerate key, update secret |
| `429 Too Many Requests` | Rate limit hit | Wait 60s or upgrade plan |
| `500 Internal Server Error` | Model misconfigured | Check model name spelling |
| `Connection timeout` | Network issue | Increase timeout to 30s |

**Enable debug logging**:
```python
# In your code
import logging
logging.basicConfig(level=logging.DEBUG)

# Or specific to httpx
logging.getLogger("httpx").setLevel(logging.DEBUG)
```

### Key Insights
- ✅ Always verify secret is mounted correctly
- ✅ Test API key with curl before debugging code
- ✅ Check backend logs for actual error message
- 💡 Rate limits reset every minute

---

## Skill #4: Handling MCP Tool Calls with OpenRouter

### When to Use
- Integrating MCP tools with AI responses
- Need AI to execute task operations
- Building function-calling workflows

### The Problem
MCP tools need to be formatted correctly for OpenRouter's function-calling.

### The Solution

**Define tools in OpenRouter format**:
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["TODO", "IN_PROGRESS", "DONE"],
                        "description": "Filter by status"
                    }
                }
            }
        }
    }
]
```

**Send with tool support**:
```python
response = await client.post(
    f"{OPENROUTER_BASE_URL}/chat/completions",
    json={
        "model": "mistralai/devstral-2512:free",
        "messages": messages,
        "tools": tools,  # Include tool definitions
        "tool_choice": "auto"  # Let AI decide when to use
    }
)
```

**Handle tool calls**:
```python
response_data = response.json()
message = response_data["choices"][0]["message"]

if message.get("tool_calls"):
    for tool_call in message["tool_calls"]:
        function_name = tool_call["function"]["name"]
        arguments = json.loads(tool_call["function"]["arguments"])
        
        # Execute the tool
        result = await execute_mcp_tool(function_name, arguments)
        
        # Send result back to AI
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": json.dumps(result)
        })
```

### Key Insights
- ✅ Not all models support function calling
- ✅ Mistral and GPT models work well
- ✅ Always handle missing tool_calls gracefully
- 💡 Test tools one at a time

---

## Skill #5: Optimizing API Costs and Performance

### When to Use
- Moving to production
- High chat volume
- Want faster responses

### The Problem
Free tier has rate limits, paid tier can get expensive.

### The Solution

**Optimization strategies**:

**1. Cache common responses**:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_static_response(question_hash):
    # For FAQ-type questions
    return cached_response
```

**2. Use streaming for better UX**:
```python
response = await client.post(
    f"{OPENROUTER_BASE_URL}/chat/completions",
    json={
        "model": MODEL,
        "messages": messages,
        "stream": True  # Enable streaming
    }
)

async for chunk in response.aiter_lines():
    # Send chunks to frontend
    yield chunk
```

**3. Implement rate limiting**:
```python
from fastapi import HTTPException
from collections import defaultdict
from time import time

rate_limit = defaultdict(list)

def check_rate_limit(user_id, max_requests=10, window=60):
    """Allow max_requests per window (seconds)"""
    now = time()
    requests = rate_limit[user_id]
    
    # Remove old requests
    requests = [r for r in requests if r > now - window]
    
    if len(requests) >= max_requests:
        raise HTTPException(429, "Rate limit exceeded")
    
    requests.append(now)
    rate_limit[user_id] = requests
```

**4. Switch to faster models for simple queries**:
```python
def select_model(message):
    """Use faster/cheaper model for simple queries"""
    if len(message) < 50:
        return "google/gemini-flash-1.5:free"  # Fast
    else:
        return "mistralai/devstral-2512:free"  # Better reasoning
```

### Key Insights
- ✅ Cache FAQ responses
- ✅ Use streaming for better perceived performance
- ✅ Implement your own rate limiting
- 💡 Profile which queries need powerful models

---

## Quick Reference

### OpenRouter Endpoints
```
Base URL: https://openrouter.ai/api/v1
Models:   GET  /models
Chat:     POST /chat/completions
```

### Free Models
```python
"mistralai/devstral-2512:free"          # Best reasoning
"google/gemini-flash-1.5:free"          # Fastest
"meta-llama/llama-3.1-8b-instruct:free" # Balanced
```

### Request Format
```python
{
    "model": "mistralai/devstral-2512:free",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"}
    ],
    "temperature": 0.7,
    "max_tokens": 500
}
```

### Required Headers
```python
{
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "http://your-domain.com",
    "X-Title": "Your App Name"
}
```

---

**Total Skills**: 5  
**Last Updated**: January 18, 2026  
**Production Tested**: ✅ Todo Hackathon Phase 5
