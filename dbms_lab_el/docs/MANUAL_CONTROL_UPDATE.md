# Manual Control Update - Psychological Profiles

## What Changed

**OLD SYSTEM**: Psychological profiles were auto-generated from person attributes (age, gender, rank, service_years)

**NEW SYSTEM**: You control all psychological profile values via UI sliders!

## UI Controls

The simulation page now has **5 sliders** to control soldier psychology:

### 1. **Trauma Sensitivity** (0.0 - 1.0)
- **Low (0.0)**: Very resistant to stress, gains little stress from triggers
- **High (1.0)**: Highly sensitive, gains a lot of stress from triggers
- **Default**: 0.5

### 2. **Emotional Regulation** (0.0 - 1.0)
- **Low (0.0)**: Poor emotional control, stress affects them more
- **High (1.0)**: Excellent control, can reduce stress impact
- **Default**: 0.5

### 3. **Recovery Rate** (0.0 - 1.0)
- **Low (0.0)**: Very slow recovery when away from triggers
- **High (1.0)**: Fast recovery, stress decreases quickly
- **Default**: 0.5

### 4. **Impulsivity** (0.0 - 1.0)
- **Low (0.0)**: Deliberate, thoughtful decision-making
- **High (1.0)**: Impulsive, reacts without thinking
- **Default**: 0.5

### 5. **Coping Mechanism** (Dropdown)
- **Avoidance**: Runs away from triggers when panicked
- **Approach**: Moves toward triggers (face the threat)
- **Freezing**: Becomes paralyzed, doesn't move
- **Suppression**: Ignores fear, moves randomly
- **Default**: Avoidance

## How It Works

### Frontend (SimulationRunner.jsx)
```javascript
// State for sliders
const [traumaSensitivity, setTraumaSensitivity] = useState(0.5);
const [emotionalRegulation, setEmotionalRegulation] = useState(0.5);
const [recoveryRate, setRecoveryRate] = useState(0.5);
const [impulsivity, setImpulsivity] = useState(0.5);
const [copingMechanism, setCopingMechanism] = useState("avoidance");

// Send to backend
await api.post('/simulations/', {
    person_id: selectedPerson,
    scenario_id: selectedScenario,
    trauma_sensitivity: traumaSensitivity,
    emotional_regulation: emotionalRegulation,
    recovery_rate: recoveryRate,
    impulsivity: impulsivity,
    coping_mechanism: copingMechanism
});
```

### Backend (routers/simulation.py)
```python
# Extract profile values from request
profile_values = {
    "trauma_sensitivity": sim_request.trauma_sensitivity,
    "emotional_regulation": sim_request.emotional_regulation,
    "recovery_rate": sim_request.recovery_rate,
    "impulsivity": sim_request.impulsivity,
    "coping_mechanism": sim_request.coping_mechanism
}

# Pass to Mesa model
model = PTSDModel(..., profile_values=profile_values)
```

### Mesa Model (mesa_model.py)
```python
# Create soldier with manual profile
self.soldier = SoldierAgent(..., profile_values=profile_values)

# In SoldierAgent
if profile_values:
    self.psychological_profile = PsychologicalProfile(**profile_values)
```

### Psychological Profile (psychological_profile.py)
```python
def __init__(self, trauma_sensitivity=0.5, emotional_regulation=0.5, 
             recovery_rate=0.5, impulsivity=0.5, coping_mechanism="avoidance"):
    # Use values directly from sliders (no auto-generation)
    self.trauma_sensitivity = trauma_sensitivity
    self.emotional_regulation = emotional_regulation
    self.recovery_rate = recovery_rate
    self.impulsivity = impulsivity
    self.coping_mechanism = coping_mechanism
```

## Impact on Simulation

### Stress Calculation
```python
# Base stress from triggers
base_stress = num_triggers * 10

# Modified by trauma sensitivity
modified = base_stress * (0.5 + trauma_sensitivity)

# Reduced by emotional regulation
reduction = emotional_regulation * base_stress * 0.2

# Final stress added
stress_increase = modified - reduction
```

**Example**:
- **Slider values**: trauma_sensitivity=0.8, emotional_regulation=0.3
- **Base stress**: 20 (2 triggers × 10)
- **Modified**: 20 × (0.5 + 0.8) = 26
- **Reduction**: 0.3 × 20 × 0.2 = 1.2
- **Final**: 26 - 1.2 = **24.8 stress gain**

vs.

- **Slider values**: trauma_sensitivity=0.2, emotional_regulation=0.8
- **Base stress**: 20 (2 triggers × 10)
- **Modified**: 20 × (0.5 + 0.2) = 14
- **Reduction**: 0.8 × 20 × 0.2 = 3.2
- **Final**: 14 - 3.2 = **10.8 stress gain**

### Recovery Calculation
```python
recovery = 2 * (0.5 + recovery_rate)
```

**Examples**:
- recovery_rate=0.1 → recovery = 2 × 0.6 = **1.2 stress/step**
- recovery_rate=0.9 → recovery = 2 × 1.4 = **2.8 stress/step**

### Stress Thresholds
```python
calm_threshold = 50 * (1 + (1 - emotional_regulation) * 0.4)
alert_threshold = 80 * (1 + (1 - emotional_regulation) * 0.3)
```

**Examples**:
- emotional_regulation=0.2 → calm=66, alert=99 (panics late)
- emotional_regulation=0.8 → calm=54, alert=85 (panics early)

### Behavior (Panic State)
- **Avoidance**: `self.avoid(triggers)` - Runs away
- **Approach**: `self.move_towards(triggers)` - Faces threat
- **Freezing**: No movement
- **Suppression**: `self.move()` - Acts normal

## Testing Different Profiles

### Profile 1: Resilient Veteran
```
trauma_sensitivity: 0.2
emotional_regulation: 0.9
recovery_rate: 0.8
impulsivity: 0.2
coping_mechanism: approach
```
**Expected**: Gains stress slowly, recovers fast, stays calm, faces threats

### Profile 2: Vulnerable Recruit
```
trauma_sensitivity: 0.9
emotional_regulation: 0.2
recovery_rate: 0.2
impulsivity: 0.8
coping_mechanism: avoidance
```
**Expected**: Gains stress quickly, recovers slowly, panics early, runs away

### Profile 3: Frozen Soldier
```
trauma_sensitivity: 0.7
emotional_regulation: 0.4
recovery_rate: 0.5
impulsivity: 0.3
coping_mechanism: freezing
```
**Expected**: Moderate stress gain, becomes paralyzed when panicked

## Summary

✅ **No auto-generation** - All values set by you via sliders  
✅ **Full control** - Experiment with different psychological profiles  
✅ **Same scenario, different outcomes** - Test how profiles affect behavior  
✅ **Real-time feedback** - See stress changes in grid visualization  
✅ **Database schema unchanged** - Profile values sent in API request, not stored

**Ready to experiment!** Run the simulation with different slider configurations to see how psychological traits affect PTSD responses.
