# app/models.py
from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    due_date = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

class Call(Base):
    __tablename__ = "calls"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    call_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(500), nullable=False)
    sector = Column(String(200))
    description = Column(Text)
    url = Column(String(1000), unique=True, nullable=False)
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(TIMESTAMP)
    processing_status = Column(String(50))
    analysis_status = Column(String(50))
    relevance_score = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    
    tasks = relationship("Task", back_populates="call")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    due_date = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), index=True)
    call = relationship("Call", back_populates="tasks")
