# Final Database Schema

## 5-Table Schema (as Requested)

### Person
Stores details of soldiers or patients undergoing psychological assessment.

**Attributes:**
- `Person_ID` (INTEGER, PRIMARY KEY)
- `Name` (TEXT)
- `Rank` (TEXT) - e.g., "Private", "Sergeant"
- `Age` (INTEGER)
- `Gender` (TEXT) - e.g., "Male", "Female"
- `Service_Years` (INTEGER)
- `Therapist_ID` (INTEGER, FOREIGN KEY → Therapist)

**Relationships:**
- Many-to-One with Therapist (each person has one therapist)
- One-to-Many with Reaction (one person has multiple reactions)
- One-to-Many with Report (one person has multiple reports)

---

### Therapist
Stores information about mental health professionals responsible for assigning scenarios and evaluating behavioral responses.

**Attributes:**
- `Therapist_ID` (INTEGER, PRIMARY KEY)
- `Name` (TEXT)
- `Qualification` (TEXT) - e.g., "PhD Clinical Psychology"
- `Specialization` (TEXT) - e.g., "Trauma"
- `Years_of_Experience` (INTEGER)

**Relationships:**
- One-to-Many with Person (one therapist supervises multiple patients)

---

### Scenario
Represents predefined psychological or situational conditions used in simulations.

**Attributes:**
- `Scenario_ID` (INTEGER, PRIMARY KEY)
- `Scenario_Type` (TEXT) - e.g., "Urban Ambush", "Crowd Chaos"
- `Environment` (TEXT) - e.g., "High Noise, Crowded", "Low Noise, Open"

**Relationships:**
- One-to-Many with Reaction (one scenario can have multiple reactions)
- One-to-Many with Report (one scenario can have multiple reports)

---

### Reaction
Captures behavioral and physical responses generated during agent-based simulations.

**Attributes:**
- `Reaction_ID` (INTEGER, PRIMARY KEY)
- `Person_ID` (INTEGER, FOREIGN KEY → Person) ⭐ NEW
- `Scenario_ID` (INTEGER, FOREIGN KEY → Scenario) ⭐ NEW
- `Reaction_Type` (TEXT) - e.g., "Step 5: Alert", "Step 12: Panic"
- `Physical_Response` (TEXT) - e.g., "Stress: 45.3, Position: (3,7)"

**Relationships:**
- Many-to-One with Person
- Many-to-One with Scenario

**Purpose:**
Tracks behavioral responses at key moments during simulation (status changes, stress milestones). Multiple reactions can be recorded per Person+Scenario pair to track progression through different states.

---

### Report
Stores psychological evaluation outcomes derived from reactions.

**Attributes:**
- `Report_ID` (INTEGER, PRIMARY KEY)
- `Person_ID` (INTEGER, FOREIGN KEY → Person) ⭐ NEW
- `Scenario_ID` (INTEGER, FOREIGN KEY → Scenario) ⭐ NEW
- `Avoidance` (TEXT) - e.g., "High", "Low"
- `Re_Experiencing` (TEXT) - e.g., "Yes", "No"
- `Negative_Alterations` (TEXT) - e.g., "Moderate", "None"
- `Hyperarousal` (TEXT) - e.g., "Severe", "Mild"

**Relationships:**
- Many-to-One with Person
- Many-to-One with Scenario

**Purpose:**
Summarizes psychological condition and recovery readiness of a person for a given scenario. Provides final assessment after simulation completes.

---

## ER Diagram

```
┌──────────────────┐
│   THERAPIST      │
├──────────────────┤
│ Therapist_ID (PK)│
│ Name             │
│ Qualification    │
│ Specialization   │
│ Years_of_Experi. │
└────────┬─────────┘
         │ 1:Many
         │
         ▼
┌──────────────────┐
│   PERSON         │
├──────────────────┤
│ Person_ID (PK)   │
│ Name             │
│ Rank             │
│ Age              │
│ Gender           │
│ Service_Years    │
│ Therapist_ID(FK) │◄────────┬──────────┐
└─────────┬────────┘         │          │
          │ 1:Many           │          │
          │                  │          │
    ┌─────▼────────────┐    │          │
    │ Reaction         │    │          │
    ├──────────────────┤    │          │
    │ Reaction_ID (PK) │    │          │
    │ Person_ID (FK)   │────┘          │
    │ Scenario_ID (FK) │────────┐      │
    │ Reaction_Type    │        │      │
    │ Physical_Response│        │      │
    └──────────────────┘        │      │
                                │      │
    ┌──────────────────────┐    │      │
    │    SCENARIO          │    │      │
    ├──────────────────────┤    │      │
    │ Scenario_ID (PK)     │◄───┘      │
    │ Scenario_Type        │           │
    │ Environment          │           │
    └──────┬───────────────┘           │
           │ 1:Many                    │
           │                           │
    ┌──────▼────────────┐              │
    │ Report           │              │
    ├──────────────────┤              │
    │ Report_ID (PK)  │              │
    │ Person_ID (FK)  │──────────────┘
    │ Scenario_ID(FK) │◄──────────────┘
    │ Avoidance       │
    │ Re_Experiencing │
    │ Negative_Altera │
    │ Hyperarousal    │
    └──────────────────┘

Legend:
(PK) = Primary Key
(FK) = Foreign Key
1:Many = One-to-Many relationship
```

---

## Relationships Summary

| From | To | Type | Cardinality |
|------|----|----|------------|
| Therapist | Person | One Therapist supervises many Persons | 1:Many |
| Person | Reaction | One Person has many Reactions | 1:Many |
| Person | Report | One Person has many Reports | 1:Many |
| Scenario | Reaction | One Scenario has many Reactions | 1:Many |
| Scenario | Report | One Scenario has many Reports | 1:Many |

---

## Key Points

✅ **5 Tables Total**: Therapist, Person, Scenario, Reaction, Report  
✅ **No Simulation Table**: Was removed for simpler schema  
✅ **Direct Links**: Reaction and Report directly reference Person+Scenario  
✅ **Flexible Queries**: Can find all reactions for a Person, or all reports for a Scenario  
✅ **Historical Tracking**: Multiple Reactions per Person+Scenario pair tracks simulation progression  

---

## Example Data

### Therapist
| Therapist_ID | Name | Qualification | Specialization | Years_of_Experience |
|---|---|---|---|---|
| 1 | Dr. Sarah Connor | PhD Clinical Psychology | Trauma | 15 |

### Person
| Person_ID | Name | Rank | Age | Gender | Service_Years | Therapist_ID |
|---|---|---|---|---|---|---|
| 1 | Pvt. Ryan | Private | 22 | Male | 1 | 1 |
| 2 | Sgt. Miller | Sergeant | 35 | Male | 12 | 1 |

### Scenario
| Scenario_ID | Scenario_Type | Environment |
|---|---|---|
| 1 | Urban Ambush | High Noise, Crowded |
| 2 | Crowd Chaos | Medium Noise, Dense Crowd |

### Reaction
| Reaction_ID | Person_ID | Scenario_ID | Reaction_Type | Physical_Response |
|---|---|---|---|---|
| 1 | 1 | 1 | Step 5: Alert | Stress: 45.3, Pos: (4, 6) |
| 2 | 1 | 1 | Step 12: Panic | Stress: 87.5, Pos: (2, 3) |
| 3 | 2 | 1 | Step 8: Alert | Stress: 32.1, Pos: (6, 5) |

### Report
| Report_ID | Person_ID | Scenario_ID | Avoidance | Re_Experiencing | Negative_Alterations | Hyperarousal |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | High | Yes | Moderate | Severe |
| 2 | 2 | 1 | Low | No | Mild | Mild |

---

## SQL Schema Definition

```sql
CREATE TABLE therapists (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    qualification TEXT,
    specialization TEXT,
    years_of_experience INTEGER
);

CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    rank TEXT,
    age INTEGER,
    gender TEXT,
    service_years INTEGER,
    therapist_id INTEGER NOT NULL,
    FOREIGN KEY (therapist_id) REFERENCES therapists(id)
);

CREATE TABLE scenarios (
    id INTEGER PRIMARY KEY,
    scenario_type TEXT,
    environment TEXT
);

CREATE TABLE reactions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    reaction_type TEXT,
    physical_response TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
);

CREATE TABLE reports (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    avoidance TEXT,
    re_experiencing TEXT,
    negative_alterations TEXT,
    hyperarousal TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
);
```

---

## Usage Example

### Find all reactions for a person
```sql
SELECT * FROM reactions WHERE person_id = 1;
```

### Find all reports for a scenario
```sql
SELECT * FROM reports WHERE scenario_id = 1;
```

### Get assessment results for a person+scenario pair
```sql
SELECT r.* FROM reactions r
WHERE r.person_id = 1 AND r.scenario_id = 1
ORDER BY r.reaction_type;

SELECT * FROM reports 
WHERE person_id = 1 AND scenario_id = 1;
```

### Find all people supervised by a therapist
```sql
SELECT p.* FROM persons p
WHERE p.therapist_id = 1;
```

### Get complete assessment summary
```sql
SELECT 
    p.name AS person_name,
    s.scenario_type,
    COUNT(r.id) AS reaction_count,
    rep.avoidance,
    rep.re_experiencing,
    rep.negative_alterations,
    rep.hyperarousal
FROM persons p
JOIN reactions r ON p.id = r.person_id
JOIN scenarios s ON r.scenario_id = s.id
LEFT JOIN reports rep ON p.id = rep.person_id AND s.id = rep.scenario_id
GROUP BY p.id, s.id;
```

---

## Schema Evolution

**Old Schema** (6 tables):
- Therapist, Person, Scenario, Simulation, Reaction, Report

**New Schema** (5 tables):
- Therapist, Person, Scenario, Reaction, Report

**Changes**:
- Removed Simulation table (intermediate entity)
- Added person_id + scenario_id to Reaction
- Added person_id + scenario_id to Report
- Direct Person↔Reaction and Scenario↔Reaction relationships
- Direct Person↔Report and Scenario↔Report relationships

**Benefits**:
- Simpler schema
- Fewer joins needed
- More intuitive data model
- Same functionality preserved
