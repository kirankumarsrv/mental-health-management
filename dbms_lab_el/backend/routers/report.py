from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[schemas.Report])
def get_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reports = crud.get_reports(db, skip=skip, limit=limit)
    return reports

@router.get("/{report_id}", response_model=schemas.Report)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(crud.models.Report).filter(crud.models.Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.post("/", response_model=schemas.Report)
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    return crud.create_report(db, report)
