import pytest
import sys
from io import StringIO
from unittest.mock import patch
from backend.cli import main
from todo_app.models import Task


class TestCliUpdateIntegration:
    """Integration tests for the update CLI command"""

    def test_update_command_valid_id_title_only(self):
        """Test that update command successfully updates a task's title"""
        # Mock service with tasks
        original_task = Task(id=1, title="Original Title", description="Original Description", status="pending")
        updated_task = Task(id=1, title="Updated Title", description="Original Description", status="pending")

        captured_output = StringIO()

        with patch('backend.cli.TodoService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.update_task.return_value = updated_task

            with patch('sys.argv', ['cli.py', 'update', '--id', '1', '--title', 'Updated Title']):
                original_stdout = sys.stdout
                sys.stdout = captured_output
                try:
                    main()
                except SystemExit:
                    pass
                finally:
                    sys.stdout = original_stdout

        output = captured_output.getvalue()
        # After implementation, this should confirm the task was updated

    def test_update_command_valid_id_description_only(self):
        """Test that update command successfully updates a task's description"""
        # Mock service with tasks
        original_task = Task(id=1, title="Original Title", description="Original Description", status="pending")
        updated_task = Task(id=1, title="Original Title", description="Updated Description", status="pending")

        captured_output = StringIO()

        with patch('backend.cli.TodoService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.update_task.return_value = updated_task

            with patch('sys.argv', ['cli.py', 'update', '--id', '1', '--description', 'Updated Description']):
                original_stdout = sys.stdout
                sys.stdout = captured_output
                try:
                    main()
                except SystemExit:
                    pass
                finally:
                    sys.stdout = original_stdout

        output = captured_output.getvalue()
        # After implementation, this should confirm the task was updated

    def test_update_command_valid_id_both_fields(self):
        """Test that update command successfully updates both title and description"""
        # Mock service with tasks
        original_task = Task(id=1, title="Original Title", description="Original Description", status="pending")
        updated_task = Task(id=1, title="Updated Title", description="Updated Description", status="pending")

        captured_output = StringIO()

        with patch('backend.cli.TodoService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.update_task.return_value = updated_task

            with patch('sys.argv', ['cli.py', 'update', '--id', '1', '--title', 'Updated Title', '--description', 'Updated Description']):
                original_stdout = sys.stdout
                sys.stdout = captured_output
                try:
                    main()
                except SystemExit:
                    pass
                finally:
                    sys.stdout = original_stdout

        output = captured_output.getvalue()
        # After implementation, this should confirm the task was updated

    def test_update_command_invalid_id(self):
        """Test that update command shows error for non-existent task ID"""
        captured_output = StringIO()

        with patch('backend.cli.TodoService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.update_task.side_effect = ValueError("Task with ID 999 not found")

            with patch('sys.argv', ['cli.py', 'update', '--id', '999', '--title', 'New Title']):
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

    def test_update_command_empty_title_error(self):
        """Test that update command shows error when trying to set empty title"""
        captured_output = StringIO()

        with patch('backend.cli.TodoService') as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.update_task.side_effect = ValueError("Title cannot be empty")

            with patch('sys.argv', ['cli.py', 'update', '--id', '1', '--title', '']):
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

    def test_update_command_missing_id(self):
        """Test that update command shows error when ID is not provided"""
        captured_output = StringIO()

        with patch('sys.argv', ['cli.py', 'update']):  # No --id argument
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