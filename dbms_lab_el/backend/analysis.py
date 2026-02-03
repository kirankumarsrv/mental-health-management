"""
Analytics module for PTSD assessment data
"""
from typing import Dict
from sqlalchemy.orm import Session
import pandas as pd
from sklearn.cluster import KMeans

from . import models


def _map_report_scores(report: models.Report) -> Dict[str, float]:
    """Map report categorical values to numeric scores for analysis."""
    avoidance_score = 1.0 if report.avoidance == "High" else 0.0
    re_experiencing_score = 1.0 if report.re_experiencing == "Yes" else 0.0
    negative_map = {"None": 0.0, "Mild": 0.25, "Moderate": 0.6, "Severe": 1.0}
    hyper_map = {"Mild": 0.25, "Moderate": 0.6, "Severe": 1.0}

    negative_score = negative_map.get(report.negative_alterations, 0.0)
    hyper_score = hyper_map.get(report.hyperarousal, 0.0)

    return {
        "avoidance_score": avoidance_score,
        "re_experiencing_score": re_experiencing_score,
        "negative_alterations_score": negative_score,
        "hyperarousal_score": hyper_score,
    }


def get_correlation_matrix(db: Session) -> Dict:
    """Compute correlation matrix between profile dimensions and report outcomes."""
    # Join assessments with reports using assessment_id
    rows = (
        db.query(models.Assessment, models.Report)
        .join(models.Report, models.Report.assessment_id == models.Assessment.id)
        .all()
    )

    if not rows:
        return {"message": "No assessment-report data available for correlation."}

    data = []
    for assessment, report in rows:
        report_scores = _map_report_scores(report)
        data.append({
            "trauma_sensitivity": assessment.trauma_sensitivity,
            "emotional_regulation": assessment.emotional_regulation,
            "recovery_rate": assessment.recovery_rate,
            "impulsivity": assessment.impulsivity,
            **report_scores
        })

    df = pd.DataFrame(data)
    corr = df.corr(numeric_only=True).round(3)
    
    # Replace NaN values with None for JSON serialization
    corr_clean = corr.fillna(0)

    return {
        "columns": list(corr_clean.columns),
        "matrix": corr_clean.values.tolist()
    }


def get_cluster_analysis(db: Session, n_clusters: int = 3) -> Dict:
    """Cluster assessments into psychological profile groups."""
    assessments = db.query(models.Assessment).all()

    if len(assessments) < n_clusters:
        return {"message": "Not enough assessments for clustering."}

    data = [
        [a.trauma_sensitivity, a.emotional_regulation, a.recovery_rate, a.impulsivity]
        for a in assessments
    ]

    df = pd.DataFrame(data, columns=[
        "trauma_sensitivity",
        "emotional_regulation",
        "recovery_rate",
        "impulsivity"
    ])

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(df)

    centers = kmeans.cluster_centers_.tolist()
    counts = pd.Series(labels).value_counts().to_dict()

    return {
        "n_clusters": n_clusters,
        "cluster_centers": centers,
        "cluster_counts": counts
    }


def get_profile_summary(db: Session) -> Dict:
    """Provide summary statistics for assessments."""
    assessments = db.query(models.Assessment).all()
    if not assessments:
        return {"message": "No assessments available."}

    df = pd.DataFrame([
        {
            "trauma_sensitivity": a.trauma_sensitivity,
            "emotional_regulation": a.emotional_regulation,
            "recovery_rate": a.recovery_rate,
            "impulsivity": a.impulsivity
        }
        for a in assessments
    ])

    summary = df.describe().round(3).to_dict()
    return {"summary": summary}


def get_person_analytics(db: Session, person_id: int) -> Dict:
    """Get person-specific analytics from their assessments and simulations."""
    person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if not person:
        return {"error": "Person not found"}
    
    assessments = db.query(models.Assessment).filter(
        models.Assessment.person_id == person_id
    ).all()
    
    if not assessments:
        return {
            "person_name": person.name,
            "message": "No assessments found for this person"
        }
    
    # Prepare assessment data
    assessment_data = []
    for assessment in assessments:
        assessment_data.append({
            "id": assessment.id,
            "trauma_sensitivity": assessment.trauma_sensitivity,
            "emotional_regulation": assessment.emotional_regulation,
            "recovery_rate": assessment.recovery_rate,
            "impulsivity": assessment.impulsivity,
            "coping_mechanism": assessment.coping_mechanism,
            "created_at": assessment.assessment_date.isoformat() if assessment.assessment_date else None
        })
    
    # Get reports linked to this person's assessments
    reports = db.query(models.Report).filter(
        models.Report.person_id == person_id
    ).all()
    
    report_data = []
    for report in reports:
        scores = _map_report_scores(report)
        # Get the assessment date for this report
        report_assessment = None
        if report.assessment_id:
            report_assessment = db.query(models.Assessment).filter(
                models.Assessment.id == report.assessment_id
            ).first()
        
        report_data.append({
            "id": report.id,
            "assessment_id": report.assessment_id,
            "avoidance": report.avoidance,
            "re_experiencing": report.re_experiencing,
            "negative_alterations": report.negative_alterations,
            "hyperarousal": report.hyperarousal,
            "created_at": report_assessment.assessment_date.isoformat() if report_assessment and report_assessment.assessment_date else None,
            **scores
        })
    
    # Calculate current profile (latest assessment)
    latest_assessment = max(assessments, key=lambda a: a.id) if assessments else None
    
    return {
        "person_name": person.name,
        "person_id": person.id,
        "rank": person.rank,
        "assessments": assessment_data,
        "reports": report_data,
        "current_profile": {
            "trauma_sensitivity": latest_assessment.trauma_sensitivity if latest_assessment else None,
            "emotional_regulation": latest_assessment.emotional_regulation if latest_assessment else None,
            "recovery_rate": latest_assessment.recovery_rate if latest_assessment else None,
            "impulsivity": latest_assessment.impulsivity if latest_assessment else None,
        },
        "assessment_count": len(assessments),
        "simulation_count": len(reports)
    }

