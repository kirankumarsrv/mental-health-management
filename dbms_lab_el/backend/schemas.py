from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import date, datetime

# --- Therapist ---
class TherapistBase(BaseModel):
    name: str
    qualification: str
    specialization: str
    years_of_experience: int

class TherapistCreate(TherapistBase):
    pass

class Therapist(TherapistBase):
    id: int
    
    class Config:
        from_attributes = True

# --- Person ---
class PersonBase(BaseModel):
    name: str
    rank: str
    age: int
    gender: str
    service_years: int
    therapist_id: Optional[int] = None

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: int

    class Config:
        from_attributes = True

# --- Scenario ---
class ScenarioBase(BaseModel):
    scenario_type: str
    environment: str
    assigned_date: Optional[date] = None  # NEW: Added assigned_date

class ScenarioCreate(ScenarioBase):
    pass

class Scenario(ScenarioBase):
    id: int

    class Config:
        from_attributes = True

# --- Reaction ---
class ReactionBase(BaseModel):
    r_type: str  # RENAMED: reaction_type → r_type
    physical_response: str
    # REMOVED: person_id, scenario_id (now in junction tables)

class ReactionCreate(ReactionBase):
    pass

class Reaction(ReactionBase):
    id: int

    class Config:
        from_attributes = True

# --- Report ---
class ReportBase(BaseModel):
    avoidance: str
    re_experiencing: str
    negative_alterations: str
    hyperarousal: str
    person_id: int
    therapist_id: Optional[int] = None  # Optional: soldier may not have therapist assigned yet
    reaction_id: int   # NEW: Added reaction_id
    assessment_id: Optional[int] = None  # Link to assessment if used
    # REMOVED: scenario_id (relationships via person/therapist/reaction)

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int

    class Config:
        from_attributes = True

# ============================================
# JUNCTION TABLE SCHEMAS
# ============================================

# --- Participates (Person ↔ Scenario) ---
class ParticipatesBase(BaseModel):
    person_id: int
    scenario_id: int

class ParticipatesCreate(ParticipatesBase):
    pass

class Participates(ParticipatesBase):
    class Config:
        from_attributes = True

# --- Assigns (Therapist ↔ Scenario) ---
class AssignsBase(BaseModel):
    therapist_id: int
    scenario_id: int

class AssignsCreate(AssignsBase):
    pass

class Assigns(AssignsBase):
    class Config:
        from_attributes = True

# --- Exhibits (Person ↔ Reaction) ---
class ExhibitsBase(BaseModel):
    person_id: int
    reaction_id: int

class ExhibitsCreate(ExhibitsBase):
    pass

class Exhibits(ExhibitsBase):
    class Config:
        from_attributes = True

# --- Triggers (Scenario ↔ Reaction) ---
class TriggersBase(BaseModel):
    scenario_id: int
    reaction_id: int

class TriggersCreate(TriggersBase):
    pass

class Triggers(TriggersBase):
    class Config:
        from_attributes = True

# ============================================
# SIMULATION REQUEST
# ============================================

# --- Simulation Run Request ---
class SimulationRunRequest(BaseModel):
    person_id: int
    scenario_id: int
    assigned_date: Optional[str] = None  # Used for scenario
    assessment_id: Optional[int] = None
    grid_size: int = 10  # UI slider (clamped server-side)
    trauma_sensitivity: float = 0.5
    emotional_regulation: float = 0.5
    recovery_rate: float = 0.5
    impulsivity: float = 0.5
    coping_mechanism: str = "avoidance"

# ============================================
# AUTHENTICATION SCHEMAS
# ============================================

class UserBase(BaseModel):
    username: str
    role: str = "soldier"

class UserCreate(UserBase):
    password: str
    # For soldiers: provide soldier details
    soldier_name: Optional[str] = None
    rank: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    service_years: Optional[int] = None
    # For therapists: provide therapist details
    therapist_name: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    years_of_experience: Optional[int] = None

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    person_id: Optional[int] = None
    therapist_id: Optional[int] = None
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

# ============================================
# QUESTIONNAIRE SCHEMAS
# ============================================

class QuestionnaireBase(BaseModel):
    question_text: str
    dimension: str  # trauma_sensitivity, emotional_regulation, recovery_rate, impulsivity
    question_type: str = "likert_5"
    options: Optional[Dict] = None
    scoring_weights: Dict  # {"1": 0.0, "2": 0.25, ...}
    is_reverse_scored: bool = False
    is_active: bool = True

class QuestionnaireCreate(QuestionnaireBase):
    pass

class Questionnaire(QuestionnaireBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ResponseBase(BaseModel):
    questionnaire_id: int
    answer_value: str
    response_time_seconds: Optional[int] = None

class ResponseCreate(ResponseBase):
    pass

class Response(ResponseBase):
    id: int
    assessment_id: int
    answer_score: float

    class Config:
        from_attributes = True

class AssessmentBase(BaseModel):
    person_id: int
    therapist_id: Optional[int] = None

class AssessmentCreate(AssessmentBase):
    responses: List[ResponseCreate]
    coping_mechanism: str = "avoidance"
    completion_time_seconds: Optional[int] = None

class Assessment(AssessmentBase):
    id: int
    assessment_date: datetime
    trauma_sensitivity: float
    emotional_regulation: float
    recovery_rate: float
    impulsivity: float
    coping_mechanism: str
    completion_time_seconds: Optional[int] = None

    class Config:
        from_attributes = True

class AssessmentWithResponses(Assessment):
    responses: List[Response] = []

    class Config:
        from_attributes = True
# --- Therapist Recommendations ---
class TherapistRecommendationBase(BaseModel):
    scenario_id: int
    suggested_coping_mechanism: str
    recommendation_text: Optional[str] = None

class TherapistRecommendationCreate(TherapistRecommendationBase):
    person_id: int

class TherapistRecommendation(TherapistRecommendationBase):
    id: int
    therapist_id: int
    person_id: int
    created_date: datetime
    status: str = "pending"
    soldier_response: Optional[str] = None

    class Config:
        from_attributes = True

# --- Patient Analysis & Dashboard ---
class PatientAssessmentSummary(BaseModel):
    id: int
    name: str
    rank: str
    age: int
    gender: str
    service_years: int
    latest_trauma_sensitivity: Optional[float] = None
    latest_emotional_regulation: Optional[float] = None
    latest_recovery_rate: Optional[float] = None
    latest_impulsivity: Optional[float] = None
    latest_coping_mechanism: Optional[str] = None
    assessment_count: int
    last_assessment_date: Optional[datetime] = None

class PatientDetailedView(PatientAssessmentSummary):
    assessments: List[Assessment] = []
    reports: List[Dict] = []
    recommendations: List[TherapistRecommendation] = []
    scenario_participation_count: int = 0

class TherapistPatientList(BaseModel):
    total_patients: int
    patients: List[PatientAssessmentSummary] = []

class TherapistDashboardStats(BaseModel):
    total_patients: int
    total_recommendations: int
    accepted_recommendations: int
    completed_simulations: int
    average_trauma_sensitivity: float
    average_emotional_regulation: float
    average_recovery_rate: float
    average_impulsivity: float