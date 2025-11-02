# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.crud import create_task, read_task, update_task, delete_task

router = APIRouter()

@router.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_new_task(task: Task, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)

@router.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def read_task_by_id(task_id: str, db: Session = Depends(get_db)):
    db_task = read_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task

@router.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_existing_task(task_id: str, task: Task, db: Session = Depends(get_db)):
    return update_task(db=db, task_id=task_id, task=task)

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(task_id: str, db: Session = Depends(get_db)):
    delete_task(db=db, task_id=task_id)
    return {"detail": "Task deleted"}
