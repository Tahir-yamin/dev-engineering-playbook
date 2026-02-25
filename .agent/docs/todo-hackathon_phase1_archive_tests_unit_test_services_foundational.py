import pytest
from todo_app.services import TodoService

def test_generate_id_sequential():
    service = TodoService()
    assert service._generate_id() == 1
    assert service._generate_id() == 2
    assert service._generate_id() == 3

def test_generate_id_unique_across_instances():
    service1 = TodoService()
    service2 = TodoService()
    assert service1._generate_id() == 1
    assert service2._generate_id() == 1  # Each service instance has its own counter
    assert service1._generate_id() == 2
    assert service2._generate_id() == 2
