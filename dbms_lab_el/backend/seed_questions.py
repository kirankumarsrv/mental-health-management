"""
Seed script to populate the questionnaires table with validated questions
Run this once after database setup:
  python -m backend.seed_questions
  OR
  python backend/seed_questions.py
"""
import os
import sys

# Ensure project root is on sys.path so absolute imports work
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.database import SessionLocal, engine
from backend import models

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Question data
QUESTIONS = [
    # TRAUMA SENSITIVITY (5 questions)
    {
        "question_text": "I often feel anxious when reminded of stressful past events.",
        "dimension": models.DimensionType.trauma_sensitivity,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": False
    },
    {
        "question_text": "Loud noises make me feel extremely uncomfortable or on edge.",
        "dimension": models.DimensionType.trauma_sensitivity,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": False
    },
    {
        "question_text": "I can easily separate current situations from past traumatic experiences.",
        "dimension": models.DimensionType.trauma_sensitivity,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": True  # Reverse scored (higher agreement = LOWER trauma sensitivity)
    },
    {
        "question_text": "I find myself constantly scanning my environment for potential threats.",
        "dimension": models.DimensionType.trauma_sensitivity,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": False
    },
    {
        "question_text": "Unexpected changes in routine cause me significant stress.",
        "dimension": models.DimensionType.trauma_sensitivity,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": False
    },
    
    # EMOTIONAL REGULATION (5 questions)
    {
        "question_text": "When I feel upset, I can calm myself down relatively quickly.",
        "dimension": models.DimensionType.emotional_regulation,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": True  # Higher agreement = BETTER regulation
    },
    {
        "question_text": "I often lose control of my emotions in stressful situations.",
        "dimension": models.DimensionType.emotional_regulation,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": False
    },
    {
        "question_text": "I can think clearly even when under significant pressure.",
        "dimension": models.DimensionType.emotional_regulation,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": True
    },
    {
        "question_text": "My emotions feel overwhelming and difficult to manage.",
        "dimension": models.DimensionType.emotional_regulation,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": False
    },
    {
        "question_text": "I use healthy strategies (breathing, mindfulness) to manage stress.",
        "dimension": models.DimensionType.emotional_regulation,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": True
    },
    
    # RECOVERY RATE (5 questions)
    {
        "question_text": "After a stressful event, it takes me days to feel normal again.",
        "dimension": models.DimensionType.recovery_rate,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": True  # Higher agreement = SLOWER recovery (we want lower scores)
    },
    {
        "question_text": "I bounce back quickly from difficult situations.",
        "dimension": models.DimensionType.recovery_rate,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": False  # Higher = faster recovery
    },
    {
        "question_text": "Negative experiences continue to affect me for a long time.",
        "dimension": models.DimensionType.recovery_rate,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": True
    },
    {
        "question_text": "I can shake off stress and move on with my day.",
        "dimension": models.DimensionType.recovery_rate,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": False
    },
    {
        "question_text": "I find it hard to stop thinking about stressful events.",
        "dimension": models.DimensionType.recovery_rate,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": True
    },
    
    # IMPULSIVITY (5 questions)
    {
        "question_text": "I often act without thinking, especially under pressure.",
        "dimension": models.DimensionType.impulsivity,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": False
    },
    {
        "question_text": "I carefully consider consequences before making decisions.",
        "dimension": models.DimensionType.impulsivity,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": True
    },
    {
        "question_text": "In stressful situations, I react immediately rather than pause.",
        "dimension": models.DimensionType.impulsivity,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": False
    },
    {
        "question_text": "I can control my urges even when feeling overwhelmed.",
        "dimension": models.DimensionType.impulsivity,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": True
    },
    {
        "question_text": "I frequently regret decisions I make during stressful moments.",
        "dimension": models.DimensionType.impulsivity,
        "question_type": models.QuestionType.likert_5,
        "scoring_weights": {"1": 0.0, "2": 0.25, "3": 0.5, "4": 0.75, "5": 1.0},
        "is_reverse_scored": False
    }
]

def seed_questions():
    """Seed the database with questionnaire questions"""
    db = SessionLocal()
    
    try:
        # Check if questions already exist
        existing_count = db.query(models.Questionnaire).count()
        if existing_count > 0:
            print(f"⚠️  Database already contains {existing_count} questions. Skipping seed.")
            print("   To re-seed, delete all questionnaires first.")
            return
        
        # Insert all questions
        print("🌱 Seeding questionnaires...")
        for idx, q_data in enumerate(QUESTIONS, 1):
            questionnaire = models.Questionnaire(**q_data)
            db.add(questionnaire)
            print(f"   [{idx}/20] Added: {q_data['dimension'].value} - {q_data['question_text'][:50]}...")
        
        db.commit()
        print(f"✅ Successfully seeded {len(QUESTIONS)} questions!")
        
        # Print summary
        print("\n📊 Summary by dimension:")
        for dimension in models.DimensionType:
            count = db.query(models.Questionnaire).filter(
                models.Questionnaire.dimension == dimension
            ).count()
            print(f"   {dimension.value}: {count} questions")
        
    except Exception as e:
        print(f"❌ Error seeding questions: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("  PTSD Assessment Questionnaire Seeder")
    print("=" * 60)
    seed_questions()
