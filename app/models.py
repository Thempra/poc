# app/models.py

from sqlalchemy import Column, Integer, String, Float, Text, UUID, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Call(Base):
    __tablename__ = "calls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    call_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(500), nullable=False)
    sector = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(1000), nullable=False)
    total_funding = Column(Float, nullable=False)
    funding_percentage = Column(Float, nullable=False)
    max_per_company = Column(Float, nullable=False)
    deadline = Column(TIMESTAMP(timezone=True), nullable=False)
    processing_status = Column(String(50), nullable=False)
    analysis_status = Column(String(50), nullable=False)
    relevance_score = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    task_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

# Define relationships if needed
