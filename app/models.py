# app/models.py
from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, UUID, TIMESTAMP, Boolean, Enum, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List

Base = declarative_base()

class Call(Base):
    __tablename__ = "calls"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500))
    sector = Column(String(200))
    description = Column(Text)
    url = Column(String(1000))
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(TIMESTAMP)
    processing_status = Column(String(50))
    analysis_status = Column(String(50))
    relevance_score = Column(Float)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(Text)
    status = Column(Enum("pending", "in_progress", "completed"), default="pending")
    due_date = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

class CallTask(Base):
    __tablename__ = "call_task"

    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

    call = relationship("Call", back_populates="task")
    task = relationship("Task", back_populates="call")

Call.task = relationship("Task", secondary=CallTask.__table__, back_populates="call")
Task.call = relationship("Call", secondary=CallTask.__table__, back_populates="task")
