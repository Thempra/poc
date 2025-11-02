import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, engine as db_engine

# Fixture for database setup/teardown
@pytest.fixture(scope="module")
def test_db():
    # Create an in-memory SQLite database for testing
    test_engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    # Create the tables in the in-memory database
    Base.metadata.create_all(bind=test_engine)
    
    yield TestingSessionLocal
    
    # Drop all tables after tests are done
    Base.metadata.drop_all(bind=test_engine)

# Fixture for TestClient
@pytest.fixture(scope="module")
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db()
    yield TestClient(app)

# CRUD operations tests
def test_create_call(client, test_db):
    call_data = {
        "call_id": "test-call-id",
        "name": "Test Call",
        "sector": "Test Sector",
        "description": "This is a test call.",
        "url": "http://example.com/test-call",
        "total_funding": 1000.0,
        "funding_percentage": 50.0,
        "max_per_company": 200.0,
        "deadline": "2023-12-31T23:59:59Z",
        "processing_status": "pending",
        "analysis_status": "not_analyzed",
        "relevance_score": 80.0
    }
    
    response = client.post("/calls/", json=call_data)
    assert response.status_code == 201
    call_id = response.json()["id"]
    
    # Verify the call was created in the database
    with test_db() as db:
        query = text("SELECT * FROM calls WHERE id = :id")
        result = db.execute(query, {"id": call_id}).fetchone()
        assert result is not None

def test_read_call(client):
    response = client.get("/calls/1")  # Assuming there's a call with id=1 in the database
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "1"  # Adjust as necessary based on actual test setup

def test_update_call(client):
    update_data = {
        "name": "Updated Call Name"
    }
    
    response = client.put("/calls/1", json=update_data)  # Assuming there's a call with id=1 in the database
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "1" and data["name"] == "Updated Call Name"

def test_delete_call(client):
    response = client.delete("/calls/1")  # Assuming there's a call with id=1 in the database
    assert response.status_code == 204
    
    # Verify the call was deleted from the database
    with test_db() as db:
        query = text("SELECT * FROM calls WHERE id = :id")
        result = db.execute(query, {"id": "1"}).fetchone()
        assert result is None

# Authentication tests (if present)
# def test_auth(client):
#     # Implement authentication tests
#     pass

# Error handling tests
def test_error_404(client):
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404
    
def test_error_400(client):
    bad_data = {
        "call_id": None,  # Invalid data to cause a 400 Bad Request
        # other required fields...
    }
    
    response = client.post("/calls/", json=bad_data)
    assert response.status_code == 400

# Edge cases and validation tests
def test_edge_case(client):
    edge_call_data = {
        "call_id": "a" * 256,  # Exceeding max length of VARCHAR(255)
        # other required fields...
    }
    
    response = client.post("/calls/", json=edge_call_data)
    assert response.status_code == 422

def test_validation(client):
    invalid_call_data = {
        "call_id": "test-call-id",
        "name": None,  # Missing a required field
        # other required fields...
    }
    
    response = client.post("/calls/", json=invalid_call_data)
    assert response.status_code == 422
