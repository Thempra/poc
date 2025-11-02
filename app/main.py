# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routers import tasks

app = FastAPI(
    title="Call for Tenders",
    version="1.0.0",
    description="API for monitoring and analyzing Call for Tenders from the European Union."
)

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    pass  # Placeholder for database startup logic

@app.on_event("shutdown")
async def shutdown():
    pass  # Placeholder for database shutdown logic

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Call for Tenders API"}

# Include routers
app.include_router(tasks.router)
