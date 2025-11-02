import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate
from app.crud import create_task, read_task, update_task, delete_task

# Fixture to set up the database before each test
@pytest.fixture(scope="module")
def db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    
    # Drop all tables at the end of the tests
    yield
    
    Base.metadata.drop_all(bind=engine)

# Test for creating a new task
def test_create_task(db: Session):
    task_data = TaskCreate(call_id="example_rss", name="Example Call")
    created_task = create_task(db, task_data)
    
    assert created_task.id is not None
    assert created_task.call_id == "example_rss"
    assert created_task.name == "Example Call"

# Test for reading a single task
def test_read_task(db: Session):
    task_data = TaskCreate(call_id="example_rss", name="Example Call")
    created_task = create_task(db, task_data)
    
    read_task_ = read_task(db, created_task.id)
    
    assert read_task_.id == created_task.id
    assert read_task_.call_id == created_task.call_id
    assert read_task_.name == created_task.name

# Test for updating a task
def test_update_task(db: Session):
    task_data = TaskCreate(call_id="example_rss", name="Example Call")
    created_task = create_task(db, task_data)
    
    updated_task_data = TaskUpdate(name="Updated Call")
    updated_task = update_task(db, created_task.id, updated_task_data)
    
    assert updated_task.name == "Updated Call"

# Test for deleting a task
def test_delete_task(db: Session):
    task_data = TaskCreate(call_id="example_rss", name="Example Call")
    created_task = create_task(db, task_data)
    
    delete_task(db, created_task.id)
    
    # Check if the task is deleted by trying to read it again
    with pytest.raises(HTTPException) as exc_info:
        read_task(db, created_task.id)
        
    assert exc_info.value.status_code == 404

# Test for error handling when reading a non-existent task
def test_read_non_existent_task(db: Session):
    with pytest.raises(HTTPException) as exc_info:
        read_task(db, 99999)
    
    assert exc_info.value.status_code == 404

# Test for error handling when updating a non-existent task
def test_update_non_existent_task(db: Session):
    updated_task_data = TaskUpdate(name="Updated Call")
    
    with pytest.raises(HTTPException) as exc_info:
        update_task(db, 99999, updated_task_data)
    
    assert exc_info.value.status_code == 404

# Test for error handling when deleting a non-existent task
def test_delete_non_existent_task(db: Session):
    with pytest.raises(HTTPException) as exc_info:
        delete_task(db, 99999)
    
    assert exc_info.value.status_code == 404
