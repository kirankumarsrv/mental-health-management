"""
Questionnaire and Assessment router
Handles questionnaire retrieval and assessment submission
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, crud, auth
from ..database import get_db

router = APIRouter(prefix="/questionnaires", tags=["Questionnaires"])

@router.get("/", response_model=List[schemas.Questionnaire])
def get_questionnaires(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Get all active questionnaires for assessment
    Returns questions ordered by ID
    """
    questionnaires = crud.get_questionnaires(db, active_only=active_only)
    return questionnaires

@router.get("/{questionnaire_id}", response_model=schemas.Questionnaire)
def get_questionnaire(
    questionnaire_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific questionnaire by ID"""
    questionnaire = crud.get_questionnaire(db, questionnaire_id)
    if not questionnaire:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    return questionnaire

@router.post("/", response_model=schemas.Questionnaire)
def create_questionnaire(
    questionnaire: schemas.QuestionnaireCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role(["admin", "therapist"]))
):
    """
    Create a new questionnaire (admin/therapist only)
    """
    return crud.create_questionnaire(db, questionnaire)

# Assessment endpoints
assessment_router = APIRouter(prefix="/assessments", tags=["Assessments"])

@assessment_router.post("/", response_model=schemas.Assessment)
def create_assessment(
    assessment: schemas.AssessmentCreate,
    db: Session = Depends(get_db)
):
    """
    Submit a completed assessment
    Automatically calculates psychological profile from responses
    """
    # Verify person exists
    person = crud.get_person(db, assessment.person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    # Verify therapist if provided
    if assessment.therapist_id:
        therapist = crud.get_therapist(db, assessment.therapist_id)
        if not therapist:
            raise HTTPException(status_code=404, detail="Therapist not found")
    
    # Create assessment with automatic scoring
    db_assessment = crud.create_assessment(db, assessment)
    return db_assessment

@assessment_router.get("/{assessment_id}", response_model=schemas.AssessmentWithResponses)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific assessment with all responses"""
    assessment = crud.get_assessment(db, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment

@assessment_router.get("/person/{person_id}", response_model=List[schemas.Assessment])
def get_person_assessments(
    person_id: int,
    db: Session = Depends(get_db)
):
    """Get all assessments for a specific person"""
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    assessments = crud.get_assessments_by_person(db, person_id)
    return assessments

@assessment_router.get("/person/{person_id}/latest", response_model=schemas.Assessment)
def get_latest_assessment(
    person_id: int,
    db: Session = Depends(get_db)
):
    """Get the most recent assessment for a person"""
    person = crud.get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    assessment = crud.get_latest_assessment(db, person_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="No assessments found for this person")
    
    return assessment

@assessment_router.get("/", response_model=List[schemas.Assessment])
def get_all_assessments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all assessments with pagination"""
    assessments = crud.get_all_assessments(db, skip=skip, limit=limit)
    return assessments
