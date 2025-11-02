# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

app = FastAPI(
    title="Call for Tenders API",
    version="1.0.0",
    description="API for managing calls for tenders.",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "John Doe",
        "url": "https://john.doe.dev",
        "email": "johndoe@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.database import Base, engine
from app.routers import tasks

Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Call for Tenders API"}

app.include_router(tasks.router)
