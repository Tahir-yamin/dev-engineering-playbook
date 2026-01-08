# Frontend Skills - Next.js & React

**Topics**: Next.js 14, React, TailwindCSS, UI components, performance
**Version**: 1.0

---

## Skill #1: Next.js App Router Patterns

### When to Use
- Building pages with App Router
- Understanding server vs client components
- Implementing layouts and route groups

### Prompt Template

```markdown
**ROLE**: Next.js 14 specialist

**TASK**: [Build page / Optimize routing / Debug issue]

**APP ROUTER STRUCTURE**:
```
app/
├── layout.tsx          # Root layout (Server Component)
├── page.tsx            # Home page
├── dashboard/
│   ├── layout.tsx      # Dashboard layout
│   └── page.tsx        # Dashboard page
└── api/
    └── auth/
        └── [...all]/route.ts  # API route
```

**SERVER VS CLIENT**:
```typescript
// Server Component (default)
async function ServerPage() {
  const data = await fetch('...') // Can fetch directly
  return <div>{data}</div>
}

// Client Component (interactive)
'use client'
function ClientComponent() {
  const [count, setCount] = useState(0) // Can use hooks
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

**DELIVERABLES**:
- Page/layout structure
- Server/client component decisions
- Data fetching strategy
- Loading/error states
```

### Key Patterns:
- **Server Components**: Default, can fetch data, no interactivity
- **Client Components**: `'use client'` directive, hooks, event handlers
- **Layouts**: Shared UI, persists across navigation
- **Loading.tsx**: Automatic loading states
- **Error.tsx**: Error boundaries

---

## Skill #2: Component Optimization

### When to Use
- Slow rendering
- Unnecessary re-renders
- Performance issues

### Prompt Template

```markdown
**ROLE**: React performance specialist

**PROBLEM**: [Component re-rendering too often / Slow interactions / etc]

**CURRENT CODE**:
```typescript
[Paste component code]
```

**OPTIMIZATION TECHNIQUES**:

1. **React.memo** (prevent re-renders):
```typescript
const TaskCard = React.memo(({ task, onDelete }) => {
  return <div>{task.title}</div>
})
```

2. **useCallback** (stable functions):
```typescript
const handleDelete = useCallback((id: string) => {
  deleteTask(id)
}, [deleteTask]) // Only recreate if deleteTask changes
```

3. **useMemo** (expensive calculations):
```typescript
const sortedTasks = useMemo(() => {
  return tasks.sort((a, b) => a.priority - b.priority)
}, [tasks])
```

4. **Code Splitting** (lazy loading):
```typescript
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />
})
```

**DELIVERABLES**:
- Optimized component code
- Performance comparison
- React DevTools Profiler results
```

### When to Optimize:
- ✅ List with 100+ items
- ✅ Complex calculations in render
- ✅ Large component trees
- ❌ Premature optimization for simple components

---

## Skill #3: TailwindCSS Advanced Patterns

### When to Use
- Building complex layouts
- Implementing design systems
- Dark mode support
- Responsive design

### Prompt Template

```markdown
**ROLE**: TailwindCSS expert

**COMPONENT**: [TaskCard / Modal / Navigation / etc]
**REQUIREMENTS**: [Responsive / Dark mode / Animations / etc]

**PATTERNS**:

1. **Component Composition**:
```typescript
// Base styles
const baseStyles = "rounded-lg border p-4"
const variantStyles = {
  default: "bg-white border-gray-200",
  primary: "bg-blue-50 border-blue-300",
  danger: "bg-red-50 border-red-300"
}

<div className={`${baseStyles} ${variantStyles.primary}`}>
```

2. **Responsive Design**:
```typescript
<div className="
  grid
  grid-cols-1           /* Mobile: 1 column */
  md:grid-cols-2        /* Tablet: 2 columns */
  lg:grid-cols-3        /* Desktop: 3 columns */
  gap-4
">
```

3. **Dark Mode**:
```typescript
<div className="
  bg-white dark:bg-slate-900
  text-gray-900 dark:text-gray-100
  border-gray-200 dark:border-gray-700
">
```

4. **Custom Utilities** (tailwind.config.js):
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {...},
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in',
      }
    }
  }
}
```

**DELIVERABLES**:
- Complete component styling
- Responsive breakpoints
- Dark mode variants
- Custom utilities if needed
```

### Tailwind Best Practices:
- Use design tokens (colors, spacing)
- Avoid !important
- Use @apply sparingly
- Leverage Tailwind plugins
- Keep classes organized

---

## Skill #4: Form Handling with React Hook Form

### When to Use
- Complex forms
- Validation requirements
- Form state management

### Prompt Template

```markdown
**ROLE**: Form specialist

**FORM**: [Create Task / Edit Profile / etc]
**VALIDATION**: [Zod / Yup / Custom]

**SETUP**:
```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  title: z.string().min(1, "Title required"),
  description: z.string().optional(),
  priority: z.enum(["low", "medium", "high"]),
  dueDate: z.date().optional()
})

type FormData = z.infer<typeof schema>

function TaskForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema)
  })
  
  const onSubmit = async (data: FormData) => {
    await createTask(data)
  }
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("title")} />
      {errors.title && <span>{errors.title.message}</span>}
      
      <button disabled={isSubmitting}>
        {isSubmitting ? "Creating..." : "Create Task"}
      </button>
    </form>
  )
}
```

**DELIVERABLES**:
- Form component
- Validation schema
- Error handling
- Loading states
- Success feedback
```

---

## Skill #5: State Management Strategy

### When to Use
- Deciding between Context, Zustand, Redux
- Managing global state
- Optimizing state updates

### Prompt Template

```markdown
**ROLE**: State architecture specialist

**APPLICATION**: [TODO app / Dashboard / etc]
**COMPLEXITY**: [Simple / Medium / Complex]

**STATE NEEDS**:
- User session: [From Better Auth]
- Tasks list: [From API]
- UI state: [Modals, sidebars, etc]
- Filters/sorting: [Client-side]

**OPTIONS**:

1. **React Context** (Simple - our choice):
```typescript
const TaskContext = createContext<TaskContextType>(null!)

export function TaskProvider({ children }: { children: ReactNode }) {
  const [tasks, setTasks] = useState<Task[]>([])
  
  return (
    <TaskContext.Provider value={{ tasks, setTasks }}>
      {children}
    </TaskContext.Provider>
  )
}
```

2. **Zustand** (Medium complexity):
```typescript
import create from 'zustand'

const useTaskStore = create((set) => ({
  tasks: [],
  addTask: (task) => set((state) => ({ 
    tasks: [...state.tasks, task] 
  })),
}))
```

3. **Server State** (React Query/SWR):
```typescript
import useSWR from 'swr'

function TaskList() {
  const { data: tasks, mutate } = useSWR('/api/tasks', fetcher)
  // Auto-revalidation, caching, etc.
}
```

**RECOMMEND**: 
- Based on complexity
- Team familiarity
- Bundle size concerns

**DELIVERABLES**:
- State management setup
- Provider/store configuration
- Hook usage examples
```

### Our Choice: React Context + SWR
- Context for UI state
- SWR for server data
- Keeps it simple

---

## Skill #6: UI Debugging (Hydration, Styling, Layout)

### When to Use
- "Hydration failed" errors
- Styles not applying
- Layout shifts
- Component not rendering

### Prompt Template

```markdown
**ROLE**: Frontend debugging specialist

**PROBLEM**: [Paste error or describe issue]

**COMMON ISSUES**:

1. **Hydration Errors**:
```
Error: Hydration failed because the initial UI does not match
```

**Causes**:
- Server HTML ≠ Client HTML
- Using browser APIs in Server Component
- Random values in SSR

**Fix**:
```typescript
// ❌ Wrong
<div>{Math.random()}</div>

// ✅ Right  
'use client'
const [id, setId] = useState('')
useEffect(() => setId(Math.random().toString()), [])
<div>{id}</div>
```

2. **Styles Not Applying**:
- Check Tailwind config includes file
- Verify globals.css is imported
- Check for CSS specificity issues
- Inspect with DevTools

3. **Component Not Showing**:
- Check conditional rendering
- Look for display: none
- Verify data is loaded
- Check z-index issues

**DEBUG PROCESS**:
1. Check browser console
2. Inspect element in DevTools
3. Check React DevTools
4. Verify props/state
5. Test in isolation

**DELIVERABLES**:
- Root cause identified
- Fix implemented
- Prevention strategy
```

---

## Quick Reference

### Essential Next.js Commands
```bash
npm run dev         # Start dev server
npm run build       # Production build
npm run start       # Start production server
npm run lint        # Run ESLint
```

### Common Next.js Patterns
```typescript
// Dynamic routes
app/tasks/[id]/page.tsx

// Route groups (don't affect URL)
app/(dashboard)/tasks/page.tsx

// Parallel routes
app/@modal/page.tsx

// Intercepting routes
app/tasks/(..)photo/page.tsx
```

### TailwindCSS Custom Config
```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'media'
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: { ... },
      fontFamily: { ... },
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

---

## Lessons Learned

### Next.js App Router
1. Server Components are the default
2. Use `'use client'` only when needed
3. Layouts persist across navigations
4. loading.tsx and error.tsx are powerful
5. Metadata API for SEO

### React Performance
1. Don't optimize prematurely
2. Use React DevTools Profiler
3. Memo for expensive renders
4. Code split heavy components
5. Virtual scrolling for long lists

### Tailwind
1. Use design system (extend theme)
2. Avoid inline styles
3. Dark mode via class strategy
4. Responsive-first approach
5. Purge unused styles in production

### State Management
1. Start simple (Context/props)
2. Server state ≠ Client state
3. Use SWR/React Query for API data
4. Zustand for complex client state
5. Redux only if truly needed

---

## Related Skills
- Phase 2: Implementation patterns
- Database Skills: Fetching data
- Backend Skills: API integration
- Debug Skills: Troubleshooting UI

**Great UX starts with solid frontend architecture!**
