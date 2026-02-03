"""
Analytics Router - FastAPI endpoints for database analysis
Add this router to your FastAPI main application to enable analytics endpoints

Usage in main.py:
    from routers.analytics_extended import router as analytics_router
    app.include_router(analytics_router, prefix="/api/analytics", tags=["analytics"])
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Person, Assessment, Report, Therapist, Scenario, Reaction
from backend.schemas import Person as PersonSchema
from person_profile_analyzer import PersonProfileAnalyzer
from typing import List, Dict, Optional
import json

router = APIRouter()

# Initialize analyzer
analyzer = PersonProfileAnalyzer()


@router.get("/person/{person_id}")
def get_person_analysis(person_id: int):
    """Get comprehensive analysis for a specific person
    
    Returns:
        - Basic information (name, rank, age, etc.)
        - Latest assessment scores
        - Therapist information
        - Scenario participation history
        - Reaction patterns
        - Clinical reports
        - Statistical summaries
    """
    profile = analyzer.get_person_profile(person_id)
    if "error" in profile:
        raise HTTPException(status_code=404, detail=profile["error"])
    return profile


@router.get("/persons")
def list_all_persons(limit: int = 100, offset: int = 0):
    """Get list of all persons in database
    
    Args:
        limit: Maximum number of records to return
        offset: Number of records to skip
    
    Returns:
        List of persons with ID, name, rank, age, gender
    """
    persons = analyzer.get_persons_list()
    return {
        "total": len(persons),
        "limit": limit,
        "offset": offset,
        "persons": persons[offset:offset+limit]
    }


@router.get("/search")
def search_persons(q: str = Query(..., min_length=1)):
    """Search for persons by name or rank
    
    Args:
        q: Search query (name or rank)
    
    Returns:
        List of matching persons
    """
    results = analyzer.search_person(q)
    return {
        "query": q,
        "count": len(results),
        "results": results
    }


@router.get("/statistics")
def get_database_statistics():
    """Get overall database statistics for comparison
    
    Returns:
        - Average age and service years
        - Average assessment scores
        - Total persons and assessments
    """
    return analyzer.get_comparison_stats()


@router.get("/person/{person_id}/assessment-history")
def get_person_assessment_history(person_id: int):
    """Get complete assessment history for a person
    
    Args:
        person_id: ID of the person
    
    Returns:
        List of all assessments with scores and dates
    """
    profile = analyzer.get_person_profile(person_id)
    if "error" in profile:
        raise HTTPException(status_code=404, detail=profile["error"])
    return profile['assessments']


@router.get("/person/{person_id}/scenarios")
def get_person_scenarios(person_id: int):
    """Get all scenarios person participated in
    
    Args:
        person_id: ID of the person
    
    Returns:
        List of scenarios with types and environments
    """
    profile = analyzer.get_person_profile(person_id)
    if "error" in profile:
        raise HTTPException(status_code=404, detail=profile["error"])
    return profile['scenarios']


@router.get("/person/{person_id}/reactions")
def get_person_reactions(person_id: int):
    """Get all reactions exhibited by a person
    
    Args:
        person_id: ID of the person
    
    Returns:
        List of reactions with types and descriptions
    """
    profile = analyzer.get_person_profile(person_id)
    if "error" in profile:
        raise HTTPException(status_code=404, detail=profile["error"])
    return profile['reactions']


@router.get("/person/{person_id}/reports")
def get_person_reports(person_id: int):
    """Get clinical reports for a person
    
    Args:
        person_id: ID of the person
    
    Returns:
        List of reports with PTSD symptom assessments
    """
    profile = analyzer.get_person_profile(person_id)
    if "error" in profile:
        raise HTTPException(status_code=404, detail=profile["error"])
    return profile['reports']


@router.get("/person/{person_id}/statistics")
def get_person_statistics(person_id: int):
    """Get statistical summary for a person
    
    Args:
        person_id: ID of the person
    
    Returns:
        Summary statistics including totals and averages
    """
    profile = analyzer.get_person_profile(person_id)
    if "error" in profile:
        raise HTTPException(status_code=404, detail=profile["error"])
    return profile['statistics']


@router.get("/comparisons/age-groups")
def compare_by_age_groups(db: Session = Depends(get_db)):
    """Compare assessment scores across age groups
    
    Returns:
        Statistics grouped by age ranges
    """
    assessments = analyzer.assessments
    persons = analyzer.persons
    
    # Merge data
    merged = persons.merge(assessments, left_on='id', right_on='person_id')
    
    # Create age groups
    merged['age_group'] = pd.cut(merged['age'], 
                                  bins=[0, 25, 35, 45, 55, 100],
                                  labels=['18-25', '26-35', '36-45', '46-55', '55+'])
    
    # Calculate statistics
    stats = merged.groupby('age_group').agg({
        'trauma_sensitivity': ['mean', 'std', 'count'],
        'emotional_regulation': ['mean', 'std'],
        'recovery_rate': ['mean', 'std'],
        'impulsivity': ['mean', 'std']
    }).round(3).to_dict()
    
    return stats


@router.get("/comparisons/gender")
def compare_by_gender(db: Session = Depends(get_db)):
    """Compare assessment scores by gender
    
    Returns:
        Statistics grouped by gender
    """
    assessments = analyzer.assessments
    persons = analyzer.persons
    
    # Merge data
    merged = persons.merge(assessments, left_on='id', right_on='person_id')
    
    # Calculate statistics
    stats = merged.groupby('gender').agg({
        'trauma_sensitivity': ['mean', 'std', 'count'],
        'emotional_regulation': ['mean', 'std'],
        'recovery_rate': ['mean', 'std'],
        'impulsivity': ['mean', 'std']
    }).round(3).to_dict()
    
    return stats


@router.get("/comparisons/rank")
def compare_by_rank(db: Session = Depends(get_db)):
    """Compare assessment scores by military rank
    
    Returns:
        Statistics grouped by rank
    """
    assessments = analyzer.assessments
    persons = analyzer.persons
    
    # Merge data
    merged = persons.merge(assessments, left_on='id', right_on='person_id')
    
    # Calculate statistics
    stats = merged.groupby('rank').agg({
        'trauma_sensitivity': ['mean', 'std', 'count'],
        'emotional_regulation': ['mean', 'std'],
        'recovery_rate': ['mean', 'std'],
        'impulsivity': ['mean', 'std']
    }).round(3).to_dict()
    
    return stats


@router.get("/therapists/workload")
def get_therapist_workload():
    """Get therapist workload metrics
    
    Returns:
        - Patient count per therapist
        - Scenarios assigned
        - Reports generated
    """
    therapists = analyzer.therapists
    persons = analyzer.persons
    
    workload = []
    for _, therapist in therapists.iterrows():
        patients = persons[persons['therapist_id'] == therapist['id']]
        workload.append({
            "id": therapist['id'],
            "name": therapist['name'],
            "specialization": therapist['specialization'],
            "experience_years": therapist['years_of_experience'],
            "patient_count": len(patients),
            "scenarios_assigned": len(analyzer.assigns[analyzer.assigns['therapist_id'] == therapist['id']]),
            "reports_generated": len(analyzer.reports[analyzer.reports['therapist_id'] == therapist['id']])
        })
    
    return {
        "total_therapists": len(workload),
        "workload": workload
    }


@router.get("/scenarios/overview")
def get_scenarios_overview():
    """Get overview of all scenarios
    
    Returns:
        - Scenario types distribution
        - Participation metrics
        - Reaction patterns
    """
    scenarios = analyzer.scenarios
    participates = analyzer.participates
    triggers = analyzer.triggers
    
    overview = []
    for _, scenario in scenarios.iterrows():
        participants = participates[participates['scenario_id'] == scenario['id']]
        reactions_triggered = triggers[triggers['scenario_id'] == scenario['id']]
        
        overview.append({
            "id": scenario['id'],
            "type": scenario['scenario_type'],
            "environment": scenario['environment'],
            "participant_count": len(participants),
            "reaction_count": len(reactions_triggered),
            "assigned_date": str(scenario['assigned_date']) if pd.notna(scenario['assigned_date']) else None
        })
    
    return {
        "total_scenarios": len(scenarios),
        "scenarios": overview
    }


@router.get("/export/person-summary/{person_id}")
def export_person_summary(person_id: int):
    """Export person data as structured summary for reports
    
    Args:
        person_id: ID of the person
    
    Returns:
        Formatted summary ready for document generation
    """
    profile = analyzer.get_person_profile(person_id)
    if "error" in profile:
        raise HTTPException(status_code=404, detail=profile["error"])
    
    # Format for export
    summary = {
        "metadata": {
            "generated_at": str(datetime.now()),
            "person_id": person_id
        },
        "profile": profile
    }
    
    return summary


# Helper imports
import pandas as pd
from datetime import datetime
