#!/usr/bin/env python3

import argparse
import sys
import os

# Add the project root directory to the path so we can import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from todo_app.services import TodoService


def format_task_output(task):
    """Format a single task for display."""
    status_icon = "✓" if task.status == "completed" else "○"
    return f"ID: {task.id} | {status_icon} {task.title} - {task.description} [{task.status}]"


def main():
    service = TodoService()

    parser = argparse.ArgumentParser(
        description="Todo CLI Application - Manage your tasks from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Add a task:           python cli.py add --title "Buy groceries" --description "Milk, bread, eggs"
  List all tasks:       python cli.py list
  Mark as complete:     python cli.py complete --id 1
  Update a task:        python cli.py update --id 1 --title "Updated title"
  Delete a task:        python cli.py delete --id 1
        """.strip()
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add Task Command
    add_parser = subparsers.add_parser("add", help="Add a new todo task")
    add_parser.add_argument("--title", required=True, help="Title of the task")
    add_parser.add_argument("--description", default="", help="Description of the task")

    # List Tasks Command
    list_parser = subparsers.add_parser("list", help="List all todo tasks")

    # Complete Task Command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("--id", type=int, required=True, help="ID of the task to complete")

    # Update Task Command
    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("--id", type=int, required=True, help="ID of the task to update")
    update_parser.add_argument("--title", required=False, help="New title for the task")
    update_parser.add_argument("--description", required=False, help="New description for the task")

    # Delete Task Command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("--id", type=int, required=True, help="ID of the task to delete")

    # If no command is provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    try:
        if args.command == "add":
            task = service.add_task(args.title, args.description)
            print(f"✓ Task added successfully: ID {task.id}, Title: {task.title}")
        elif args.command == "list":
            tasks = service.get_all_tasks()
            if not tasks:
                print("ℹ️  No tasks found.")
            else:
                print("📋 All Tasks:")
                for task in tasks:
                    print(f"  {format_task_output(task)}")
        elif args.command == "complete":
            completed_task = service.mark_task_complete(args.id)
            print(f"✓ Task marked as complete: ID {completed_task.id}, Title: {completed_task.title}")
        elif args.command == "update":
            updated_task = service.update_task(args.id, args.title, args.description)
            print(f"✓ Task updated successfully: ID {updated_task.id}, Title: {updated_task.title}")
        elif args.command == "delete":
            deleted_task = service.delete_task(args.id)
            print(f"✓ Task deleted successfully: ID {deleted_task.id}, Title: {deleted_task.title}")
        else:
            # This should not happen if argparse is working correctly
            parser.print_help()
            sys.exit(1)
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
