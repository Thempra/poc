# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from app.models import Base
from app.routers.tasks import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Call for Tenders API",
    description="API for managing Call for Tenders data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
origins = [
    "http://localhost",
    "http://localhost:3000",  # React app default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["health"])
async def health_check(db: Session = Depends(get_db)):
    try:
        # Perform a simple query to check database connection
        db.execute("SELECT 1")
        return {"status": "healthy"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Include routers
app.include_router(tasks_router, prefix="/tasks")

@app.on_event("startup")
def startup_event():
    # Perform any necessary startup tasks here
    pass

@app.on_event("shutdown")
def shutdown_event():
    # Perform any necessary cleanup tasks here
    pass
