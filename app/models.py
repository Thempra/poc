from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, UUID, ForeignKey, Boolean, Text as TEXT
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from uuid import uuid4

Base = declarative_base()

class Call(Base):
    __tablename__ = 'calls'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    call_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(500), nullable=False)
    sector = Column(String(200))
    description = Column(TEXT)
    url = Column(String(1000))
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(TIMESTAMP(timezone=True))
    processing_status = Column(String(50), nullable=False)
    analysis_status = Column(String(50), nullable=False)
    relevance_score = Column(Float)

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(255), nullable=False)
    description = Column(TEXT)
    status = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=text('now()'))

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)

class UserRole(Base):
    __tablename__ = 'user_roles'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True)

# Assuming a one-to-many relationship from User to Task
User.tasks = relationship("Task", back_populates="owner")

# Assuming a many-to-many relationship between User and Role
User.roles = relationship("Role", secondary="user_roles", back_populates="users")
