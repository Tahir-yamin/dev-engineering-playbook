# Data Model: Phase I: In-Memory Python Console App

**Date**: 2025-12-06
**Feature**: [specs/001-in-memory-todo-app/spec.md](specs/001-in-memory-todo-app/spec.md)

## Entity: Task

### Description

Represents a single todo item managed by the application.

### Attributes

-   **id** (Integer): A unique identifier for the task. Automatically assigned upon creation.
    -   *Validation*: Must be unique and non-negative.
-   **title** (String): A brief, descriptive name for the task.
    -   *Validation*: Must not be empty.
-   **description** (String): A detailed explanation of the task.
    -   *Validation*: Can be empty.
-   **status** (String): The current state of the task.
    -   *Allowed Values*: `pending`, `completed`.
    -   *Default*: `pending` upon creation.

### Relationships

-   None (Task is a standalone entity in this in-memory application).

### State Transitions

-   A task's status can transition from `pending` to `completed`.
