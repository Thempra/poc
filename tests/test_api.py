# tests/test_api.py
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app, get_db
from app.models import Call
from app.crud import create_call, read_calls

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
def db():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    Base.metadata.create_all(bind=engine)
    yield db
    Base.metadata.drop_all(bind=engine)

def test_create_call(client: TestClient, db: Session):
    data = {
        "call_id": "test-call-id",
        "name": "Test Call",
        "sector": "Technology",
        "description": "This is a test call.",
        "url": "http://example.com/test",
        "total_funding": 1000.0,
        "funding_percentage": 50.0,
        "max_per_company": 200.0,
        "deadline": "2023-12-31T23:59:59Z",
        "processing_status": "Pending",
        "analysis_status": "Not Started",
        "relevance_score": 85.0
    }
    response = client.post("/tasks/calls", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    call_id = response.json()["id"]
    created_call = read_calls(db, call_id=call_id)
    assert created_call.call_id == data["call_id"]

def test_read_calls(client: TestClient, db: Session):
    create_call(db, Call(call_id="test-call-id", name="Test Call"))
    response = client.get("/tasks/calls")
    assert response.status_code == status.HTTP_200_OK
    calls = response.json()
    assert len(calls) == 1
    assert calls[0]["name"] == "Test Call"

def test_update_call(client: TestClient, db: Session):
    call = create_call(db, Call(call_id="test-call-id", name="Old Name"))
    data = {
        "name": "Updated Name"
    }
    response = client.put(f"/tasks/calls/{call.id}", json=data)
    assert response.status_code == status.HTTP_200_OK
    updated_call = read_calls(db, call_id=call.call_id)
    assert updated_call.name == data["name"]

def test_delete_call(client: TestClient, db: Session):
    call = create_call(db, Call(call_id="test-call-id", name="Test Call"))
    response = client.delete(f"/tasks/calls/{call.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(CallNotFound):
        read_calls(db, call_id=call.call_id)
