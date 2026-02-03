# Quick Reference: Simulation → Reaction + Report

## What Happened?

**Removed**: Simulation table from database schema  
**Kept**: Person, Therapist, Scenario, Reaction, Report

---

## New Schema (5 Tables)

```
Therapist
├─ id (PK)
├─ name
├─ qualification
├─ specialization
├─ years_of_experience
└─ [has many] patients (Person)

Person
├─ id (PK)
├─ name
├─ rank
├─ age
├─ gender
├─ service_years
├─ therapist_id (FK → Therapist)
├─ [has many] reactions
└─ [has many] reports

Scenario
├─ id (PK)
├─ scenario_type
├─ environment
├─ [has many] reactions
└─ [has many] reports

Reaction ⭐ (was nested under Simulation, now independent)
├─ id (PK)
├─ person_id (FK → Person) ✨ NEW
├─ scenario_id (FK → Scenario) ✨ NEW
├─ reaction_type
└─ physical_response

Report ⭐ (was nested under Simulation, now independent)
├─ id (PK)
├─ person_id (FK → Person) ✨ NEW
├─ scenario_id (FK → Scenario) ✨ NEW
├─ avoidance
├─ re_experiencing
├─ negative_alterations
└─ hyperarousal
```

---

## What Changed in Code

| Component | Change |
|-----------|--------|
| **Models** | Removed Simulation class |
| **Schemas** | Removed SimulationCreate/Simulation schemas |
| **CRUD** | Removed create_simulation, get_simulation, get_simulations |
| **Routers** | Removed GET /simulations/, added GET/POST /reactions/, /reports/ |
| **Frontend** | Updated Dashboard to show reactions + reports instead of simulations |
| **Main** | Added reaction and report router imports |

---

## API Changes

### Removed
- ❌ `GET /simulations/` - List simulations
- ❌ `GET /simulations/{id}` - Get simulation

### Still Works (Same Endpoint, Different Logic)
- ✏️ `POST /simulations/` - Runs simulation, saves to Reaction + Report instead of Simulation

### New
- ✅ `GET /reactions/` - List all behavioral reactions
- ✅ `GET /reactions/{id}` - Get specific reaction
- ✅ `POST /reactions/` - Create reaction
- ✅ `GET /reports/` - List all assessment reports
- ✅ `GET /reports/{id}` - Get specific report
- ✅ `POST /reports/` - Create report

---

## Database Relationships

### OLD: Simulation was the junction
```
Person --[has many]--> Simulation --[has many]--> Reaction
Scenario --[has many]--> Simulation --[has many]--> Reaction
```

### NEW: Direct relationships
```
Person --[has many]--> Reaction <--[has many]-- Scenario
Person --[has many]--> Report <--[has many]-- Scenario
```

---

## Example: Viewing Assessment Results

### OLD Way
```python
simulation = db.query(Simulation).filter(id=123).first()
person_id = simulation.person_id
reactions = simulation.reactions  # Nested list
report = simulation.report  # Nested object
```

### NEW Way
```python
reactions = db.query(Reaction).filter(
    Reaction.person_id == 1, 
    Reaction.scenario_id == 2
).all()

report = db.query(Report).filter(
    Report.person_id == 1,
    Report.scenario_id == 2
).first()
```

---

## For Your App

✅ **Frontend**: Simulations still run the same way  
✅ **Backend**: Saving to database changed, but frontend doesn't care about that  
✅ **Data**: All reaction and report data is preserved  
✅ **Dashboard**: Shows Reactions + Reports counts instead of Simulation count  

**Everything works the same from the user's perspective!**

---

## Files Modified

### Backend
- `backend/models.py` - Removed Simulation, updated relationships
- `backend/schemas.py` - Removed Simulation schemas
- `backend/crud.py` - Removed Simulation CRUD, added Reaction/Report functions
- `backend/routers/simulation.py` - Updated to create Reaction + Report
- `backend/routers/reaction.py` - NEW
- `backend/routers/report.py` - NEW
- `backend/main.py` - Added new router imports

### Frontend
- `frontend/src/pages/Dashboard.jsx` - Updated stats display
- `frontend/src/pages/SimulationRunner.jsx` - No changes needed

### Documentation
- `SCHEMA_RESTRUCTURING.md` - Detailed explanation
- `QUICK_REFERENCE.md` - This file
