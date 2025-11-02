# tests/test_api.py
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import Task

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def setup_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_task(client):
    task_data = {
        "name": "Test Task",
        "description": "This is a test task"
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == task_data["name"]
    assert data["description"] == task_data["description"]

def test_read_task(client):
    task_data = {
        "name": "Test Task",
        "description": "This is a test task"
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    created_task = response.json()
    
    read_response = client.get(f"/tasks/{created_task['id']}/")
    assert read_response.status_code == 200
    data = read_response.json()
    assert data["name"] == created_task["name"]
    assert data["description"] == created_task["description"]

def test_update_task(client):
    task_data = {
        "name": "Test Task",
        "description": "This is a test task"
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    created_task = response.json()
    
    updated_data = {
        "name": "Updated Test Task",
        "description": "This is an updated test task"
    }
    update_response = client.put(f"/tasks/{created_task['id']}/", json=updated_data)
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == updated_data["name"]
    assert data["description"] == updated_data["description"]

def test_delete_task(client):
    task_data = {
        "name": "Test Task",
        "description": "This is a test task"
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    created_task = response.json()
    
    delete_response = client.delete(f"/tasks/{created_task['id']}/")
    assert delete_response.status_code == 204

def test_read_nonexistent_task(client):
    response = client.get("/tasks/999/")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Task not found"

def test_create_task_with_invalid_data(client):
    task_data = {
        "name": "Test Task",
        "description": None  # Invalid data
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 400

def test_update_task_with_invalid_data(client):
    task_data = {
        "name": "Test Task",
        "description": "This is a test task"
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    created_task = response.json()
    
    updated_data = {
        "name": None,  # Invalid data
        "description": "This is an updated test task"
    }
    update_response = client.put(f"/tasks/{created_task['id']}/", json=updated_data)
    assert update_response.status_code == 400

def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/999/")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Task not found"
