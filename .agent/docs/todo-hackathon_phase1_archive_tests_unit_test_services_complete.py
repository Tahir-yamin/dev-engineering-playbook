import pytest
from todo_app.models import Task
from todo_app.services import TodoService


class TestTodoServiceComplete:
    """Unit tests for TodoService.mark_task_complete method"""

    def test_mark_task_complete_success(self):
        """Test that mark_task_complete successfully changes a task's status to completed"""
        service = TodoService()
        task = service.add_task("Test Task", "Test Description")

        # Verify initial status
        assert task.status == "pending"

        # Mark task as complete
        result = service.mark_task_complete(task.id)

        # Verify the returned task has updated status
        assert result is not None
        assert result.id == task.id
        assert result.status == "completed"

        # Verify the task in storage has updated status
        stored_tasks = service.get_all_tasks()
        completed_task = next((t for t in stored_tasks if t.id == task.id), None)
        assert completed_task is not None
        assert completed_task.status == "completed"

    def test_mark_task_complete_already_completed(self):
        """Test that mark_task_complete works on a task that is already completed"""
        service = TodoService()
        task = service.add_task("Test Task", "Test Description")

        # First, mark as complete
        service.mark_task_complete(task.id)

        # Try to mark as complete again
        result = service.mark_task_complete(task.id)

        # Should still return the completed task
        assert result is not None
        assert result.id == task.id
        assert result.status == "completed"

    def test_mark_task_complete_non_existent_id(self):
        """Test that mark_task_complete raises exception for non-existent task ID"""
        service = TodoService()

        # Try to mark a task with ID that doesn't exist
        with pytest.raises(ValueError, match="Task with ID 999 not found"):
            service.mark_task_complete(999)

        # Verify no tasks were added
        assert len(service.get_all_tasks()) == 0

    def test_mark_task_complete_multiple_tasks(self):
        """Test that mark_task_complete only affects the specified task"""
        service = TodoService()
        task1 = service.add_task("Task 1", "Description 1")
        task2 = service.add_task("Task 2", "Description 2")
        task3 = service.add_task("Task 3", "Description 3")

        # Verify all tasks are pending initially
        for task in [task1, task2, task3]:
            assert task.status == "pending"

        # Mark only task2 as complete
        service.mark_task_complete(task2.id)

        # Verify only task2 is completed
        all_tasks = service.get_all_tasks()
        for task in all_tasks:
            if task.id == task2.id:
                assert task.status == "completed"
            else:
                assert task.status == "pending"