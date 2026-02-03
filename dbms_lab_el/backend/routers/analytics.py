"""
Analytics router for data analysis endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import analysis

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/correlations")
def get_correlations(db: Session = Depends(get_db)):
    """Get correlation matrix between profile dimensions and report outcomes"""
    return analysis.get_correlation_matrix(db)

@router.get("/clusters")
def get_clusters(n_clusters: int = 3, db: Session = Depends(get_db)):
    """Get clustering results for psychological profiles"""
    return analysis.get_cluster_analysis(db, n_clusters=n_clusters)

@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    """Get summary statistics for assessment profiles"""
    return analysis.get_profile_summary(db)

@router.get("/person/{person_id}")
def get_person_analytics(person_id: int, db: Session = Depends(get_db)):
    """Get person-specific analytics from their assessments and simulations"""
    return analysis.get_person_analytics(db, person_id)
