"""
Test script showing psychological profiles for different soldiers
Demonstrates how the same scenario produces different outcomes
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import SessionLocal
from backend import models, crud
from backend.psychological_profile import PsychologicalProfile

db = SessionLocal()

# Get some soldiers from database
persons = crud.get_persons(db, limit=5)

print("=" * 80)
print("PSYCHOLOGICAL PROFILES - Same Scenario, Different Reactions")
print("=" * 80)

for person in persons:
    profile = PsychologicalProfile(person, randomize=True)
    print(profile)
    print()

print("=" * 80)
print("IMPACT COMPARISON")
print("=" * 80)

# Scenario: Same trigger stress for everyone
base_trigger_stress = 20

for person in persons:
    profile = PsychologicalProfile(person, randomize=True)
    
    # Without psychological modifiers (old system)
    old_resilience = min(5, person.service_years)
    old_stress = max(0, base_trigger_stress - old_resilience)
    
    # With psychological modifiers (new system)
    new_stress = profile.get_modified_stress_increment(base_trigger_stress)
    
    print(f"\n{person.name} ({person.rank}, {person.service_years} years)")
    print(f"  OLD system: +{old_stress:.1f} stress")
    print(f"  NEW system: +{new_stress:.1f} stress")
    print(f"  Difference: {new_stress - old_stress:+.1f}")
    print(f"  Coping: {profile.should_fight_or_flight()}")

db.close()
