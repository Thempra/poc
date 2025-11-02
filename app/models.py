# app/models.py

from sqlalchemy import Column, Integer, String, Float, UUID, DateTime, ForeignKey, Text, Boolean, Numeric, PickleType, JSON, LargeBinary, SmallInteger, BigInteger, Binary, Date, Time, Interval, NullType
from sqlalchemy.dialects.postgresql import JSONB, BYTEA
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Call(Base):
    __tablename__ = 'calls'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500))
    sector = Column(String(200))
    description = Column(Text)
    url = Column(String(1000))
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(DateTime(timezone=True))
    processing_status = Column(String(50))
    analysis_status = Column(String(50))
    relevance_score = Column(Float)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_name = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class CallTask(Base):
    __tablename__ = 'call_tasks'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(UUID(as_uuid=True), ForeignKey('calls.id'), index=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'), index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    call = relationship("Call", backref=backref("call_tasks", lazy="dynamic"))
    task = relationship("Task", backref=backref("call_tasks", lazy="dynamic"))

