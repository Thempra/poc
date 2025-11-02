# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from app.routers.tasks import router as tasks_router
from app.models import Call
from app.schemas import TaskCreate, TaskUpdate

app = FastAPI(
    title="Call for Tenders API",
    version="1.0.0",
    description="Documentation of the Call for Tenders API.",
    terms_of_service="https://example.com/terms",
    contact={
        "name": "John Doe",
        "url": "https://example.com/contact",
        "email": "johndoe@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    }
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

@app.on_event("shutdown")
async def shutdown():
    # Perform any necessary cleanup here
    pass

app.include_router(tasks_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Call for Tenders API"}

# Dependency injection for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Additional routes or endpoints can be added here as needed

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
