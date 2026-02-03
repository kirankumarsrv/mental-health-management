import sys
from pathlib import Path
# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import SessionLocal, engine, Base
from backend import models, presets

# Ensure tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed():
    # check if data exists
    if db.query(models.Therapist).first():
        print("Data already exists.")
        return

    print("Seeding data...")

    # 1. Therapist
    t1 = models.Therapist(name="Dr. Sarah Connor", qualification="PhD Clinical Psychology", specialization="Trauma", years_of_experience=15)
    db.add(t1)
    db.commit()
    db.refresh(t1)

    # 2. Persons (Soldiers)
    # Rookie
    p1 = models.Person(name="Pvt. Ryan", rank="Private", age=22, gender="Male", service_years=1, therapist_id=t1.id)
    # Veteran
    p2 = models.Person(name="Sgt. Miller", rank="Sergeant", age=35, gender="Male", service_years=12, therapist_id=t1.id)
    # Average
    p3 = models.Person(name="Cpl. Ripley", rank="Corporal", age=28, gender="Female", service_years=5, therapist_id=t1.id)

    db.add_all([p1, p2, p3])
    db.commit()

    # 3. Scenarios (predefined catalog)
    scenario_models = []
    for preset in presets.SCENARIO_CATALOG:
        scenario_models.append(
            models.Scenario(
                scenario_type=preset["scenario_type"],
                environment=preset["environment"],
                assigned_date=None,
            )
        )

    db.add_all(scenario_models)
    db.commit()

    print("Seeding complete!")

if __name__ == "__main__":
    seed()
    db.close()
