from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/reactions",
    tags=["reactions"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[schemas.Reaction])
def get_reactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reactions = crud.get_reactions(db, skip=skip, limit=limit)
    return reactions

@router.get("/{reaction_id}", response_model=schemas.Reaction)
def get_reaction(reaction_id: int, db: Session = Depends(get_db)):
    reaction = db.query(crud.models.Reaction).filter(crud.models.Reaction.id == reaction_id).first()
    if not reaction:
        raise HTTPException(status_code=404, detail="Reaction not found")
    return reaction

@router.post("/", response_model=schemas.Reaction)
def create_reaction(reaction: schemas.ReactionCreate, db: Session = Depends(get_db)):
    return crud.create_reaction(db, reaction)
