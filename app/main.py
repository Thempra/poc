# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from app.routers.tasks import router as tasks_router

app = FastAPI(
    title="Call for Tenders API",
    description="FastAPI application for managing Call for Tenders data.",
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

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Database initialization (create tables)
Base.metadata.create_all(bind=engine)

# Router imports from app.routers.tasks
app.include_router(tasks_router)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def read_health():
    return {"status": "healthy"}

# Startup/shutdown events for database
@app.on_event("startup")
def startup_event():
    try:
        # Perform any startup logic here, such as connecting to databases or initializing external services
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown_event():
    try:
        # Perform any cleanup logic here, such as closing database connections or releasing resources
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
