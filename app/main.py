# app/__init__.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

app = FastAPI(
    title="Call for Tenders API",
    version="1.0.0",
    description="API for managing Call for Tenders data"
)

# CORS configuration (permissive for development)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.database import engine, Base
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)  # Create tables

@app.on_event("startup")
async def startup():
    db = SessionLocal()
    try:
        db.execute('SELECT 1')
    except SQLAlchemyError as e:
        print(f"Failed to connect to the database: {e}")
    finally:
        db.close()

@app.on_event("shutdown")
async def shutdown():
    db = SessionLocal()
    try:
        db.execute('SELECT 1')
    except SQLAlchemyError as e:
        print(f"Failed to connect to the database during shutdown: {e}")
    finally:
        db.close()

from app.routers import tasks

app.include_router(tasks.router)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
