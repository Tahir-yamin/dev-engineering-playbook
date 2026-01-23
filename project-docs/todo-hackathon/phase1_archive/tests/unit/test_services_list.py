import pytest
from todo_app.models import Task
from todo_app.services import TodoService


class TestTodoServiceList:
    """Unit tests for TodoService.get_all_tasks method"""

    def test_get_all_tasks_empty_list(self):
        """Test that get_all_tasks returns an empty list when no tasks exist"""
        service = TodoService()
        tasks = service.get_all_tasks()

        assert tasks == []
        assert len(tasks) == 0

    def test_get_all_tasks_single_task(self):
        """Test that get_all_tasks returns a single task when one exists"""
        service = TodoService()
        task = service.add_task("Test Title", "Test Description")
        tasks = service.get_all_tasks()

        assert len(tasks) == 1
        assert tasks[0] == task
        assert tasks[0].title == "Test Title"
        assert tasks[0].description == "Test Description"
        assert tasks[0].status == "pending"

    def test_get_all_tasks_multiple_tasks(self):
        """Test that get_all_tasks returns all tasks when multiple exist"""
        service = TodoService()

        # Add multiple tasks
        task1 = service.add_task("Task 1", "Description 1")
        task2 = service.add_task("Task 2", "Description 2")
        task3 = service.add_task("Task 3", "Description 3")

        tasks = service.get_all_tasks()

        assert len(tasks) == 3
        assert tasks[0] == task1
        assert tasks[1] == task2
        assert tasks[2] == task3

        # Verify they're in the order they were added
        for i, task in enumerate(tasks):
            assert task.title == f"Task {i+1}"
            assert task.description == f"Description {i+1}"

    def test_get_all_tasks_with_completed_tasks(self):
        """Test that get_all_tasks returns both pending and completed tasks"""
        service = TodoService()

        # Add a task and mark it as complete (we'll test this functionality separately)
        task1 = service.add_task("Pending Task", "Pending Description")
        task2 = service.add_task("Completed Task", "Completed Description")

        # Manually mark task2 as completed for testing purposes
        task2.status = "completed"

        tasks = service.get_all_tasks()

        assert len(tasks) == 2
        assert any(task.id == task1.id and task.status == "pending" for task in tasks)
        assert any(task.id == task2.id and task.status == "completed" for task in tasks)