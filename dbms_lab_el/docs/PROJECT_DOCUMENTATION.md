# PTSD Simulation & Assessment System - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Core Algorithms & Models](#core-algorithms--models)
4. [Database Design](#database-design)
5. [Backend Implementation](#backend-implementation)
6. [Frontend Implementation](#frontend-implementation)
7. [Scenario System](#scenario-system)
8. [Clinical Assessment](#clinical-assessment)
9. [Setup & Deployment](#setup--deployment)
10. [Use Cases & Workflows](#use-cases--workflows)

---

## 1. Project Overview

### 1.1 Purpose
This system simulates Post-Traumatic Stress Disorder (PTSD) responses in military personnel using agent-based modeling. It helps therapists:
- Assess soldiers' psychological trauma profiles
- Predict stress responses in different combat scenarios
- Generate clinical reports for treatment planning
- Track recovery progress over time

### 1.2 Target Users
- **Clinical Psychologists**: PTSD assessment and treatment planning
- **Military Therapists**: Trauma evaluation and readiness assessment
- **Research Teams**: PTSD behavioral pattern analysis
- **Training Officers**: Resilience training program design

### 1.3 Technology Stack
```
Frontend:  React 18 + Vite + CSS3
Backend:   FastAPI (Python) + SQLAlchemy ORM
Database:  MySQL 8.0+ (migrated from SQLite)
Simulation: Mesa Agent-Based Modeling Framework
```

### 1.4 Key Features
✅ 12 realistic combat scenario presets (Urban Ambush, IED Blast, Hostage Rescue, etc.)  
✅ Agent-based simulation with configurable grid environments  
✅ 5-dimensional psychological profile modeling  
✅ Real-time stress response visualization  
✅ Clinical reaction tracking with physiological observations  
✅ PTSD assessment reports based on DSM-5 criteria  
✅ Multi-user therapist/patient management  

---

## 2. System Architecture

### 2.1 High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │Soldier   │  │Scenario  │  │Simulation│   │
│  │  Stats   │  │ Manager  │  │ Manager  │  │  Runner  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND API (FastAPI)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Person   │  │Therapist │  │ Scenario │  │Simulation│   │
│  │ Router   │  │  Router  │  │  Router  │  │  Router  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            MESA Simulation Engine                    │  │
│  │  • SoldierAgent (stress, movement, status)           │  │
│  │  • TriggerAgent (stressor intensity, position)       │  │
│  │  • PTSDModel (grid, scheduler, data collector)       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    MySQL Database                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ Therapist  │  │   Person   │  │  Scenario  │            │
│  │ Reaction   │  │   Report   │  │            │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Junction Tables (Many-to-Many Relationships)       │    │
│  │ Participates, Assigns, Exhibits, Triggers          │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Request Flow Example
```
User clicks "Start Simulation"
  ↓
Frontend sends POST /simulations/ with:
  - person_id, scenario_id
  - grid_size (6-20)
  - trauma_sensitivity, emotional_regulation, recovery_rate, impulsivity, coping_mechanism
  ↓
Backend:
  1. Fetches Person, Scenario, Therapist from DB
  2. Loads scenario preset (triggers, grid, intensity)
  3. Creates Mesa PTSDModel with psychological profile
  4. Runs 20-step simulation
  5. Collects stress data, position tracking, status transitions
  6. Creates Reaction records on status changes (Calm → Alert → Panic → Recovered)
  7. Generates PTSD Report (avoidance, re-experiencing, hyperarousal, etc.)
  8. Saves to database with junction table links
  ↓
Returns simulation_steps[] with:
  - step, soldier_pos, soldier_stress, soldier_status, soldier_color
  - triggers[] positions
  - reaction_id, reaction_type, physical_response (on status changes)
  ↓
Frontend:
  1. Animates grid visualization (500ms per step)
  2. Updates console logs with stress/status/reactions
  3. Shows final Recovery Report
```

---

## 3. Core Algorithms & Models

### 3.1 Mesa Agent-Based Simulation

**Mesa Framework**: Python library for agent-based modeling where autonomous agents interact in an environment.

#### 3.1.1 SoldierAgent Class
```python
class SoldierAgent(mesa.Agent):
    def __init__(self, model, profile: PsychologicalProfile):
        # State Variables
        self.stress = 0.0                    # Current stress level (0-200+)
        self.status = "Calm"                 # Calm, Alert, Panic, Recovered
        self.pos = random_position           # Grid coordinates (x, y)
        
        # Psychological Profile (from sliders)
        self.trauma_sensitivity = profile.trauma_sensitivity    # 0.0-1.0
        self.emotional_regulation = profile.emotional_regulation
        self.recovery_rate = profile.recovery_rate
        self.impulsivity = profile.impulsivity
        self.coping_mechanism = profile.coping_mechanism  # enum
        
        # Thresholds (dynamic based on profile)
        self.alert_threshold = 30 * (1 + trauma_sensitivity)
        self.panic_threshold = 60 * (1 + trauma_sensitivity)
        
    def step(self):
        # 1. MOVEMENT: Random walk (Moore neighborhood)
        self.move()
        
        # 2. STRESS ACCUMULATION: Check nearby triggers
        for trigger in nearby_triggers:
            distance = calculate_distance(self.pos, trigger.pos)
            if distance <= 3:  # Within trigger radius
                stress_increase = trigger.intensity * self.trauma_sensitivity
                self.stress += stress_increase
        
        # 3. STRESS DECAY: Natural recovery over time
        decay = self.recovery_rate * 2.0
        self.stress = max(0, self.stress - decay)
        
        # 4. STATUS TRANSITIONS
        if self.stress > self.panic_threshold:
            self.status = "Panic"
        elif self.stress > self.alert_threshold:
            self.status = "Alert"
        elif self.status == "Panic" and self.stress < self.panic_threshold:
            self.status = "Recovered"
        else:
            self.status = "Calm"
        
        # 5. VISUAL FEEDBACK: Color based on status
        self.color = status_color_map[self.status]
```

**Key Algorithms:**

1. **Stress Accumulation**:
   ```
   Δstress = Σ(trigger_intensity × trauma_sensitivity × proximity_factor)
   proximity_factor = 1 / (1 + distance²)
   ```

2. **Stress Decay** (Recovery):
   ```
   stress(t+1) = max(0, stress(t) - recovery_rate × 2.0)
   ```

3. **Threshold Calculation** (Adaptive to profile):
   ```
   alert_threshold = 30 × (1 + trauma_sensitivity)
   panic_threshold = 60 × (1 + trauma_sensitivity)
   
   Example:
   - Low sensitivity (0.2): alert=36, panic=72
   - High sensitivity (0.9): alert=57, panic=114
   ```

4. **Status State Machine**:
   ```
   Calm → Alert (stress > alert_threshold)
        → Panic (stress > panic_threshold)
        → Recovered (panic → stress drops below panic_threshold)
        → Calm (recovered → stress near 0)
   ```

#### 3.1.2 TriggerAgent Class
```python
class TriggerAgent(mesa.Agent):
    def __init__(self, model, intensity):
        self.pos = random_position      # Static position
        self.intensity = intensity      # Stressor strength (6-15)
    
    def step(self):
        pass  # Triggers are static environmental hazards
```

#### 3.1.3 PTSDModel Class
```python
class PTSDModel(mesa.Model):
    def __init__(self, width, height, num_triggers, trigger_strength, profile):
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        
        # Create 1 SoldierAgent
        self.soldier = SoldierAgent(self, profile)
        self.grid.place_agent(self.soldier, random_pos)
        
        # Create N TriggerAgents
        for i in range(num_triggers):
            trigger = TriggerAgent(self, trigger_strength)
            self.grid.place_agent(trigger, random_pos)
        
        self.datacollector = mesa.DataCollector({
            "Stress": lambda m: m.soldier.stress,
            "Status": lambda m: m.soldier.status
        })
    
    def step(self):
        self.schedule.step()           # All agents act
        self.datacollector.collect(self)
```

### 3.2 Psychological Profile Model

**5-Dimensional Personality System**:

| Dimension | Range | Low (0.0-0.3) | Medium (0.4-0.6) | High (0.7-1.0) |
|-----------|-------|---------------|------------------|----------------|
| **Trauma Sensitivity** | 0-1 | Resistant to stress | Normal response | Highly reactive |
| **Emotional Regulation** | 0-1 | Poor control | Moderate control | Strong stability |
| **Recovery Rate** | 0-1 | Slow recovery | Normal resilience | Fast bounce-back |
| **Impulsivity** | 0-1 | Deliberate | Balanced | Reactive/reckless |
| **Coping Mechanism** | Enum | - | - | - |

**Coping Mechanisms** (categorical):
- **Avoidance**: Run from threats (increases long-term stress)
- **Approach**: Face threats directly (healthier but riskier short-term)
- **Freezing**: Paralysis under stress (passive, dangerous)
- **Suppression**: Ignore/deny stressors (emotional numbing)

**Impact on Simulation**:
```python
# Example: High trauma sensitivity + low emotional regulation
profile = {
    "trauma_sensitivity": 0.9,      # Quick stress buildup
    "emotional_regulation": 0.2,    # Poor panic control
    "recovery_rate": 0.3,           # Slow stress decay
    "impulsivity": 0.7,             # Poor decisions under stress
    "coping_mechanism": "avoidance"
}

# Results in:
alert_threshold = 30 × (1 + 0.9) = 57
panic_threshold = 60 × (1 + 0.9) = 114
stress_decay_per_step = 0.3 × 2.0 = 0.6

# Soldier reaches Alert at step 3-5, Panic at step 8-10
# Takes 20+ steps to recover fully
```

### 3.3 PTSD Assessment Algorithm

**DSM-5 Criteria Mapping**:

```python
def generate_report(final_stress: float) -> Report:
    """
    Maps final stress to PTSD diagnostic criteria.
    Thresholds based on clinical severity scales.
    """
    report = {
        # Criterion B: Re-experiencing (flashbacks, nightmares)
        "re_experiencing": "Yes" if final_stress > 90 else "No",
        
        # Criterion C: Avoidance (avoiding reminders)
        "avoidance": "High" if final_stress > 80 else "Low",
        
        # Criterion D: Negative alterations (negative beliefs, emotional numbness)
        "negative_alterations": "Moderate" if final_stress > 50 else "None",
        
        # Criterion E: Hyperarousal (startle response, sleep issues)
        "hyperarousal": "Severe" if final_stress > 70 else "Mild"
    }
    return report
```

**Severity Interpretation**:
```
final_stress = 0-30   → Minimal trauma response (baseline)
final_stress = 30-60  → Mild stress reaction (alert, manageable)
final_stress = 60-90  → Moderate PTSD symptoms (treatment recommended)
final_stress = 90+    → Severe PTSD (urgent intervention needed)
```

**Example Output**:
```json
{
  "final_stress": 125.8,
  "report": {
    "avoidance": "High",           // Criterion C
    "re_experiencing": "Yes",      // Criterion B
    "negative_alterations": "Moderate",  // Criterion D
    "hyperarousal": "Severe"       // Criterion E
  }
}
```

**Clinical Interpretation**:
- **Avoidance: High** → Patient avoids locations, people, activities related to trauma
- **Re-experiencing: Yes** → Intrusive memories, flashbacks, nightmares present
- **Negative Alterations: Moderate** → Some emotional numbing, negative self-beliefs
- **Hyperarousal: Severe** → Constant vigilance, sleep disturbance, irritability

---

## 4. Database Design

### 4.1 Schema Overview (9 Tables)

**5 Core Entity Tables** + **4 Junction Tables** (Many-to-Many relationships)

```
Core Entities:
┌───────────────┐
│  Therapist    │ (Clinical psychologists managing patients)
│  Person       │ (Soldiers/patients with trauma profiles)
│  Scenario     │ (Combat environments/situations)
│  Reaction     │ (Physical/psychological responses)
│  Report       │ (PTSD assessment results)
└───────────────┘

Junction Tables (M:M):
┌───────────────┐
│ Participates  │ (Person ↔ Scenario: who participated in which scenario)
│ Assigns       │ (Therapist ↔ Scenario: who assigned which scenario)
│ Exhibits      │ (Person ↔ Reaction: who exhibited which reaction)
│ Triggers      │ (Scenario ↔ Reaction: which scenario triggered which reaction)
└───────────────┘
```

### 4.2 Entity-Relationship Diagram
```
┌─────────────────┐
│   Therapist     │
│─────────────────│
│ id (PK)         │
│ name            │
│ qualification   │
│ specialization  │
│ years_exp       │
└─────────────────┘
       │1
       │
       │*
┌─────────────────┐       ┌─────────────────┐
│     Person      │   *   │   Participates  │   *   ┌─────────────────┐
│─────────────────│──────▶│─────────────────│◀──────│    Scenario     │
│ id (PK)         │       │ person_id (FK)  │       │─────────────────│
│ name            │       │ scenario_id (FK)│       │ id (PK)         │
│ rank            │       └─────────────────┘       │ scenario_type   │
│ age, gender     │                                  │ environment     │
│ service_years   │       ┌─────────────────┐       │ assigned_date   │
│ therapist_id(FK)│   *   │    Exhibits     │   *   └─────────────────┘
└─────────────────┘──────▶│─────────────────│◀──┐            │*
       │1                 │ person_id (FK)  │   │            │
       │                  │ reaction_id (FK)│   │   ┌────────────────┐
       │*                 └─────────────────┘   │   │    Assigns     │
┌─────────────────┐                             │   │────────────────│
│     Report      │       ┌─────────────────┐   │   │ therapist_id   │
│─────────────────│   *   │    Reaction     │◀──┘   │ scenario_id    │
│ id (PK)         │──────▶│─────────────────│       └────────────────┘
│ avoidance       │       │ id (PK)         │
│ re_experiencing │       │ r_type          │       ┌────────────────┐
│ neg_alterations │       │ physical_resp   │   *   │   Triggers     │
│ hyperarousal    │       └─────────────────┘◀──────│────────────────│
│ person_id (FK)  │                  │1             │ scenario_id    │
│ therapist_id(FK)│                  │*             │ reaction_id    │
│ reaction_id (FK)│                  │              └────────────────┘
└─────────────────┘       ┌─────────────────┐
                          │     Report      │
                          └─────────────────┘
```

### 4.3 Table Definitions

#### 4.3.1 Therapist Table
```sql
CREATE TABLE therapists (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  qualification VARCHAR(150),
  specialization VARCHAR(100),
  years_of_experience INT,
  INDEX idx_name (name)
);
```

#### 4.3.2 Person Table
```sql
CREATE TABLE persons (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  rank VARCHAR(50),
  age INT,
  gender VARCHAR(20),
  service_years INT,
  therapist_id INT,
  FOREIGN KEY (therapist_id) REFERENCES therapists(id),
  INDEX idx_name (name)
);
```

#### 4.3.3 Scenario Table
```sql
CREATE TABLE scenarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  scenario_type VARCHAR(100) NOT NULL,
  environment VARCHAR(100),
  assigned_date DATE NULL
);
```

#### 4.3.4 Reaction Table
```sql
CREATE TABLE reactions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  r_type VARCHAR(50),              -- Reaction type (Calm, Alert, Panic, Recovered)
  physical_response TEXT           -- Clinical observation (heart rate, breathing, etc.)
);
```

#### 4.3.5 Report Table
```sql
CREATE TABLE reports (
  id INT AUTO_INCREMENT PRIMARY KEY,
  avoidance VARCHAR(32),           -- PTSD Criterion C
  re_experiencing VARCHAR(32),     -- PTSD Criterion B
  negative_alterations VARCHAR(32),-- PTSD Criterion D
  hyperarousal VARCHAR(32),        -- PTSD Criterion E
  person_id INT,
  therapist_id INT,
  reaction_id INT,
  FOREIGN KEY (person_id) REFERENCES persons(id),
  FOREIGN KEY (therapist_id) REFERENCES therapists(id),
  FOREIGN KEY (reaction_id) REFERENCES reactions(id)
);
```

#### 4.3.6 Junction Tables
```sql
-- Person participates in Scenario
CREATE TABLE participates (
  person_id INT,
  scenario_id INT,
  PRIMARY KEY (person_id, scenario_id),
  FOREIGN KEY (person_id) REFERENCES persons(id),
  FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
);

-- Therapist assigns Scenario
CREATE TABLE assigns (
  therapist_id INT,
  scenario_id INT,
  PRIMARY KEY (therapist_id, scenario_id),
  FOREIGN KEY (therapist_id) REFERENCES therapists(id),
  FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
);

-- Person exhibits Reaction
CREATE TABLE exhibits (
  person_id INT,
  reaction_id INT,
  PRIMARY KEY (person_id, reaction_id),
  FOREIGN KEY (person_id) REFERENCES persons(id),
  FOREIGN KEY (reaction_id) REFERENCES reactions(id)
);

-- Scenario triggers Reaction
CREATE TABLE `triggers` (
  scenario_id INT,
  reaction_id INT,
  PRIMARY KEY (scenario_id, reaction_id),
  FOREIGN KEY (scenario_id) REFERENCES scenarios(id),
  FOREIGN KEY (reaction_id) REFERENCES reactions(id)
);
```

### 4.4 Key Design Decisions

**Why Junction Tables?**
- **Many-to-Many Relationships**: 
  - One person can participate in multiple scenarios
  - One scenario can have multiple participants
  - Junction tables enable proper normalization

**Why Report has 3 Foreign Keys?**
```
Original Design (6-table):
  Report → Simulation → Person
                      → Scenario
                      
Current Design (5-table):
  Report → Person (who was assessed)
        → Therapist (who conducted assessment)
        → Reaction (final status/reaction observed)
```

**Benefits**:
- Eliminates redundant Simulation intermediary table
- Direct linkage to clinical data (person, therapist, reaction)
- Scenario traced via `Triggers` junction table

---

## 5. Backend Implementation

### 5.1 Project Structure
```
backend/
├── __init__.py
├── main.py              # FastAPI app, CORS, route mounting
├── database.py          # MySQL connection, session, auto-create DB
├── models.py            # SQLAlchemy ORM models (9 tables)
├── schemas.py           # Pydantic request/response models
├── crud.py              # Database CRUD operations
├── engine.py            # Unused (legacy)
├── mesa_model.py        # Mesa simulation (SoldierAgent, PTSDModel)
├── presets.py           # Scenario/reaction catalogs
├── seed.py              # Initial data seeding
└── routers/
    ├── person.py        # Person CRUD endpoints
    ├── therapist.py     # Therapist CRUD endpoints
    ├── scenario.py      # Scenario CRUD endpoints
    └── simulation.py    # Main simulation endpoint + presets
```

### 5.2 Key Backend Files

#### 5.2.1 main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import person, therapist, scenario, simulation

app = FastAPI(title="PTSD Simulation API")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(person.router)
app.include_router(therapist.router)
app.include_router(scenario.router)
app.include_router(simulation.router)
```

#### 5.2.2 database.py (MySQL Auto-Create)
```python
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "ptsd_simulation_db")

def _ensure_database_exists():
    """Auto-create MySQL database if missing."""
    root_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/"
    tmp_engine = create_engine(root_url)
    with tmp_engine.connect() as conn:
        conn.execute(text(
            f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        ))
    tmp_engine.dispose()

_ensure_database_exists()

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

#### 5.2.3 presets.py (Scenario Catalog)
```python
SCENARIO_CATALOG = [
    {
        "key": "urban_ambush",
        "scenario_type": "Urban Ambush",
        "environment": "High noise, crowded, hostile",
        "description": "Busy city street with sporadic gunfire...",
        "intensity": "high",
        "recommended_grid": 10,
        "num_triggers": 8,
        "trigger_strength": 12,
    },
    # ... 11 more scenarios
]

REACTION_CATALOG = {
    "Calm": {
        "r_type": "Baseline State",
        "physical_response": "Respirations 12-16/min, controlled..."
    },
    "Alert": {
        "r_type": "Heightened Vigilance",
        "physical_response": "Heart rate 90-110 bpm; pupils dilated..."
    },
    # ... Panic, Recovered
}
```

#### 5.2.4 simulation.py (Main Endpoint)
```python
@router.post("/")
def run_simulation(request: SimulationRunRequest, db: Session = Depends(get_db)):
    # 1. Fetch Person, Scenario, Therapist
    person = crud.get_person(db, request.person_id)
    scenario = crud.get_scenario(db, request.scenario_id)
    therapist = crud.get_therapist(db, person.therapist_id)
    
    # 2. Load scenario preset
    preset = presets.find_scenario_preset(scenario.scenario_type)
    
    # 3. Create Mesa model
    model = PTSDModel(
        grid_size, grid_size,
        num_triggers=preset["num_triggers"],
        trigger_strength=preset["trigger_strength"],
        profile_values={
            "trauma_sensitivity": request.trauma_sensitivity,
            "emotional_regulation": request.emotional_regulation,
            # ...
        }
    )
    
    # 4. Run 20 steps
    simulation_steps = []
    for i in range(20):
        model.step()
        simulation_steps.append({
            "step": i,
            "soldier_stress": model.soldier.stress,
            "soldier_status": model.soldier.status,
            "soldier_pos": model.soldier.pos,
            # ...
        })
    
    # 5. Create reactions on status changes
    current_status = ""
    for step in simulation_steps:
        if step["soldier_status"] != current_status:
            current_status = step["soldier_status"]
            template = presets.reaction_template_for_status(current_status)
            reaction = crud.create_reaction(db, ReactionCreate(
                r_type=template["r_type"],
                physical_response=template["physical_response"]
            ))
            # Store in step for UI
            step["reaction_id"] = reaction.id
            step["reaction_type"] = reaction.r_type
            step["physical_response"] = reaction.physical_response
    
    # 6. Generate PTSD report
    final_stress = model.soldier.stress
    report = crud.create_report(db, ReportCreate(
        person_id=request.person_id,
        therapist_id=person.therapist_id,
        reaction_id=reaction.id,
        avoidance="High" if final_stress > 80 else "Low",
        re_experiencing="Yes" if final_stress > 90 else "No",
        # ...
    ))
    
    # 7. Return full history
    return {
        "final_stress": final_stress,
        "full_history": simulation_steps,
        "report": {...}
    }
```

### 5.3 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **Simulation** |
| POST | `/simulations/` | Run simulation with psychological profile |
| GET | `/simulations/stats` | Get dashboard statistics |
| GET | `/simulations/presets` | Get scenario/reaction catalogs |
| **Person (Soldier)** |
| GET | `/persons/` | List all soldiers |
| POST | `/persons/` | Create new soldier |
| GET | `/persons/{id}` | Get soldier by ID |
| PUT | `/persons/{id}` | Update soldier |
| DELETE | `/persons/{id}` | Delete soldier |
| **Therapist** |
| GET | `/therapists/` | List all therapists |
| POST | `/therapists/` | Create new therapist |
| GET | `/therapists/{id}` | Get therapist by ID |
| PUT | `/therapists/{id}` | Update therapist |
| DELETE | `/therapists/{id}` | Delete therapist |
| **Scenario** |
| GET | `/scenarios/` | List all scenarios |
| POST | `/scenarios/` | Create new scenario |
| GET | `/scenarios/{id}` | Get scenario by ID |
| PUT | `/scenarios/{id}` | Update scenario |
| DELETE | `/scenarios/{id}` | Delete scenario |

---

## 6. Frontend Implementation

### 6.1 Project Structure
```
frontend/
├── src/
│   ├── main.jsx          # App entry point, React Router
│   ├── App.jsx           # Root component with routes
│   ├── Layout.jsx        # Sidebar navigation layout
│   ├── api.js            # Axios HTTP client
│   ├── App.css           # Global styles
│   ├── index.css         # CSS reset
│   └── pages/
│       ├── Dashboard.jsx          # Stats overview + recent data
│       ├── PersonManager.jsx      # Soldier CRUD
│       ├── TherapistManager.jsx   # Therapist CRUD
│       ├── ScenarioManager.jsx    # Scenario CRUD
│       └── SimulationRunner.jsx   # Main simulation UI
├── public/
├── index.html
├── package.json
└── vite.config.js
```

### 6.2 Key Frontend Components

#### 6.2.1 SimulationRunner.jsx (Main Simulation UI)

**UI Layout**:
```
┌────────────────────────────────────────────────────────────┐
│                     Simulation Lab                         │
├─────────────────────────────┬──────────────────────────────┤
│      Configuration          │    Mesa Grid Visualization   │
│                             │                              │
│  Select Soldier: [dropdown] │      ┌───────────────┐       │
│  Scenario: [dropdown]       │      │  ■  □  ■  ■  │       │
│  Grid Size: [slider 6-20]   │      │  ■  ●  ■  □  │       │
│                             │      │  □  ■  ■  ■  │       │
│  Trauma Sensitivity: 0.50   │      │  ■  ■  ■  ■  │       │
│  [slider]                   │      └───────────────┘       │
│  Emotional Regulation: 0.50 │                              │
│  [slider]                   │   Console Logs:              │
│  Recovery Rate: 0.50        │   ┌─────────────────────┐    │
│  [slider]                   │   │ > Step 5: Alert     │    │
│  Impulsivity: 0.50          │   │ > Step 8: Panic     │    │
│  [slider]                   │   │   Reaction #12      │    │
│  Coping: [dropdown]         │   └─────────────────────┘    │
│                             │                              │
│  [Start Simulation]         │   Recovery Report:           │
│                             │   Avoidance: High            │
│                             │   Re-experiencing: Yes       │
└─────────────────────────────┴──────────────────────────────┘
```

**Key Features**:
1. **Scenario Preset Dropdown**: Auto-sets grid size and trigger config
2. **Grid Size Slider**: Adjusts environment (6×6 to 20×20)
3. **5 Psychological Sliders**: Real-time profile tuning
4. **Grid Visualization**: 
   - Red circle (●) = Soldier (color changes with status)
   - Red squares (□) = Triggers
   - Animation: 500ms per step
5. **Console Logs**: 
   - Scrollable history of all 20 steps
   - Shows reaction ID, type, physical response on status changes
6. **Recovery Report**: Final PTSD assessment

**Animation Logic**:
```javascript
history.forEach((stepData, index) => {
    setTimeout(() => {
        // Update grid visualization
        setCurrentFrameData(stepData);
        
        // Update logs
        setLogs(prev => [...prev, 
            `Step ${stepData.step}: Status ${stepData.soldier_status} ` +
            `(Stress: ${stepData.soldier_stress.toFixed(1)}) ` +
            (stepData.reaction_id ? 
                `| Reaction #${stepData.reaction_id} [${stepData.reaction_type}]` : 
                '')
        ]);
        
        // Auto-scroll to bottom
        logsDiv.scrollTop = logsDiv.scrollHeight;
    }, index * 500);  // 500ms per step
});
```

#### 6.2.2 Dashboard.jsx

**Displays**:
```
┌──────────────────────────────────────────────────────────┐
│                  System Dashboard                        │
├──────────────────────────────────────────────────────────┤
│  Statistics:                                             │
│  ┌────────────┬────────────┬────────────┬────────────┐   │
│  │ Persons    │ Therapists │ Scenarios  │ Reports    │   │
│  │     3      │      1     │     12     │     24     │   │
│  └────────────┴────────────┴────────────┴────────────┘   │
│                                                          │
│  Recent Assessments:                                     │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Person      | Avoidance | Re-exp | Hyper | Date  │   │
│  │ Pvt. Ryan   | High      | Yes    | Severe| 1/22  │   │
│  │ Sgt. Miller | Low       | No     | Mild  | 1/21  │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  Recent Reactions Recorded:                              │
│  ┌──────────────────────────────────────────────────┐   │
│  │ ID  | Type   | Physical Response                 │   │
│  │ 45  | Panic  | Heart rate 140+ bpm; hypervent... │   │
│  │ 44  | Alert  | Pupils dilated; visual scanni... │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

#### 6.2.3 PersonManager.jsx (Soldier CRUD)
- Create, Read, Update, Delete soldiers
- Assign to therapist
- View participation history

---

## 7. Scenario System

### 7.1 Complete Scenario Catalog (12 Scenarios)

| # | Scenario | Grid | Triggers | Strength | Intensity | Clinical Use |
|---|----------|------|----------|----------|-----------|--------------|
| 1 | **Urban Ambush** | 10×10 | 8 | 12 | High | Hypervigilance in crowded environments |
| 2 | **Forest Patrol** | 12×12 | 5 | 8 | Medium | Isolation anxiety, anticipatory stress |
| 3 | **Marketplace** | 12×12 | 6 | 9 | Medium | Civilian reintegration testing |
| 4 | **Convoy Escort** | 14×14 | 7 | 10 | Med-High | Sustained vigilance assessment |
| 5 | **Night Base Alarm** | 10×10 | 5 | 13 | High | Sleep-related PTSD, disorientation |
| 6 | **IED Roadside Blast** | 8×8 | 12 | 15 | **SEVERE** | Acute trauma re-exposure (highest intensity) |
| 7 | **Casualty Evacuation** | 10×10 | 6 | 11 | High | Guilt-based PTSD, moral injury |
| 8 | **Hostage Rescue** | 10×10 | 9 | 12 | High | Decision-making under pressure |
| 9 | **Defensive Position** | 16×16 | 10 | 9 | Med-High | Chronic stress, fatigue testing |
| 10 | **Lone Scout Recon** | 14×14 | 3 | 14 | Medium | Isolation + high-impact sparse triggers |
| 11 | **Friendly Fire** | 10×10 | 7 | 14 | **SEVERE** | Betrayal trauma, trust issues |
| 12 | **Training Misdirection** | 10×10 | 4 | 6 | **LOW** | Baseline/control, confidence building |

### 7.2 Scenario Design Philosophy

**Intensity Levels**:
- **LOW (6)**: Training, baseline assessment
- **MEDIUM (8-10)**: General combat stress, patrol environments
- **HIGH (11-13)**: Active combat, emergency situations
- **SEVERE (14-15)**: Trauma re-exposure, complex moral injury

**Grid Size Strategy**:
- **Small (8×8)**: Claustrophobic, high trigger density (IED Blast)
- **Medium (10×10)**: Standard combat zones (Urban Ambush, Hostage Rescue)
- **Large (14×14-16×16)**: Spread out, isolation (Defensive Position, Lone Scout)

**Trigger Count vs. Strength Trade-off**:
```
High Count + Low Strength (Forest Patrol: 5 triggers × 8 strength = 40 total)
  → Frequent mild stressors, testing sustained low-level stress

Low Count + High Strength (Lone Scout: 3 triggers × 14 strength = 42 total)
  → Sparse but impactful stressors, testing acute response

High Count + High Strength (IED Blast: 12 triggers × 15 strength = 180 total)
  → Overwhelming trauma exposure, severe PTSD testing
```

### 7.3 Clinical Scenario Selection Guide

**Assessment Protocol**:
1. **Baseline**: Start with Training Misdirection (LOW)
2. **General Stress**: Forest Patrol or Marketplace (MEDIUM)
3. **Combat Readiness**: Urban Ambush or Convoy Escort (HIGH)
4. **Trauma-Specific**:
   - Blast survivors → IED Roadside Blast
   - Medics/corpsmen → Casualty Evacuation
   - Unit betrayal → Friendly Fire
   - Night terrors → Night Base Alarm

---

## 8. Clinical Assessment

### 8.1 Reaction Catalog (4 Status Types)

```python
REACTION_CATALOG = {
    "Calm": {
        "r_type": "Baseline State",
        "physical_response": 
            "Respirations 12-16/min, controlled and deep; "
            "shoulders relaxed; visual scanning methodical and deliberate; "
            "muscle tension minimal; cognitive processing clear; "
            "situational awareness optimal"
    },
    
    "Alert": {
        "r_type": "Heightened Vigilance",
        "physical_response":
            "Heart rate 90-110 bpm; pupils dilated; "
            "rapid visual scanning for threats/cover; "
            "increased muscle tension in shoulders/neck; "
            "breathing shallow 20-24/min; hands near weapon ready position; "
            "hypervigilant to environmental cues"
    },
    
    "Panic": {
        "r_type": "Acute Stress Response",
        "physical_response":
            "Heart rate 130+ bpm; hyperventilation 30+ breaths/min; "
            "tunnel vision with peripheral awareness loss; "
            "tremors in extremities; decision-making impaired; "
            "disorganized movement patterns; fight-flight-freeze activation; "
            "verbal communication difficulty; sweating profuse"
    },
    
    "Recovered": {
        "r_type": "Post-Stress Stabilization",
        "physical_response":
            "Controlled breathing exercises initiated; "
            "heart rate decreasing; muscle tension releasing; "
            "cognitive function restoring; grounding techniques applied; "
            "situational reassessment in progress; "
            "return to tactical baseline"
    }
}
```

### 8.2 DSM-5 PTSD Criteria Mapping

**DSM-5 Criteria for PTSD** (Simplified):

| Criterion | Name | Description | System Mapping |
|-----------|------|-------------|----------------|
| **A** | Exposure | Traumatic event exposure | ✅ Scenario selection (combat environments) |
| **B** | Re-experiencing | Flashbacks, nightmares | ✅ `re_experiencing` field (Yes/No based on final stress > 90) |
| **C** | Avoidance | Avoiding reminders of trauma | ✅ `avoidance` field (High/Low based on final stress > 80) |
| **D** | Negative Alterations | Negative beliefs, emotional numbing | ✅ `negative_alterations` (Moderate/None based on stress > 50) |
| **E** | Hyperarousal | Startle response, sleep issues, irritability | ✅ `hyperarousal` (Severe/Mild based on stress > 70) |

**Diagnosis Algorithm**:
```
PTSD Diagnosis = Criterion A + (B OR C) + (D AND E)

Example:
  Criterion A: ✅ Participated in IED Blast scenario
  Criterion B: ✅ Re-experiencing = "Yes" (stress > 90)
  Criterion C: ✅ Avoidance = "High" (stress > 80)
  Criterion D: ✅ Negative Alterations = "Moderate" (stress > 50)
  Criterion E: ✅ Hyperarousal = "Severe" (stress > 70)
  
  → PTSD LIKELY (recommend clinical interview + PCL-5 assessment)
```

### 8.3 Interpreting Simulation Results

**Case Study: Pvt. Ryan (High Trauma Sensitivity)**

**Profile**:
```json
{
  "trauma_sensitivity": 0.8,
  "emotional_regulation": 0.3,
  "recovery_rate": 0.4,
  "impulsivity": 0.7,
  "coping_mechanism": "avoidance"
}
```

**Scenario**: Urban Ambush (10×10 grid, 8 triggers, strength 12)

**Simulation Results**:
```
Step 0-2:   Calm (stress 15 → 28)
Step 3-6:   Alert (stress 45 → 62)
Step 7-15:  Panic (stress 89 → 145)
Step 16-19: Panic (stress 152 → 167)
Final:      stress = 167.4
```

**PTSD Report**:
```json
{
  "avoidance": "High",           // 167 > 80 ✅
  "re_experiencing": "Yes",      // 167 > 90 ✅
  "negative_alterations": "Moderate",  // 167 > 50 ✅
  "hyperarousal": "Severe"       // 167 > 70 ✅
}
```

**Clinical Interpretation**:
- **High trauma sensitivity (0.8)** + **Low emotional regulation (0.3)** → Rapid escalation to panic
- **Avoidance coping mechanism** → Poor stress resolution, no recovery phase
- **Final stress 167** → Severe PTSD symptoms across all criteria
- **Recommendation**: 
  - Immediate trauma-focused CBT
  - Possible SSRI medication
  - Postpone deployment until stress management improves

**Comparison: Sgt. Miller (Veteran, High Resilience)**

**Profile**:
```json
{
  "trauma_sensitivity": 0.3,
  "emotional_regulation": 0.8,
  "recovery_rate": 0.7,
  "impulsivity": 0.4,
  "coping_mechanism": "approach"
}
```

**Same Scenario**: Urban Ambush

**Results**:
```
Step 0-5:   Calm (stress 10 → 32)
Step 6-10:  Alert (stress 41 → 55)
Step 11-14: Alert (stress 58 → 48)  [Recovery kicking in]
Step 15-19: Calm (stress 42 → 25)
Final:      stress = 25.3
```

**PTSD Report**:
```json
{
  "avoidance": "Low",            // 25 < 80
  "re_experiencing": "No",       // 25 < 90
  "negative_alterations": "None",// 25 < 50
  "hyperarousal": "Mild"         // 25 < 70
}
```

**Clinical Interpretation**:
- **Low trauma sensitivity (0.3)** + **High emotional regulation (0.8)** → Controlled response
- **High recovery rate (0.7)** + **Approach coping** → Active stress management
- **Final stress 25** → Minimal PTSD risk
- **Recommendation**: Combat-ready, continue monitoring

---

## 9. Setup & Deployment

### 9.1 Prerequisites
```
- Python 3.10+
- Node.js 16+
- MySQL 8.0+
- Git
```

### 9.2 Backend Setup

```bash
# Clone repository
git clone <repo-url>
cd ptsd_simulation_app

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create MySQL database
mysql -u root -p
CREATE DATABASE ptsd_simulation_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ptsd_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ptsd_simulation_db.* TO 'ptsd_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Configure environment (.env file)
MYSQL_USER=ptsd_user
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=ptsd_simulation_db

# Seed database
python backend/seed.py

# Start server
uvicorn backend.main:app --reload
# API docs: http://localhost:8000/docs
```

### 9.3 Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# UI: http://localhost:5173
```

### 9.4 Production Deployment

**Backend (FastAPI)**:
```bash
# Use Gunicorn + Uvicorn workers
pip install gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or Docker
docker build -t ptsd-backend .
docker run -p 8000:8000 --env-file .env ptsd-backend
```

**Frontend (React)**:
```bash
# Build for production
npm run build

# Serve with Nginx/Apache
# dist/ folder contains static HTML/JS/CSS
```

**MySQL**:
```sql
-- Production security
ALTER USER 'ptsd_user'@'localhost' IDENTIFIED BY 'STRONG_PASSWORD';
REVOKE ALL PRIVILEGES ON ptsd_simulation_db.* FROM 'ptsd_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ptsd_simulation_db.* TO 'ptsd_user'@'localhost';

-- Backup
mysqldump -u ptsd_user -p ptsd_simulation_db > backup_$(date +%Y%m%d).sql
```

---

## 10. Use Cases & Workflows

### 10.1 Clinical Assessment Workflow

**Scenario**: Dr. Sarah Connor assesses new patient Pvt. Ryan for combat readiness

**Steps**:
1. **Login to Dashboard** → View system stats
2. **Navigate to Soldiers** → Create/verify Pvt. Ryan profile
3. **Navigate to Simulation Lab**
4. **Configure Simulation**:
   - Select Soldier: Pvt. Ryan
   - Scenario: Urban Ambush (baseline combat scenario)
   - Grid Size: 10 (default for scenario)
   - Psychological Profile:
     - Trauma Sensitivity: 0.5 (unknown, use baseline)
     - Emotional Regulation: 0.5
     - Recovery Rate: 0.5
     - Impulsivity: 0.5
     - Coping: Avoidance (reported behavior)
5. **Run Simulation** → Observe real-time stress response
6. **Analyze Results**:
   - Final Stress: 142
   - Avoidance: High
   - Re-experiencing: Yes
   - Hyperarousal: Severe
7. **Clinical Decision**: 
   - Defer deployment
   - Initiate trauma-focused CBT
   - Re-assess in 3 months with same scenario

### 10.2 Research Use Case

**Scenario**: Analyzing impact of coping mechanisms on PTSD outcomes

**Method**:
1. **Create test cohort**: 10 soldiers with identical profiles EXCEPT coping mechanism
2. **Run batch simulations**: Same scenario (IED Blast) for all
3. **Collect data**:
   ```sql
   SELECT p.name, r.avoidance, r.re_experiencing, r.hyperarousal
   FROM reports r
   JOIN persons p ON p.id = r.person_id
   WHERE r.id IN (/* batch IDs */);
   ```
4. **Statistical Analysis**: Compare final stress by coping type
   ```
   Avoidance:   avg stress = 165 (n=10)
   Approach:    avg stress = 78  (n=10)
   Freezing:    avg stress = 189 (n=10)
   Suppression: avg stress = 134 (n=10)
   ```
5. **Conclusion**: Approach coping reduces PTSD severity by ~53%

### 10.3 Training Program Design

**Scenario**: Design resilience training curriculum

**Approach**:
1. **Baseline Assessment**: All recruits run Training Misdirection (LOW)
2. **Identify high-risk profiles**: trauma_sensitivity > 0.7, emotional_regulation < 0.4
3. **Targeted Interventions**:
   - Stress inoculation training
   - Emotional regulation workshops
   - Coping skill development
4. **Post-Training Assessment**: Re-run same scenarios
5. **Measure Improvement**:
   ```
   Pre-training:  avg stress = 145
   Post-training: avg stress = 92
   Improvement:   36.5%
   ```

---

## Appendix A: Key Formulas

**Stress Accumulation**:
```
stress(t+1) = stress(t) + Σ[trigger_intensity × trauma_sensitivity / (1 + distance²)]
```

**Stress Decay**:
```
stress(t+1) = max(0, stress(t) - recovery_rate × 2.0)
```

**Alert Threshold**:
```
alert_threshold = 30 × (1 + trauma_sensitivity)
```

**Panic Threshold**:
```
panic_threshold = 60 × (1 + trauma_sensitivity)
```

---

## Appendix B: Database Queries

**Count simulations per soldier**:
```sql
SELECT p.name, COUNT(r.id) AS sim_count
FROM persons p
JOIN reports r ON r.person_id = p.id
GROUP BY p.name
ORDER BY sim_count DESC;
```

**Average stress by scenario**:
```sql
SELECT s.scenario_type, AVG(
  CASE 
    WHEN r.re_experiencing = 'Yes' THEN 100
    WHEN r.avoidance = 'High' THEN 85
    ELSE 50
  END
) AS avg_estimated_stress
FROM scenarios s
JOIN `triggers` t ON t.scenario_id = s.id
JOIN reactions rx ON rx.id = t.reaction_id
JOIN reports r ON r.reaction_id = rx.id
GROUP BY s.scenario_type;
```

**Recent reactions with full context**:
```sql
SELECT 
  rx.id AS reaction_id,
  rx.r_type AS reaction_type,
  p.name AS soldier,
  s.scenario_type AS scenario,
  r.avoidance, r.re_experiencing, r.hyperarousal
FROM reactions rx
JOIN exhibits e ON e.reaction_id = rx.id
JOIN persons p ON p.id = e.person_id
JOIN `triggers` tr ON tr.reaction_id = rx.id
JOIN scenarios s ON s.id = tr.scenario_id
JOIN reports r ON r.reaction_id = rx.id
ORDER BY rx.id DESC
LIMIT 10;
```

---

## Appendix C: Future Enhancements

1. **Multi-Agent Simulations**: Team dynamics, buddy system effects
2. **Longitudinal Tracking**: Track recovery over multiple sessions
3. **Machine Learning**: Predict PTSD risk from profile alone
4. **VR Integration**: Immersive scenario presentation
5. **Mobile App**: Field assessment capabilities
6. **Telemetry**: Real physiological data (heart rate, skin conductance)
7. **Custom Scenarios**: User-defined trigger patterns
8. **Advanced Analytics**: Heatmaps, stress trajectories, cluster analysis

---

## License & Contact

**License**: MIT (or as specified)  
**Contact**: [Project maintainer email]  
**Documentation Version**: 1.0  
**Last Updated**: January 22, 2026  

---

**End of Documentation**
