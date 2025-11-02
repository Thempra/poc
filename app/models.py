from sqlalchemy import Column, Integer, String, Text, Float, UUID, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from datetime import datetime

UUID_VERSION = "4"

class Call(Base):
    __tablename__ = "calls"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    call_id = Column(String(255), unique=True)
    name = Column(String(500))
    sector = Column(String(200))
    description = Column(Text)
    url = Column(String(1000))
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(TIMESTAMP(timezone=True))
    processing_status = Column(String(50))
    analysis_status = Column(String(50))
    relevance_score = Column(Float)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String(255), index=True)
    description = Column(Text)
    status = Column(String(50))
    due_date = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

class CallTasks(Base):
    __tablename__ = "call_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), index=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), index=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String(255), unique=True)
    description = Column(Text)

class UserRole(Base):
    __tablename__ = "user_roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), index=True)
