# app/models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(String, index=True)
    due_date = Column(DateTime, default=datetime.utcnow)

class Call(Base):
    __tablename__ = "calls"
    id = Column(Integer, primary_key=True, index=True)
