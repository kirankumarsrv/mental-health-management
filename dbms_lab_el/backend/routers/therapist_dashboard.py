"""
Therapist Dashboard API Routes
Features: Patient management, analysis, recommendations, filtering
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime
from .. import crud, models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(
    prefix="/therapist",
    tags=["therapist-dashboard"],
    responses={404: {"description": "Not found"}},
)

# ============================================
# THERAPIST AUTHENTICATION & CURRENT USER
# ============================================

@router.get("/me", response_model=schemas.Therapist)
def get_current_therapist(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current logged-in therapist"""
    if current_user.role.value != "therapist":
        raise HTTPException(status_code=403, detail="Access denied. Therapist role required.")
    
    therapist = db.query(models.Therapist).filter(models.Therapist.id == current_user.therapist_id).first()
    if not therapist:
        raise HTTPException(status_code=404, detail="Therapist profile not found")
    return therapist


# ============================================
# PATIENT LIST & FILTERING
# ============================================

@router.get("/patients", response_model=schemas.TherapistPatientList)
def get_therapist_patients(
    therapist_id: int,
    min_age: Optional[int] = Query(None),
    max_age: Optional[int] = Query(None),
    min_service_years: Optional[int] = Query(None),
    max_service_years: Optional[int] = Query(None),
    gender: Optional[str] = Query(None),
    rank: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get all patients assigned to a therapist with advanced filtering
    Filters: age range, service years range, gender, rank
    """
    query = db.query(models.Person).filter(models.Person.therapist_id == therapist_id)
    
    # Apply filters
    if min_age is not None:
        query = query.filter(models.Person.age >= min_age)
    if max_age is not None:
        query = query.filter(models.Person.age <= max_age)
    if min_service_years is not None:
        query = query.filter(models.Person.service_years >= min_service_years)
    if max_service_years is not None:
        query = query.filter(models.Person.service_years <= max_service_years)
    if gender:
        query = query.filter(models.Person.gender == gender)
    if rank:
        query = query.filter(models.Person.rank == rank)
    
    patients = query.all()
    
    patient_summaries = []
    for patient in patients:
        latest_assessment = db.query(models.Assessment).filter(
            models.Assessment.person_id == patient.id
        ).order_by(models.Assessment.assessment_date.desc()).first()
        
        assessment_count = db.query(models.Assessment).filter(
            models.Assessment.person_id == patient.id
        ).count()
        
        summary = schemas.PatientAssessmentSummary(
            id=patient.id,
            name=patient.name,
            rank=patient.rank,
            age=patient.age,
            gender=patient.gender,
            service_years=patient.service_years,
            latest_trauma_sensitivity=latest_assessment.trauma_sensitivity if latest_assessment else None,
            latest_emotional_regulation=latest_assessment.emotional_regulation if latest_assessment else None,
            latest_recovery_rate=latest_assessment.recovery_rate if latest_assessment else None,
            latest_impulsivity=latest_assessment.impulsivity if latest_assessment else None,
            latest_coping_mechanism=latest_assessment.coping_mechanism if latest_assessment else None,
            assessment_count=assessment_count,
            last_assessment_date=latest_assessment.assessment_date if latest_assessment else None
        )
        patient_summaries.append(summary)
    
    return schemas.TherapistPatientList(
        total_patients=len(patient_summaries),
        patients=patient_summaries
    )


@router.get("/patients/{patient_id}", response_model=schemas.PatientDetailedView)
def get_patient_details(patient_id: int, therapist_id: int, db: Session = Depends(get_db)):
    """
    Get detailed view of a specific patient including:
    - Demographics
    - All assessments history
    - Reports
    - Therapist recommendations
    - Scenario participation
    """
    patient = db.query(models.Person).filter(
        and_(models.Person.id == patient_id, models.Person.therapist_id == therapist_id)
    ).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found or not assigned to this therapist")
    
    # Get latest assessment for summary
    latest_assessment = db.query(models.Assessment).filter(
        models.Assessment.person_id == patient_id
    ).order_by(models.Assessment.assessment_date.desc()).first()
    
    # Get all assessments
    assessments = db.query(models.Assessment).filter(
        models.Assessment.person_id == patient_id
    ).order_by(models.Assessment.assessment_date.desc()).all()
    
    # Get reports
    reports = db.query(models.Report).filter(
        models.Report.person_id == patient_id
    ).all()
    
    # Get recommendations
    recommendations = db.query(models.TherapistRecommendation).filter(
        models.TherapistRecommendation.person_id == patient_id
    ).order_by(models.TherapistRecommendation.created_date.desc()).all()
    
    # Count scenario participation
    scenario_count = db.query(models.Participates).filter(
        models.Participates.person_id == patient_id
    ).count()
    
    assessment_count = len(assessments)
    
    return schemas.PatientDetailedView(
        id=patient.id,
        name=patient.name,
        rank=patient.rank,
        age=patient.age,
        gender=patient.gender,
        service_years=patient.service_years,
        latest_trauma_sensitivity=latest_assessment.trauma_sensitivity if latest_assessment else None,
        latest_emotional_regulation=latest_assessment.emotional_regulation if latest_assessment else None,
        latest_recovery_rate=latest_assessment.recovery_rate if latest_assessment else None,
        latest_impulsivity=latest_assessment.impulsivity if latest_assessment else None,
        latest_coping_mechanism=latest_assessment.coping_mechanism if latest_assessment else None,
        assessment_count=assessment_count,
        last_assessment_date=latest_assessment.assessment_date if latest_assessment else None,
        assessments=[schemas.Assessment.from_orm(a) for a in assessments],
        reports=[{
            "id": r.id,
            "avoidance": r.avoidance,
            "re_experiencing": r.re_experiencing,
            "negative_alterations": r.negative_alterations,
            "hyperarousal": r.hyperarousal,
            "created_date": r.assessment_id
        } for r in reports],
        recommendations=[schemas.TherapistRecommendation.from_orm(r) for r in recommendations],
        scenario_participation_count=scenario_count
    )


# ============================================
# THERAPIST RECOMMENDATIONS
# ============================================

@router.post("/recommend/{patient_id}", response_model=schemas.TherapistRecommendation)
def create_recommendation(
    patient_id: int,
    therapist_id: int,
    recommendation: schemas.TherapistRecommendationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new recommendation for a patient
    Therapist suggests a scenario and coping mechanism
    """
    # Verify patient belongs to therapist
    patient = db.query(models.Person).filter(
        and_(models.Person.id == patient_id, models.Person.therapist_id == therapist_id)
    ).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found or not assigned to this therapist")
    
    # Verify scenario exists
    scenario = db.query(models.Scenario).filter(models.Scenario.id == recommendation.scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    db_recommendation = models.TherapistRecommendation(
        therapist_id=therapist_id,
        person_id=patient_id,
        scenario_id=recommendation.scenario_id,
        suggested_coping_mechanism=recommendation.suggested_coping_mechanism,
        recommendation_text=recommendation.recommendation_text,
        status="pending"
    )
    
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    
    return db_recommendation


@router.get("/recommendations/{patient_id}", response_model=List[schemas.TherapistRecommendation])
def get_patient_recommendations(
    patient_id: int,
    therapist_id: int,
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get all recommendations for a patient
    Optional filter by status: pending, accepted, rejected, completed
    """
    query = db.query(models.TherapistRecommendation).filter(
        and_(
            models.TherapistRecommendation.person_id == patient_id,
            models.TherapistRecommendation.therapist_id == therapist_id
        )
    )
    
    if status:
        query = query.filter(models.TherapistRecommendation.status == status)
    
    recommendations = query.order_by(models.TherapistRecommendation.created_date.desc()).all()
    return recommendations


@router.put("/recommendations/{recommendation_id}/status", response_model=schemas.TherapistRecommendation)
def update_recommendation_status(
    recommendation_id: int,
    new_status: str,
    soldier_response: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Update recommendation status when soldier accepts/rejects/completes it
    Status values: pending, accepted, rejected, completed
    """
    recommendation = db.query(models.TherapistRecommendation).filter(
        models.TherapistRecommendation.id == recommendation_id
    ).first()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    recommendation.status = new_status
    if soldier_response:
        recommendation.soldier_response = soldier_response
    
    db.commit()
    db.refresh(recommendation)
    
    return recommendation


# ============================================
# PATIENT ANALYTICS & STATISTICS
# ============================================

@router.get("/dashboard/stats/{therapist_id}", response_model=schemas.TherapistDashboardStats)
def get_therapist_dashboard_stats(therapist_id: int, db: Session = Depends(get_db)):
    """
    Get overall statistics for therapist dashboard
    - Total patients
    - Total recommendations & statuses
    - Completed simulations
    - Average assessment scores
    """
    # Total patients
    total_patients = db.query(func.count(models.Person.id)).filter(
        models.Person.therapist_id == therapist_id
    ).scalar()
    
    # Total recommendations
    total_recommendations = db.query(func.count(models.TherapistRecommendation.id)).filter(
        models.TherapistRecommendation.therapist_id == therapist_id
    ).scalar()
    
    # Accepted recommendations
    accepted_recommendations = db.query(func.count(models.TherapistRecommendation.id)).filter(
        and_(
            models.TherapistRecommendation.therapist_id == therapist_id,
            models.TherapistRecommendation.status == "accepted"
        )
    ).scalar()
    
    # Completed simulations (recommendations with status = completed)
    completed_simulations = db.query(func.count(models.TherapistRecommendation.id)).filter(
        and_(
            models.TherapistRecommendation.therapist_id == therapist_id,
            models.TherapistRecommendation.status == "completed"
        )
    ).scalar()
    
    # Average assessment scores for all patients
    avg_trauma = db.query(func.avg(models.Assessment.trauma_sensitivity)).filter(
        models.Assessment.therapist_id == therapist_id
    ).scalar() or 0.0
    
    avg_emotional = db.query(func.avg(models.Assessment.emotional_regulation)).filter(
        models.Assessment.therapist_id == therapist_id
    ).scalar() or 0.0
    
    avg_recovery = db.query(func.avg(models.Assessment.recovery_rate)).filter(
        models.Assessment.therapist_id == therapist_id
    ).scalar() or 0.0
    
    avg_impulsivity = db.query(func.avg(models.Assessment.impulsivity)).filter(
        models.Assessment.therapist_id == therapist_id
    ).scalar() or 0.0
    
    return schemas.TherapistDashboardStats(
        total_patients=total_patients,
        total_recommendations=total_recommendations,
        accepted_recommendations=accepted_recommendations,
        completed_simulations=completed_simulations,
        average_trauma_sensitivity=round(float(avg_trauma), 3),
        average_emotional_regulation=round(float(avg_emotional), 3),
        average_recovery_rate=round(float(avg_recovery), 3),
        average_impulsivity=round(float(avg_impulsivity), 3)
    )


@router.get("/analytics/patient-progress/{patient_id}")
def get_patient_progress(patient_id: int, therapist_id: int, db: Session = Depends(get_db)):
    """
    Get patient assessment progress over time
    Returns chronological assessment data for trend analysis
    """
    # Verify patient belongs to therapist
    patient = db.query(models.Person).filter(
        and_(models.Person.id == patient_id, models.Person.therapist_id == therapist_id)
    ).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    assessments = db.query(models.Assessment).filter(
        models.Assessment.person_id == patient_id
    ).order_by(models.Assessment.assessment_date).all()
    
    progress_data = []
    for assessment in assessments:
        progress_data.append({
            "id": assessment.id,
            "assessment_date": assessment.assessment_date,
            "trauma_sensitivity": assessment.trauma_sensitivity,
            "emotional_regulation": assessment.emotional_regulation,
            "recovery_rate": assessment.recovery_rate,
            "impulsivity": assessment.impulsivity,
            "coping_mechanism": assessment.coping_mechanism
        })
    
    return {
        "patient_id": patient_id,
        "patient_name": patient.name,
        "total_assessments": len(assessments),
        "progress_data": progress_data
    }


@router.get("/analytics/comparison")
def compare_patients(
    therapist_id: int,
    metric: str = Query("trauma_sensitivity", description="Metric to compare: trauma_sensitivity, emotional_regulation, recovery_rate, impulsivity"),
    db: Session = Depends(get_db)
):
    """
    Compare all patients on a specific metric for the therapist
    Shows relative performance and identifies outliers
    """
    patients = db.query(models.Person).filter(
        models.Person.therapist_id == therapist_id
    ).all()
    
    comparison_data = []
    
    for patient in patients:
        latest_assessment = db.query(models.Assessment).filter(
            models.Assessment.person_id == patient.id
        ).order_by(models.Assessment.assessment_date.desc()).first()
        
        if latest_assessment:
            metric_value = getattr(latest_assessment, metric, None)
            comparison_data.append({
                "patient_id": patient.id,
                "name": patient.name,
                "rank": patient.rank,
                "age": patient.age,
                "service_years": patient.service_years,
                metric: metric_value,
                "assessment_date": latest_assessment.assessment_date
            })
    
    # Sort by metric value
    comparison_data.sort(key=lambda x: x[metric] if x[metric] is not None else 0, reverse=True)
    
    return {
        "therapist_id": therapist_id,
        "metric": metric,
        "total_patients": len(comparison_data),
        "comparison": comparison_data
    }


@router.get("/analytics/scenario-recommendations/{patient_id}")
def get_recommended_scenarios(patient_id: int, therapist_id: int, db: Session = Depends(get_db)):
    """
    Get scenarios recommended to a patient and their status
    Shows which scenarios therapist suggested and if patient completed them
    """
    recommendations = db.query(models.TherapistRecommendation).filter(
        and_(
            models.TherapistRecommendation.person_id == patient_id,
            models.TherapistRecommendation.therapist_id == therapist_id
        )
    ).all()
    
    scenario_data = []
    for rec in recommendations:
        scenario = db.query(models.Scenario).filter(
            models.Scenario.id == rec.scenario_id
        ).first()
        
        # Check if patient participated in this scenario
        participated = db.query(models.Participates).filter(
            and_(
                models.Participates.person_id == patient_id,
                models.Participates.scenario_id == rec.scenario_id
            )
        ).first()
        
        scenario_data.append({
            "recommendation_id": rec.id,
            "scenario_id": scenario.id,
            "scenario_type": scenario.scenario_type,
            "environment": scenario.environment,
            "suggested_coping_mechanism": rec.suggested_coping_mechanism,
            "recommendation_text": rec.recommendation_text,
            "recommended_date": rec.created_date,
            "status": rec.status,
            "completed": participated is not None,
            "soldier_response": rec.soldier_response
        })
    
    return {
        "patient_id": patient_id,
        "total_recommendations": len(scenario_data),
        "scenario_recommendations": scenario_data
    }
