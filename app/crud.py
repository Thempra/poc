from sqlalchemy.orm import Session
from typing import Optional

# Assuming the Task model is defined in models.py
from app.models import Task, Call  # Import other relevant models as needed
from fastapi import HTTPException, status

def get_task(db: Session, task_id: str):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, task_id: str, task: Task):
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    for attr, value in task.dict().items():
        setattr(db_task, attr, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: str):
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}
