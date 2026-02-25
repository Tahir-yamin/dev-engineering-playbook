---
description: Step-by-step guide for implementing new functionality in your application
---

# Adding New Feature Workflow

## When to Use
- Implementing new functionality
- Adding new page or component
- Creating new API endpoint

---

## Step 1: Plan the Feature

Define:
- What it does
- API endpoints needed (if any)
- Database changes needed (if any)
- UI components needed

---

## Step 2: Database Changes (if needed)

Use @.claude/database-skills.md Skill #4

```bash
# Update Prisma schema
# Create migration
npx prisma migrate dev --name feature_name

# Test migration
npx prisma studio
```

---

## Step 3: Backend Implementation

Use @.claude/backend-skills.md

1. Create Pydantic schemas (models/schemas.py)
2. Add router (backend/routers/feature.py)
3. Implement endpoints
4. Add to main.py
5. Test with docs (/docs)

Example:
```python
# routers/feature.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/feature")
async def get_feature():
    return {"message": "Feature works"}
```

```python
# main.py
from routers import feature

app.include_router(feature.router, prefix="/api/feature", tags=["feature"])
```

---

## Step 4: Frontend Implementation

Use @.claude/frontend-skills.md

1. Create components (components/Feature.tsx)
2. Add API integration
3. Implement UI
4. Add routing (if new page)
5. Handle loading/error states

Example:
```typescript
// components/Feature.tsx
'use client'

export function Feature() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    fetch('/api/feature')
      .then(r => r.json())
      .then(setData)
      .finally(() => setLoading(false))
  }, [])
  
  if (loading) return <div>Loading...</div>
  return <div>{data?.message}</div>
}
```

---

## Step 5: Testing

Test:
- [ ] API endpoints work
- [ ] UI renders correctly
- [ ] Error handling works
- [ ] Loading states show
- [ ] Edge cases handled

---

## Step 6: Integration

Test full flow:
1. User action → Backend → Database → Response → UI update

Check:
- Network tab (request/response)
- Console (no errors)
- State updates correctly
- UI reflects changes

---

## Step 7: Commit

// turbo
```bash
git add .
git commit -m "feat: add [feature name]"
```

---

**Related Skills**: phase2/3-skills.md, backend-skills.md, frontend-skills.md
