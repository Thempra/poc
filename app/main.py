# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from app.routers.tasks import router as tasks_router
from app.models import Call
from datetime import datetime
import time

app = FastAPI(
    title="Call for Tenders API",
    description="A web service to monitor and analyze calls for tenders from the EU.",
    version="1.0.0",
    openapi_url="/openapi.json"
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown():
    pass

app.include_router(tasks_router, prefix="/tasks")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Call for Tenders API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# app/database.py
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://callfortenders_user:callfortenders_password@postgres/callfortenders"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# app/models.py
from sqlalchemy import Column, Integer, String, Float, Text, UUID, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    processing_status = Column(String(50))
    analysis_status = Column(String(50))
    relevance_score = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    status = Column(String(50))

# app/crud.py
from sqlalchemy.orm import Session
from app.models import Call

def get_calls(db: Session):
    return db.query(Call).all()

def create_call(db: Session, call_data: dict):
    db_call = Call(**call_data)
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call

# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Task
from app.crud import create_task

router = APIRouter()

@router.post("/tasks/", response_model=Task)
async def create_new_task(task: Task, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)

# app/tasks.py
import time
from fastapi import BackgroundTasks
from app.database import SessionLocal
from app.models import Call, Task
from app.crud import get_calls

def perform_tasks():
    while True:
        db = SessionLocal()
        calls = get_calls(db)
        for call in calls:
            # Perform task logic here
            time.sleep(1)  # Simulate work
        db.close()

@app.on_event("startup")
async def startup_task():
    background_tasks = BackgroundTasks(add_task=perform_tasks)

# app/scrapers/main.py
import asyncio
from fastapi import FastAPI, BackgroundTasks
from app.database import SessionLocal
from app.models import Call

app = FastAPI()

def perform_scrape(background_tasks: BackgroundTasks):
    # Scrape logic here
    pass

@app.on_event("startup")
async def startup_scraper():
    background_tasks = BackgroundTasks(add_task=perform_scrape)

# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from app.routers.tasks import router as tasks_router
from app.models import Call
from datetime import datetime
import time

app = FastAPI(
    title="Call for Tenders API",
    description="A web service to monitor and analyze calls for tenders from the EU.",
    version="1.0.0",
    openapi_url="/openapi.json"
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    perform_scrape(background_tasks=BackgroundTasks(add_task=perform_scrape))
    perform_tasks(background_tasks=BackgroundTasks(add_task=perform_tasks))

@app.on_event("shutdown")
async def shutdown():
    pass

app.include_router(tasks_router, prefix="/tasks")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Call for Tenders API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# app/database.py
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://callfortenders_user:callfortenders_password@postgres/callfortenders"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# app/models.py
from sqlalchemy import Column, Integer, String, Float, Text, UUID, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    processing_status = Column(String(50))
    analysis_status = Column(String(50))
    relevance_score = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    status = Column(String(50))

# app/crud.py
from sqlalchemy.orm import Session
from app.models import Call

def get_calls(db: Session):
    return db.query(Call).all()

def create_call(db: Session, call_data: dict):
    db_call = Call(**call_data)
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call

# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Task
from app.crud import create_task

router = APIRouter()

@router.post("/tasks/", response_model=Task)
async def create_new_task(task: Task, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)

# app/tasks.py
import time
from fastapi import BackgroundTasks
from app.database import SessionLocal
from app.models import Call, Task
from app.crud import get_calls

def perform_tasks():
    while True:
        db = SessionLocal()
        calls = get_calls(db)
        for call in calls:
            # Perform task logic here
            time.sleep(1)  # Simulate work
        db.close()

@app.on_event("startup")
async def startup_task():
    background_tasks = BackgroundTasks(add_task=perform_tasks)

# app/scrapers