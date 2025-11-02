import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base
from app.models import Call

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def override_get_db():
    try:
        yield TestingSessionLocal()
    finally:
        pass

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def db_session():
    testing_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=testing_engine)
    Base.metadata.create_all(bind=testing_engine)
    yield testing_session()
    Base.metadata.drop_all(bind=testing_engine)

def test_create_task(db_session):
    payload = {
        "task_id": "12345",
        "name": "Test Task",
        "description": "This is a test task",
        "status": "pending"
    }
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 200
    created_task = response.json()
    assert created_task["id"] is not None
    assert created_task["task_id"] == payload["task_id"]
    assert created_task["name"] == payload["name"]
    assert created_task["description"] == payload["description"]
    assert created_task["status"] == payload["status"]

def test_read_task(db_session):
    payload = {
        "task_id": "12345",
        "name": "Test Task",
        "description": "This is a test task",
        "status": "pending"
    }
    response = client.post("/tasks/", json=payload)
    created_task_id = response.json()["id"]

    read_response = client.get(f"/tasks/{created_task_id}")
    assert read_response.status_code == 200
    read_task = read_response.json()
    assert read_task["id"] == created_task_id
    assert read_task["task_id"] == payload["task_id"]
    assert read_task["name"] == payload["name"]
    assert read_task["description"] == payload["description"]
    assert read_task["status"] == payload["status"]

def test_update_task(db_session):
    payload = {
        "task_id": "12345",
        "name": "Test Task",
        "description": "This is a test task",
        "status": "pending"
    }
    response = client.post("/tasks/", json=payload)
    created_task_id = response.json()["id"]

    update_payload = {
        "task_id": "12345",
        "name": "Updated Task Name",
        "description": "This is an updated test task",
        "status": "completed"
    }

    update_response = client.put(f"/tasks/{created_task_id}", json=update_payload)
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["id"] == created_task_id
    assert updated_task["task_id"] == payload["task_id"]
    assert updated_task["name"] == update_payload["name"]
    assert updated_task["description"] == update_payload["description"]
    assert updated_task["status"] == update_payload["status"]

def test_delete_task(db_session):
    payload = {
        "task_id": "12345",
        "name": "Test Task",
        "description": "This is a test task",
        "status": "pending"
    }
    response = client.post("/tasks/", json=payload)
    created_task_id = response.json()["id"]

    delete_response = client.delete(f"/tasks/{created_task_id}")
    assert delete_response.status_code == 204

def test_read_nonexistent_task(db_session):
    non_existent_id = "non_existent"
    read_response = client.get(f"/tasks/{non_existent_id}")
    assert read_response.status_code == 404

def test_create_duplicate_task(db_session):
    payload = {
        "task_id": "12345",
        "name": "Test Task",
        "description": "This is a test task",
        "status": "pending"
    }
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 200

    duplicate_response = client.post("/tasks/", json=payload)
    assert duplicate_response.status_code == 400
