"""
Authentication router for user registration, login, and profile management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user (soldier or therapist)
    - For soldiers: creates a new Person record, then links User to it
    - For therapists: creates a new Therapist record, then links User to it
    """
    # Check if username already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    hashed_password = auth.get_password_hash(user.password)
    person_id = None
    therapist_id = None
    
    # For soldiers: create a new Person
    if user.role == "soldier":
        new_person = models.Person(
            name=user.soldier_name or user.username,
            rank=user.rank or "Private",
            age=user.age or 25,
            gender=user.gender or "Unknown",
            service_years=user.service_years or 0,
            therapist_id=None  # Soldier can select therapist later
        )
        db.add(new_person)
        db.flush()  # Flush to get the ID without committing
        person_id = new_person.id
    
    # For therapists: create a new Therapist
    elif user.role == "therapist":
        new_therapist = models.Therapist(
            name=user.therapist_name or user.username,
            qualification=user.qualification or "",
            specialization=user.specialization or "General",
            years_of_experience=user.years_of_experience or 0
        )
        db.add(new_therapist)
        db.flush()
        therapist_id = new_therapist.id
    
    # Create new user linked to the newly created person/therapist
    db_user = models.User(
        username=user.username,
        password_hash=hashed_password,
        role=models.UserRole[user.role],
        person_id=person_id,
        therapist_id=therapist_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with username and password, returns JWT token
    """
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login-json", response_model=schemas.Token)
def login_json(
    credentials: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with JSON body (for React frontend)
    """
    user = auth.authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.User)
async def get_current_user_info(
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Get current logged-in user information
    """
    return current_user

@router.get("/me/profile")
async def get_user_profile(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed profile information for current user
    """
    profile = {
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "role": current_user.role.value,
            "created_at": current_user.created_at,
            "last_login": current_user.last_login
        }
    }
    
    # Add person details if soldier
    if current_user.role.value == "soldier" and current_user.person_id:
        person = db.query(models.Person).filter(models.Person.id == current_user.person_id).first()
        if person:
            profile["person"] = {
                "id": person.id,
                "name": person.name,
                "rank": person.rank,
                "age": person.age,
                "gender": person.gender,
                "service_years": person.service_years,
                "therapist_id": person.therapist_id
            }
            
            # Get latest assessment if exists
            latest_assessment = db.query(models.Assessment)\
                .filter(models.Assessment.person_id == person.id)\
                .order_by(models.Assessment.assessment_date.desc())\
                .first()
            
            if latest_assessment:
                profile["latest_assessment"] = {
                    "id": latest_assessment.id,
                    "assessment_date": latest_assessment.assessment_date,
                    "trauma_sensitivity": latest_assessment.trauma_sensitivity,
                    "emotional_regulation": latest_assessment.emotional_regulation,
                    "recovery_rate": latest_assessment.recovery_rate,
                    "impulsivity": latest_assessment.impulsivity,
                    "coping_mechanism": latest_assessment.coping_mechanism.value
                }
    
    # Add therapist details if therapist
    elif current_user.role.value == "therapist" and current_user.therapist_id:
        therapist = db.query(models.Therapist).filter(models.Therapist.id == current_user.therapist_id).first()
        if therapist:
            profile["therapist"] = {
                "id": therapist.id,
                "name": therapist.name,
                "qualification": therapist.qualification,
                "specialization": therapist.specialization,
                "years_of_experience": therapist.years_of_experience
            }
    
    return profile
