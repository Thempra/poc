import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base, engine
from app.models import Call

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Fixtures for setting up and tearing down the database
@pytest.fixture(autouse=True)
def setup_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Tests for CRUD operations on the Call model
def test_create_call():
    call_data = {
        "call_id": "test_call_1",
        "name": "Test Call",
        "sector": "IT",
        "description": "This is a test call",
        "url": "http://example.com/test",
        "total_funding": 1000.0,
        "funding_percentage": 50.0,
        "max_per_company": 200.0,
        "deadline": "2023-12-31T23:59:59Z",
        "processing_status": "pending",
        "analysis_status": "unanalyzed",
        "relevance_score": 80.0
    }
    response = client.post("/calls/", json=call_data)
    assert response.status_code == 201
    created_call = response.json()
    assert created_call["name"] == call_data["name"]
    return created_call

def test_get_call(created_call):
    response = client.get(f"/calls/{created_call['id']}")
    assert response.status_code == 200
    retrieved_call = response.json()
    assert retrieved_call["name"] == created_call["name"]

def test_update_call(created_call):
    update_data = {
        "name": "Updated Test Call",
        "total_funding": 1500.0
    }
    response = client.put(f"/calls/{created_call['id']}", json=update_data)
    assert response.status_code == 200
    updated_call = response.json()
    assert updated_call["name"] == update_data["name"]
    assert updated_call["total_funding"] == update_data["total_funding"]

def test_delete_call(created_call):
    response = client.delete(f"/calls/{created_call['id']}")
    assert response.status_code == 204
    response = client.get(f"/calls/{created_call['id']}")
    assert response.status_code == 404

# Test for authentication (if present)
# def test_auth():
#     # Add authentication tests here
#     pass

# Test for error handling
def test_error_handling():
    response = client.post("/calls/", json={"name": "Invalid Call"})
    assert response.status_code == 422

# Test for edge cases and validation
def test_edge_cases_and_validation():
    # Add edge case and validation tests here
    pass
