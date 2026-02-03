from sqlalchemy.orm import Session
from . import models, schemas

# ============================================
# CORE ENTITIES CRUD
# ============================================

# --- Therapist ---
def get_therapist(db: Session, therapist_id: int):
    return db.query(models.Therapist).filter(models.Therapist.id == therapist_id).first()

def get_therapists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Therapist).offset(skip).limit(limit).all()

def create_therapist(db: Session, therapist: schemas.TherapistCreate):
    db_therapist = models.Therapist(**therapist.dict())
    db.add(db_therapist)
    db.commit()
    db.refresh(db_therapist)
    return db_therapist

def update_therapist(db: Session, therapist_id: int, therapist: schemas.TherapistCreate):
    db_therapist = db.query(models.Therapist).filter(models.Therapist.id == therapist_id).first()
    if db_therapist:
        for key, value in therapist.dict().items():
            setattr(db_therapist, key, value)
        db.commit()
        db.refresh(db_therapist)
    return db_therapist

def delete_therapist(db: Session, therapist_id: int):
    db_therapist = db.query(models.Therapist).filter(models.Therapist.id == therapist_id).first()
    if db_therapist:
        db.delete(db_therapist)
        db.commit()
    return db_therapist

# --- Person ---
def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()

def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).offset(skip).limit(limit).all()

def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def update_person(db: Session, person_id: int, person: schemas.PersonCreate):
    db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if db_person:
        for key, value in person.dict().items():
            setattr(db_person, key, value)
        db.commit()
        db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: int):
    db_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if db_person:
        db.delete(db_person)
        db.commit()
    return db_person

# --- Scenario ---
def get_scenario(db: Session, scenario_id: int):
    return db.query(models.Scenario).filter(models.Scenario.id == scenario_id).first()

def get_scenarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Scenario).offset(skip).limit(limit).all()

def create_scenario(db: Session, scenario: schemas.ScenarioCreate):
    db_scenario = models.Scenario(**scenario.dict())
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    return db_scenario

def update_scenario(db: Session, scenario_id: int, scenario: schemas.ScenarioCreate):
    db_scenario = db.query(models.Scenario).filter(models.Scenario.id == scenario_id).first()
    if db_scenario:
        for key, value in scenario.dict().items():
            setattr(db_scenario, key, value)
        db.commit()
        db.refresh(db_scenario)
    return db_scenario

def delete_scenario(db: Session, scenario_id: int):
    db_scenario = db.query(models.Scenario).filter(models.Scenario.id == scenario_id).first()
    if db_scenario:
        db.delete(db_scenario)
        db.commit()
    return db_scenario

# --- Reaction ---
def create_reaction(db: Session, reaction: schemas.ReactionCreate):
    db_reaction = models.Reaction(**reaction.dict())
    db.add(db_reaction)
    db.commit()
    db.refresh(db_reaction)
    return db_reaction

def get_reaction(db: Session, reaction_id: int):
    return db.query(models.Reaction).filter(models.Reaction.id == reaction_id).first()

def get_reactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Reaction).offset(skip).limit(limit).all()

# --- Report ---
def create_report(db: Session, report: schemas.ReportCreate):
    db_report = models.Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_report(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.id == report_id).first()

def get_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Report).offset(skip).limit(limit).all()

def get_reports_by_person(db: Session, person_id: int):
    return db.query(models.Report).filter(models.Report.person_id == person_id).all()

# ============================================
# JUNCTION TABLES CRUD
# ============================================

# --- Participates (Person ↔ Scenario) ---
def create_participates(db: Session, participates: schemas.ParticipatesCreate):
    existing = db.query(models.Participates).filter(
        models.Participates.person_id == participates.person_id,
        models.Participates.scenario_id == participates.scenario_id,
    ).first()
    if existing:
        return existing

    db_participates = models.Participates(**participates.dict())
    db.add(db_participates)
    db.commit()
    db.refresh(db_participates)
    return db_participates

def get_participates_by_person(db: Session, person_id: int):
    """Get all scenarios a person participated in"""
    return db.query(models.Participates).filter(models.Participates.person_id == person_id).all()

def get_participates_by_scenario(db: Session, scenario_id: int):
    """Get all persons who participated in a scenario"""
    return db.query(models.Participates).filter(models.Participates.scenario_id == scenario_id).all()

# --- Assigns (Therapist ↔ Scenario) ---
def create_assigns(db: Session, assigns: schemas.AssignsCreate):
    existing = db.query(models.Assigns).filter(
        models.Assigns.therapist_id == assigns.therapist_id,
        models.Assigns.scenario_id == assigns.scenario_id,
    ).first()
    if existing:
        return existing

    db_assigns = models.Assigns(**assigns.dict())
    db.add(db_assigns)
    db.commit()
    db.refresh(db_assigns)
    return db_assigns

def get_assigns_by_therapist(db: Session, therapist_id: int):
    """Get all scenarios assigned by a therapist"""
    return db.query(models.Assigns).filter(models.Assigns.therapist_id == therapist_id).all()

def get_assigns_by_scenario(db: Session, scenario_id: int):
    """Get therapist who assigned a scenario"""
    return db.query(models.Assigns).filter(models.Assigns.scenario_id == scenario_id).all()

# --- Exhibits (Person ↔ Reaction) ---
def create_exhibits(db: Session, exhibits: schemas.ExhibitsCreate):
    existing = db.query(models.Exhibits).filter(
        models.Exhibits.person_id == exhibits.person_id,
        models.Exhibits.reaction_id == exhibits.reaction_id,
    ).first()
    if existing:
        return existing

    db_exhibits = models.Exhibits(**exhibits.dict())
    db.add(db_exhibits)
    db.commit()
    db.refresh(db_exhibits)
    return db_exhibits

def get_exhibits_by_person(db: Session, person_id: int):
    """Get all reactions exhibited by a person"""
    return db.query(models.Exhibits).filter(models.Exhibits.person_id == person_id).all()

def get_exhibits_by_reaction(db: Session, reaction_id: int):
    """Get persons who exhibited a reaction"""
    return db.query(models.Exhibits).filter(models.Exhibits.reaction_id == reaction_id).all()

# --- Triggers (Scenario ↔ Reaction) ---
def create_triggers(db: Session, triggers: schemas.TriggersCreate):
    existing = db.query(models.Triggers).filter(
        models.Triggers.scenario_id == triggers.scenario_id,
        models.Triggers.reaction_id == triggers.reaction_id,
    ).first()
    if existing:
        return existing

    db_triggers = models.Triggers(**triggers.dict())
    db.add(db_triggers)
    db.commit()
    db.refresh(db_triggers)
    return db_triggers

def get_triggers_by_scenario(db: Session, scenario_id: int):
    """Get all reactions triggered by a scenario"""
    return db.query(models.Triggers).filter(models.Triggers.scenario_id == scenario_id).all()

def get_triggers_by_reaction(db: Session, reaction_id: int):
    """Get scenarios that triggered a reaction"""
    return db.query(models.Triggers).filter(models.Triggers.reaction_id == reaction_id).all()

# ============================================
# STATISTICS
# ============================================

def get_statistics(db: Session):
    """Get dashboard statistics"""
    return {
        "total_persons": db.query(models.Person).count(),
        "total_therapists": db.query(models.Therapist).count(),
        "total_scenarios": db.query(models.Scenario).count(),
        "total_reactions": db.query(models.Reaction).count(),
        "total_reports": db.query(models.Report).count(),
        "total_participations": db.query(models.Participates).count(),
        "total_assignments": db.query(models.Assigns).count()
    }

# ============================================
# QUESTIONNAIRE & ASSESSMENT CRUD
# ============================================

# --- Questionnaire ---
def get_questionnaires(db: Session, active_only: bool = True):
    """Get all questionnaires, optionally filter by active status"""
    query = db.query(models.Questionnaire)
    if active_only:
        query = query.filter(models.Questionnaire.is_active == True)
    return query.order_by(models.Questionnaire.id).all()

def get_questionnaire(db: Session, questionnaire_id: int):
    """Get a single questionnaire by ID"""
    return db.query(models.Questionnaire).filter(models.Questionnaire.id == questionnaire_id).first()

def create_questionnaire(db: Session, questionnaire: schemas.QuestionnaireCreate):
    """Create a new questionnaire"""
    db_questionnaire = models.Questionnaire(**questionnaire.dict())
    db.add(db_questionnaire)
    db.commit()
    db.refresh(db_questionnaire)
    return db_questionnaire

# --- Assessment ---
def create_assessment(db: Session, assessment: schemas.AssessmentCreate):
    """
    Create a new assessment with responses and calculate profile scores
    """
    # Calculate profile scores from responses
    dimension_scores = {
        'trauma_sensitivity': [],
        'emotional_regulation': [],
        'recovery_rate': [],
        'impulsivity': []
    }

    # First, create the assessment without responses
    db_assessment = models.Assessment(
        person_id=assessment.person_id,
        therapist_id=assessment.therapist_id,
        completion_time_seconds=assessment.completion_time_seconds,
        coping_mechanism=models.CopingMechanism[assessment.coping_mechanism],
        # These will be calculated below
        trauma_sensitivity=0.0,
        emotional_regulation=0.0,
        recovery_rate=0.0,
        impulsivity=0.0
    )
    db.add(db_assessment)
    db.flush()  # Get the assessment ID without committing

    # Process each response
    for response in assessment.responses:
        # Get the questionnaire to access scoring weights
        questionnaire = get_questionnaire(db, response.questionnaire_id)
        if not questionnaire:
            continue
    
        # Calculate score from answer value
        answer_value = response.answer_value
        scoring_weights = questionnaire.scoring_weights
    
        # Get the score from weights
        answer_score = float(scoring_weights.get(answer_value, 0.0))
    
        # Apply reverse scoring if needed
        if questionnaire.is_reverse_scored:
            answer_score = 1.0 - answer_score
    
        # Create response record
        db_response = models.Response(
            assessment_id=db_assessment.id,
            questionnaire_id=response.questionnaire_id,
            answer_value=answer_value,
            answer_score=answer_score,
            response_time_seconds=response.response_time_seconds
        )
        db.add(db_response)
    
        # Accumulate scores by dimension
        dimension = questionnaire.dimension.value
        dimension_scores[dimension].append(answer_score)

    # Calculate average scores for each dimension
    db_assessment.trauma_sensitivity = sum(dimension_scores['trauma_sensitivity']) / len(dimension_scores['trauma_sensitivity']) if dimension_scores['trauma_sensitivity'] else 0.5
    db_assessment.emotional_regulation = sum(dimension_scores['emotional_regulation']) / len(dimension_scores['emotional_regulation']) if dimension_scores['emotional_regulation'] else 0.5
    db_assessment.recovery_rate = sum(dimension_scores['recovery_rate']) / len(dimension_scores['recovery_rate']) if dimension_scores['recovery_rate'] else 0.5
    db_assessment.impulsivity = sum(dimension_scores['impulsivity']) / len(dimension_scores['impulsivity']) if dimension_scores['impulsivity'] else 0.5

    # Update person's current_assessment_id
    person = get_person(db, assessment.person_id)
    if person:
        person.current_assessment_id = db_assessment.id

    db.commit()
    db.refresh(db_assessment)
    return db_assessment

def get_assessment(db: Session, assessment_id: int):
    """Get a single assessment by ID"""
    return db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()

def get_assessments_by_person(db: Session, person_id: int):
    """Get all assessments for a specific person, ordered by date"""
    return db.query(models.Assessment)\
        .filter(models.Assessment.person_id == person_id)\
        .order_by(models.Assessment.assessment_date.desc())\
        .all()

def get_latest_assessment(db: Session, person_id: int):
    """Get the most recent assessment for a person"""
    return db.query(models.Assessment)\
        .filter(models.Assessment.person_id == person_id)\
        .order_by(models.Assessment.assessment_date.desc())\
        .first()

def get_all_assessments(db: Session, skip: int = 0, limit: int = 100):
    """Get all assessments with pagination"""
    return db.query(models.Assessment)\
        .order_by(models.Assessment.assessment_date.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

# --- Response ---
def get_responses_by_assessment(db: Session, assessment_id: int):
    """Get all responses for a specific assessment"""
    return db.query(models.Response)\
        .filter(models.Response.assessment_id == assessment_id)\
        .all()
