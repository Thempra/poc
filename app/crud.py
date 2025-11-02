# app/crud.py

from sqlalchemy.orm import Session
from app.models import Call
from datetime import datetime
from typing import List, Optional

def get_call(db: Session, call_id: str):
    return db.query(Call).filter(Call.call_id == call_id).first()

def get_calls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Call).offset(skip).limit(limit).all()

def create_call(db: Session, call: Call):
    db.add(call)
    db.commit()
    db.refresh(call)
    return call

def update_call(db: Session, call_id: str, call_data: dict):
    call = get_call(db, call_id=call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    for key, value in call_data.items():
        setattr(call, key, value)
    db.commit()
    return call

def delete_call(db: Session, call_id: str):
    call = get_call(db, call_id=call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    db.delete(call)
    db.commit()
    return {"message": "Call deleted"}
