from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/therapists",
    tags=["therapists"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Therapist)
def create_therapist(therapist: schemas.TherapistCreate, db: Session = Depends(get_db)):
    return crud.create_therapist(db=db, therapist=therapist)

@router.get("/", response_model=List[schemas.Therapist])
def read_therapists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_therapists(db, skip=skip, limit=limit)
    return users

@router.get("/{therapist_id}", response_model=schemas.Therapist)
def read_therapist(therapist_id: int, db: Session = Depends(get_db)):
    db_therapist = crud.get_therapist(db, therapist_id=therapist_id)
    if db_therapist is None:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return db_therapist

@router.put("/{therapist_id}", response_model=schemas.Therapist)
def update_therapist(therapist_id: int, therapist: schemas.TherapistCreate, db: Session = Depends(get_db)):
    db_therapist = crud.update_therapist(db, therapist_id=therapist_id, therapist=therapist)
    if db_therapist is None:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return db_therapist

@router.delete("/{therapist_id}", response_model=schemas.Therapist)
def delete_therapist(therapist_id: int, db: Session = Depends(get_db)):
    db_therapist = crud.delete_therapist(db, therapist_id=therapist_id)
    if db_therapist is None:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return db_therapist
