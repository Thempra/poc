from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, UUID, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    description = Column(Text, index=True)
    status = Column(String(20), index=True)
    due_date = Column(DateTime, index=True)

class Call(Base):
    __tablename__ = "calls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500), index=True)
    sector = Column(String(200), index=True)
    description = Column(Text, index=True)
    url = Column(String(1000), index=True)
    total_funding = Column(Float, index=True)
    funding_percentage = Column(Float, index=True)
    max_per_company = Column(Float, index=True)
    deadline = Column(DateTime, index=True)
    processing_status = Column(String(50), index=True)
    analysis_status = Column(String(50), index=True)
    relevance_score = Column(Float, index=True)

# Define relationships
Task.call_id = relationship(Call, back_populates="tasks")
Call.tasks = relationship("Task", order_by=Task.id, back_populates="call")

# Database connection and session setup
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
