---
description: "Task list for Phase I: In-Memory Python Console App"
---

# Tasks: Phase I: In-Memory Python Console App

**Input**: Design documents from `/specs/001-in-memory-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: The specification implies a need for robust testing to ensure functionality. Therefore, test tasks are included to follow a Test-Driven Development (TDD) approach.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project as per plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create `src/todo_app/` and `tests/unit/`, `tests/integration/` directories
- [ ] T002 Create `src/cli.py` and add shebang and basic script structure
- [ ] T003 Create `src/todo_app/__init__.py`, `src/todo_app/models.py`, `src/todo_app/services.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement `Task` data class in `src/todo_app/models.py` with `id`, `title`, `description`, `status` attributes.
- [x] T005 Create `TodoService` class in `src/todo_app/services.py` with an in-memory storage (e.g., a list or dictionary) and a method to generate unique task IDs.
- [x] T006 [P] Create `tests/unit/test_models.py` and add unit tests for `Task` data class (e.g., initialization, default status).
- [x] T007 [P] Create `tests/unit/test_services_foundational.py` and add unit tests for `TodoService` ID generation.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add a new todo task (Priority: P1) 🎯 MVP

**Goal**: Users can create new todo items with a title and description.

**Independent Test**: Add a task via CLI and verify its presence and details using the `list` command (once implemented).

### Tests for User Story 1 (TDD Approach)

- [x] T008 [P] [US1] Add unit tests for `TodoService.add_task` in `tests/unit/test_services_add.py` (e.g., successful addition, handling empty title).
- [x] T009 [P] [US1] Add integration tests for `add` CLI command in `tests/integration/test_cli_add.py` (e.g., valid input, invalid input).

### Implementation for User Story 1

- [x] T010 [US1] Implement `add_task(title: str, description: str)` method in `src/todo_app/services.py` to create and store a new task, assigning a unique ID and `pending` status. (Depends on T004, T005).
- [x] T011 [US1] Implement `add` command in `src/cli.py` to parse `--title` and `--description` arguments and call `TodoService.add_task`. Handle empty title validation.

**Checkpoint**: At this point, User Story 1 (Add Task) should be fully functional and testable independently

---

## Phase 4: User Story 2 - View all tasks (Priority: P1)

**Goal**: Users can see a list of all their todo tasks, including their completion status.

**Independent Test**: Add multiple tasks (some pending, some complete), then view the list to confirm all are displayed correctly with their status.

### Tests for User Story 2 (TDD Approach)

- [x] T012 [P] [US2] Add unit tests for `TodoService.get_all_tasks` in `tests/unit/test_services_list.py` (e.g., empty list, multiple tasks).
- [x] T013 [P] [US2] Add integration tests for `list` CLI command in `tests/integration/test_cli_list.py` (e.g., empty list output, formatted output).

### Implementation for User Story 2

- [x] T014 [US2] Implement `get_all_tasks()` method in `src/todo_app/services.py` to return the current list of tasks.
- [x] T015 [US2] Implement `list` command in `src/cli.py` to call `TodoService.get_all_tasks` and display tasks in a user-friendly format.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark a task as complete (Priority: P2)

**Goal**: Users can mark a pending task as complete.

**Independent Test**: Mark an existing task as complete via CLI and verify its status using the `list` command.

### Tests for User Story 3 (TDD Approach)

- [x] T016 [P] [US3] Add unit tests for `TodoService.mark_task_complete` in `tests/unit/test_services_complete.py` (e.g., successful completion, already complete, non-existent ID).
- [x] T017 [P] [US3] Add integration tests for `complete` CLI command in `tests/integration/test_cli_complete.py` (e.g., valid ID, invalid ID).

### Implementation for User Story 3

- [x] T018 [US3] Implement `mark_task_complete(task_id: int)` method in `src/todo_app/services.py` to update a task's status to `completed`.
- [x] T019 [US3] Implement `complete` command in `src/cli.py` to parse `--id` argument and call `TodoService.mark_task_complete`. Handle task not found.

**Checkpoint**: All user stories up to P2 should now be independently functional

---

## Phase 6: User Story 4 - Update an existing task (Priority: P2)

**Goal**: Users can modify the title or description of an existing task.

**Independent Test**: Update an existing task's title and/or description via CLI and verify changes using the `list` command.

### Tests for User Story 4 (TDD Approach)

- [x] T020 [P] [US4] Add unit tests for `TodoService.update_task` in `tests/unit/test_services_update.py` (e.g., update title, update description, update both, empty title, non-existent ID).
- [x] T021 [P] [US4] Add integration tests for `update` CLI command in `tests/integration/test_cli_update.py` (e.g., valid ID with new title/description, invalid ID).

### Implementation for User Story 4

- [x] T022 [US4] Implement `update_task(task_id: int, new_title: str = None, new_description: str = None)` method in `src/todo_app/services.py` to modify task details. Handle empty title validation.
- [x] T023 [US4] Implement `update` command in `src/cli.py` to parse `--id`, `--title`, `--description` arguments and call `TodoService.update_task`. Handle task not found and empty title validation.

**Checkpoint**: All user stories up to P2 should now be independently functional, including update operations.

---

## Phase 7: User Story 5 - Delete a task (Priority: P3)

**Goal**: Users can remove a task by its ID.

**Independent Test**: Delete an existing task via CLI and verify its removal using the `list` command.

### Tests for User Story 5 (TDD Approach)

- [x] T024 [P] [US5] Add unit tests for `TodoService.delete_task` in `tests/unit/test_services_delete.py` (e.g., successful deletion, non-existent ID).
- [x] T025 [P] [US5] Add integration tests for `delete` CLI command in `tests/integration/test_cli_delete.py` (e.g., valid ID, invalid ID).

### Implementation for User Story 5

- [x] T026 [US5] Implement `delete_task(task_id: int)` method in `src/todo_app/services.py` to remove a task from storage.
- [x] T027 [US5] Implement `delete` command in `src/cli.py` to parse `--id` argument and call `TodoService.delete_task`. Handle task not found.

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T028 Refactor `src/cli.py` for consistent error messages and user feedback across all commands.
- [x] T029 Add a main entry point in `src/cli.py` to handle command parsing gracefully using `argparse` or similar.
- [x] T030 Review and ensure all unit and integration tests have good coverage and handle edge cases as defined in the spec.

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
-   **User Stories (Phase 3-7)**: All depend on Foundational phase completion
    -   User stories can then proceed in parallel (if staffed)
    -   Or sequentially in priority order (P1 → P2 → P3)
-   **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

-   **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
-   **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
-   **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
-   **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
-   **User Story 5 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

-   Tests MUST be written and FAIL before implementation
-   Models before services
-   Services before CLI commands
-   Core implementation before integration
-   Story complete before moving to next priority

### Parallel Opportunities

-   Tasks marked [P] within a phase or story can run in parallel.
-   Once Foundational phase completes, User Stories 1 and 2 (both P1) can start in parallel.
-   Similarly, User Stories 3 and 4 (both P2) can run in parallel after Foundational and P1 stories are underway or complete.
-   Unit and Integration tests for a given user story can often be developed in parallel with their corresponding service/CLI implementations.

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Add unit tests for TodoService.add_task in tests/unit/test_services_add.py"
Task: "Add integration tests for add CLI command in tests/integration/test_cli_add.py"

# Launch implementations sequentially as they depend on the service:
Task: "Implement add_task(title: str, description: str) method in src/todo_app/services.py"
Task: "Implement add command in src/cli.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1 (Add Task)
4.  Complete Phase 4: User Story 2 (View Tasks)
5.  **STOP and VALIDATE**: Test User Stories 1 and 2 independently.
6.  Deploy/demo if ready.

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 (Add Task) → Test independently → Deploy/Demo (MVP!)
3.  Add User Story 2 (View Tasks) → Test independently → Deploy/Demo
4.  Add User Story 3 (Mark Complete) → Test independently → Deploy/Demo
5.  Add User Story 4 (Update Task) → Test independently → Deploy/Demo
6.  Add User Story 5 (Delete Task) → Test independently → Deploy/Demo
7.  Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together
2.  Once Foundational is done:
    -   Developer A: User Story 1 (Add Task)
    -   Developer B: User Story 2 (View Tasks)
    -   Developer C: User Story 3 (Mark Complete)
3.  Stories complete and integrate independently.

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tests fail before implementing
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
