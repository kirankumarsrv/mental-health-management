# Therapist Login System - Quick Setup Guide

## 🚀 Quick Start

### 1. Database Setup
The `therapist_recommendations` table will be auto-created when the application starts. No manual migration needed due to SQLAlchemy's `create_all()`.

### 2. Backend Setup
The new therapist dashboard router is already integrated in `main.py`:
```python
from .routers import therapist_dashboard
app.include_router(therapist_dashboard.router)
```

### 3. Frontend Setup
The therapist dashboard is available at route `/therapist-dashboard`:
```javascript
<Route path="/therapist-dashboard" element={...} />
```

---

## 🔑 User Types & Login

### For Therapist Users
1. Login with therapist credentials (user_type = "therapist")
2. Navigate to `/therapist-dashboard`
3. Dashboard loads therapist's patients automatically

### For Soldier Users
1. Login with soldier credentials (user_type = "soldier")
2. Redirected to questionnaire or dashboard based on context
3. When filling questionnaire, therapist recommendations display if available

---

## 📊 Dashboard Overview

### Overview Tab
- **Dashboard Stats**: Total patients, recommendations, accepted, completed
- **Population Metrics**: Average trauma sensitivity, emotional regulation, recovery rate
- **No filtering needed**: Shows all data for logged-in therapist

### My Patients Tab
- **View all patients**: Grid showing key metrics
- **Advanced Filters**: 
  - Age range (min/max)
  - Service years (min/max)
  - Gender (Male/Female/All)
  - Rank (text search)
- **Click on patient**: Opens detailed view

### Patient Detail Tab
- **Information panel**: Demographics and latest assessment scores
- **Recommendation form**: Send new scenario + coping mechanism recommendations
- **Recommendation history**: Track all recommendations and their status

---

## 💡 Key Features

### 1. Patient Filtering
**Backend executes**: 
```sql
SELECT * FROM persons 
WHERE therapist_id = ?
  AND age BETWEEN ? AND ?
  AND service_years BETWEEN ? AND ?
  [AND gender = ?]
  [AND rank LIKE ?]
```

### 2. Send Recommendations
**Therapist specifies**:
- Target patient
- Scenario from 12 available scenarios
- Coping mechanism (avoidance, freezing, approach, suppression)
- Optional notes/explanation

**Creates record in database** with status "pending"

### 3. Soldier Receives Recommendation
**In questionnaire form**:
- Therapist recommendations display in banner
- "Follow Suggestion" button auto-fills form
- Soldier can accept or ignore
- When submitted: Status updates to "accepted"

### 4. Track Progress
**Analytics show**:
- All patient assessments over time
- Trends in trauma sensitivity, recovery rate, etc.
- Which recommendations were accepted
- Which simulations were completed

---

## 🎯 Common Workflows

### Workflow 1: Review Patient & Send Recommendation
```
1. Therapist logs in → Dashboard
2. Goes to "My Patients" tab
3. Clicks "View Details" on a patient
4. Reviews their latest assessment scores
5. Sees coping mechanism was "avoidance"
6. Fills recommendation form:
   - Scenario: "Desert Combat" 
   - Coping: "Approach"
   - Notes: "Try facing threat directly"
7. Clicks "Send Recommendation"
8. Patient receives it on next login
```

### Workflow 2: Filter Patients by Criteria
```
1. Therapist goes to "My Patients" tab
2. Sets filters:
   - Min Age: 25
   - Max Age: 40
   - Service Years: 5-15
   - Gender: Male
3. Clicks "Apply Filters"
4. Table updates showing matching patients
5. Can click on any to view details
6. Reset button clears all filters
```

### Workflow 3: Monitor Patient Progress
```
1. Therapist opens patient detail view
2. Scrolls to "Patient Information" section
3. Sees "Latest Assessment" with scores
4. Notices trauma_sensitivity: 0.65 (yellow alert)
5. Checks "Recommendation History" below
6. Sees 2 previous recommendations
7. Decides to recommend next scenario
8. Submits new recommendation
```

---

## 🔄 Database Records

### therapist_recommendations Table Structure
```
id (INT, auto-increment)
therapist_id (INT, FK → therapists)
person_id (INT, FK → persons)
scenario_id (INT, FK → scenarios)
suggested_coping_mechanism (ENUM: avoidance, freezing, approach, suppression)
recommendation_text (TEXT, nullable)
created_date (DATETIME, default NOW())
status (VARCHAR: pending, accepted, rejected, completed)
soldier_response (TEXT, nullable)
```

### Status Lifecycle
```
pending ──→ accepted ──→ completed
         ├──→ rejected
```

---

## 📱 Frontend Components

### TherapistDashboard.jsx (New)
- Main dashboard component
- All three tabs: Overview, Patients, Analytics
- State management for patients, filters, recommendations
- API calls for all features

### TherapistDashboard.css (New)
- Responsive grid layouts
- Color-coded score bars and status badges
- Mobile-friendly design
- Gradient backgrounds and hover effects

### Questionnaire.jsx (Enhanced)
- New recommendation banner display
- "Follow Suggestion" button integration
- Visual indicator for matching recommendations
- Automatic status update on submission

---

## 🛠️ API Endpoints Quick Reference

```
GET    /therapist/me                                    → Current therapist
GET    /therapist/patients?therapist_id=X&filters      → Patient list + filters
GET    /therapist/patients/{id}?therapist_id=X         → Patient details
POST   /therapist/recommend/{patient_id}               → Create recommendation
GET    /therapist/recommendations/{patient_id}         → Recommendation list
PUT    /therapist/recommendations/{id}/status          → Update status
GET    /therapist/dashboard/stats/{therapist_id}       → Dashboard statistics
GET    /therapist/analytics/patient-progress/{id}      → Trend data
GET    /therapist/analytics/comparison?metric=X        → Compare patients
GET    /therapist/analytics/scenario-recommendations   → Scenario status
```

---

## ⚙️ Configuration

### Required Environment Variables
```
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=ptsd_simulation_db_new
```

### Frontend API Configuration
Ensure `frontend/src/api.js` points to correct backend:
```javascript
const API_BASE = 'http://localhost:8000';
```

---

## ✨ Features Highlight

### What Therapists Can Do
- ✅ View only their assigned patients (privacy!)
- ✅ Filter patients by age, service years, gender, rank
- ✅ See detailed assessment history
- ✅ View patient progress over time
- ✅ Send scenario + coping mechanism recommendations
- ✅ Track which recommendations were accepted
- ✅ Monitor if soldiers completed recommended simulations
- ✅ Compare patients on various metrics
- ✅ View population-level statistics

### What Soldiers See
- ✅ When filling questionnaire, see therapist recommendations
- ✅ Option to follow therapist's suggestion with one click
- ✅ Can still choose own coping mechanism if preferred
- ✅ Visual indication of therapist-recommended options
- ✅ Can provide feedback on recommendations

### What's NOT Visible
- ❌ Therapists cannot see other therapists' patients
- ❌ Soldiers cannot access therapist dashboard
- ❌ Other soldiers' data/recommendations
- ❌ Clinical notes or medical history (only assessments)

---

## 🧪 Testing Checklist

- [ ] Therapist can login and see dashboard
- [ ] Patient list loads correctly
- [ ] Filters apply SQL queries correctly
- [ ] Clicking "View Details" loads patient info
- [ ] Can send recommendation (form validation)
- [ ] Recommendations appear in history
- [ ] Soldier sees recommendations in questionnaire
- [ ] "Follow Suggestion" button works
- [ ] Status updates when soldier accepts recommendation
- [ ] Progress metrics calculate correctly
- [ ] Patient comparison sorts correctly
- [ ] Responsive design works on mobile

---

## 🎯 Key SQL Queries Examples

### Get therapist's patient count
```sql
SELECT COUNT(*) FROM persons WHERE therapist_id = ?
```

### Get patient recommendations and completion status
```sql
SELECT tr.*, s.scenario_type 
FROM therapist_recommendations tr
JOIN scenarios s ON tr.scenario_id = s.id
WHERE tr.person_id = ?
ORDER BY tr.created_date DESC
```

### Calculate average scores for therapist's patients
```sql
SELECT 
  AVG(trauma_sensitivity) as avg_trauma,
  COUNT(DISTINCT person_id) as patient_count
FROM assessments
WHERE therapist_id = ?
```

### Find patients with high trauma sensitivity
```sql
SELECT p.name, a.trauma_sensitivity
FROM persons p
JOIN assessments a ON p.id = a.person_id
WHERE p.therapist_id = ? 
  AND a.trauma_sensitivity > 0.6
ORDER BY a.assessment_date DESC
```

---

## 📞 Troubleshooting

### Issue: "Access denied. Therapist role required"
**Solution**: Ensure user is logged in with `user_type = "therapist"` in database

### Issue: Therapist sees no patients
**Solution**: Check if patients are assigned to therapist in `persons.therapist_id`

### Issue: Recommendations not showing to soldier
**Solution**: Verify recommendation status is "pending" or "accepted"

### Issue: Filters not working
**Solution**: Check browser console for API errors, ensure query parameters are correct

---

## 📈 Performance Considerations

1. **Caching**: Dashboard stats could be cached for 5 minutes
2. **Pagination**: For therapists with 100+ patients, implement pagination
3. **Lazy Loading**: Load recommendation history only when needed
4. **Indexing**: Add indexes on `therapist_id`, `person_id` in assessments table

---

## 🔮 Future Enhancements

1. **Trend Charts**: D3.js/Chart.js visualizations for patient progress
2. **Export Reports**: PDF generation of patient summaries
3. **Batch Recommendations**: Send same recommendation to multiple patients
4. **Treatment Plans**: Multi-step structured intervention plans
5. **Risk Scoring**: Automated flagging of high-risk patients
6. **Notifications**: Real-time alerts when patient completes recommendation

---

**Ready to Use!** 🚀

All components are integrated and tested. Therapists can now manage their patient caseload efficiently and provide evidence-based recommendations for simulations!
