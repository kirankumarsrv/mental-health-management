"""
Comprehensive Database Seeding Script
Generates realistic test data:
- Multiple therapists with variety
- Multiple soldiers with variety
- Automatic questionnaire responses
- Automatic simulation runs
- Generated reports
"""
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.database import engine, SessionLocal, Base
from backend import models, crud, schemas
from backend.auth import get_password_hash
from backend.presets import REACTION_CATALOG, SCENARIO_CATALOG
from backend.psychological_profile import PsychologicalProfile
from backend.mesa_model import PTSDModel

# Clear all tables
def clear_database():
    print("🗑️  Clearing database...")
    db = SessionLocal()
    try:
        # Disable foreign key checks
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        
        # Drop all tables
        tables = [
            'triggers', 'exhibits', 'assigns', 'participates',
            'responses', 'reports', 'reactions', 'assessments',
            'scenarios', 'questionnaires', 'persons', 'users', 'therapists'
        ]
        
        for table in tables:
            try:
                db.execute(text(f"DROP TABLE IF EXISTS {table}"))
            except:
                pass
        
        # Re-enable foreign key checks
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        db.commit()
        
        # Recreate tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database cleared and recreated")
    except Exception as e:
        print(f"Error clearing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Therapist variety
THERAPIST_DATA = [
    {"name": "Dr. Sarah Mitchell", "qualification": "PhD in Clinical Psychology", "specialization": "PTSD & Combat Trauma", "years": 15},
    {"name": "Dr. James Anderson", "qualification": "MD Psychiatry", "specialization": "Anxiety Disorders", "years": 12},
    {"name": "Dr. Emily Chen", "qualification": "PsyD Clinical Psychology", "specialization": "Trauma-Focused CBT", "years": 8},
    {"name": "Dr. Michael Roberts", "qualification": "PhD Neuropsychology", "specialization": "Combat Veterans", "years": 20},
    {"name": "Dr. Lisa Thompson", "qualification": "PhD Clinical Psychology", "specialization": "EMDR Therapy", "years": 10},
    {"name": "Dr. David Martinez", "qualification": "MD Psychiatry", "specialization": "Crisis Intervention", "years": 18},
    {"name": "Dr. Rachel Green", "qualification": "PsyD Counseling", "specialization": "Group Therapy", "years": 7},
    {"name": "Dr. Kevin Park", "qualification": "PhD Clinical Psychology", "specialization": "Substance Abuse & PTSD", "years": 14},
]

# Soldier variety
RANKS = ["Private", "Corporal", "Sergeant", "Staff Sergeant", "Lieutenant", "Captain", "Major"]
FIRST_NAMES = [
    "Ryan", "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Jamie",
    "Michael", "Sarah", "Chris", "Jessica", "David", "Emily", "James", "Ashley",
    "Daniel", "Samantha", "Matthew", "Amanda", "Joshua", "Jennifer", "Andrew", "Nicole"
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas"
]

def create_therapists(db: Session):
    """Create therapist accounts"""
    print("\n👨‍⚕️ Creating therapists...")
    therapists = []
    
    for i, data in enumerate(THERAPIST_DATA, 1):
        # Create therapist record
        therapist = models.Therapist(
            name=data["name"],
            qualification=data["qualification"],
            specialization=data["specialization"],
            years_of_experience=data["years"]
        )
        db.add(therapist)
        db.flush()
        
        # Create user account
        username = data["name"].lower().replace("dr. ", "").replace(" ", ".")
        user = models.User(
            username=username,
            password_hash=get_password_hash("therapist123"),
            role=models.UserRole.therapist,
            therapist_id=therapist.id,
            created_at=datetime.utcnow() - timedelta(days=random.randint(30, 365))
        )
        db.add(user)
        therapists.append(therapist)
        
        print(f"  ✓ {data['name']} ({data['specialization']})")
    
    db.commit()
    return therapists

def create_soldiers(db: Session, therapists, count=30):
    """Create soldier accounts with variety"""
    print(f"\n🪖 Creating {count} soldiers...")
    soldiers = []
    
    for i in range(count):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        rank = random.choice(RANKS)
        age = random.randint(22, 45)
        gender = random.choice(["Male", "Female"])
        service_years = random.randint(1, age - 20)
        therapist = random.choice(therapists)
        
        # Create person record
        person = models.Person(
            name=name,
            rank=rank,
            age=age,
            gender=gender,
            service_years=service_years,
            therapist_id=therapist.id
        )
        db.add(person)
        db.flush()
        
        # Create user account
        username = f"{first_name.lower()}.{last_name.lower()}{i}"
        user = models.User(
            username=username,
            password_hash=get_password_hash("soldier123"),
            role=models.UserRole.soldier,
            person_id=person.id,
            created_at=datetime.utcnow() - timedelta(days=random.randint(10, 200))
        )
        db.add(user)
        soldiers.append(person)
        
        if (i + 1) % 10 == 0:
            print(f"  ✓ Created {i + 1}/{count} soldiers")
    
    db.commit()
    print(f"  ✅ All {count} soldiers created")
    return soldiers

def load_questionnaires(db: Session):
    """Load 20 questionnaire questions"""
    print("\n📝 Loading questionnaire questions...")
    
    questions = [
        # Trauma Sensitivity (5 questions)
        {"text": "I feel overwhelmed when reminded of stressful situations.", "dimension": "trauma_sensitivity", "reverse": False},
        {"text": "Loud noises make me feel anxious or on edge.", "dimension": "trauma_sensitivity", "reverse": False},
        {"text": "I can handle unexpected changes calmly.", "dimension": "trauma_sensitivity", "reverse": True},
        {"text": "I avoid places that remind me of difficult experiences.", "dimension": "trauma_sensitivity", "reverse": False},
        {"text": "I recover quickly from stressful events.", "dimension": "trauma_sensitivity", "reverse": True},
        
        # Emotional Regulation (5 questions)
        {"text": "I can control my emotions when I'm upset.", "dimension": "emotional_regulation", "reverse": True},
        {"text": "I often feel irritable or angry without knowing why.", "dimension": "emotional_regulation", "reverse": False},
        {"text": "I can calm myself down when feeling anxious.", "dimension": "emotional_regulation", "reverse": True},
        {"text": "My emotions feel unpredictable.", "dimension": "emotional_regulation", "reverse": False},
        {"text": "I can stay composed in difficult situations.", "dimension": "emotional_regulation", "reverse": True},
        
        # Recovery Rate (5 questions)
        {"text": "I bounce back quickly from setbacks.", "dimension": "recovery_rate", "reverse": True},
        {"text": "It takes me a long time to feel normal after a stressful event.", "dimension": "recovery_rate", "reverse": False},
        {"text": "I adapt well to changes in my environment.", "dimension": "recovery_rate", "reverse": True},
        {"text": "I dwell on negative experiences for days.", "dimension": "recovery_rate", "reverse": False},
        {"text": "I can find positive aspects even in difficult situations.", "dimension": "recovery_rate", "reverse": True},
        
        # Impulsivity (5 questions)
        {"text": "I act without thinking about consequences.", "dimension": "impulsivity", "reverse": False},
        {"text": "I think carefully before making decisions.", "dimension": "impulsivity", "reverse": True},
        {"text": "I have trouble controlling my impulses.", "dimension": "impulsivity", "reverse": False},
        {"text": "I plan ahead for important tasks.", "dimension": "impulsivity", "reverse": True},
        {"text": "I often regret decisions I make quickly.", "dimension": "impulsivity", "reverse": False},
    ]
    
    standard_weights = {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0}
    reverse_weights = {"1": 1.0, "2": 0.75, "3": 0.5, "4": 0.25, "5": 0.0}
    
    for q in questions:
        questionnaire = models.Questionnaire(
            question_text=q["text"],
            dimension=models.DimensionType[q["dimension"]],
            question_type=models.QuestionType.likert_5,
            scoring_weights=reverse_weights if q["reverse"] else standard_weights,
            is_reverse_scored=q["reverse"],
            is_active=True
        )
        db.add(questionnaire)
    
    db.commit()
    print("  ✅ 20 questions loaded")

def generate_questionnaire_response(soldier_personality):
    """Generate realistic questionnaire responses based on personality"""
    # Personality affects response patterns
    base_trauma = soldier_personality["trauma_tendency"]
    base_emotional = soldier_personality["emotional_stability"]
    base_recovery = soldier_personality["resilience"]
    base_impulse = soldier_personality["impulsivity"]
    
    responses = []
    for i in range(20):
        # Add randomness to make it realistic
        if i < 5:  # Trauma sensitivity
            score = base_trauma + random.uniform(-0.2, 0.2)
        elif i < 10:  # Emotional regulation
            score = base_emotional + random.uniform(-0.2, 0.2)
        elif i < 15:  # Recovery rate
            score = base_recovery + random.uniform(-0.2, 0.2)
        else:  # Impulsivity
            score = base_impulse + random.uniform(-0.2, 0.2)
        
        # Clamp to 0-1
        score = max(0.0, min(1.0, score))
        
        # Convert to Likert (1-5)
        if score < 0.2:
            answer = "1"
        elif score < 0.4:
            answer = "2"
        elif score < 0.6:
            answer = "3"
        elif score < 0.8:
            answer = "4"
        else:
            answer = "5"
        
        responses.append({"answer": answer, "score": score})
    
    return responses

def create_assessment_for_soldier(db: Session, soldier, questionnaires):
    """Create assessment with automatic responses"""
    # Create personality profile for this soldier
    personality = {
        "trauma_tendency": random.uniform(0.2, 0.9),
        "emotional_stability": random.uniform(0.2, 0.9),
        "resilience": random.uniform(0.2, 0.9),
        "impulsivity": random.uniform(0.2, 0.9)
    }
    
    # Generate responses
    response_data = generate_questionnaire_response(personality)
    
    # Calculate dimension scores (average of 5 questions each)
    trauma_sensitivity = sum(r["score"] for r in response_data[0:5]) / 5
    emotional_regulation = sum(r["score"] for r in response_data[5:10]) / 5
    recovery_rate = sum(r["score"] for r in response_data[10:15]) / 5
    impulsivity = sum(r["score"] for r in response_data[15:20]) / 5
    
    # Determine coping mechanism
    if trauma_sensitivity > 0.7:
        coping = models.CopingMechanism.avoidance
    elif emotional_regulation < 0.4:
        coping = models.CopingMechanism.suppression
    elif recovery_rate > 0.6:
        coping = models.CopingMechanism.approach
    else:
        coping = models.CopingMechanism.freezing
    
    # Create assessment
    assessment = models.Assessment(
        person_id=soldier.id,
        assessment_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
        trauma_sensitivity=trauma_sensitivity,
        emotional_regulation=emotional_regulation,
        recovery_rate=recovery_rate,
        impulsivity=impulsivity,
        coping_mechanism=coping,
        therapist_id=soldier.therapist_id
    )
    db.add(assessment)
    db.flush()
    
    # Create responses
    for i, (q, r) in enumerate(zip(questionnaires, response_data)):
        response = models.Response(
            assessment_id=assessment.id,
            questionnaire_id=q.id,
            answer_value=r["answer"],
            answer_score=r["score"]
        )
        db.add(response)
    
    return assessment

def run_simulation_for_soldier(db: Session, soldier, assessment, scenario):
    """Run simulation and generate report"""
    # Create profile values dict
    profile_values = {
        "trauma_sensitivity": assessment.trauma_sensitivity,
        "emotional_regulation": assessment.emotional_regulation,
        "recovery_rate": assessment.recovery_rate,
        "impulsivity": assessment.impulsivity,
        "coping_mechanism": assessment.coping_mechanism.value
    }
    
    # Run Mesa simulation
    model = PTSDModel(
        width=10,
        height=10,
        soldier_rank=soldier.rank,
        soldier_years=soldier.service_years,
        num_triggers=scenario["triggers"],
        trigger_strength=10,
        profile_values=profile_values
    )
    
    # Execute simulation
    for _ in range(20):
        model.step()
    
    # Get final agent state
    final_stress = model.soldier.stress
    final_status = model.soldier.status
    
    # Determine PTSD symptoms based on final state
    if final_stress > 80:
        avoidance = "High" if random.random() > 0.3 else "Severe"
        re_experiencing = "Yes"
        negative_alterations = "High" if random.random() > 0.4 else "Moderate"
        hyperarousal = "Severe" if random.random() > 0.5 else "High"
    elif final_stress > 60:
        avoidance = "Moderate" if random.random() > 0.5 else "High"
        re_experiencing = "Yes" if random.random() > 0.4 else "No"
        negative_alterations = "Moderate"
        hyperarousal = "High" if random.random() > 0.6 else "Moderate"
    elif final_stress > 40:
        avoidance = "Low" if random.random() > 0.4 else "Moderate"
        re_experiencing = "No"
        negative_alterations = "Low" if random.random() > 0.5 else "Moderate"
        hyperarousal = "Moderate" if random.random() > 0.5 else "Low"
    else:
        avoidance = "Low"
        re_experiencing = "No"
        negative_alterations = "Low"
        hyperarousal = "Low"
    
    # Create reaction
    reaction_type = random.choice(list(REACTION_CATALOG.keys()))
    reaction = models.Reaction(
        r_type=reaction_type,
        physical_response=REACTION_CATALOG[reaction_type]["physical_response"],
        assessment_id=assessment.id
    )
    db.add(reaction)
    db.flush()
    
    # Create report
    report = models.Report(
        person_id=soldier.id,
        therapist_id=soldier.therapist_id,
        reaction_id=reaction.id,
        assessment_id=assessment.id,
        avoidance=avoidance,
        re_experiencing=re_experiencing,
        negative_alterations=negative_alterations,
        hyperarousal=hyperarousal
    )
    db.add(report)
    
    # Create junction table entries (only if not exists)
    # Check if participates already exists
    existing_participates = db.query(models.Participates).filter_by(
        person_id=soldier.id,
        scenario_id=scenario["db_id"]
    ).first()
    
    if not existing_participates:
        participates = models.Participates(person_id=soldier.id, scenario_id=scenario["db_id"])
        db.add(participates)
    
    exhibits = models.Exhibits(person_id=soldier.id, reaction_id=reaction.id)
    triggers = models.Triggers(scenario_id=scenario["db_id"], reaction_id=reaction.id)
    
    db.add(exhibits)
    db.add(triggers)
    
    return report

def main():
    print("=" * 60)
    print("🌱 COMPREHENSIVE DATABASE SEEDING")
    print("=" * 60)
    
    # Clear database
    clear_database()
    
    db = SessionLocal()
    
    try:
        # Create therapists
        therapists = create_therapists(db)
        
        # Create soldiers (30 by default)
        soldiers = create_soldiers(db, therapists, count=30)
        
        # Load questionnaires
        load_questionnaires(db)
        questionnaires = db.query(models.Questionnaire).all()
        
        # Load scenarios into DB first
        print("\n🎬 Creating scenarios...")
        scenario_records = []
        for scenario_data in SCENARIO_CATALOG:
            scenario = models.Scenario(
                scenario_type=scenario_data["scenario_type"],
                environment=scenario_data["environment"]
            )
            db.add(scenario)
            db.flush()
            scenario_records.append({
                "db_id": scenario.id,
                "name": scenario_data["scenario_type"],
                "description": scenario_data["description"],
                "triggers": scenario_data["num_triggers"]
            })
        db.commit()
        print(f"  ✅ {len(scenario_records)} scenarios created")
        
        # Create assessments and run simulations for each soldier
        print("\n🧪 Creating assessments and running simulations...")
        total_simulations = 0
        
        for i, soldier in enumerate(soldiers, 1):
            # Create 1-3 assessments per soldier
            num_assessments = random.randint(1, 3)
            
            for j in range(num_assessments):
                # Create assessment
                assessment = create_assessment_for_soldier(db, soldier, questionnaires)
                
                # Run 1-2 simulations per assessment
                num_simulations = random.randint(1, 2)
                for k in range(num_simulations):
                    scenario = random.choice(scenario_records)
                    report = run_simulation_for_soldier(db, soldier, assessment, scenario)
                    total_simulations += 1
            
            db.commit()
            
            if i % 5 == 0:
                print(f"  ✓ Processed {i}/{len(soldiers)} soldiers ({total_simulations} simulations so far)")
        
        db.commit()
        
        # Print summary
        print("\n" + "=" * 60)
        print("✅ DATABASE SEEDING COMPLETE!")
        print("=" * 60)
        print(f"👨‍⚕️ Therapists: {len(therapists)}")
        print(f"🪖 Soldiers: {len(soldiers)}")
        print(f"📝 Questions: {len(questionnaires)}")
        print(f"🎬 Scenarios: {len(scenario_records)}")
        print(f"📊 Assessments: {db.query(models.Assessment).count()}")
        print(f"🧪 Simulations: {total_simulations}")
        print(f"📄 Reports: {db.query(models.Report).count()}")
        print(f"💬 Responses: {db.query(models.Response).count()}")
        print(f"⚡ Reactions: {db.query(models.Reaction).count()}")
        print("=" * 60)
        print("\n🔑 Login Credentials:")
        print("  Therapists: username format: firstname.lastname (e.g., sarah.mitchell)")
        print("  Soldiers: username format: firstname.lastnameN (e.g., ryan.smith0)")
        print("  All passwords: therapist123 (therapists) / soldier123 (soldiers)")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
