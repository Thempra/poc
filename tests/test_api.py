# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from app.database import Base, engine as db_engine
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database and tables
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def db():
    """Create a new database session for each test function."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c


# CRUD operations for Call model
def test_create_call(client, db):
    call_data = {
        "call_id": "test-call-id",
        "name": "Test Call",
        "sector": "IT",
        "description": "A test call",
        "url": "http://example.com/test",
        "total_funding": 100000.0,
        "funding_percentage": 50.0,
        "max_per_company": 5000.0,
        "deadline": func.now(),
        "processing_status": "Pending",
        "analysis_status": "Not Started",
        "relevance_score": 85.0
    }
    response = client.post("/calls/", json=call_data)
    assert response.status_code == 201
    created_call = response.json()
    assert created_call["name"] == call_data["name"]
    db.query(Call).filter_by(id=created_call["id"]).delete()


def test_read_calls(client, db):
    calls = [
        {
            "call_id": f"test-call-id-{i}",
            "name": f"Test Call {i}",
            "sector": "IT",
            "description": f"A test call {i}",
            "url": f"http://example.com/test{i}",
            "total_funding": 100000.0 * i,
            "funding_percentage": 50.0 * i,
            "max_per_company": 5000.0 * i,
            "deadline": func.now(),
            "processing_status": f"Pending {i}",
            "analysis_status": f"Not Started {i}",
            "relevance_score": 85.0 - i
        }
        for i in range(1, 6)
    ]
    for call_data in calls:
        client.post("/calls/", json=call_data)

    response = client.get("/calls/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(calls)


def test_update_call(client, db):
    call_data = {
        "call_id": "test-call-id",
        "name": "Test Call",
        "sector": "IT",
        "description": "A test call",
        "url": "http://example.com/test",
        "total_funding": 100000.0,
        "funding_percentage": 50.0,
        "max_per_company": 5000.0,
        "deadline": func.now(),
        "processing_status": "Pending",
        "analysis_status": "Not Started",
        "relevance_score": 85.0
    }
    response = client.post("/calls/", json=call_data)
    call_id = response.json()["id"]

    update_data = {
        "name": "Updated Call Name"
    }
    response = client.put(f"/calls/{call_id}", json=update_data)
    assert response.status_code == 200
    updated_call = response.json()
    assert updated_call["name"] == update_data["name"]
    db.query(Call).filter_by(id=updated_call["id"]).delete()


def test_delete_call(client, db):
    call_data = {
        "call_id": "test-call-id",
        "name": "Test Call",
        "sector": "IT",
        "description": "A test call",
        "url": "http://example.com/test",
        "total_funding": 100000.0,
        "funding_percentage": 50.0,
        "max_per_company": 5000.0,
        "deadline": func.now(),
        "processing_status": "Pending",
        "analysis_status": "Not Started",
        "relevance_score": 85.0
    }
    response = client.post("/calls/", json=call_data)
    call_id = response.json()["id"]

    response = client.delete(f"/calls/{call_id}")
    assert response.status_code == 204
    with pytest.raises(CallNotFound):
        db.query(Call).filter_by(id=call_id).one()

# Authentication tests (if present)
# Error handling tests (e.g., 404, 400, etc.)
# Edge cases and validation tests

