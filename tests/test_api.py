import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app, TaskCreate, TaskUpdate, get_db

# Define an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a simple Task model for testing
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Fixtures for testing
@pytest.fixture
def task_data():
    return TaskCreate(name="Test Task", description="This is a test task.")

# CRUD tests
def test_create_task(task_data):
    response = client.post("/tasks/", json=task_data.dict())
    assert response.status_code == 201
    created_task = response.json()
    assert created_task["name"] == task_data.name
    assert created_task["description"] == task_data.description

def test_read_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) > 0

def test_update_task(task_data):
    # First, create a task to update
    created_response = client.post("/tasks/", json=task_data.dict())
    created_task_id = created_response.json()["id"]

    updated_task_data = TaskUpdate(description="Updated description")
    response = client.put(f"/tasks/{created_task_id}", json=updated_task_data.dict())
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["description"] == updated_task_data.description

def test_delete_task(task_data):
    # First, create a task to delete
    created_response = client.post("/tasks/", json=task_data.dict())
    created_task_id = created_response.json()["id"]

    response = client.delete(f"/tasks/{created_task_id}")
    assert response.status_code == 204

# Error handling tests
def test_read_nonexistent_task():
    response = client.get("/tasks/999")
    assert response.status_code == 404

def test_update_nonexistent_task(task_data):
    response = client.put("/tasks/999", json=task_data.dict())
    assert response.status_code == 404

def test_delete_nonexistent_task():
    response = client.delete("/tasks/999")
    assert response.status_code == 404
