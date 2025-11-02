from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP, UUID as sqla_UUID, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from uuid import UUID
import datetime

Base = declarative_base()

class Call(Base):
    __tablename__ = "calls"

    id = Column(sqla_UUID(as_uuid=True), primary_key=True, default=UUID)
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
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(sqla_UUID(as_uuid=True), primary_key=True, default=UUID)
    call_id = Column(sqla_UUID(as_uuid=True), ForeignKey("calls.id"), nullable=False)
    task_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.utcnow)

# Define relationships
Call.tasks = relationship("Task", back_populates="call")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(sqla_UUID(as_uuid=True), primary_key=True, default=UUID)
    call_id = Column(sqla_UUID(as_uuid=True), ForeignKey("calls.id"), nullable=False)
    notification_type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

# Define relationships
Call.notifications = relationship("Notification", back_populates="call")

class User(Base):
    __tablename__ = "users"

    id = Column(sqla_UUID(as_uuid=True), primary_key=True, default=UUID)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.utcnow)

# Define relationships
User.tasks = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(sqla_UUID(as_uuid=True), primary_key=True, default=UUID)
    user_id = Column(sqla_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    task_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.utcnow)

# Define relationships
Task.user = relationship("User", back_populates="tasks")
