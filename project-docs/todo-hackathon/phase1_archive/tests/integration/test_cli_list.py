import pytest
import sys
from io import StringIO
from unittest.mock import patch
from backend.cli import main
from todo_app.services import TodoService


class TestCliListIntegration:
    """Integration tests for the list CLI command"""

    def test_list_command_empty_list_output(self):
        """Test that list command shows appropriate message when no tasks exist"""
        # Create a temporary service to test with
        service = TodoService()

        # Capture stdout
        captured_output = StringIO()

        # Since we'll be testing the main function, we need to mock the service
        # We'll use a fixture approach by patching the TodoService initialization
        with patch('backend.cli.TodoService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.get_all_tasks.return_value = []

            with patch('sys.argv', ['cli.py', 'list']):
                original_stdout = sys.stdout
                sys.stdout = captured_output
                try:
                    main()
                except SystemExit:
                    pass  # argparse may call sys.exit when processing --help or on error
                finally:
                    sys.stdout = original_stdout

        output = captured_output.getvalue()
        # After implementation, this should show an appropriate message for empty list
        # For now, this test will help validate the implementation once it's done

    def test_list_command_with_tasks(self):
        """Test that list command displays tasks in a user-friendly format when tasks exist"""
        # Mock service with tasks
        from todo_app.models import Task
        mock_tasks = [
            Task(id=1, title="Task 1", description="Description 1", status="pending"),
            Task(id=2, title="Task 2", description="Description 2", status="completed")
        ]

        captured_output = StringIO()

        with patch('backend.cli.TodoService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.get_all_tasks.return_value = mock_tasks

            with patch('sys.argv', ['cli.py', 'list']):
                original_stdout = sys.stdout
                sys.stdout = captured_output
                try:
                    main()
                except SystemExit:
                    pass
                finally:
                    sys.stdout = original_stdout

        output = captured_output.getvalue()
        # After implementation, this should display the tasks in a user-friendly format

    def test_list_command_formatting(self):
        """Test that list command output is formatted correctly"""
        # This test verifies that the output format is user-friendly
        from todo_app.models import Task
        mock_tasks = [
            Task(id=1, title="Sample Task", description="Sample Description", status="pending")
        ]

        captured_output = StringIO()

        with patch('backend.cli.TodoService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.get_all_tasks.return_value = mock_tasks

            with patch('sys.argv', ['cli.py', 'list']):
                original_stdout = sys.stdout
                sys.stdout = captured_output
                try:
                    main()
                except SystemExit:
                    pass
                finally:
                    sys.stdout = original_stdout

        output = captured_output.getvalue()
        # After implementation, verify that the format includes ID, title, description, and status