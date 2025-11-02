# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from app.routers.tasks import router as tasks_router

app = FastAPI(
    title="Call for Tenders API",
    description="FastAPI application for managing Call for Tenders data",
    version="1.0.0"
)

# CORS Configuration
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Initialization
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(tasks_router)

# Health Check Endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Startup/Shutdown Events for Database
@app.on_event("startup")
def startup_db():
    engine.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

@app.on_event("shutdown")
def shutdown_db():
    pass

# Dependency Injection for Database Sessions
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
