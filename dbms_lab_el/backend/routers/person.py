from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/persons",
    tags=["persons"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.create_person(db=db, person=person)

@router.get("/", response_model=List[schemas.Person])
def read_persons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = crud.get_persons(db, skip=skip, limit=limit)
    return persons

@router.get("/{person_id}", response_model=schemas.Person)
def read_person(person_id: int, db: Session = Depends(get_db)):
    db_person = crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@router.put("/{person_id}", response_model=schemas.Person)
def update_person(person_id: int, person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = crud.update_person(db, person_id=person_id, person=person)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@router.delete("/{person_id}", response_model=schemas.Person)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    db_person = crud.delete_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person
