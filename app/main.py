# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from app.routers.tasks import router as tasks_router
from app.models import Call
from app.schemas import CallCreate, CallUpdate

app = FastAPI(
    title="Call for Tenders API",
    description="An API to manage and analyze EU tender calls.",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    pass

app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])

# Health check endpoint
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"message": "I'm healthy!"}
