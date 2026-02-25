import pytest
from todo_app.models import Task

def test_task_creation():
    task = Task(id=1, title="Test Task", description="This is a test description")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "This is a test description"
    assert task.status == "pending"

def test_task_creation_with_default_status():
    task = Task(id=2, title="Another Task", description="")
    assert task.id == 2
    assert task.title == "Another Task"
    assert task.description == ""
    assert task.status == "pending"

def test_task_creation_with_custom_status():
    task = Task(id=3, title="Completed Task", description="Done", status="completed")
    assert task.id == 3
    assert task.title == "Completed Task"
    assert task.description == "Done"
    assert task.status == "completed"
