"""Pydantic Schemas"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None

class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
