import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "ptsd_simulation_db")

# Connect to MySQL without a database
engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/")

with engine.connect() as conn:
    # Drop database
    conn.execute(text(f"DROP DATABASE IF EXISTS `{MYSQL_DATABASE}`"))
    # Create database
    conn.execute(text(f"CREATE DATABASE `{MYSQL_DATABASE}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    conn.commit()

print(f"Database {MYSQL_DATABASE} recreated successfully")

# Now create tables
from backend.database import engine as app_engine, Base
from backend import models

Base.metadata.create_all(bind=app_engine)
print("Tables created successfully")

# Seed initial data
from backend.database import SessionLocal
from backend import presets

db = SessionLocal()

try:
    # Add therapist
    from backend.models import Therapist
    t1 = Therapist(name="Dr. Sarah Connor", qualification="PhD Clinical Psychology", specialization="Trauma", years_of_experience=15)
    db.add(t1)
    db.commit()
    db.refresh(t1)

    # Add persons
    from backend.models import Person
    p1 = Person(name="Pvt. Ryan", rank="Private", age=22, gender="Male", service_years=1, therapist_id=t1.id)
    p2 = Person(name="Sgt. Miller", rank="Sergeant", age=35, gender="Male", service_years=12, therapist_id=t1.id)
    p3 = Person(name="Cpl. Ripley", rank="Corporal", age=28, gender="Female", service_years=5, therapist_id=t1.id)

    db.add_all([p1, p2, p3])
    db.commit()

    # Add scenarios
    from backend.models import Scenario
    scenario_models = []
    for preset in presets.SCENARIO_CATALOG:
        scenario_models.append(
            Scenario(
                scenario_type=preset["scenario_type"],
                environment=preset["environment"],
                assigned_date=None,
            )
        )

    db.add_all(scenario_models)
    db.commit()

    # Add questionnaire questions (20 questions, 5 per dimension)
    from backend.models import Questionnaire
    
    # Standard scoring weights for Likert-5 scale: 1=0.0, 2=0.25, 3=0.5, 4=0.75, 5=1.0
    standard_weights = {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0}
    # Reverse scoring for emotional_regulation and recovery_rate (higher score = better)
    reverse_weights = {"1": 1.0, "2": 0.75, "3": 0.5, "4": 0.25, "5": 0.0}
    
    questions = [
        # Trauma Sensitivity (5 questions) - higher score = more sensitive
        Questionnaire(question_text="I often have intrusive memories or flashbacks of traumatic events.", dimension="trauma_sensitivity", question_type="likert_5", scoring_weights=standard_weights, is_active=True),
        Questionnaire(question_text="Loud noises or sudden movements make me feel extremely anxious.", dimension="trauma_sensitivity", question_type="likert_5", scoring_weights=standard_weights, is_active=True),
        Questionnaire(question_text="I avoid places or situations that remind me of past traumatic experiences.", dimension="trauma_sensitivity", question_type="likert_5", scoring_weights=standard_weights, is_active=True),
        Questionnaire(question_text="I feel on edge or easily startled in everyday situations.", dimension="trauma_sensitivity", question_type="likert_5", scoring_weights=standard_weights, is_active=True),
        Questionnaire(question_text="Certain smells, sounds, or images trigger strong emotional reactions in me.", dimension="trauma_sensitivity", question_type="likert_5", scoring_weights=standard_weights, is_active=True),
        
        # Emotional Regulation (5 questions) - higher score = better regulation (REVERSE SCORED)
        Questionnaire(question_text="I can calm myself down when I feel upset or angry.", dimension="emotional_regulation", question_type="likert_5", scoring_weights=reverse_weights, is_reverse_scored=True, is_active=True),
        Questionnaire(question_text="I am able to think clearly even when under pressure.", dimension="emotional_regulation", question_type="likert_5", scoring_weights=reverse_weights, is_reverse_scored=True, is_active=True),
        Questionnaire(question_text="I can control my emotional reactions in stressful situations.", dimension="emotional_regulation", question_type="likert_5", scoring_weights=reverse_weights, is_reverse_scored=True, is_active=True),
        Questionnaire(question_text="I rarely let my emotions get the best of me.", dimension="emotional_regulation", question_type="likert_5", scoring_weights=reverse_weights, is_reverse_scored=True, is_active=True),
        Questionnaire(question_text="I find it easy to maintain composure during conflict.", dimension="emotional_regulation", question_type="likert_5", scoring_weights=reverse_weights, is_reverse_scored=True, is_active=True),
        
        # Recovery Rate (5 questions) - higher score = better recovery (REVERSE SCORED)
        Questionnaire(question_text="I bounce back quickly after stressful events.", dimension="recovery_rate", question_type="likert_5", scoring_weights=reverse_weights, is_reverse_scored=True, is_active=True),
        Questionnaire(question_text="I can return to normal functioning soon after experiencing distress.", dimension="recovery_rate", question_type="likert_5", scoring_weights=reverse_weights, is_reverse_scored=True, is_active=True),
        Questionnaire(question_text="I recover from setbacks faster than most people.", dimension="recovery_rate", question_type="likert_5", scoring_weights=reverse_weights, is_reverse_scored=True, is_active=True),
        Questionnaire(question_text="After a difficult experience, I am able to move forward without dwelling on it.", dimension="recovery_rate", question_type="likert_5", scoring_weights=reverse_weights, is_reverse_scored=True, is_active=True),
        Questionnaire(question_text="I adapt well to changes and unexpected situations.", dimension="recovery_rate", question_type="likert_5", scoring_weights=reverse_weights, is_reverse_scored=True, is_active=True),
        
        # Impulsivity (5 questions) - higher score = more impulsive
        Questionnaire(question_text="I often act without thinking about the consequences.", dimension="impulsivity", question_type="likert_5", scoring_weights=standard_weights, is_active=True),
        Questionnaire(question_text="I make decisions quickly, even in high-stakes situations.", dimension="impulsivity", question_type="likert_5", scoring_weights=standard_weights, is_active=True),
        Questionnaire(question_text="I find it hard to wait or be patient when I want something.", dimension="impulsivity", question_type="likert_5", scoring_weights=standard_weights, is_active=True),
        Questionnaire(question_text="I sometimes do things on the spur of the moment without planning.", dimension="impulsivity", question_type="likert_5", scoring_weights=standard_weights, is_active=True),
        Questionnaire(question_text="I have difficulty controlling my urges or impulses.", dimension="impulsivity", question_type="likert_5", scoring_weights=standard_weights, is_active=True),
    ]
    
    db.add_all(questions)
    db.commit()

    print("Initial data seeded successfully")
finally:
    db.close()
