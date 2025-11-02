# app/models.py
from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Call(Base):
    __tablename__ = 'calls'
    id = Column(pgUUID(as_uuid=True), primary_key=True, default=pgUUID(uuid.uuid4))
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500), nullable=False)
    sector = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    url = Column(String(1000), nullable=False)
    total_funding = Column(Float, nullable=False)
    funding_percentage = Column(Float, nullable=False)
    max_per_company = Column(Float, nullable=False)
    deadline = Column(TIMESTAMP, nullable=False)
    processing_status = Column(String(50), nullable=False)
    analysis_status = Column(String(50), nullable=False)
    relevance_score = Column(Float, nullable=False)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(pgUUID(as_uuid=True), unique=True, index=True)
    call_id = Column(pgUUID(as_uuid=True), ForeignKey('calls.id'), index=True)
    name = Column(String(250), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, onupdate=func.current_timestamp())

class CallTask(Base):
    __tablename__ = 'call_tasks'
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(pgUUID(as_uuid=True), ForeignKey('calls.id'), index=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), index=True)
