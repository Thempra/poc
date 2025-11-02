from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/tasks", status_code=status.HTTP_200_OK)
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return {"tasks": tasks}

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_data, db: Session = Depends(get_db)):
    new_task = Task(**task_data.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"task": new_task}

@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"task": task}

@router.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: int, task_data, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    for key, value in task_data.dict().items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return {"task": task}

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    db.delete(task)
    db.commit()
