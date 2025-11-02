# app/models.py

from sqlalchemy import Column, Integer, String, Text, Float, UUID, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from app.database import Base

class Call(Base):
    __tablename__ = "calls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500), index=True)
    sector = Column(String(200))
    description = Column(Text)
    url = Column(String(1000))
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(TIMESTAMP)
    processing_status = Column(String(50), default="Pending")
    analysis_status = Column(String(50), default="Not Started")
    relevance_score = Column(Float, default=0.0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

class CallBid(Base):
    __tablename__ = "call_bids"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), index=True)
    company_name = Column(String(255))
    bid_amount = Column(Float)
    submission_date = Column(TIMESTAMP)
    status = Column(String(50), default="Pending")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

    call = relationship("Call", back_populates="bids")

Call.bids = relationship("CallBid", order_by=CallBid.id, back_populates="call")
