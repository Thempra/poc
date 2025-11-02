# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routers import tasks

app = FastAPI(
    title="Call for Tenders",
    description="API para el monitoreo y análisis de convocatorias de la Unión Europea",
    version="1.0.0",
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

# Database initialization (create tables)
Base.metadata.create_all(bind=engine)

# Router imports from app.routers.tasks
app.include_router(tasks.router, prefix="/api")

@app.on_event("startup")
async def startup():
    try:
        db = next(get_db())
        # Perform any database initialization tasks here
    finally:
        db.close()

@app.on_event("shutdown")
async def shutdown():
    try:
        db = next(get_db())
        # Perform any cleanup tasks before shutting down the application
    finally:
        db.close()

# Health check endpoint
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy"}
