# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# CRUD Operations for Task Model

def test_create_task(setup_database):
    response = client.post("/tasks/", json={"name": "Test Task", "description": "This is a test task.", "status": "pending", "due_date": "2023-12-31T23:59:59"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Task"
    assert data["description"] == "This is a test task."
    assert data["status"] == "pending"

def test_get_task(setup_database):
    response = client.post("/tasks/", json={"name": "Test Task", "description": "This is a test task.", "status": "pending", "due_date": "2023-12-31T23:59:59"})
    assert response.status_code == 201
    data = response.json()
    response = client.get(f"/tasks/{data['id']}")
    assert response.status_code == 200
    task_data = response.json()
    assert task_data["name"] == "Test Task"

def test_update_task(setup_database):
    response = client.post("/tasks/", json={"name": "Test Task", "description": "This is a test task.", "status": "pending", "due_date": "2023-12-31T23:59:59"})
    assert response.status_code == 201
    data = response.json()
    updated_data = {"name": "Updated Task", "description": "This task has been updated.", "status": "completed"}
    response = client.put(f"/tasks/{data['id']}", json=updated_data)
    assert response.status_code == 200
    task_data = response.json()
    assert task_data["name"] == "Updated Task"

def test_delete_task(setup_database):
    response = client.post("/tasks/", json={"name": "Test Task", "description": "This is a test task.", "status": "pending", "due_date": "2023-12-31T23:59:59"})
    assert response.status_code == 201
    data = response.json()
    response = client.delete(f"/tasks/{data['id']}")
    assert response.status_code == 204

# Authentication (Placeholder, to be implemented)

def test_authenticate_user(setup_database):
    # This will be implemented based on the actual authentication mechanism
    pass

# Error Handling and Edge Cases

def test_read_task_not_found(setup_database):
    response = client.get("/tasks/1")
    assert response.status_code == 404

def test_create_task_with_invalid_data(setup_database):
    response = client.post("/tasks/", json={"name": "Test Task"})
    assert response.status_code == 422
