from sqlalchemy import Column, String, Integer, Float, TIMESTAMP, ForeignKey, UUID, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from datetime import datetime

Base = declarative_base()

def generate_uuid():
    return str(uuid4())

class Call(Base):
    __tablename__ = "calls"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    call_id = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(500), nullable=False)
    sector = Column(String(200))
    description = Column(TEXT)
    url = Column(String(1000), nullable=False)
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(TIMESTAMP(timezone=True))
    processing_status = Column(String(50), default='Pending')
    analysis_status = Column(String(50), default='Pending')
    relevance_score = Column(Float)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    call_id = Column(String(255), ForeignKey("calls.call_id"), nullable=False)
    task_type = Column(String(100), nullable=False)
    status = Column(String(50), default='Pending')
    data = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    call = relationship("Call", backref=backref("tasks", lazy="dynamic"))

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    call_id = Column(String(255), ForeignKey("calls.call_id"), nullable=False)
    analysis_type = Column(String(100), nullable=False)
    results = Column(JSONB)
    status = Column(String(50), default='Pending')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    call = relationship("Call", backref=backref("analyses", lazy="dynamic"))
