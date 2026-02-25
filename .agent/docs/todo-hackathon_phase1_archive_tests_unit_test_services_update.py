import pytest
from todo_app.models import Task
from todo_app.services import TodoService


class TestTodoServiceUpdate:
    """Unit tests for TodoService.update_task method"""

    def test_update_task_title_success(self):
        """Test that update_task successfully changes a task's title"""
        service = TodoService()
        task = service.add_task("Original Title", "Original Description")

        # Update only the title
        updated_task = service.update_task(task.id, new_title="Updated Title")

        # Verify the returned task has updated title
        assert updated_task.id == task.id
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged
        assert updated_task.status == "pending"  # Should remain unchanged

        # Verify the task in storage has updated title
        stored_tasks = service.get_all_tasks()
        updated_stored_task = next((t for t in stored_tasks if t.id == task.id), None)
        assert updated_stored_task is not None
        assert updated_stored_task.title == "Updated Title"

    def test_update_task_description_success(self):
        """Test that update_task successfully changes a task's description"""
        service = TodoService()
        task = service.add_task("Original Title", "Original Description")

        # Update only the description
        updated_task = service.update_task(task.id, new_description="Updated Description")

        # Verify the returned task has updated description
        assert updated_task.id == task.id
        assert updated_task.title == "Original Title"  # Should remain unchanged
        assert updated_task.description == "Updated Description"
        assert updated_task.status == "pending"  # Should remain unchanged

    def test_update_task_both_fields_success(self):
        """Test that update_task successfully changes both title and description"""
        service = TodoService()
        task = service.add_task("Original Title", "Original Description")

        # Update both title and description
        updated_task = service.update_task(task.id, new_title="Updated Title", new_description="Updated Description")

        # Verify the returned task has both fields updated
        assert updated_task.id == task.id
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.status == "pending"  # Should remain unchanged

    def test_update_task_non_existent_id(self):
        """Test that update_task raises exception for non-existent task ID"""
        service = TodoService()

        # Try to update a task with ID that doesn't exist
        with pytest.raises(ValueError, match="Task with ID 999 not found"):
            service.update_task(999, new_title="New Title")

        # Verify no tasks were added
        assert len(service.get_all_tasks()) == 0

    def test_update_task_empty_title_validation(self):
        """Test that update_task validates empty title"""
        service = TodoService()
        task = service.add_task("Original Title", "Original Description")

        # Try to update with empty title
        with pytest.raises(ValueError, match="Title cannot be empty"):
            service.update_task(task.id, new_title="")

        # Verify the original task remains unchanged
        stored_tasks = service.get_all_tasks()
        original_task = next((t for t in stored_tasks if t.id == task.id), None)
        assert original_task is not None
        assert original_task.title == "Original Title"
        assert original_task.description == "Original Description"

    def test_update_task_only_description_when_title_provided_empty(self):
        """Test that update_task can update description even if empty title is not changing"""
        service = TodoService()
        task = service.add_task("Original Title", "Original Description")

        # Update only description, not changing the title (passing None for title)
        updated_task = service.update_task(task.id, new_description="New Description")

        # Verify only description was updated
        assert updated_task.title == "Original Title"
        assert updated_task.description == "New Description"

    def test_update_task_multiple_tasks(self):
        """Test that update_task only affects the specified task"""
        service = TodoService()
        task1 = service.add_task("Task 1", "Description 1")
        task2 = service.add_task("Task 2", "Description 2")
        task3 = service.add_task("Task 3", "Description 3")

        # Update only task2
        service.update_task(task2.id, new_title="Updated Task 2", new_description="Updated Description 2")

        # Verify only task2 was updated
        all_tasks = service.get_all_tasks()
        for task in all_tasks:
            if task.id == task2.id:
                assert task.title == "Updated Task 2"
                assert task.description == "Updated Description 2"
            elif task.id == task1.id:
                assert task.title == "Task 1"
                assert task.description == "Description 1"
            elif task.id == task3.id:
                assert task.title == "Task 3"
                assert task.description == "Description 3"