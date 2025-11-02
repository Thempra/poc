from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TaskCreate, TaskUpdate, Task as TaskSchema
from app.crud import create_task, update_task, get_task, get_tasks

router = APIRouter()

@router.post("/tasks/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)

@router.get("/tasks/{task_id}", response_model=TaskSchema, status_code=status.HTTP_200_OK)
def read_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/tasks/", response_model=list[TaskSchema], status_code=status.HTTP_200_OK)
def read_tasks_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = get_tasks(db=db, skip=skip, limit=limit)
    return tasks

@router.put("/tasks/{task_id}", response_model=TaskSchema, status_code=status.HTTP_200_OK)
def update_task_endpoint(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return update_task(db=db, task_id=task_id, task=task)

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return None
