# Phase I: In-Memory Python Console App

A simple CLI-based todo application that stores tasks in memory.

## Description

This is the Phase I implementation of the hackathon project - a Python console application with an interactive command-line interface for managing todo tasks.

## Features

- ✅ Add new tasks with title and description
- ✅ View all tasks with their status
- ✅ Mark tasks as complete
- ✅ Update task details
- ✅ Delete tasks
- ✅ In-memory storage (data persists during runtime only)

## Requirements

- Python 3.13+

## Quick Start

### Option 1: Interactive CLI (Recommended)
```bash
cd phase1
python interactive_cli.py
```

### Option 2: Main CLI
```bash
cd phase1
python cli.py
```

### Option 3: Demo
```bash
cd phase1
python demo_cli.py
```

## Usage

The interactive CLI provides a menu with the following options:

1. **Add Task** - Create a new task with title and description
2. **View Tasks** - List all tasks with their status
3. **Mark Task Complete** - Change a task's status to completed
4. **Update Task** - Modify task title or description
5. **Delete Task** - Remove a task by ID
6. **Exit** - Quit the application

## Project Structure

```
phase1/
├── cli.py                      # Main CLI implementation
├── interactive_cli.py          # Interactive menu-based CLI
├── demo_cli.py                 # Demo script
├── demo_new_features.py        # Feature demonstrations
├── test_full_functionality.py  # Functionality tests
└── todo_app/                   # Core application logic
    ├── __init__.py
    ├── task.py                 # Task model
    └── todo_manager.py         # Task management
```

## Technical Details

- **Storage**: In-memory (dictionary-based)
- **Interface**: Command-line (CLI)
- **Architecture**: Modular with separation of concerns
- **Task IDs**: Auto-incrementing integers

## Acceptance Criteria (as per specification)

✅ **FR-001**: Create todo items with title and description
✅ **FR-002**: View list of all tasks with completion status
✅ **FR-003**: Mark existing task as complete
✅ **FR-004**: Update task title or description
✅ **FR-005**: Delete task by ID
✅ **FR-006**: Unique identifier for each task
✅ **FR-007**: In-memory storage
✅ **FR-008**: Command-line interface

## Notes

- Data is stored in memory only and will be lost when the application exits
- Each task has a unique ID, title, description, and status (pending/completed)
- Empty titles are not allowed
