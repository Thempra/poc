from sqlalchemy.orm import Session
from app.models import Call, Task
from datetime import datetime
from typing import List, Optional

def get_call(db: Session, call_id: str):
    return db.query(Call).filter(Call.call_id == call_id).first()

def get_calls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Call).offset(skip).limit(limit).all()

def create_call(db: Session, call: Call):
    db.add(call)
    db.commit()
    db.refresh(call)
    return call

def update_call(db: Session, call_id: str, call_data: dict):
    call = get_call(db, call_id=call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    for key, value in call_data.items():
        setattr(call, key, value)
    db.commit()
    return call

def delete_call(db: Session, call_id: str):
    call = get_call(db, call_id=call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    db.delete(call)
    db.commit()

def create_task(db: Session, task: Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, task_data: dict):
    task = get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task_data.items():
        setattr(task, key, value)
    db.commit()
    return task

def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
