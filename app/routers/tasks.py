from sqlalchemy.orm import Session
from app.models import Task

def create_task(db: Session, task_id: str, name: str, description: str = None, status: str = "pending"):
    db_task = Task(task_id=task_id, name=name, description=description, status=status)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def read_task(db: Session, task_id: str):
    return db.query(Task).filter(Task.task_id == task_id).first()

def update_task(db: Session, task_id: str, name: str = None, description: str = None, status: str = None):
    db_task = db.query(Task).filter(Task.task_id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    update_data = {key: value for key, value in locals().items() if key != "db" and value is not None}
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: str):
    db_task = db.query(Task).filter(Task.task_id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return db_task
