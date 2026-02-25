import pytest
from todo_app.models import Task
from todo_app.services import TodoService


class TestTodoServiceDelete:
    """Unit tests for TodoService.delete_task method"""

    def test_delete_task_success(self):
        """Test that delete_task successfully removes a task"""
        service = TodoService()
        task = service.add_task("Test Task", "Test Description")

        # Verify task exists before deletion
        tasks_before = service.get_all_tasks()
        assert len(tasks_before) == 1
        assert tasks_before[0].id == task.id

        # Delete the task
        result = service.delete_task(task.id)

        # Verify the returned task matches the deleted one
        assert result is not None
        assert result.id == task.id
        assert result.title == "Test Task"

        # Verify the task is no longer in storage
        tasks_after = service.get_all_tasks()
        assert len(tasks_after) == 0

    def test_delete_task_multiple_tasks(self):
        """Test that delete_task only removes the specified task"""
        service = TodoService()
        task1 = service.add_task("Task 1", "Description 1")
        task2 = service.add_task("Task 2", "Description 2")
        task3 = service.add_task("Task 3", "Description 3")

        # Verify all tasks exist before deletion
        tasks_before = service.get_all_tasks()
        assert len(tasks_before) == 3

        # Delete only task2
        deleted_task = service.delete_task(task2.id)

        # Verify the returned task is the one that was deleted
        assert deleted_task.id == task2.id

        # Verify only task2 is gone from storage
        tasks_after = service.get_all_tasks()
        assert len(tasks_after) == 2

        # Verify task1 and task3 still exist
        remaining_ids = [t.id for t in tasks_after]
        assert task1.id in remaining_ids
        assert task3.id in remaining_ids
        assert task2.id not in remaining_ids

    def test_delete_task_non_existent_id(self):
        """Test that delete_task raises exception for non-existent task ID"""
        service = TodoService()

        # Try to delete a task with ID that doesn't exist
        with pytest.raises(ValueError, match="Task with ID 999 not found"):
            service.delete_task(999)

        # Verify no tasks were added or removed
        assert len(service.get_all_tasks()) == 0

    def test_delete_task_empty_list(self):
        """Test that delete_task raises exception when list is empty"""
        service = TodoService()

        # Try to delete a task from an empty list
        with pytest.raises(ValueError, match="Task with ID 1 not found"):
            service.delete_task(1)

        # Verify no tasks exist
        assert len(service.get_all_tasks()) == 0

    def test_delete_task_completed_task(self):
        """Test that delete_task can delete a completed task"""
        service = TodoService()
        task = service.add_task("Test Task", "Test Description")
        service.mark_task_complete(task.id)  # Mark as completed first

        # Verify task exists and is completed
        tasks_before = service.get_all_tasks()
        assert len(tasks_before) == 1
        assert tasks_before[0].status == "completed"

        # Delete the completed task
        deleted_task = service.delete_task(task.id)

        # Verify the task is returned and was deleted from storage
        assert deleted_task.id == task.id
        assert deleted_task.status == "completed"  # Should maintain original status

        tasks_after = service.get_all_tasks()
        assert len(tasks_after) == 0

    def test_delete_all_tasks(self):
        """Test that deleting all tasks results in an empty list"""
        service = TodoService()
        task1 = service.add_task("Task 1", "Description 1")
        task2 = service.add_task("Task 2", "Description 2")

        # Delete both tasks
        service.delete_task(task1.id)
        service.delete_task(task2.id)

        # Verify the list is empty
        tasks_after = service.get_all_tasks()
        assert len(tasks_after) == 0