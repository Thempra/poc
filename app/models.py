# app/models.py
from sqlalchemy import Column, Integer, String, Float, Text, UUID, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, declarative_base

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
    processing_status = Column(String(50), index=True)
    analysis_status = Column(String(50), index=True)
    relevance_score = Column(Float)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    # Relationships
    # Add any relationships here if needed

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(255), unique=True, index=True)
    description = Column(Text)
    status = Column(String(50), index=True)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    # Relationships
    # Add any relationships here if needed

# Add more models as per your requirements
