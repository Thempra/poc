import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app, get_db

# Create a fixture to handle database operations
@pytest.fixture(scope="module")
def db_session():
    """Create a new database session for testing"""
    from app.database import engine, Base
    Base.metadata.create_all(bind=engine)
    yield SessionLocal()
    Base.metadata.drop_all(bind=engine)

# Create a client fixture that will use the test database
@pytest.fixture
def client(db_session):
    """Create a test client for the FastAPI application"""
    def override_get_db():
        return db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client

# CRUD Operations Tests
def test_create_task(client: TestClient, db_session):
    """Test creating a task"""
    response = client.post("/tasks/", json={"name": "Test Task", "description": "This is a test task"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Task"
    assert data["description"] == "This is a test task"

def test_read_task(client: TestClient, db_session):
    """Test reading a task"""
    # First, create a task to read
    client.post("/tasks/", json={"name": "Task for Reading", "description": "Read this task"})
    response = client.get("/tasks/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Task for Reading"

def test_update_task(client: TestClient, db_session):
    """Test updating a task"""
    # First, create a task to update
    client.post("/tasks/", json={"name": "Task for Updating", "description": "Update this task"})
    response = client.put("/tasks/1", json={"name": "Updated Task Name", "description": "This task has been updated"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Task Name"

def test_delete_task(client: TestClient, db_session):
    """Test deleting a task"""
    # First, create a task to delete
    client.post("/tasks/", json={"name": "Task for Deleting", "description": "Delete this task"})
    response = client.delete("/tasks/1")
    assert response.status_code == 204

# Error Handling Tests
def test_read_task_not_found(client: TestClient, db_session):
    """Test reading a non-existent task"""
    response = client.get("/tasks/999")
    assert response.status_code == 404

def test_create_task_missing_fields(client: TestClient, db_session):
    """Test creating a task without required fields"""
    response = client.post("/tasks/", json={"name": "Missing Description"})
    assert response.status_code == 422

# Edge Cases and Validation Tests
def test_read_all_tasks(client: TestClient, db_session):
    """Test reading all tasks"""
    # Create multiple tasks to read all of them
    for i in range(5):
        client.post("/tasks/", json={"name": f"Task {i}", "description": f"This is task {i}"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

# Authentication Tests (if implemented)
# def test_authenticate_user(client: TestClient, db_session):
#     """Test authenticating a user"""
#     response = client.post("/auth/token", data={"username": "testuser", "password": "testpass"})
#     assert response.status_code == 200
#     data = response.json()
#     assert "access_token" in data

