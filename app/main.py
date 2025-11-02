# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from app.routers.tasks import router as tasks_router
from app.models import Call

app = FastAPI(
    title="Call for Tenders API",
    description="FastAPI application for managing Call for Tenders data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
origins = ["*"]  # Permissive for development, use specific origins in production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(tasks_router)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Startup/shutdown events for database
@app.on_event("startup")
async def startup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown_db():
    async with engine.begin() as conn:
        await conn.close()
