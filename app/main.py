# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from app.routers.tasks import router as tasks_router

app = FastAPI(
    title="Call for Tenders API",
    description="FastAPI application to manage call for tenders data.",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Initialization
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    # Perform any necessary database setup or migrations here

@app.on_event("shutdown")
async def shutdown():
    # Clean up resources if needed

# Include router for tasks
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])

# Health Check Endpoint
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}
