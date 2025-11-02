# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routers import tasks
from app.schemas import CallCre  # Import the schema here

# Initialize FastAPI application with metadata from docs
app = FastAPI(
    title="Call for Tenders API",
    description="API for managing and analyzing EU tenders",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS configuration (permissive for development)
origins = ["http://localhost", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization (create tables)
Base.metadata.create_all(bind=engine)

# Import router from app.routers.tasks
router = tasks.router

# Include the router in the FastAPI application
app.include_router(router, prefix="/api")

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

# Startup/shutdown events for database
@app.on_event("startup")
def startup_db():
    # Perform any database initialization tasks here
    pass

@app.on_event("shutdown")
def shutdown_db():
    # Perform any cleanup tasks here
    pass
