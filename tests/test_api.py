# tests/test_api.py
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from uuid import uuid4

from app.main import app, get_db
from app.database import engine, Base
from app.models import Call
from app.schemas import CallCreate, CallUpdate

# Create an in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class TestCall(Base):
    __tablename__ = "calls"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500))
    sector = Column(String(200))
    description = Column(Text)
    url = Column(String(1000))
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(TIMESTAMP)
    processing_status = Column(String(50), default="pending")
    analysis_status = Column(String(50), default="pending")
    relevance_score = Column(Float, default=0.0)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def test_data():
    call_data = CallCreate(
        call_id="test_call_id",
        name="Test Call",
        sector="Test Sector",
        description="This is a test call.",
        url="http://example.com/test",
        total_funding=1000.0,
        funding_percentage=50.0,
        max_per_company=200.0,
        deadline="2023-12-31T23:59:59Z"
    )
    response = client.post("/calls/", json=call_data.dict())
    assert response.status_code == 200
    return response.json()

def test_read_call(test_data):
    call_id = test_data["id"]
    response = client.get(f"/calls/{call_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == call_id
    assert data["name"] == "Test Call"

def test_update_call(test_data):
    new_name = "Updated Test Call"
    updated_data = CallUpdate(name=new_name)
    response = client.put(f"/calls/{test_data['id']}", json=updated_data.dict())
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_name

def test_delete_call(test_data):
    call_id = test_data["id"]
    response = client.delete(f"/calls/{call_id}")
    assert response.status_code == 204
    with pytest.raises(Exception) as e:
        client.get(f"/calls/{call_id}")

def test_create_call_with_invalid_data():
    invalid_data = CallCreate(
        call_id="test_call_id",
        name=None,
        sector="Test Sector",
        description="This is a test call.",
        url="http://example.com/test",
        total_funding=1000.0,
        funding_percentage=50.0,
        max_per_company=200.0,
        deadline="2023-12-31T23:59:59Z"
    )
    response = client.post("/calls/", json=invalid_data.dict())
    assert response.status_code == 422

def test_read_nonexistent_call():
    response = client.get("/calls/nonexistent_id")
    assert response.status_code == 404

def test_update_nonexistent_call():
    updated_data = CallUpdate(name="Updated Test Call")
    response = client.put("/calls/nonexistent_id", json=updated_data.dict())
    assert response.status_code == 404

def test_delete_nonexistent_call():
    response = client.delete("/calls/nonexistent_id")
    assert response.status_code == 404
