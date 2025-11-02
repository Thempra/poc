# app/__init__.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

app = FastAPI(
    title="Call for Tenders API",
    version="1.0.0",
    description="API for managing tender calls from the European Union."
)

# CORS Configuration (permissive for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Initialization
from app.database import engine, SessionLocal, get_db
Base.metadata.create_all(bind=engine)

# Include router from tasks module
from app.routers.tasks import router as tasks_router
app.include_router(tasks_router, prefix="/tasks")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Call for Tenders API"}

@app.on_event("startup")
def startup():
    pass

@app.on_event("shutdown")
def shutdown():
    pass
