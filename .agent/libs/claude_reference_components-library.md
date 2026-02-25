# Components & UI Library Reference

**Project**: TODO Hackathon  
**Purpose**: Complete catalog of all React components created  
**Last Updated**: December 29, 2025

---

## 📋 Overview

This document catalogs all React components built for the project, organized by category with props, usage examples, and implementation notes.

**Total Components**: 15+

---

## 📁 Component Organization

```
phase2/frontend/src/
├── app/                    # Page components (App Router)
│   ├── page.tsx           # Home/Dashboard
│   ├── login/page.tsx     # Login page
│   └── signup/page.tsx    # Signup page
│
└── components/             # Reusable components
    ├── TaskList.tsx        # Main task list
    ├── TaskCard.tsx        # Individual task card
    ├── TaskForm.tsx        # Task creation/edit form
    ├── Header.tsx          # App header/navigation
    ├── ThemeToggle.tsx     # Dark mode toggle
    ├── AIChat.tsx          # AI chat interface
    └── ui/                 # Base UI components
        ├── Button.tsx
        ├── Input.tsx
        ├── Modal.tsx
        └── Toast.tsx
```

---

## 🎯 Core Components

### TaskList

**File**: `components/TaskList.tsx`  
**Purpose**: Main container for displaying and managing tasks  
**Complexity**: High

#### Props
```typescript
interface TaskListProps {
  initialFilter?: 'all' | 'active' | 'completed'
  userId: string
}
```

#### Features
- ✅ Fetches tasks from API
- ✅ Filters (all/active/completed)
- ✅ Sorting (date, priority, title)
- ✅ Search functionality
- ✅ Optimistic updates
- ✅ Empty state handling
- ✅ Loading state
- ✅ Error handling

#### Implementation Highlights
```typescript
'use client'

export function TaskList({ initialFilter = 'all' }: TaskListProps) {
  const [filter, setFilter] = useState(initialFilter)
  const { data: tasks, mutate } = useSWR('/api/tasks', fetcher)
  
  const filteredTasks = tasks?.filter(task => {
    if (filter === 'completed') return task.is_completed
    if (filter === 'active') return !task.is_completed
    return true
  })
  
  return (
    <div className="space-y-4">
      {/* Filter buttons */}
      {/* Task cards */}
      {filteredTasks?.map(task => (
        <TaskCard key={task.id} task={task} onUpdate={handleUpdate} />
      ))}
    </div>
  )
}
```

#### Lessons Learned
- ✅ Use SWR for automatic caching and revalidation
- ✅ Filter/sort on client side for responsiveness
- ✅ Memoize filtered results to prevent re-calculations
- ⚠️ Handle empty states gracefully
- 💡 Virtual scrolling recommended for 100+ tasks

#### Styling
```css
.task-list {
  overflow-y: auto;
  max-height: calc(100vh - 200px);
  scrollbar-width: none; /* Hide scrollbar */
}
```

---

### TaskCard

**File**: `components/TaskCard.tsx`  
**Purpose**: Display individual task with inline editing  
**Complexity**: Medium

#### Props
```typescript
interface TaskCardProps {
  task: Task
  onUpdate?: (id: string, updates: Partial<Task>) => void
  onDelete?: (id: string) => void
}
```

#### Features
- ✅ Display task details
- ✅ Checkbox to toggle completion
- ✅ Inline editing (title, description)
- ✅ Priority indicator (color-coded)
- ✅ Due date display
- ✅ Delete button
- ✅ Hover effects

#### Implementation
```typescript
export function TaskCard({ task, onUpdate, onDelete }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false)
  
  const handleToggle = () => {
    onUpdate?.(task.id, { is_completed: !task.is_completed })
  }
  
  return (
    <div className={cn(
      "rounded-lg border p-4 transition-colors",
      task.is_completed ? "bg-slate-900 border-slate-800" : "bg-slate-800 border-slate-700",
      task.priority === 'high' && "border-l-4 border-l-red-500"
    )}>
      <div className="flex items-start gap-3">
        <Checkbox checked={task.is_completed} onCheckedChange={handleToggle} />
        {isEditing ? (
          <TaskForm task={task} onSave={handleSave} />
        ) : (
          <div onClick={() => setIsEditing(true)}>
            <h3>{task.title}</h3>
            <p>{task.description}</p>
          </div>
        )}
      </div>
    </div>
  )
}
```

#### Styling Variants
```typescript
// Priority colors
const priorityColors = {
  low: 'border-l-green-500',
  medium: 'border-l-yellow-500',
  high: 'border-l-red-500'
}

// Completion state
const completionStyles = task.is_completed 
  ? 'opacity-60 line-through'
  : ''
```

#### Lessons Learned
- ✅ Inline editing improves UX
- ✅ Color-coding priorities aids quick scanning
- ✅ Optimistic updates feel instant
- ⚠️ Handle click vs. edit mode carefully
- 💡 Debounce auto-save to reduce API calls

---

### TaskForm

**File**: `components/TaskForm.tsx`  
**Purpose**: Form for creating/editing tasks  
**Complexity**: Medium

#### Props
```typescript
interface TaskFormProps {
  task?: Task  // If editing
  onSave: (data: TaskCreate) => void
  onCancel?: () => void
}
```

#### Features
- ✅ React Hook Form integration
- ✅ Validation
- ✅ Priority selector
- ✅ Due date picker
- ✅ Description textarea
- ✅ Submit/cancel buttons

#### Implementation
```typescript
import { useForm } from 'react-hook-form'

export function TaskForm({ task, onSave }: TaskFormProps) {
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: task || {}
  })
  
  return (
    <form onSubmit={handleSubmit(onSave)} className="space-y-4">
      <Input
        {...register('title', { required: 'Title is required' })}
        placeholder="Task title"
        error={errors.title?.message}
      />
      
      <select {...register('priority')}>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
      
      <Input
        type="date"
        {...register('due_date')}
      />
      
      <Button type="submit">Save</Button>
    </form>
  )
}
```

#### Validation Rules
```typescript
{
  title: { required: true, minLength: 1, maxLength: 200 },
  priority: { required: true, enum: ['low', 'medium', 'high'] },
  due_date: { validate: (date) => date > new Date() }
}
```

---

## 🎨 UI Base Components

### Button

**File**: `components/ui/Button.tsx`  
**Purpose**: Customizable button component  
**Complexity**: Low

#### Props
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
  type?: 'button' | 'submit'
}
```

#### Variants
```typescript
const variants = {
  primary: 'bg-blue-600 hover:bg-blue-700 text-white',
  secondary: 'bg-slate-700 hover:bg-slate-600 text-slate-200',
  ghost: 'hover:bg-slate-800 text-slate-300',
  danger: 'bg-red-600 hover:bg-red-700 text-white'
}

const sizes = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg'
}
```

#### Usage
```tsx
<Button variant="primary" size="md" onClick={handleClick}>
  Create Task
</Button>
```

---

### Input

**File**: `components/ui/Input.tsx`  
**Purpose**: Styled form input  
**Complexity**: Low

#### Props
```typescript
interface InputProps {
  type?: 'text' | 'email' | 'password' | 'date'
  placeholder?: string
  error?: string
  disabled?: boolean
  value?: string
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void
}
```

#### Styling
```css
.input {
  @apply w-full rounded-md border px-3 py-2;
  @apply bg-slate-900 border-slate-700 text-slate-100;
  @apply focus:outline-none focus:ring-2 focus:ring-blue-500;
  @apply placeholder:text-slate-500;
}
```

---

### Modal

**File**: `components/ui/Modal.tsx`  
**Purpose**: Reusable modal dialog  
**Complexity**: Medium

#### Props
```typescript
interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  children: React.ReactNode
  size?: 'sm' | 'md' | 'lg'
}
```

#### Features
- ✅ Backdrop overlay
- ✅ Click outside to close
- ✅ ESC key to close
- ✅ Focus trap
- ✅ Smooth animations
- ✅ Responsive sizing

#### Implementation
```typescript
export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    
    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
      document.body.style.overflow = 'hidden'
    }
    
    return () => {
      document.removeEventListener('keydown', handleEscape)
      document.body.style.overflow = 'unset'
    }
  }, [isOpen, onClose])
  
  if (!isOpen) return null
  
  return (
    <div className="fixed inset-0 z-50">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/50"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="absolute inset-0 flex items-center justify-center p-4">
        <div className="bg-slate-800 rounded-lg p-6 max-w-md w-full">
          {title && <h2>{title}</h2>}
          {children}
        </div>
      </div>
    </div>
  )
}
```

---

## 🎭 Feature Components

### Header

**File**: `components/Header.tsx`  
**Purpose**: App header with navigation and user menu  
**Complexity**: Medium

#### Features
- ✅ App title/logo
- ✅ Navigation links
- ✅ User avatar/menu
- ✅ Dark mode toggle
- ✅ Logout button

#### Implementation
```typescript
export function Header() {
  const { data: session } = useSession()
  
  return (
    <header className="border-b border-slate-700 bg-slate-900">
      <div className="container flex items-center justify-between py-4">
        <h1 className="text-2xl font-bold">TODO App</h1>
        
        <div className="flex items-center gap-4">
          <ThemeToggle />
          
          {session && (
            <DropdownMenu>
              <DropdownMenuTrigger>
                <Avatar user={session.user} />
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuItem onClick={handleLogout}>
                  Logout
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </div>
      </div>
    </header>
  )
}
```

---

### ThemeToggle

**File**: `components/ThemeToggle.tsx`  
**Purpose**: Dark/light mode toggle  
**Complexity**: Low

#### Implementation
```typescript
import { useTheme } from 'next-themes'

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  
  return (
    <button
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="p-2 rounded-lg hover:bg-slate-800"
    >
      {theme === 'dark' ? <Sun /> : <Moon />}
    </button>
  )
}
```

---

### AIChat

**File**: `components/AIChat.tsx`  
**Purpose**: AI chat interface  
**Complexity**: High

#### Features
- ✅ Chat input
- ✅ Message history
- ✅ Streaming responses
- ✅ Loading indicator
- ✅ Error handling
- ✅ Auto-scroll

#### Implementation Highlights
```typescript
export function AIChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  
  const sendMessage = async () => {
    setIsLoading(true)
    setMessages(prev => [...prev, { role: 'user', content: input }])
    
    const response = await fetch('/api/ai/chat', {
      method: 'POST',
      body: JSON.stringify({ message: input })
    })
    
    const data = await response.json()
    setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
    setIsLoading(false)
  }
  
  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto">
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}
      </div>
      
      <div className="border-t border-slate-700 p-4">
        <Input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && sendMessage()}
          placeholder="Ask AI..."
        />
      </div>
    </div>
  )
}
```

---

## 📊 Component Statistics

| Category | Components | Complexity |
|----------|------------|---|
| Core | 3 (TaskList, TaskCard, TaskForm) | High |
| UI Base | 4 (Button, Input, Modal, Toast) | Low-Medium |
| Feature | 3 (Header, ThemeToggle, AIChat) | Medium-High |
| Pages | 3 (Home, Login, Signup) | Medium |
| **Total** | **13+** | **Mixed** |

---

## 🎨 Design Patterns Used

### Composition Pattern
```typescript
<TaskList>
  <TaskCard>
    <Button />
    <Checkbox />
  </TaskCard>
</TaskList>
```

### Render Props
```typescript
<DataFetcher
  url="/api/tasks"
  render={({ data, loading }) => (
    loading ? <Skeleton /> : <TaskList tasks={data} />
  )}
/>
```

### Compound Components
```typescript
<Modal.Root>
  <Modal.Trigger />
  <Modal.Content />
  <Modal.Close />
</Modal.Root>
```

---

## 💡 Best Practices

### Component Structure
```typescript
// 1. Imports
import { useState } from 'react'
import { Button } from '@/components/ui/Button'

// 2. Types
interface Props {
  // ...
}

// 3. Component
export function Component({ prop }: Props) {
  // 4. Hooks
  const [state, setState] = useState()
  
  // 5. Handlers
  const handleClick = () => {}
  
  // 6. Effects
  useEffect(() => {}, [])
  
  // 7. Render
  return <div>...</div>
}
```

### Naming Conventions
- ✅ PascalCase for components
- ✅ camelCase for props and functions
- ✅ Descriptive names
- ✅ Handler prefix: `handle` or `on`

### File Organization
- ✅ One component per file
- ✅ Co-locate styles if CSS Modules
- ✅ Group related components in folders
- ✅ Index files for cleaner imports

---

## 🔗 Related Documentation

- **Design System**: `.specify/design-system.md`
- **Frontend Skills**: `.claude/frontend-skills.md`
- **Features**: `.claude/reference/features-implementation.md`
- **Workflows**: `.agent/workflows/adding-new-feature.md`

---

**Every component documented and ready to reuse!** 🎉
