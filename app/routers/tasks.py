from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CallCreate, CallUpdate
from app.crud import create_call, delete_call, get_call, get_calls, update_call

router = APIRouter()

@router.post("/calls/", response_model=CallCreate, status_code=status.HTTP_201_CREATED)
def create_new_call(call: CallCreate, db: Session = Depends(get_db)):
    return create_call(db=db, call=call)

@router.get("/calls/", response_model=list[Call], status_code=status.HTTP_200_OK)
def read_calls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_calls(db=db, skip=skip, limit=limit)

@router.get("/calls/{call_id}", response_model=Call, status_code=status.HTTP_200_OK)
def read_call(call_id: int, db: Session = Depends(get_db)):
    call = get_call(db, call_id=call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call

@router.put("/calls/{call_id}", response_model=CallUpdate, status_code=status.HTTP_200_OK)
def update_call_item(call_id: int, call_update: CallUpdate, db: Session = Depends(get_db)):
    updated_call = update_call(db=db, call_id=call_id, call_update=call_update)
    if not updated_call:
        raise HTTPException(status_code=404, detail="Call not found")
    return updated_call

@router.delete("/calls/{call_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_call_item(call_id: int, db: Session = Depends(get_db)):
    call_to_delete = get_call(db=db, call_id=call_id)
    if not call_to_delete:
        raise HTTPException(status_code=404, detail="Call not found")
    delete_call(db=db, call_id=call_id)
    return {"detail": "Call deleted"}
