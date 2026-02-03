from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Float, Boolean, Enum as SQLEnum, DateTime, JSON
from datetime import datetime
import enum
from sqlalchemy.orm import relationship
from .database import Base

# ============================================
# CORE ENTITIES (5 Tables)
# ============================================

class Therapist(Base):
    __tablename__ = "therapists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    qualification = Column(String(150))
    specialization = Column(String(100))
    years_of_experience = Column(Integer)

    # Relationships
    patients = relationship("Person", back_populates="therapist")
    reports = relationship("Report", back_populates="therapist")
    # Many-to-many with Scenario via Assigns
    assigned_scenarios = relationship("Assigns", back_populates="therapist")

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    rank = Column(String(50))
    age = Column(Integer)
    gender = Column(String(20))
    service_years = Column(Integer)
    therapist_id = Column(Integer, ForeignKey("therapists.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    current_assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=True)

    # Relationships
    therapist = relationship("Therapist", back_populates="patients")
    reports = relationship("Report", back_populates="person")
    # Many-to-many relationships via junction tables
    participated_scenarios = relationship("Participates", back_populates="person")
    exhibited_reactions = relationship("Exhibits", back_populates="person")

class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)
    scenario_type = Column(String(100))
    environment = Column(String(100))
    assigned_date = Column(Date, nullable=True)  # NEW: Added assigned_date

    # Many-to-many relationships via junction tables
    participants = relationship("Participates", back_populates="scenario")
    assigned_therapists = relationship("Assigns", back_populates="scenario")
    triggered_reactions = relationship("Triggers", back_populates="scenario")

class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    r_type = Column(String(50))  # RENAMED: reaction_type → r_type
    physical_response = Column(Text)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=True)
    # REMOVED: person_id, scenario_id (moved to junction tables)

    # Many-to-many relationships via junction tables
    reports = relationship("Report", back_populates="reaction")
    exhibiting_persons = relationship("Exhibits", back_populates="reaction")
    triggering_scenarios = relationship("Triggers", back_populates="reaction")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    avoidance = Column(String(32))
    re_experiencing = Column(String(32))
    negative_alterations = Column(String(32))
    hyperarousal = Column(String(32))
    
    # NEW: Three foreign keys instead of person_id + scenario_id
    person_id = Column(Integer, ForeignKey("persons.id"))
    therapist_id = Column(Integer, ForeignKey("therapists.id"))  # NEW
    reaction_id = Column(Integer, ForeignKey("reactions.id"))    # NEW
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=True)

    # Relationships
    person = relationship("Person", back_populates="reports")
    therapist = relationship("Therapist", back_populates="reports")
    reaction = relationship("Reaction", back_populates="reports")
    assessment = relationship("Assessment", back_populates="reports")

# ============================================
# JUNCTION TABLES (4 Tables for M:M relationships)
# ============================================

class Participates(Base):
    """Person ↔ Scenario: Who participated in which scenario"""
    __tablename__ = "participates"

    person_id = Column(Integer, ForeignKey("persons.id"), primary_key=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), primary_key=True)

    # Relationships
    person = relationship("Person", back_populates="participated_scenarios")
    scenario = relationship("Scenario", back_populates="participants")

class Assigns(Base):
    """Therapist ↔ Scenario: Which therapist assigned which scenario"""
    __tablename__ = "assigns"

    therapist_id = Column(Integer, ForeignKey("therapists.id"), primary_key=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), primary_key=True)

    # Relationships
    therapist = relationship("Therapist", back_populates="assigned_scenarios")
    scenario = relationship("Scenario", back_populates="assigned_therapists")

class Exhibits(Base):
    """Person ↔ Reaction: Who exhibited which reaction"""
    __tablename__ = "exhibits"

    person_id = Column(Integer, ForeignKey("persons.id"), primary_key=True)
    reaction_id = Column(Integer, ForeignKey("reactions.id"), primary_key=True)

    # Relationships
    person = relationship("Person", back_populates="exhibited_reactions")
    reaction = relationship("Reaction", back_populates="exhibiting_persons")

class Triggers(Base):
    """Scenario ↔ Reaction: Which scenario triggered which reaction"""
    __tablename__ = "triggers"

    scenario_id = Column(Integer, ForeignKey("scenarios.id"), primary_key=True)
    reaction_id = Column(Integer, ForeignKey("reactions.id"), primary_key=True)

    # Relationships
    scenario = relationship("Scenario", back_populates="triggered_reactions")
    reaction = relationship("Reaction", back_populates="triggering_scenarios")

# ============================================
# AUTHENTICATION & QUESTIONNAIRE MODELS (4 Tables)
# ============================================

class UserRole(enum.Enum):
    soldier = "soldier"
    therapist = "therapist"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.soldier)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=True)
    therapist_id = Column(Integer, ForeignKey("therapists.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    person = relationship("Person", foreign_keys=[person_id], backref="user_account")
    therapist = relationship("Therapist", foreign_keys=[therapist_id], backref="user_account")

class DimensionType(enum.Enum):
    trauma_sensitivity = "trauma_sensitivity"
    emotional_regulation = "emotional_regulation"
    recovery_rate = "recovery_rate"
    impulsivity = "impulsivity"

class QuestionType(enum.Enum):
    likert_5 = "likert_5"
    yes_no = "yes_no"
    multiple_choice = "multiple_choice"

class Questionnaire(Base):
    __tablename__ = "questionnaires"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    dimension = Column(SQLEnum(DimensionType), nullable=False)
    question_type = Column(SQLEnum(QuestionType), default=QuestionType.likert_5)
    options = Column(JSON, nullable=True)  # For multiple choice options
    scoring_weights = Column(JSON, nullable=False)  # {"1": 0.0, "2": 0.25, ...}
    is_reverse_scored = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    responses = relationship("Response", back_populates="questionnaire")

class CopingMechanism(enum.Enum):
    avoidance = "avoidance"
    approach = "approach"
    freezing = "freezing"
    suppression = "suppression"

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    assessment_date = Column(DateTime, default=datetime.utcnow)
    
    # Calculated Profile Scores (from responses)
    trauma_sensitivity = Column(Float, nullable=False)
    emotional_regulation = Column(Float, nullable=False)
    recovery_rate = Column(Float, nullable=False)
    impulsivity = Column(Float, nullable=False)
    coping_mechanism = Column(SQLEnum(CopingMechanism), default=CopingMechanism.avoidance)
    
    # Metadata
    completion_time_seconds = Column(Integer, nullable=True)
    therapist_id = Column(Integer, ForeignKey("therapists.id"), nullable=True)
    
    # Relationships
    person = relationship("Person", foreign_keys=[person_id], backref="assessments")
    therapist = relationship("Therapist", foreign_keys=[therapist_id], backref="assessments")
    responses = relationship("Response", back_populates="assessment", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="assessment")

class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id"), nullable=False)
    answer_value = Column(String(255), nullable=False)  # "3" for Likert, "Yes", "Option A"
    answer_score = Column(Float, nullable=False)  # Normalized 0.0-1.0
    response_time_seconds = Column(Integer, nullable=True)
    
    # Relationships
    assessment = relationship("Assessment", back_populates="responses")
    questionnaire = relationship("Questionnaire", back_populates="responses")

class TherapistRecommendation(Base):
    __tablename__ = "therapist_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    therapist_id = Column(Integer, ForeignKey("therapists.id"), nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)
    suggested_coping_mechanism = Column(SQLEnum(CopingMechanism), nullable=False)
    recommendation_text = Column(Text, nullable=True)  # Optional notes from therapist
    created_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="pending")  # pending, accepted, rejected, completed
    soldier_response = Column(Text, nullable=True)  # Soldier's feedback
    
    # Relationships
    therapist = relationship("Therapist", backref="recommendations")
    person = relationship("Person", backref="therapist_recommendations")
    scenario = relationship("Scenario", backref="recommendations")
