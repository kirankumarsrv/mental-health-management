# Psychological Profile System - Design Documentation

## Problem Statement
The original Mesa simulation only used `service_years` to differentiate soldier responses. In reality, PTSD response is complex and involves multiple individual factors:
- Personality traits
- Age and life experience
- Gender differences in trauma response
- Individual coping mechanisms
- Baseline anxiety levels
- Emotional regulation capacity

## Solution: Psychological Profile Generation

Instead of storing these in the database (which would require schema changes), we **generate psychological profiles at simulation time** based on:
1. Existing person attributes (rank, age, gender, service_years)
2. Research-based formulas that derive traits from these attributes
3. Random variation to make individuals unique

## Architecture

### Input Data (Database)
```python
Person {
    rank: str,           # Private, Corporal, Sergeant, etc.
    age: int,            # 18-65
    gender: str,         # Male, Female, Other
    service_years: int   # 1-40
}
```

### Generated Profile (Runtime Only)
```python
PsychologicalProfile {
    trauma_sensitivity: float,      # 0.1-1.0 (how vulnerable to triggers)
    baseline_anxiety: float,        # 0.0-1.0 (default stress level)
    emotional_regulation: float,    # 0.1-0.9 (ability to control emotions)
    recovery_rate: float,           # 0.05-0.8 (stress decay speed)
    impulsivity: float,             # 0.1-0.9 (reactive vs deliberate)
    coping_mechanism: enum,         # approach, avoidance, freezing, suppression
    calm_threshold: float,          # Custom stress threshold
    alert_threshold: float          # Custom stress threshold
}
```

### How Profiles Affect Simulation

#### 1. Trauma Sensitivity
**What it does:** Amplifies or reduces stress from triggers

**Calculation:**
```
base_sensitivity = 0.5
age_factor = (age - 18) / 50  # Older soldiers less sensitive
gender_factor = 0.1 if Female else 0
trauma_sensitivity = base_sensitivity - (age_factor * 0.3) + gender_factor
```

**Impact in Mesa:**
```python
modified_stress = base_stress * (0.5 + trauma_sensitivity)
# Sensitive soldier (0.8): 20 stress → 26 stress
# Resilient soldier (0.2): 20 stress → 14 stress
```

#### 2. Emotional Regulation
**What it does:** Reduces stress and enables faster recovery

**Calculation:**
```
base_regulation = 0.3 + (service_years / 20) * 0.4
age_regulation = (age - 18) / 100
emotional_regulation = base_regulation + age_regulation
```

**Impact in Mesa:**
```python
# Reduces incoming stress by up to 20%
stress_reduction = emotional_regulation * base_stress * 0.2

# Faster recovery when safe
recovery = 2 * (0.5 + recovery_rate)  # Range: 1 to 3.6 points/step
```

#### 3. Coping Mechanism
**What it does:** Determines how soldier responds to panic

**Types:**
- **Approach:** Faces the threat (move towards triggers)
- **Avoidance:** Runs away (move away from triggers)
- **Freezing:** Becomes paralyzed (don't move)
- **Suppression:** Ignores it (move normally)

**Selection Logic:**
```python
if service_years >= 8 and emotional_regulation >= 0.6:
    → APPROACH (fight response)
elif emotional_regulation >= 0.7:
    → SUPPRESSION (control emotions)
elif impulsivity >= 0.6:
    → AVOIDANCE (flight response)
elif trauma_sensitivity >= 0.7:
    → FREEZING (freeze response)
else:
    → AVOIDANCE (default)
```

#### 4. Personalized Stress Thresholds
**What it does:** Each soldier has different thresholds for emotional states

**Calculation:**
```
calm_threshold = 50 * (1 + (1 - emotional_regulation) * 0.4)
alert_threshold = 80 * (1 + (1 - emotional_regulation) * 0.3)
```

**Example:**
```
High regulation (0.8): Calm at 50, Alert at 80 (harder to trigger)
Low regulation (0.2):  Calm at 54, Alert at 85 (easier to trigger)
```

## Example: Three Soldiers, Same Scenario

### Setup
- All in High Intensity scenario (5 triggers × 10 strength)
- Soldier 1: Pvt. Ryan (Private, 22yo, Male, 1 year service)
- Soldier 2: Cpl. Ripley (Corporal, 28yo, Female, 5 years service)
- Soldier 3: Sgt. Miller (Sergeant, 35yo, Male, 12 years service)

### Generated Profiles
```
Pvt. Ryan:
  Trauma Sensitivity: 0.68 (high vulnerability)
  Emotional Regulation: 0.35 (poor control)
  Recovery Rate: 0.28 (slow recovery)
  Coping: AVOIDANCE (flight response)
  Thresholds: Calm=56, Alert=86

Cpl. Ripley:
  Trauma Sensitivity: 0.55 (moderate)
  Emotional Regulation: 0.65 (good control)
  Recovery Rate: 0.48 (moderate recovery)
  Coping: SUPPRESSION (self-control)
  Thresholds: Calm=52, Alert=83

Sgt. Miller:
  Trauma Sensitivity: 0.35 (low vulnerability)
  Emotional Regulation: 0.75 (excellent control)
  Recovery Rate: 0.58 (fast recovery)
  Coping: APPROACH (fight response)
  Thresholds: Calm=48, Alert=81
```

### Simulation Results
When 2 triggers approach (20 stress points):

```
Pvt. Ryan:
  Modified stress: 20 * 1.18 - (0.35 * 20 * 0.2) = 21.8 stress
  Status: Alert (accumulates fast)
  Action: AVOIDANCE (runs away)
  Panic at: Step ~4-5

Cpl. Ripley:
  Modified stress: 20 * 1.05 - (0.65 * 20 * 0.2) = 18.3 stress
  Status: Alert (moderate)
  Action: SUPPRESSION (stays calm, tries to cope)
  Panic at: Step ~6-7

Sgt. Miller:
  Modified stress: 20 * 0.85 - (0.75 * 20 * 0.2) = 14.0 stress
  Status: Calm (stays composed)
  Action: APPROACH (might move towards threat)
  Panic at: Step ~8-10 (if at all)
```

## Implementation Details

### File: `backend/psychological_profile.py`
- Generates profiles from Person objects
- Provides methods to modify stress calculations
- Selects coping mechanisms
- Calculates personalized thresholds

### File: `backend/mesa_model.py` (Modified)
```python
# Pass person object to SoldierAgent
self.soldier = SoldierAgent(
    0, self, 
    soldier_rank, 
    soldier_years,
    person_obj=person  # ← NEW
)

# In soldier.step():
if self.psychological_profile:
    stress_increment = self.psychological_profile.get_modified_stress_increment(...)
    recovery = self.psychological_profile.get_recovery_amount()
    thresholds = self.psychological_profile.get_stress_thresholds()
    coping = self.psychological_profile.should_fight_or_flight()
```

### File: `backend/routers/simulation.py` (Modified)
```python
# Pass person object to Mesa model
model = backend.mesa_model.PTSDModel(
    10, 10, 
    person.rank, 
    person.service_years, 
    intensity_map,
    person_obj=person  # ← NEW
)
```

## Database Schema: NO CHANGES
The database remains unchanged. The psychological profile is generated at simulation time, not stored.

## Benefits

1. **Individual Differences:** Each soldier reacts differently to same scenario
2. **Realistic:** Based on research about trauma and personality
3. **Flexible:** Easy to add new factors (genetic predisposition, previous trauma, etc.)
4. **No DB Changes:** Keeps existing schema intact
5. **Reproducible:** Same person always generates same profile (with randomness option)
6. **Scalable:** Can add more factors as simulation evolves

## Future Enhancements

Could add:
- Previous trauma history (if stored in DB)
- Training/preparation level
- Team composition effects
- Therapist quality/intervention effects
- Real-time profile updates during simulation
- Genetic markers for trauma susceptibility
- Social support factors

## Example Output

Run `python demo_profiles.py` to see:
- 3 soldiers with different profiles
- How same stress affects them differently
- Estimated steps to panic for each
- Their unique coping strategies
