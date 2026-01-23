# Quickstart Guide: Phase I: In-Memory Python Console App

**Date**: 2025-12-06
**Feature**: [specs/001-in-memory-todo-app/spec.md](specs/001-in-memory-todo-app/spec.md)

## Overview

This guide provides instructions for running and interacting with the In-Memory Python Console Todo Application. This application allows users to manage tasks directly from the command line.

## Setup

1.  **Prerequisites**: Ensure you have Python 3.13+ installed on your system.
2.  **Clone the repository**: (If applicable, not for in-memory console app, but for general project structure context) `git clone <repo-url>`
3.  **Navigate to project root**: `cd /home/linux/todo_hackathon_phase1`

## Running the Application

The application will be run directly via the `cli.py` script once implemented.

```bash
python src/cli.py
```

## CLI Commands

Once the application is running, users will interact with it using various commands.

-   **Add Task**:
    ```bash
    python src/cli.py add --title "My new task" --description "Details about my task"
    ```

-   **View Task List**:
    ```bash
    python src/cli.py list
    ```

-   **Mark Task as Complete**:
    ```bash
    python src/cli.py complete --id <task_id>
    ```

-   **Update Task**:
    ```bash
    python src/cli.py update --id <task_id> --title "Updated title" --description "Updated description"
    ```

-   **Delete Task**:
    ```bash
    python src/cli.py delete --id <task_id>
    ```

## Example Workflow

1.  Add a task:
    ```bash
    python src/cli.py add --title "Buy groceries" --description "Milk, eggs, bread"
    ```
2.  Add another task:
    ```bash
    python src/cli.py add --title "Walk the dog" --description "Evening walk"
    ```
3.  View tasks:
    ```bash
    python src/cli.py list
    ```
4.  Complete a task (assuming ID 1 is "Buy groceries"):
    ```bash
    python src/cli.py complete --id 1
    ```
5.  View tasks again:
    ```bash
    python src/cli.py list
    ```
