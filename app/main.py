# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from app.routers.tasks import router as tasks_router
from app.models import Call

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Call for Tenders API",
    description="A RESTful API for managing tenders from the EU",
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Router imports from app.routers.tasks
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])

@app.on_event("startup")
async def startup_db_client():
    # Initialize database here if needed

@app.on_event("shutdown")
async def shutdown_db_client():
    # Close database connection here if needed

