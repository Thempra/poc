# app/routers/tasks.py

from fastapi import APIRouter, Depends, HTTPException, status, Body, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import create_task, delete_task, get_task, get_tasks, update_task
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()

@router.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(task: TaskCreate = Body(...), db: Session = Depends(get_db)):
    task_instance = create_task(db=db, task=task)
    return task_instance

@router.get("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def read_task(task_id: str = Path(..., description="The ID of the task to get"), db: Session = Depends(get_db)):
    task = get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.get("/tasks/", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
def read_tasks(db: Session = Depends(get_db)):
    tasks = get_tasks(db=db)
    return tasks

@router.put("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task_item(task_id: str = Path(..., description="The ID of the task to update"), task_data: TaskUpdate = Body(...), db: Session = Depends(get_db)):
    updated_task = update_task(db=db, task_id=task_id, task_update=task_data)
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated_task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_item(task_id: str = Path(..., description="The ID of the task to delete"), db: Session = Depends(get_db)):
    deleted = delete_task(db=db, task_id=task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
