# Dependencies & Imports Changed

## Summary

Removed Simulation table requires updates to database access paths throughout the codebase. All imports and relationships have been updated to use Person+Scenario composite key instead.

---

## Files That Changed

### 1. `backend/models.py`
**Import Changes**: None  
**Relationship Changes**:
```python
# OLD Person Model
simulations = relationship("Simulation", back_populates="person")

# NEW Person Model
reactions = relationship("Reaction", back_populates="person")
reports = relationship("Report", back_populates="person")
```

**Why**: Person no longer connects through Simulation; instead directly to Reaction and Report

---

### 2. `backend/schemas.py`
**Removed Imports/Classes**:
- ❌ `SimulationBase`
- ❌ `SimulationCreate`
- ❌ `Simulation`

**Schema Updates**:
```python
# OLD Reaction
class ReactionCreate(BaseModel):
    simulation_id: int
    reaction_type: str
    physical_response: str

# NEW Reaction
class ReactionCreate(BaseModel):
    person_id: int
    scenario_id: int
    reaction_type: str
    physical_response: str
```

**Why**: Reactions now store person and scenario directly

---

### 3. `backend/crud.py`
**Removed Functions**:
```python
❌ create_simulation(db, simulation)
❌ get_simulation(db, simulation_id)
❌ get_simulations(db, skip, limit)
```

**Updated Functions**:
```python
# OLD signature
def create_reaction(db, reaction, simulation_id):
    db_reaction = models.Reaction(**reaction.dict(), simulation_id=simulation_id)

# NEW signature
def create_reaction(db, reaction):
    db_reaction = models.Reaction(**reaction.dict())
```

**New Functions**:
```python
✅ get_reactions(db, skip, limit)
✅ get_reactions_by_person(db, person_id)
✅ get_report_by_person_scenario(db, person_id, scenario_id)
```

**Why**: No more Simulation entity to track; direct Person+Scenario queries

---

### 4. `backend/routers/simulation.py`
**Removed Imports**:
- ❌ `from .. import schemas` (no longer use SimulationCreate schema)
- ❌ `from typing import List` (no longer return list of simulations)

**Updated Imports**:
```python
# Added
from datetime import date
```

**Signature Changes**:
```python
# OLD - took request object
def run_simulation(sim_request: schemas.SimulationCreate, db: Session):

# NEW - takes individual params
def run_simulation(
    person_id: int,
    scenario_id: int,
    trauma_sensitivity: float = 0.5,
    emotional_regulation: float = 0.5,
    recovery_rate: float = 0.5,
    impulsivity: float = 0.5,
    coping_mechanism: str = "avoidance",
    db: Session = Depends(get_db)
):
```

**Removed Code**:
```python
❌ db_simulation = crud.create_simulation(db, sim_request)  # No longer create Simulation
❌ crud.create_reaction(db, ..., db_simulation.id)  # No longer pass simulation_id
❌ Report creation with simulation_id
```

**Added Code**:
```python
✅ crud.create_reaction(db, schemas.ReactionCreate(
    person_id=person_id,
    scenario_id=scenario_id,
    ...
))
✅ crud.create_report(db, schemas.ReportCreate(
    person_id=person_id,
    scenario_id=scenario_id,
    ...
))
```

**Why**: Removed Simulation as intermediary; now save directly with Person+Scenario keys

---

### 5. `backend/routers/reaction.py` (NEW)
**New File**: Complete file created  
**Imports**:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db
```

**Endpoints**:
```python
@router.get("/", response_model=List[schemas.Reaction])
@router.get("/{reaction_id}", response_model=schemas.Reaction)
@router.post("/", response_model=schemas.Reaction)
```

**Why**: Reactions are now first-class API resources

---

### 6. `backend/routers/report.py` (NEW)
**New File**: Complete file created  
**Imports**:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db
```

**Endpoints**:
```python
@router.get("/", response_model=List[schemas.Report])
@router.get("/{report_id}", response_model=schemas.Report)
@router.post("/", response_model=schemas.Report)
```

**Why**: Reports are now first-class API resources

---

### 7. `backend/main.py`
**Updated Imports**:
```python
# OLD
from .routers import therapist, person, scenario, simulation

# NEW
from .routers import therapist, person, scenario, simulation, reaction, report
```

**Updated Router Registration**:
```python
# OLD
app.include_router(therapist.router)
app.include_router(person.router)
app.include_router(scenario.router)
app.include_router(simulation.router)

# NEW
app.include_router(therapist.router)
app.include_router(person.router)
app.include_router(scenario.router)
app.include_router(simulation.router)
app.include_router(reaction.router)      # ✨ NEW
app.include_router(report.router)         # ✨ NEW
```

**Why**: Register new routers for API endpoints

---

### 8. `frontend/src/pages/Dashboard.jsx`
**Updated State**:
```javascript
// OLD
total_simulations: 0

// NEW
total_reactions: 0
total_reports: 0
```

**Updated Data Fetch**:
```javascript
// OLD
const [statsRes, simsRes] = await Promise.all([
    api.get('/simulations/stats'),
    api.get('/simulations/?limit=5')
]);
setStats(statsRes.data);
setRecentSimulations(simsRes.data);

// NEW
const statsRes = await api.get('/simulations/stats');
setStats(statsRes.data);
const reportsRes = await api.get('/reports/?limit=5');
setRecentReports(reportsRes.data);
```

**Updated Display**:
```javascript
// OLD
<h3>Simulations Run</h3>
<h2>{stats.total_simulations}</h2>
{recentSimulations.length > 0 && (
    <h3>Recent Simulations</h3>

// NEW
<h3>Reactions Recorded</h3>
<h2>{stats.total_reactions}</h2>
<h3>Reports Generated</h3>
<h2>{stats.total_reports}</h2>
{recentReports.length > 0 && (
    <h3>Recent Assessments</h3>
```

**Why**: Dashboard now shows Reaction and Report metrics instead of Simulation count

---

### 9. `frontend/src/pages/SimulationRunner.jsx`
**No Import Changes Required**  
**Endpoint Call Changed**:
```javascript
// OLD
const response = await api.post('/simulations/', {
    person_id: selectedPerson,
    scenario_id: selectedScenario,
    assigned_date: new Date().toISOString().split('T')[0],
    trauma_sensitivity: traumaSensitivity,
    ...
});

// NEW - Same endpoint, but no simulation_id in response
const response = await api.post('/simulations/', {
    person_id: selectedPerson,
    scenario_id: selectedScenario,
    trauma_sensitivity: traumaSensitivity,
    ...
});

// Response structure same (has full_history), but doesn't contain simulation object
```

**Why**: Response format changed but frontend usage pattern same

---

## Dependency Chain

```
database.py (unchanged)
    ↓
models.py (modified - removed Simulation)
    ↓
crud.py (modified - removed Simulation CRUD)
    ↓
routers/
    ├─ simulation.py (modified - doesn't create Simulation)
    ├─ reaction.py (NEW - CRUD endpoints)
    └─ report.py (NEW - CRUD endpoints)
    ↓
main.py (modified - register new routers)
    ↓
frontend/ (modified - updated API calls)
```

---

## Import Resolution

### Frontend imports (unchanged)
```javascript
import api from '../api';  // HTTP client - works same way
```

### Backend imports (may need updates)
If any custom code imports from these removed classes:
```python
# ❌ These no longer exist
from backend.schemas import SimulationCreate, Simulation
from backend import models  # models.Simulation no longer exists

# ✅ Use these instead
from backend.schemas import ReactionCreate, ReportCreate
from backend.crud import get_reactions, get_reports
```

---

## Database Migration Path

If migrating existing database:

```sql
-- 1. Create new columns on Reaction table
ALTER TABLE reactions ADD COLUMN person_id INTEGER;
ALTER TABLE reactions ADD COLUMN scenario_id INTEGER;

-- 2. Create new columns on Report table
ALTER TABLE reports ADD COLUMN person_id INTEGER;
ALTER TABLE reports ADD COLUMN scenario_id INTEGER;

-- 3. Migrate data from Simulation table
UPDATE reactions 
SET person_id = (SELECT person_id FROM simulations WHERE id = reaction.simulation_id),
    scenario_id = (SELECT scenario_id FROM simulations WHERE id = reaction.simulation_id);

UPDATE reports 
SET person_id = (SELECT person_id FROM simulations WHERE id = report.simulation_id),
    scenario_id = (SELECT scenario_id FROM simulations WHERE id = report.simulation_id);

-- 4. Add foreign key constraints
ALTER TABLE reactions ADD CONSTRAINT fk_reactions_person 
    FOREIGN KEY (person_id) REFERENCES persons(id);
ALTER TABLE reactions ADD CONSTRAINT fk_reactions_scenario 
    FOREIGN KEY (scenario_id) REFERENCES scenarios(id);

ALTER TABLE reports ADD CONSTRAINT fk_reports_person 
    FOREIGN KEY (person_id) REFERENCES persons(id);
ALTER TABLE reports ADD CONSTRAINT fk_reports_scenario 
    FOREIGN KEY (scenario_id) REFERENCES scenarios(id);

-- 5. Drop old columns and table
ALTER TABLE reactions DROP COLUMN simulation_id;
ALTER TABLE reports DROP COLUMN simulation_id;
DROP TABLE simulations;
```

---

## Testing Changed Dependencies

To verify dependencies are correct:

1. **Check imports**: Verify no imports of removed classes
2. **Check relationships**: Person and Scenario objects should have `reactions` and `reports` attributes
3. **Check API responses**: `/simulations/stats` should return `total_reactions` and `total_reports`
4. **Check CRUD**: `crud.create_simulation()` should not exist
5. **Check routers**: GET `/reactions/`, `/reports/` should return 200 OK

---

## Summary of Dependency Changes

| Type | Old | New | Impact |
|------|-----|-----|--------|
| **Tables** | 6 (with Simulation) | 5 (without) | Database queries change |
| **Relationships** | Person → Simulation → Reaction | Person → Reaction | Direct access paths |
| **CRUD Functions** | ~4 Simulation functions | 0 Simulation functions | Some code paths removed |
| **API Endpoints** | GET /simulations/, GET /simulations/{id} | GET /reactions/, GET /reports/ | API clients must update |
| **Schemas** | SimulationCreate required | person_id + scenario_id in Reaction/Report | Request body structure changes |
| **Frontend API Calls** | Same, but response format different | Same endpoint, updated handling | Frontend must adapt |

All changes maintain data integrity while simplifying the schema structure.
