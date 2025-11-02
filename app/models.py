# app/models.py

from sqlalchemy import Column, String, Integer, Float, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Call(Base):
    __tablename__ = "calls"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500), nullable=False)
    sector = Column(String(200))
    description = Column(String(10000))  # Adjusted for larger text
    url = Column(String(1000), nullable=False)
    total_funding = Column(Float, default=0.0)
    funding_percentage = Column(Float, default=0.0)
    max_per_company = Column(Float, default=0.0)
    deadline = Column(TIMESTAMP(timezone=True))
    processing_status = Column(String(50), default="pending")
    analysis_status = Column(String(50), default="pending")
    relevance_score = Column(Float, default=0.0)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

# Assuming there is a related model named 'Analysis'
class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    call_id = Column(String(255), ForeignKey("calls.call_id"), nullable=False)
    call = relationship("Call", back_populates="analysis")
    # Add other fields related to the analysis here
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

# Ensure you have relationships set up correctly in your models if necessary
Call.analysis = relationship("Analysis", back_populates="call")
