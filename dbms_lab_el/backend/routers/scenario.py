from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/scenarios",
    tags=["scenarios"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Scenario)
def create_scenario(scenario: schemas.ScenarioCreate, db: Session = Depends(get_db)):
    return crud.create_scenario(db=db, scenario=scenario)

@router.get("/", response_model=List[schemas.Scenario])
def read_scenarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    scenarios = crud.get_scenarios(db, skip=skip, limit=limit)
    return scenarios

@router.get("/{scenario_id}", response_model=schemas.Scenario)
def read_scenario(scenario_id: int, db: Session = Depends(get_db)):
    db_scenario = crud.get_scenario(db, scenario_id=scenario_id)
    if db_scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return db_scenario

@router.put("/{scenario_id}", response_model=schemas.Scenario)
def update_scenario(scenario_id: int, scenario: schemas.ScenarioCreate, db: Session = Depends(get_db)):
    db_scenario = crud.update_scenario(db, scenario_id=scenario_id, scenario=scenario)
    if db_scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return db_scenario

@router.delete("/{scenario_id}", response_model=schemas.Scenario)
def delete_scenario(scenario_id: int, db: Session = Depends(get_db)):
    db_scenario = crud.delete_scenario(db, scenario_id=scenario_id)
    if db_scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return db_scenario
