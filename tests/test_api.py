import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base, get_db
from app.crud import create_task, update_task, get_task, delete_task

# Create a test database engine and session
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)

# Override the get_db dependency to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

# Test Create Task
def test_create_task(client):
    response = client.post(
        "/tasks/",
        json={
            "name": "Test Task",
            "description": "This is a test task.",
            "status": "pending",
            "due_date": "2023-12-31"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Task"

# Test Read Task
def test_read_task(client):
    task = create_task(
        db=TestingSessionLocal(),
        task={"name": "Read Test", "description": "For reading purposes.", "status": "completed", "due_date": "2023-12-31"}
    )
    response = client.get(f"/tasks/{task.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(task.id)

# Test Update Task
def test_update_task(client):
    task = create_task(
        db=TestingSessionLocal(),
        task={"name": "Update Test", "description": "For updating purposes.", "status": "pending", "due_date": "2023-12-31"}
    )
    response = client.put(
        f"/tasks/{task.id}",
        json={"status": "completed"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(task.id)
    assert data["status"] == "completed"

# Test Delete Task
def test_delete_task(client):
    task = create_task(
        db=TestingSessionLocal(),
        task={"name": "Delete Test", "description": "For deleting purposes.", "status": "pending", "due_date": "2023-12-31"}
    )
    response = client.delete(f"/tasks/{task.id}")
    assert response.status_code == 204
    with pytest.raises(Exception) as exc_info:
        get_task(db=TestingSessionLocal(), task_id=task.id)
    assert "Task not found" in str(exc_info.value)

# Test Error Handling (404)
def test_read_nonexistent_task(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404

# Test Validation
def test_create_task_with_invalid_data(client):
    response = client.post(
        "/tasks/",
        json={
            "name": "",
            "description": "This is a test task.",
            "status": "pending",
            "due_date": "2023-12-31"
        }
    )
    assert response.status_code == 422
