# tests/test_api.py
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.main import app, get_db
from app.database import Base, engine
from app.crud import create_task, delete_task
from app.schemas import TaskCreate

# Create test database and session
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

# Fixture to provide a fresh database for each test
@pytest.fixture(autouse=True)
def db_session(test_client):
    Base.metadata.create_all(bind=engine)
    yield SessionLocal()
    Base.metadata.drop_all(bind=engine)

# Test create task
def test_create_task(test_client, db_session):
    task_data = TaskCreate(name="Test Task", description="This is a test task.")
    response = test_client.post("/tasks/", json=task_data.dict())
    assert response.status_code == 201
    created_task = response.json()
    assert created_task["name"] == "Test Task"
    assert created_task["description"] == "This is a test task."

# Test read task by ID
def test_read_task(test_client, db_session):
    task_data = TaskCreate(name="Read Task", description="Task to be read.")
    created_task = create_task(db_session, task_data)
    response = test_client.get(f"/tasks/{created_task.id}")
    assert response.status_code == 200
    read_task = response.json()
    assert read_task["id"] == str(created_task.id)

# Test update task
def test_update_task(test_client, db_session):
    task_data = TaskCreate(name="Update Task", description="Task to be updated.")
    created_task = create_task(db_session, task_data)
    new_data = {"name": "Updated Task"}
    response = test_client.put(f"/tasks/{created_task.id}", json=new_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["id"] == str(created_task.id)
    assert updated_task["name"] == "Updated Task"

# Test delete task
def test_delete_task(test_client, db_session):
    task_data = TaskCreate(name="Delete Task", description="Task to be deleted.")
    created_task = create_task(db_session, task_data)
    response = test_client.delete(f"/tasks/{created_task.id}")
    assert response.status_code == 204
    # Verify deletion by attempting to read the task again
    response = test_client.get(f"/tasks/{created_task.id}")
    assert response.status_code == 404

# Test error handling for non-existent task
def test_read_non_existent_task(test_client):
    response = test_client.get("/tasks/999")
    assert response.status_code == 404

# Test validation for empty name
def test_create_task_with_empty_name(test_client, db_session):
    task_data = TaskCreate(name="", description="Task with empty name.")
    response = test_client.post("/tasks/", json=task_data.dict())
    assert response.status_code == 422

# Test validation for long name
def test_create_task_with_long_name(test_client, db_session):
    task_data = TaskCreate(name="a" * 1001, description="Task with long name.")
    response = test_client.post("/tasks/", json=task_data.dict())
    assert response.status_code == 422

# Test validation for empty description
def test_create_task_with_empty_description(test_client, db_session):
    task_data = TaskCreate(name="Valid Name", description="")
    response = test_client.post("/tasks/", json=task_data.dict())
    assert response.status_code == 201
