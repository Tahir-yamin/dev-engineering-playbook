---
description: Fix slow page loads, laggy interactions, and optimize application performance
---

# Performance Problems Workflow

## When to Use
- Slow page load
- Laggy interactions
- High memory usage
- Unresponsive UI

---

## Step 1: Measure Performance

Use Chrome DevTools:
1. Press F12 (Windows) or Cmd+Option+I (Mac)
2. Go to Performance tab
3. Click Record
4. Interact with app
5. Stop recording

Look for:
- Long tasks (>50ms) - yellow/red bars
- Layout shifts
- Large bundles

---

## Step 2: Identify Bottleneck

### Slow Initial Load
Causes:
- Large JavaScript bundle
- Unoptimized images
- Too many API calls
- No code splitting

### Laggy Interactions
Causes:
- Too many re-renders
- Heavy computations in render
- No virtualization for long lists
- Blocking main thread

### Slow API Responses
Causes:
- N+1 query problem
- Missing database indexes
- No caching
- Inefficient queries

---

## Step 3: Frontend Optimizations

### Reduce Bundle Size

```typescript
// Use dynamic imports
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />
})
```

### Optimize Re-renders

```typescript
// Use React.memo
const TaskCard = React.memo(({ task }) => {
  return <div>{task.title}</div>
})

// Use useCallback
const handleDelete = useCallback((id) => {
  deleteTask(id)
}, [deleteTask])
```

**Reference**: @.claude/frontend-skills.md Skill #2

### Optimize Images

```typescript
// Use Next.js Image
import Image from 'next/image'

<Image 
  src="/image.jpg"
  width={500}
  height={300}
  alt="Description"
/>
```

### Virtual Scrolling

```typescript
// For lists with 100+ items
import { FixedSizeList } from 'react-window'

<FixedSizeList
  height={600}
  itemCount={1000}
  itemSize={50}
>
  {Row}
</FixedSizeList>
```

---

## Step 4: Backend Optimizations

### Fix N+1 Queries

```typescript
// Bad: N+1 problem
const tasks = await prisma.task.findMany()
for (const task of tasks) {
  const user = await prisma.user.findUnique({ where: { id: task.userId }})
}

// Good: Include relation
const tasks = await prisma.task.findMany({
  include: { user: true }
})
```

**Reference**: @.claude/database-skills.md Skill #5

### Add Database Indexes

```prisma
model Task {
  id String @id
  userId String
  
  @@index([userId])  // Index for faster filtering
}
```

### Implement Caching

```typescript
// Frontend: Use SWR
import useSWR from 'swr'

const { data: tasks } = useSWR('/api/tasks', fetcher, {
  revalidateOnFocus: false,
  dedupingInterval: 60000  // Cache for 1 minute
})
```

---

## Step 5: Measure Improvement

Use Chrome DevTools Performance tab again and compare:
- Load time
- Time to Interactive
- Bundle size
- Number of re-renders

---

**Related Skills**: frontend-skills.md #2, database-skills.md #5, debug-skills.md #6
