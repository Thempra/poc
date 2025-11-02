# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import TaskCreate, TaskUpdate, Task as TaskSchema
from app.crud import create_task, get_task, get_tasks, update_task

router = APIRouter()

@router.post("/tasks/", response_model=TaskSchema)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)

@router.get("/tasks/", response_model=List[TaskSchema])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = get_tasks(db=db, skip=skip, limit=limit)
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskSchema)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task_item(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    updated_task = update_task(db=db, task_id=task_id, task=task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
