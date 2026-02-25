import pytest
from todo_app.models import Task
from todo_app.services import TodoService

def test_add_task_success():
    service = TodoService()
    task = service.add_task("Buy groceries", "Milk, eggs, bread")
    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs, bread"
    assert task.status == "pending"
    assert len(service._tasks) == 1
    assert service._tasks[0] == task

def test_add_task_empty_description():
    service = TodoService()
    task = service.add_task("Walk the dog", "")
    assert task.id == 1
    assert task.title == "Walk the dog"
    assert task.description == ""
    assert task.status == "pending"
    assert len(service._tasks) == 1
    assert service._tasks[0] == task

def test_add_task_multiple_tasks():
    service = TodoService()
    task1 = service.add_task("Task 1", "Desc 1")
    task2 = service.add_task("Task 2", "Desc 2")

    assert task1.id == 1
    assert task2.id == 2
    assert len(service._tasks) == 2
    assert service._tasks[0] == task1
    assert service._tasks[1] == task2

def test_add_task_empty_title_raises_error():
    service = TodoService()
    with pytest.raises(ValueError, match="Title cannot be empty"):  # Expect a ValueError for empty title
        service.add_task("", "Description")
    assert len(service._tasks) == 0
