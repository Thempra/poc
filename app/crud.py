from sqlalchemy.orm import Session
from app.models import Call
from app.schemas import CallCreate, CallUpdate

def get_call(db: Session, call_id: int):
    return db.query(Call).filter(Call.id == call_id).first()

def get_calls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Call).offset(skip).limit(limit).all()

def create_call(db: Session, call: CallCreate):
    db_call = Call(**call.dict())
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call

def update_call(db: Session, call_id: int, call_update: CallUpdate):
    db_call = get_call(db, call_id)
    if not db_call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    for field, value in call_update.dict(exclude_unset=True).items():
        setattr(db_call, field, value)
    db.commit()
    db.refresh(db_call)
    return db_call

def delete_call(db: Session, call_id: int):
    db_call = get_call(db, call_id)
    if not db_call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    db.delete(db_call)
    db.commit()
