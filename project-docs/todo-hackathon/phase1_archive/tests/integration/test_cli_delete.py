import pytest
import sys
from io import StringIO
from unittest.mock import patch
from backend.cli import main
from todo_app.models import Task


class TestCliDeleteIntegration:
    """Integration tests for the delete CLI command"""

    def test_delete_command_valid_id(self):
        """Test that delete command successfully removes a task"""
        # Mock service with tasks
        task_to_delete = Task(id=1, title="Task to Delete", description="Description", status="pending")

        captured_output = StringIO()

        with patch('backend.cli.TodoService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.delete_task.return_value = task_to_delete

            with patch('sys.argv', ['cli.py', 'delete', '--id', '1']):
                original_stdout = sys.stdout
                sys.stdout = captured_output
                try:
                    main()
                except SystemExit:
                    pass
                finally:
                    sys.stdout = original_stdout

        output = captured_output.getvalue()
        # After implementation, this should confirm the task was deleted

    def test_delete_command_invalid_id(self):
        """Test that delete command shows error for non-existent task ID"""
        captured_output = StringIO()

        with patch('backend.cli.TodoService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.delete_task.side_effect = ValueError("Task with ID 999 not found")

            with patch('sys.argv', ['cli.py', 'delete', '--id', '999']):
                original_stdout = sys.stdout
                sys.stdout = captured_output
                try:
                    main()
                except SystemExit:
                    pass
                finally:
                    sys.stdout = original_stdout

        output = captured_output.getvalue()
        # After implementation, this should show an error message

    def test_delete_command_missing_id(self):
        """Test that delete command shows error when ID is not provided"""
        captured_output = StringIO()

        with patch('sys.argv', ['cli.py', 'delete']):  # No --id argument
            original_stdout = sys.stdout
            sys.stdout = captured_output
            try:
                main()
            except SystemExit:
                pass  # Expected for missing required argument
            finally:
                sys.stdout = original_stdout

        output = captured_output.getvalue()
        # Should show usage error or similar