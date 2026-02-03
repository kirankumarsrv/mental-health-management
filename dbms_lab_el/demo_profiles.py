"""
Demonstration of Psychological Profiles
Shows how the same soldier reacts differently with the new system
"""

# Mock person object for testing
class MockPerson:
    def __init__(self, name, rank, age, gender, service_years):
        self.name = name
        self.rank = rank
        self.age = age
        self.gender = gender
        self.service_years = service_years

from backend.psychological_profile import PsychologicalProfile

# Create diverse soldiers
soldiers = [
    MockPerson("Pvt. Ryan", "Private", 22, "Male", 1),
    MockPerson("Cpl. Ripley", "Corporal", 28, "Female", 5),
    MockPerson("Sgt. Miller", "Sergeant", 35, "Male", 12),
]

print("=" * 100)
print("PSYCHOLOGICAL PROFILES - How Same Triggers Affect Different Soldiers")
print("=" * 100)
print()

for soldier in soldiers:
    profile = PsychologicalProfile(soldier, randomize=True)
    print(profile)
    print()

print("=" * 100)
print("STRESS RESPONSE COMPARISON")
print("=" * 100)
print()

# Simulate exposure to same trigger stress
trigger_stress = 20  # 2 triggers of strength 10 each

for soldier in soldiers:
    profile = PsychologicalProfile(soldier, randomize=False)  # No randomness for clarity
    
    modified_stress = profile.get_modified_stress_increment(trigger_stress)
    recovery = profile.get_recovery_amount()
    thresholds = profile.get_stress_thresholds()
    coping = profile.should_fight_or_flight()
    
    print(f"\n{soldier.name} ({soldier.rank}, {soldier.service_years} years, Age {soldier.age})")
    print("-" * 100)
    print(f"  Trauma Sensitivity:      {profile.trauma_sensitivity:.2f}")
    print(f"  Emotional Regulation:    {profile.emotional_regulation:.2f}")
    print(f"  Recovery Rate:           {profile.recovery_rate:.2f}")
    print(f"  ──────────────────────────────────────")
    print(f"  Trigger Stress (Raw):    +{trigger_stress} points")
    print(f"  Trigger Stress (Modified): +{modified_stress:.1f} points")
    print(f"  Recovery per step (safe): -{recovery:.2f} points")
    print(f"  ──────────────────────────────────────")
    print(f"  Calm Threshold:          {thresholds['calm_threshold']:.0f} stress")
    print(f"  Alert Threshold:         {thresholds['alert_threshold']:.0f} stress")
    print(f"  Coping Mechanism:        {coping}")
    print(f"  ──────────────────────────────────────")
    
    # Estimate steps to panic
    stress = 0
    steps = 0
    while stress < thresholds['alert_threshold'] and steps < 100:
        stress += modified_stress
        if stress > 0 and steps > 5:  # After 5 steps, exposure ends
            stress -= recovery
        steps += 1
    
    print(f"  Steps to PANIC:          ~{steps} steps")

print("\n" + "=" * 100)
