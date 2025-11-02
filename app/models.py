# app/models.py

from sqlalchemy import Column, Integer, String, Text, Float, UUID, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Call(Base):
    __tablename__ = "calls"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500))
    sector = Column(String(200))
    description = Column(Text)
    url = Column(String(1000))
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(TIMESTAMP)
    processing_status = Column(String(50), index=True)
    analysis_status = Column(String(50), index=True)
    relevance_score = Column(Float)
    created_at = Column(TIMESTAMP, server_default=datetime.utcnow())
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow())

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String(255), index=True)
    description = Column(Text)
    status = Column(String(50), index=True)
    created_at = Column(TIMESTAMP, server_default=datetime.utcnow())
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow())

class CallDetail(Base):
    __tablename__ = "call_details"
    
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), index=True)
    detail_data = Column(JSONB)
    created_at = Column(TIMESTAMP, server_default=datetime.utcnow())
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow())

    call = relationship("Call", back_populates="details")
