# Testing Checklist - Schema Restructuring Verification

Complete this checklist to verify the new 5-table schema is working correctly.

---

## Phase 1: Database Verification ✅

### 1.1 Delete Old Database
- [ ] Stop the uvicorn server (Ctrl+C)
- [ ] Delete `ptsd_simulation.db` file (if it exists)
- [ ] Verify file is deleted

**Why**: Force creation of new database with 5 tables instead of 6

---

### 1.2 Verify Tables Created
- [ ] Restart uvicorn server
- [ ] Wait for "Uvicorn running on http://127.0.0.1:8000" message
- [ ] Check `ptsd_simulation.db` file exists
- [ ] Use SQLite viewer to check tables:
  - [ ] `therapist` table exists (no Simulation table!)
  - [ ] `person` table exists
  - [ ] `scenario` table exists
  - [ ] `reaction` table exists
  - [ ] `report` table exists
  - [ ] Confirm: exactly 5 tables (no Simulation)

**Why**: Ensure new schema created correctly

---

## Phase 2: Backend API Verification ✅

### 2.1 Test Therapist Endpoint
```bash
# Create therapist
POST http://localhost:8000/therapists/
{
  "name": "Dr. Smith",
  "specialty": "PTSD"
}

# Expected: 201 Created, returns therapist_id
```
- [ ] Create therapist successfully
- [ ] Get therapist_id from response (note it down: __________)

---

### 2.2 Test Person Endpoint
```bash
# Create person
POST http://localhost:8000/people/
{
  "name": "John Doe",
  "age": 35,
  "gender": "M",
  "military_rank": "Captain",
  "years_of_service": 10,
  "therapist_id": <from above>
}

# Expected: 201 Created, returns person_id
```
- [ ] Create person successfully
- [ ] Get person_id from response (note it down: __________)

---

### 2.3 Test Scenario Endpoint
```bash
# Create scenario
POST http://localhost:8000/scenarios/
{
  "name": "Combat Simulation",
  "description": "High-stress combat scenario"
}

# Expected: 201 Created, returns scenario_id
```
- [ ] Create scenario successfully
- [ ] Get scenario_id from response (note it down: __________)

---

### 2.4 Test Simulation Endpoint (Core Test!)
```bash
# Run simulation with manual profile values
POST http://localhost:8000/simulations/
{
  "person_id": <from 2.2>,
  "scenario_id": <from 2.3>,
  "trauma_sensitivity": 0.7,
  "emotional_regulation": 0.5,
  "recovery_rate": 0.3,
  "impulsivity": 0.6,
  "coping_mechanism": "approach"
}

# Expected: 200 OK, returns:
# {
#   "person_id": <value>,
#   "scenario_id": <value>,
#   "final_stress": <0.0-1.0>,
#   "full_history": [... stress values ...],
#   "report": {
#     "timestamp": "2024-...",
#     "summary": "...",
#     "recommendations": [...]
#   }
# }
```
- [ ] Simulation runs successfully
- [ ] Response contains full_history array (stress values)
- [ ] Response contains report object
- [ ] final_stress is between 0.0 and 1.0
- [ ] **NO Simulation object returned** (just the data)

---

### 2.5 Test Reactions Endpoint (New!)
```bash
# Get all reactions
GET http://localhost:8000/reactions/

# Expected: 200 OK, returns array of reactions
```
- [ ] Reactions endpoint works
- [ ] Returns array of reactions
- [ ] Each reaction has: id, person_id, scenario_id, stress_values, timestamp
- [ ] Person_id and scenario_id match what we used in 2.4

---

### 2.6 Test Reports Endpoint (New!)
```bash
# Get all reports
GET http://localhost:8000/reports/

# Expected: 200 OK, returns array of reports
```
- [ ] Reports endpoint works
- [ ] Returns array of reports
- [ ] Each report has: id, person_id, scenario_id, summary, recommendations
- [ ] Person_id and scenario_id match what we used in 2.4

---

### 2.7 Test Statistics Endpoint
```bash
# Get statistics
GET http://localhost:8000/simulations/stats

# Expected: 200 OK, returns:
# {
#   "total_people": 1,
#   "total_scenarios": 1,
#   "total_therapists": 1,
#   "total_reactions": 1,
#   "total_reports": 1
# }
```
- [ ] Stats endpoint works
- [ ] Shows total_reactions (not total_simulations)
- [ ] Shows total_reports
- [ ] Counts match expected values

---

## Phase 3: Database Verification

### 3.1 Check Database Records
Using SQLite viewer:

```sql
-- Check Reaction table
SELECT * FROM reaction;
-- Should show: id, person_id, scenario_id, stress_values, timestamp

-- Check Report table
SELECT * FROM report;
-- Should show: id, person_id, scenario_id, summary, recommendations, timestamp

-- Verify relationships
SELECT COUNT(*) FROM reaction WHERE person_id = <from 2.2>;
SELECT COUNT(*) FROM report WHERE scenario_id = <from 2.3>;
```

- [ ] Reaction records exist with person_id and scenario_id (no simulation_id)
- [ ] Report records exist with person_id and scenario_id (no simulation_id)
- [ ] Foreign key relationships are correct
- [ ] NO Simulation table exists!

---

## Phase 4: Frontend Verification ✅

### 4.1 Test Dashboard
- [ ] Load http://localhost:5173/dashboard
- [ ] Page loads without errors
- [ ] "Total Reactions" stat shows (should be 1 or more)
- [ ] "Total Reports" stat shows (should be 1 or more)
- [ ] NO "Total Simulations" stat visible
- [ ] Check browser console: no errors ✅

---

### 4.2 Test Simulation Runner Page
- [ ] Load http://localhost:5173/simulation-runner
- [ ] Page loads without errors

#### Check Sliders Present:
- [ ] Trauma Sensitivity slider (0-1)
- [ ] Emotional Regulation slider (0-1)
- [ ] Recovery Rate slider (0-1)
- [ ] Impulsivity slider (0-1)
- [ ] Coping Mechanism dropdown (4 options)

#### Check Functionality:
- [ ] Move trauma_sensitivity slider to 0.8
- [ ] Move emotional_regulation slider to 0.3
- [ ] Set coping_mechanism to "freezing"
- [ ] Select a person (use the one created in 2.2)
- [ ] Select a scenario (use the one created in 2.3)
- [ ] Click "Run Simulation" button
- [ ] Wait for results...

#### Check Results:
- [ ] Results appear on page
- [ ] Shows line graph of stress over time
- [ ] Shows final stress value
- [ ] Shows report text
- [ ] Check browser console: no errors ✅

---

### 4.3 Test Person Manager
- [ ] Load http://localhost:5173/person-manager
- [ ] Can create new person
- [ ] Can view person list
- [ ] Can update person
- [ ] Can delete person
- [ ] NO errors in console ✅

---

### 4.4 Test Scenario Manager
- [ ] Load http://localhost:5173/scenario-manager
- [ ] Can create new scenario
- [ ] Can view scenario list
- [ ] Can update scenario
- [ ] Can delete scenario
- [ ] NO errors in console ✅

---

### 4.5 Test Therapist Manager
- [ ] Load http://localhost:5173/therapist-manager
- [ ] Can create new therapist
- [ ] Can view therapist list
- [ ] Can update therapist
- [ ] Can delete therapist
- [ ] NO errors in console ✅

---

## Phase 5: Integration Test ✅

### 5.1 Complete Workflow
Follow this exact sequence:

1. [ ] Start with fresh database (deleted old one)
2. [ ] Create new therapist
3. [ ] Create new person linked to therapist
4. [ ] Create new scenario
5. [ ] Run simulation with slider values
6. [ ] Check Dashboard shows updated counts
7. [ ] Check new reaction in /reactions/ endpoint
8. [ ] Check new report in /reports/ endpoint
9. [ ] Verify database has no Simulation table
10. [ ] Verify person_id and scenario_id in reaction/report match

---

## Phase 6: Error Scenarios ✅

### 6.1 Test Missing Person
```bash
POST http://localhost:8000/simulations/
{
  "person_id": 9999,  # Does not exist
  "scenario_id": 1,
  ...
}
# Expected: 404 Not Found or similar error
```
- [ ] Returns appropriate error message

---

### 6.2 Test Missing Scenario
```bash
POST http://localhost:8000/simulations/
{
  "person_id": 1,
  "scenario_id": 9999,  # Does not exist
  ...
}
# Expected: 404 Not Found or similar error
```
- [ ] Returns appropriate error message

---

### 6.3 Test Invalid Slider Values
```bash
POST http://localhost:8000/simulations/
{
  "person_id": 1,
  "scenario_id": 1,
  "trauma_sensitivity": 1.5,  # Out of range (should be 0-1)
  ...
}
# Expected: 400 Bad Request or handles gracefully
```
- [ ] Returns appropriate error message

---

## Phase 7: Console Verification ✅

### 7.1 Backend Console (uvicorn terminal)
- [ ] No error messages
- [ ] No stack traces
- [ ] Shows request logs like: `POST /simulations/ 200 OK`
- [ ] Shows database connection messages

---

### 7.2 Frontend Console (browser DevTools)
- [ ] Open http://localhost:5173
- [ ] Open DevTools (F12)
- [ ] Go to Console tab
- [ ] No red error messages ✅
- [ ] No warnings about "Simulation" ✅
- [ ] Check all pages for errors

---

## Phase 8: Performance Check ✅

### 8.1 API Response Times
- [ ] POST /simulations/ takes < 5 seconds
- [ ] GET /reactions/ takes < 1 second
- [ ] GET /reports/ takes < 1 second
- [ ] GET /simulations/stats takes < 1 second

---

## Final Verification ✅

### All Systems Go?

Run this final test:

```bash
# Terminal 1: Check database schema
sqlite3 ptsd_simulation.db ".tables"
# Should show: person  reaction  report  scenario  therapist
# Should NOT show: simulation
```

- [ ] Database has exactly 5 tables
- [ ] No Simulation table present
- [ ] All foreign keys correct
- [ ] All endpoints responding
- [ ] Frontend shows correct UI
- [ ] No console errors
- [ ] Simulations run and create reactions/reports

---

## ✅ All Tests Pass?

If all checkboxes above are checked:

**Congratulations!** ✨

The schema restructuring is complete and verified:
- ✅ Simulation table removed
- ✅ 5-table schema working
- ✅ Direct person+scenario → reaction+report relationships
- ✅ Manual profile control working
- ✅ API endpoints updated
- ✅ Frontend updated
- ✅ No data loss
- ✅ No breaking changes for users

---

## Troubleshooting

### Issue: "Simulation table still exists"
**Solution**: 
1. Stop uvicorn
2. Delete ptsd_simulation.db
3. Restart uvicorn
4. Check database schema again

### Issue: "simulation_id not found error"
**Solution**: 
1. Check that models.py uses person_id and scenario_id (not simulation_id)
2. Restart uvicorn to reload code
3. Test again

### Issue: "Reactions endpoint returns 404"
**Solution**:
1. Check reaction.py router file exists
2. Check main.py has `app.include_router(reaction.router)`
3. Restart uvicorn
4. Test again

### Issue: "Console error about Simulation"
**Solution**:
1. Check frontend/src/pages/Dashboard.jsx doesn't reference simulations
2. Search for "simulation" in frontend (case-insensitive)
3. Update any remaining references
4. Refresh browser cache (Ctrl+Shift+Delete)

### Issue: "Dashboard shows wrong stats"
**Solution**:
1. Check schemas.py has updated Statistics response
2. Check crud.py returns total_reactions and total_reports
3. Check frontend/src/pages/Dashboard.jsx reads correct fields
4. Restart both backend and frontend

---

## Need Help?

Refer to documentation:
- **Schema questions**: See FINAL_SCHEMA.md
- **Code changes**: See DEPENDENCIES_CHANGED.md
- **What broke**: See WHAT_CHANGED.md
- **Overview**: See COMPLETE_SUMMARY.md
- **Quick lookup**: See QUICK_REFERENCE.md

---

## Success Criteria ✅

You've successfully verified the restructuring when:

1. Database has 5 tables (no Simulation)
2. All API endpoints respond correctly
3. Simulations create Reaction + Report records
4. Dashboard shows correct statistics
5. Frontend has no console errors
6. All CRUD operations work
7. Profile sliders work on frontend
8. Results display correctly

**Everything working? You're done! 🎉**
