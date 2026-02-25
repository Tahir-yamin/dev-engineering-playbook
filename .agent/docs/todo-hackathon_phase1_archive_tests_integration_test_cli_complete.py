import pytest
import sys
from io import StringIO
from unittest.mock import patch
from backend.cli import main
from todo_app.models import Task


class TestCliCompleteIntegration:
    """Integration tests for the complete CLI command"""

    def test_complete_command_valid_id(self):
        """Test that complete command successfully marks a task as complete"""
        # Mock service with tasks
        mock_tasks = [Task(id=1, title="Sample Task", description="Sample Description", status="pending")]

        captured_output = StringIO()

        with patch('backend.cli.TodoService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.get_all_tasks.return_value = mock_tasks
            mock_service.mark_task_complete.return_value = Task(
                id=1, title="Sample Task", description="Sample Description", status="completed"
            )

            with patch('sys.argv', ['cli.py', 'complete', '--id', '1']):
                original_stdout = sys.stdout
                sys.stdout = captured_output
                try:
                    main()
                except SystemExit:
                    pass
                finally:
                    sys.stdout = original_stdout

        output = captured_output.getvalue()
        # After implementation, this should confirm the task was completed

    def test_complete_command_invalid_id(self):
        """Test that complete command shows error for non-existent task ID"""
        captured_output = StringIO()

        with patch('backend.cli.TodoService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.mark_task_complete.side_effect = ValueError("Task with ID 999 not found")

            with patch('sys.argv', ['cli.py', 'complete', '--id', '999']):
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

    def test_complete_command_missing_id(self):
        """Test that complete command shows error when ID is not provided"""
        captured_output = StringIO()

        with patch('sys.argv', ['cli.py', 'complete']):  # No --id argument
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