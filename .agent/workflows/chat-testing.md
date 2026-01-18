---
description: Comprehensive chat widget testing for all MCP tool operations
---

# Chat Widget Testing Workflow

Complete testing checklist for all chat-based task management operations.

## Prerequisites

**Start Services**:
```bash
# Navigate to backend
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2\backend"

# Start backend (if not running)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**In a new terminal, start frontend**:
```bash
# Navigate to frontend
cd "d:\Hackathon phase 1 TODO App\todo_hackathon_phase1\phase2\frontend"

# Start frontend (if not running)
npm run dev
```

**Open Application**: Navigate to `http://localhost:3000` and log in

---

## Test Suite 1: Add Tasks (add_task tool)

### Test 1.1: Basic Task Creation
1. Open chat widget (click chat button bottom-right)
2. Type: `Create a task to buy groceries`
3. **Expected**: AI confirms "I have created the task: Buy groceries with medium priority"
4. **Verify**: Check task list - new task should appear

### Test 1.2: Task with Priority
1. In chat: `Add a high priority task to complete project report`
2. **Expected**: AI confirms task creation with High priority
3. **Verify**: Task appears with red/high priority indicator

### Test 1.3: Task with Category
1. In chat: `Create a work task to review code`
2. **Expected**: AI creates task with "work" category
3. **Verify**: Task shows in Work category

---

## Test Suite 2: List Tasks (list_tasks tool)

### Test 2.1: List All Open Tasks
1. Ensure you have at least 3 open tasks (status: todo)
2. In chat: `Show me all my tasks`
3. **Expected**: AI displays markdown table with all open tasks
4. **Verify**: Only shows tasks with status "todo" or "in_progress", NOT completed

### Test 2.2: Filter by Priority
1. Create tasks with different priorities (low, medium, high)
2. In chat: `Show me all medium priority tasks`
3. **Expected**: AI displays only medium priority tasks in table format
4. **Verify**: Table contains only medium priority items

### Test 2.3: Filter by Status
1. Complete at least one task via UI
2. In chat: `Show me completed tasks`
3. **Expected**: AI displays only completed tasks
4. **Verify**: Only shows completed status tasks

### Test 2.4: Empty Results
1. Ensure you have no high priority tasks
2. In chat: `Show me high priority tasks`
3. **Expected**: "You have no tasks at the moment" or similar message

---

## Test Suite 3: Update Tasks (update_task tool)

### Test 3.1: Update Task Priority
1. Note the ID of a task from list (or view in logs)
2. In chat: `Update task [TASK_ID] to high priority`
3. **Expected**: AI confirms "I have updated the task: [Task Title]"
4. **Verify**: Task priority changes to High in UI

### Test 3.2: Update Task Status
1. In chat: `Mark task [TASK_ID] as in progress`
2. **Expected**: AI confirms update
3. **Verify**: Task status changes in UI

---

## Test Suite 4: Complete Tasks (update_task & bulk_complete_tasks)

### Test 4.1: Complete Single Task
1. In chat: `Complete task [TASK_ID]`
2. **Expected**: AI confirms task completion
3. **Verify**: Task marked as completed in UI

### Test 4.2: Bulk Complete All Tasks
1. Ensure you have at least 3 open tasks
2. In chat: `Complete all my tasks` OR `Mark everything as done`
3. **Expected**: AI confirms "I have marked [N] tasks as completed"
4. **Verify**: All open tasks now show as completed

---

## Test Suite 5: Delete Tasks (delete_task tool)

### Test 5.1: Delete Single Task
1. Create a test task: "Delete me"
2. Note the task ID
3. In chat: `Delete task [TASK_ID]`
4. **Expected**: AI confirms "I have deleted the task: Delete me"
5. **Verify**: Task removed from UI

### Test 5.2: Delete Non-Existent Task
1. In chat: `Delete task xyz-fake-id-123`
2. **Expected**: Error message "Task with ID xyz-fake-id-123 not found"

---

## Test Suite 6: Phase 5 Features (set_reminder tool)

### Test 6.1: Set Task Reminder
1. Create a task with future due date
2. In chat: `Set reminder for task [TASK_ID] at 2026-01-18T10:00:00`
3. **Expected**: AI confirms reminder set
4. **Verify**: Task shows reminder icon/time

---

## Test Suite 7: Error Handling

### Test 7.1: API Key Issues
1. If API key is invalid/expired
2. In chat: Send any message
3. **Expected**: Formatted error message about API credits
4. **Verify**: User-friendly error, not raw JSON

### Test 7.2: Empty Message
1. Click send button with empty input
2. **Expected**: Button should be disabled, no request sent

### Test 7.3: Network Error
1. Stop backend server
2. In chat: `Show my tasks`
3. **Expected**: Error message about connection failure

---

## Test Suite 8: UI/UX Verification

### Test 8.1: Chat History Persistence
1. Send several messages in chat
2. Close chat widget
3. Reopen chat widget
4. **Expected**: Previous conversation is still visible

### Test 8.2: Task Update Callback
1. In chat: `Create a task to test refresh`
2. **Expected**: Task list automatically refreshes after AI confirms
3. **Verify**: New task appears without manual page refresh

### Test 8.3: Loading States
1. In chat: Send a message
2. **Expected**: See animated "..." loading indicator while AI processes
3. **Verify**: Input is disabled during loading

---

## Known Issues / Expected Behaviors

- **Bulk Delete**: Currently unsupported - AI will explain this limitation
- **Open Tasks**: Interpreted as status `todo` OR `in_progress`
- **Task ID**: Users typically don't know task IDs, so delete operations may require listing tasks first
- **Free Tier Limits**: May encounter token limits with free OpenRouter model

---

## Test Completion Checklist

- [ ] All Add Task tests passed (3/3)
- [ ] All List Tasks tests passed (4/4)
- [ ] All Update Tasks tests passed (2/2)
- [ ] All Complete Tasks tests passed (2/2)
- [ ] All Delete Tasks tests passed (2/2)
- [ ] Phase 5 features tested (1/1)
- [ ] Error handling verified (3/3)
- [ ] UI/UX checks passed (3/3)

**Total Tests**: 20 test cases

---

## Debugging Tips

**Check Backend Logs**:
- Look for `🔧 Executing tool: [tool_name]` logs
- Verify user ID matches logged user
- Check for tool execution errors

**Check Browser Console**:
- Look for `✅ Task operation completed` messages
- Verify `task-update` events are fired
- Check for network errors (500/404)

**Common Issues**:
1. **Chat returns error**: Check `OPENROUTER_API_KEY` environment variable
2. **Tasks don't refresh**: Verify `onTaskUpdated` callback is passed to ChatWidget
3. **Wrong user tasks shown**: Check `X-User-ID` header in network tab
