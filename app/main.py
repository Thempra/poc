# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response
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

# Include routers
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Call for Tenders API"}

@app.on_event("startup")
async def startup():
    # Perform any startup tasks here (e.g., database migrations)
    pass

@app.on_event("shutdown")
async def shutdown():
    # Perform any shutdown tasks here
    pass

# Health check endpoint
@app.get("/health", tags=["system"])
def health_check():
    return {"status": "healthy"}

