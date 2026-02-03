# Schema Restructuring: Removed Simulation Table

## Summary of Changes

The database schema has been restructured to remove the Simulation table while maintaining all functionality. Results are now stored directly in Reaction and Report tables.

---

## Database Schema (5 Core Entities)

### 1. **Therapist**
Stores information about mental health professionals responsible for assigning scenarios and evaluating behavioral responses.

**Attributes:**
- `id` (INT, Primary Key)
- `name` (STRING)
- `qualification` (STRING) - e.g., "PhD Clinical Psychology"
- `specialization` (STRING) - e.g., "Trauma"
- `years_of_experience` (INT)

**Relationships:**
- One-to-Many with Person (one therapist supervises multiple patients)

---

### 2. **Person**
Stores details of soldiers or patients undergoing psychological assessment.

**Attributes:**
- `id` (INT, Primary Key)
- `name` (STRING)
- `rank` (STRING) - e.g., "Private", "Sergeant"
- `age` (INT)
- `gender` (STRING)
- `service_years` (INT)
- `therapist_id` (INT, Foreign Key) → Therapist

**Relationships:**
- Many-to-One with Therapist
- One-to-Many with Reaction (multiple reactions per person)
- One-to-Many with Report (multiple reports per person)

---

### 3. **Scenario**
Represents predefined psychological or situational conditions used in simulations.

**Attributes:**
- `id` (INT, Primary Key)
- `scenario_type` (STRING) - e.g., "Urban Ambush", "Crowd Chaos"
- `environment` (STRING) - e.g., "High Noise, Crowded", "Low Noise, Open"

**Relationships:**
- One-to-Many with Reaction (multiple reactions per scenario)
- One-to-Many with Report (multiple reports per scenario)

---

### 4. **Reaction**
Captures behavioral and physical responses generated during agent-based simulations.

**Attributes:**
- `id` (INT, Primary Key)
- `person_id` (INT, Foreign Key) → Person
- `scenario_id` (INT, Foreign Key) → Scenario
- `reaction_type` (STRING) - e.g., "Step 5: Alert", "Step 12: Panic"
- `physical_response` (STRING) - e.g., "Stress: 45.3, Pos: (3, 7)"

**Relationships:**
- Many-to-One with Person
- Many-to-One with Scenario

**Purpose:** Tracks behavioral responses at key moments during simulation (status changes, stress milestones)

---

### 5. **Report**
Stores psychological evaluation outcomes derived from reactions.

**Attributes:**
- `id` (INT, Primary Key)
- `person_id` (INT, Foreign Key) → Person
- `scenario_id` (INT, Foreign Key) → Scenario
- `avoidance` (STRING) - e.g., "High", "Low"
- `re_experiencing` (STRING) - e.g., "Yes", "No"
- `negative_alterations` (STRING) - e.g., "Moderate", "None"
- `hyperarousal` (STRING) - e.g., "Severe", "Mild"

**Relationships:**
- Many-to-One with Person
- Many-to-One with Scenario

**Purpose:** Summarizes psychological condition and recovery readiness of a person for a given scenario

---

## Dependency Changes

### Backend Changes

**1. Models (backend/models.py)**
- ❌ **Removed** `Simulation` class
- ✏️ **Updated** `Person` relationships:
  - Removed: `simulations = relationship("Simulation", ...)`
  - Added: `reactions = relationship("Reaction", ...)`
  - Added: `reports = relationship("Report", ...)`
- ✏️ **Updated** `Scenario` relationships:
  - Removed: `simulations = relationship("Simulation", ...)`
  - Added: `reactions = relationship("Reaction", ...)`
  - Added: `reports = relationship("Report", ...)`
- ✏️ **Updated** `Reaction` foreign keys:
  - Changed: `simulation_id` → `person_id` + `scenario_id`
  - Updated relationships accordingly
- ✏️ **Updated** `Report` foreign keys:
  - Changed: `simulation_id` → `person_id` + `scenario_id`
  - Updated relationships accordingly

**2. Schemas (backend/schemas.py)**
- ❌ **Removed** `SimulationBase`, `SimulationCreate`, `Simulation` schemas
- ✏️ **Updated** `ReactionBase`:
  - Added: `person_id` (int)
  - Added: `scenario_id` (int)
  - Kept: `reaction_type`, `physical_response`
- ✏️ **Updated** `ReportBase`:
  - Added: `person_id` (int)
  - Added: `scenario_id` (int)
  - Kept: `avoidance`, `re_experiencing`, `negative_alterations`, `hyperarousal`

**3. CRUD (backend/crud.py)**
- ❌ **Removed** `create_simulation()`, `get_simulation()`, `get_simulations()`
- ✏️ **Updated** `create_reaction()`:
  - Changed signature: `create_reaction(db, reaction)` (no simulation_id)
  - Now accepts person_id and scenario_id from Reaction schema
- ✏️ **Updated** `create_report()`:
  - Changed signature: `create_report(db, report)` (no simulation_id)
  - Now accepts person_id and scenario_id from Report schema
- ✏️ **Added** new CRUD functions:
  - `get_reactions()` - List all reactions
  - `get_reactions_by_person()` - Get reactions for a specific person
  - `get_reports()` - List all reports
  - `get_report_by_person_scenario()` - Get report for person + scenario combo
- ✏️ **Updated** `get_statistics()`:
  - Removed: `total_simulations`
  - Added: `total_reactions`
  - Added: `total_reports`

**4. Routers**
- ✏️ **Updated** `backend/routers/simulation.py`:
  - Changed endpoint signature: `run_simulation(person_id, scenario_id, trauma_sensitivity, ..., db)`
  - No longer creates Simulation record
  - Instead creates Reaction record(s) with `person_id` + `scenario_id`
  - Instead creates single Report record with `person_id` + `scenario_id`
  - Returns dict with `full_history` for frontend visualization
- 🆕 **Created** `backend/routers/reaction.py`:
  - `GET /reactions/` - List all reactions
  - `GET /reactions/{id}` - Get single reaction
  - `POST /reactions/` - Create reaction
- 🆕 **Created** `backend/routers/report.py`:
  - `GET /reports/` - List all reports
  - `GET /reports/{id}` - Get single report
  - `POST /reports/` - Create report

**5. Main App (backend/main.py)**
- ✏️ **Updated** imports:
  - Added: `from .routers import reaction, report`
- ✏️ **Updated** router registration:
  - Added: `app.include_router(reaction.router)`
  - Added: `app.include_router(report.router)`

---

### Frontend Changes

**1. SimulationRunner.jsx**
- ✏️ **Updated** POST endpoint call:
  - Changed from: `api.post('/simulations/', {...})`
  - To: `api.post('/simulations/', {...})` (same endpoint, different data model)
  - Now sends `person_id`, `scenario_id`, `trauma_sensitivity`, etc. as query/body params
  - Backend no longer returns a Simulation object, but direct step data

**2. Dashboard.jsx**
- ✏️ **Updated** statistics fetching:
  - Removed: `total_simulations` stat
  - Added: `total_reactions` stat
  - Added: `total_reports` stat
- ✏️ **Updated** recent data display:
  - Changed from: Fetching simulations list
  - To: Fetching reports list
  - Updated UI labels from "Recent Simulations" to "Recent Assessments"
- ✏️ **Updated** grid display:
  - Changed from: 4 statistics
  - To: 5 statistics (added Reactions + Reports)

---

## API Endpoint Changes

### Removed Endpoints
- ❌ `GET /simulations/` - List all simulations
- ❌ `GET /simulations/{id}` - Get specific simulation
- ❌ `POST /simulations/` (old format) - Create simulation record

### Updated Endpoints
- ✏️ `POST /simulations/` - **Different signature now**
  - Old: Takes `person_id`, `scenario_id`, `assigned_date`
  - New: Takes `person_id`, `scenario_id`, `trauma_sensitivity`, `emotional_regulation`, `recovery_rate`, `impulsivity`, `coping_mechanism`
  - Returns: `{person_id, scenario_id, final_stress, full_history, report}`
  - Side effects: Creates 1+ Reaction records + 1 Report record

- ✏️ `GET /simulations/stats` - **Updated response**
  - Old: `{total_persons, total_therapists, total_scenarios, total_simulations}`
  - New: `{total_persons, total_therapists, total_scenarios, total_reactions, total_reports}`

### New Endpoints
- 🆕 `GET /reactions/` - List all reactions
- 🆕 `GET /reactions/{id}` - Get reaction detail
- 🆕 `POST /reactions/` - Create reaction
- 🆕 `GET /reports/` - List all reports
- 🆕 `GET /reports/{id}` - Get report detail
- 🆕 `POST /reports/` - Create report

---

## Data Flow Changes

### Old Flow (with Simulation table)
```
Frontend POST /simulations/ with person_id, scenario_id
    ↓
Backend creates Simulation record (gets id)
    ↓
Backend runs Mesa simulation
    ↓
Backend creates Reaction records (reference simulation_id)
    ↓
Backend creates Report record (reference simulation_id)
    ↓
Backend returns Simulation object with nested reactions
```

### New Flow (without Simulation table)
```
Frontend POST /simulations/ with person_id, scenario_id, profile values
    ↓
Backend runs Mesa simulation (no record created yet)
    ↓
Backend creates Reaction records (reference person_id + scenario_id)
    ↓
Backend creates Report record (reference person_id + scenario_id)
    ↓
Backend returns {person_id, scenario_id, final_stress, full_history, report}
```

---

## Migration Impact

### Database
- ❌ Drop Simulation table
- ✏️ Update Reaction table
  - Add: `person_id` column
  - Add: `scenario_id` column
  - Remove: `simulation_id` column
  - Add: Foreign key constraints to Person and Scenario
- ✏️ Update Report table
  - Add: `person_id` column
  - Add: `scenario_id` column
  - Remove: `simulation_id` column
  - Add: Foreign key constraints to Person and Scenario
- ✏️ Update Person table
  - Remove relationship to Simulation table
  - Add relationship to Reaction and Report tables
- ✏️ Update Scenario table
  - Remove relationship to Simulation table
  - Add relationship to Reaction and Report tables

### Code
- Delete `/backend/routers/simulation.py` (old code removed)
- Create `/backend/routers/reaction.py`
- Create `/backend/routers/report.py`
- Update `/backend/models.py`
- Update `/backend/schemas.py`
- Update `/backend/crud.py`
- Update `/backend/main.py`
- Update `/frontend/src/pages/Dashboard.jsx`
- Update `/frontend/src/pages/SimulationRunner.jsx`

---

## Benefits of This Change

✅ **Simplified Schema**: 5 core tables instead of 6  
✅ **Direct Relationships**: Reactions and Reports directly linked to Person and Scenario  
✅ **No Intermediate Entity**: Eliminates the need for a Simulation "session" entity  
✅ **Flexibility**: Can rerun same Person+Scenario combo and track multiple reactions  
✅ **Cleaner API**: Results returned directly without nested object traversal  
✅ **Better Semantics**: Reaction and Report directly represent what they measure (not nested under Simulation)

---

## Example: Running a Simulation

### Request
```bash
POST /simulations/?person_id=1&scenario_id=2&trauma_sensitivity=0.7&emotional_regulation=0.3&recovery_rate=0.5&impulsivity=0.6&coping_mechanism=avoidance
```

### Response
```json
{
  "person_id": 1,
  "scenario_id": 2,
  "final_stress": 87.5,
  "full_history": [
    {
      "step": 0,
      "soldier_pos": [5, 5],
      "soldier_stress": 0,
      "soldier_color": "green",
      "soldier_status": "Calm",
      "triggers": [...]
    },
    ...
  ],
  "report": {
    "avoidance": "High",
    "re_experiencing": "Yes",
    "negative_alterations": "Moderate",
    "hyperarousal": "Severe"
  }
}
```

### Database Records Created
**Reaction 1**: Person 1, Scenario 2, "Step 5: Alert", "Stress: 45.3, Pos: (4, 6)"  
**Reaction 2**: Person 1, Scenario 2, "Step 12: Panic", "Stress: 87.5, Pos: (2, 3)"  
**Report 1**: Person 1, Scenario 2, "High", "Yes", "Moderate", "Severe"

---

## Checking Your Changes

To verify the schema restructuring was successful:

1. **Check Models**: Review `backend/models.py` - should have 5 tables only
2. **Check Relationships**: Person and Scenario should have direct relationships to Reaction and Report
3. **Check CRUD**: `crud.create_simulation()` should no longer exist
4. **Check Routers**: `/reactions` and `/reports` endpoints should be available
5. **Check Frontend**: Dashboard should show Reactions and Reports counts instead of Simulations

---

## Summary

The Simulation table has been successfully removed from the schema. All functionality is preserved through:
- Direct Person → Reaction relationship
- Direct Scenario → Reaction relationship  
- Direct Person → Report relationship
- Direct Scenario → Report relationship

This creates a **cleaner, more direct data model** while maintaining the ability to track all psychological assessment results.
