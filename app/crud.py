from sqlalchemy.orm import Session
from app.models import Call
from uuid import UUID
from typing import List, Optional

def get_call(db: Session, call_id: UUID):
    return db.query(Call).filter(Call.id == call_id).first()

def get_calls(db: Session, skip: int = 0, limit: int = 100) -> List[Call]:
    return db.query(Call).offset(skip).limit(limit).all()

def create_call(db: Session, call: Call):
    db.add(call)
    db.commit()
    db.refresh(call)
    return call

def update_call(db: Session, call_id: UUID, call_data):
    call = get_call(db, call_id)
    if call:
        for key, value in call_data.items():
            setattr(call, key, value)
        db.commit()
        db.refresh(call)
    return call

def delete_call(db: Session, call_id: UUID):
    call = get_call(db, call_id)
    if call:
        db.delete(call)
        db.commit()
    return call
