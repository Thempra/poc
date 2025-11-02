from sqlalchemy.orm import Session
from app.models import Task
from uuid import UUID
from typing import List, Optional

def get_task(db: Session, task_id: UUID):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
    return db.query(Task).offset(skip).limit(limit).all()

def create_task(db: Session, task):
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def update_task(db: Session, task_id: UUID, task_data):
    task = get_task(db, task_id)
    if task:
        for key, value in task_data.items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")

def delete_task(db: Session, task_id: UUID):
    task = get_task(db, task_id)
    if task:
        db.delete(task)
        db.commit()
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")
