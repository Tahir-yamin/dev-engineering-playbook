# UI Pages Specification

## Overview

This document defines the frontend pages for the Full-Stack Web Application built with Next.js. The UI will provide a responsive, accessible interface for managing tasks.

## Technology Stack

- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Headless UI or Radix UI primitives
- **Forms**: React Hook Form with Zod validation
- **HTTP Client**: Axios for API requests

## Page Structure

### 1. Login Page (`/login`)

#### Purpose
Allow users to authenticate with their credentials.

#### Components
- Email input field
- Password input field
- Submit button
- "Forgot password" link
- "Sign up" link (redirects to registration)
- Social login buttons (optional future enhancement)

#### Layout
- Centered card layout
- Responsive design for mobile and desktop
- Loading state during authentication
- Error message display for authentication failures

#### Behavior
- Form validation on submit
- Redirect to dashboard on successful login
- Display error messages for invalid credentials
- Password visibility toggle

#### API Integration
- POST `/api/v1/auth/login`

---

### 2. Registration Page (`/register`)

#### Purpose
Allow new users to create an account.

#### Components
- Username input field
- Email input field
- Password input field
- Confirm password field
- Submit button
- "Already have an account?" link (redirects to login)

#### Layout
- Centered card layout
- Responsive design for mobile and desktop
- Loading state during registration
- Error message display for registration failures

#### Behavior
- Form validation on submit
- Password strength indicator
- Match validation for password confirmation
- Redirect to login on successful registration

#### API Integration
- POST `/api/v1/auth/register`

---

### 3. Dashboard Page (`/dashboard`)

#### Purpose
Provide an overview of user's tasks and quick actions.

#### Components
- Navigation sidebar
- Header with user profile
- Task statistics cards (total tasks, completed, pending, overdue)
- Quick task creation form
- Recent tasks list (showing last 5 tasks)
- Upcoming deadlines section

#### Layout
- Two-column layout (sidebar + main content)
- Responsive grid for statistic cards
- Clean, minimalist design
- Consistent spacing and typography

#### Behavior
- Real-time statistics updates
- Quick-add form submission
- Links to full task list
- Auto-refresh of data periodically

#### API Integration
- GET `/api/v1/tasks` (with filters for stats)
- POST `/api/v1/tasks` (for quick add)

---

### 4. Task List Page (`/tasks`)

#### Purpose
Display all tasks with filtering, sorting, and management capabilities.

#### Components
- Navigation sidebar
- Header with user profile and search
- Task creation button
- Filter controls (status, priority)
- Sort controls (date, priority, title)
- Task list/grid view toggle
- Task cards showing title, description, priority, status, due date
- Pagination controls
- Bulk action controls (select, mark complete, delete)

#### Layout
- Sidebar navigation
- Main content area with controls and task list
- Responsive grid for task cards
- Mobile-friendly stacked layout

#### Behavior
- Dynamic filtering and sorting
- Infinite scroll or pagination
- Checkbox selection for bulk actions
- Visual feedback for completed tasks
- Empty state when no tasks exist
- Loading states during data fetch

#### API Integration
- GET `/api/v1/tasks` (with query params for filtering/sorting)
- PUT `/api/v1/tasks/{id}` (for individual updates)
- DELETE `/api/v1/tasks/{id}` (for individual deletes)
- PATCH `/api/v1/tasks/{id}/complete` (for toggling completion)

---

### 5. Task Detail/Edit Page (`/tasks/[id]`)

#### Purpose
View or edit details of a specific task.

#### Components
- Navigation sidebar
- Header with user profile
- Back button to task list
- Task title input
- Description textarea
- Priority selector (low, medium, high)
- Due date picker
- Status toggle (completed/pending)
- Save changes button
- Cancel button
- Delete task button (with confirmation)

#### Layout
- Sidebar navigation
- Main content area with form
- Consistent spacing and alignment
- Mobile-responsive form layout

#### Behavior
- Pre-populate form with existing task data
- Form validation on save
- Confirmation dialog for deletions
- Success/error feedback messages
- Auto-save indicators

#### API Integration
- GET `/api/v1/tasks/{id}` (to fetch task)
- PUT `/api/v1/tasks/{id}` (to update task)
- DELETE `/api/v1/tasks/{id}` (to delete task)

---

### 6. Profile Settings Page (`/profile`)

#### Purpose
Allow users to manage their account information.

#### Components
- Navigation sidebar
- Header with user profile
- Profile picture upload (optional)
- Username input
- Email input
- Current password (for changes)
- New password (if changing)
- Confirm new password
- Save changes button
- Account deletion option (with confirmation)

#### Layout
- Sidebar navigation
- Main content area with settings form
- Sectioned organization of settings
- Consistent form styling

#### Behavior
- Form validation
- Password change confirmation
- Success feedback for updates
- Confirmation for account deletion
- Real-time validation where appropriate

#### API Integration
- GET `/api/v1/profile` (to fetch profile)
- PUT `/api/v1/profile` (to update profile)

---

### 7. Landing Page (`/`)

#### Purpose
Public landing page for unauthenticated users.

#### Components
- Hero section with app description
- Features highlights
- Call-to-action buttons (Sign up, Learn more)
- Footer with links

#### Layout
- Full-width hero section
- Grid-based features section
- Responsive design for all devices

#### Behavior
- Redirect authenticated users to dashboard
- Smooth scrolling navigation
- Animated elements for engagement

## Common UI Elements

### Navigation Sidebar
- Logo/branding
- Menu items (Dashboard, Tasks, Profile)
- User profile dropdown
- Collapsible on mobile

### Header
- User profile avatar and menu
- Notification bell icon
- Search bar
- Responsive behavior

### Task Cards
- Title with truncation
- Description preview
- Priority badge (color-coded)
- Status indicator
- Due date display
- Action buttons (edit, complete, delete)

## Responsive Design

### Desktop (>1024px)
- Full sidebar navigation
- Multi-column layouts
- Hover effects and tooltips

### Tablet (768px - 1024px)
- Collapsible sidebar
- Adjusted column counts
- Touch-friendly controls

### Mobile (<768px)
- Hamburger menu for navigation
- Single-column layouts
- Larger touch targets
- Stacked form elements

## Accessibility Requirements

- Semantic HTML structure
- Proper heading hierarchy (H1, H2, H3)
- ARIA labels for interactive elements
- Keyboard navigation support
- Screen reader compatibility
- Color contrast ratios (WCAG AA minimum)
- Focus indicators for interactive elements

## State Management

- Global authentication state
- Loading states for API requests
- Error handling and display
- Form state management
- Task list filtering state
- Theme preference (light/dark mode)

## Error Handling

- Network error notifications
- Validation error displays
- 404 and 500 error pages
- Graceful degradation for offline states
- Retry mechanisms for failed requests

## Performance Considerations

- Code splitting for page routes
- Image optimization
- Lazy loading for task lists
- Debounced search inputs
- Efficient re-rendering with React.memo
- Optimistic updates where appropriate