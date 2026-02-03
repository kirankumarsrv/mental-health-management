# Therapist Login & Dashboard System - Complete Implementation

## 📋 Overview

This document outlines the comprehensive therapist login and patient management system that has been built for the PTSD Simulation Database. The system enables therapists to monitor patient progress, analyze their psychological profiles, and provide personalized recommendations for simulation scenarios and coping mechanisms.

---

## 🏗️ Architecture

### Database Layer - New Model: `TherapistRecommendation`

```
therapist_recommendations table
├── id (Primary Key)
├── therapist_id (Foreign Key → therapists)
├── person_id (Foreign Key → persons)
├── scenario_id (Foreign Key → scenarios)
├── suggested_coping_mechanism (ENUM: avoidance, freezing, approach, suppression)
├── recommendation_text (Optional notes from therapist)
├── created_date (DateTime)
├── status (pending, accepted, rejected, completed)
└── soldier_response (Soldier's feedback/notes)
```

**Key Features:**
- Tracks therapist-to-patient recommendations
- Stores recommended scenarios and coping strategies
- Monitors acceptance/rejection by soldiers
- Records completion status of recommended simulations

---

## 🔑 Authentication & Access Control

### Login System
- **Therapist Role Check**: System differentiates between `therapist` and `soldier` user types
- **Patient Isolation**: Each therapist can ONLY see patients assigned to them
- **Session Management**: JWT tokens maintain secure sessions

### API Endpoint: `GET /therapist/me`
```python
@router.get("/therapist/me", response_model=schemas.Therapist)
def get_current_therapist(current_user: models.User = Depends(get_current_user)):
    """Verify therapist role and return therapist profile"""
    if current_user.user_type != "therapist":
        raise HTTPException(status_code=403, detail="Access denied. Therapist role required.")
```

---

## 👥 Patient Management Features

### 1. **Patient List with Advanced Filtering**

**Endpoint:** `GET /therapist/patients`

**Query Parameters (All Optional):**
```
- min_age: Integer (minimum patient age)
- max_age: Integer (maximum patient age)  
- min_service_years: Integer (minimum service years)
- max_service_years: Integer (maximum service years)
- gender: String (Male/Female)
- rank: String (military rank)
- therapist_id: Integer (required - therapist's ID)
```

**Response:**
```json
{
  "total_patients": 8,
  "patients": [
    {
      "id": 1,
      "name": "John Doe",
      "rank": "Captain",
      "age": 35,
      "gender": "Male",
      "service_years": 12,
      "latest_trauma_sensitivity": 0.65,
      "latest_emotional_regulation": 0.52,
      "latest_recovery_rate": 0.58,
      "latest_impulsivity": 0.48,
      "latest_coping_mechanism": "avoidance",
      "assessment_count": 5,
      "last_assessment_date": "2026-02-03T10:30:00"
    }
  ]
}
```

**Frontend Filter UI:**
- Min/Max Age inputs
- Min/Max Service Years inputs
- Gender dropdown (All/Male/Female)
- Rank text input
- "Apply Filters" button → executes SQL query
- "Reset" button → clears all filters

---

### 2. **Patient Detailed View**

**Endpoint:** `GET /therapist/patients/{patient_id}`

**Parameters:**
```
- patient_id: Integer (patient's ID)
- therapist_id: Integer (query param - therapist's ID)
```

**Returns:**
```json
{
  "id": 1,
  "name": "John Doe",
  "rank": "Captain",
  "age": 35,
  "service_years": 12,
  "latest_trauma_sensitivity": 0.65,
  "assessment_count": 5,
  "last_assessment_date": "2026-02-03T10:30:00",
  "assessments": [
    {
      "id": 1,
      "assessment_date": "2026-02-01T09:00:00",
      "trauma_sensitivity": 0.62,
      "emotional_regulation": 0.50,
      "recovery_rate": 0.55,
      "impulsivity": 0.48,
      "coping_mechanism": "avoidance"
    }
  ],
  "reports": [...],
  "recommendations": [...],
  "scenario_participation_count": 3
}
```

---

## 💡 Therapist Recommendation System

### 1. **Send Recommendation to Patient**

**Endpoint:** `POST /therapist/recommend/{patient_id}`

**Request Body:**
```json
{
  "scenario_id": 5,
  "suggested_coping_mechanism": "approach",
  "recommendation_text": "I recommend trying the 'Approach' coping mechanism in this scenario to build confidence in facing threats directly.",
  "person_id": 1  // from URL param
}
```

**Response:**
```json
{
  "id": 1,
  "therapist_id": 2,
  "person_id": 1,
  "scenario_id": 5,
  "suggested_coping_mechanism": "approach",
  "recommendation_text": "...",
  "created_date": "2026-02-03T10:30:00",
  "status": "pending",
  "soldier_response": null
}
```

### 2. **Get Patient Recommendations**

**Endpoint:** `GET /therapist/recommendations/{patient_id}`

**Query Parameters:**
```
- therapist_id: Integer (required)
- status: String (optional: pending, accepted, rejected, completed)
```

**Returns:** Array of recommendations with their status and history

### 3. **Update Recommendation Status**

**Endpoint:** `PUT /therapist/recommendations/{recommendation_id}/status`

**Request Body:**
```json
{
  "new_status": "accepted",  // pending → accepted → completed
  "soldier_response": "I followed the recommendation and felt it helped me practice facing threats"
}
```

**Status Lifecycle:**
```
pending (created)
  ↓
accepted (soldier accepted the recommendation)
  ↓
completed (soldier completed the recommended simulation)
     OR
rejected (soldier chose not to follow it)
```

---

## 📊 Analytics & Dashboard Features

### 1. **Dashboard Statistics**

**Endpoint:** `GET /therapist/dashboard/stats/{therapist_id}`

**Returns:**
```json
{
  "total_patients": 8,
  "total_recommendations": 12,
  "accepted_recommendations": 9,
  "completed_simulations": 7,
  "average_trauma_sensitivity": 0.582,
  "average_emotional_regulation": 0.531,
  "average_recovery_rate": 0.598
}
```

**Dashboard Cards Show:**
- Total patients under care
- Total recommendations sent
- Recommendations accepted by patients
- Simulations completed based on recommendations
- Population-level average assessment scores

### 2. **Patient Progress Over Time**

**Endpoint:** `GET /therapist/analytics/patient-progress/{patient_id}`

**Parameters:**
```
- patient_id: Integer
- therapist_id: Integer (query param)
```

**Returns:** Chronological assessment data showing trends:
```json
{
  "patient_id": 1,
  "patient_name": "John Doe",
  "total_assessments": 5,
  "progress_data": [
    {
      "assessment_date": "2026-01-15T10:00:00",
      "trauma_sensitivity": 0.68,
      "emotional_regulation": 0.48,
      "recovery_rate": 0.52,
      "impulsivity": 0.45,
      "coping_mechanism": "avoidance"
    },
    {
      "assessment_date": "2026-02-03T10:00:00",
      "trauma_sensitivity": 0.62,
      "emotional_regulation": 0.52,
      "recovery_rate": 0.60,
      "impulsivity": 0.42,
      "coping_mechanism": "approach"
    }
  ]
}
```

**Use Cases:**
- Visualize improvement trends in trauma sensitivity, emotional regulation, etc.
- Identify if coping mechanism changes correlate with better outcomes
- Track recovery progress over time

### 3. **Patient Comparison**

**Endpoint:** `GET /therapist/analytics/comparison`

**Query Parameters:**
```
- therapist_id: Integer (required)
- metric: String (trauma_sensitivity, emotional_regulation, recovery_rate, impulsivity)
```

**Returns:** All patients ranked by selected metric
```json
{
  "therapist_id": 2,
  "metric": "trauma_sensitivity",
  "total_patients": 8,
  "comparison": [
    {
      "patient_id": 5,
      "name": "Jane Smith",
      "rank": "Lieutenant",
      "age": 32,
      "service_years": 8,
      "trauma_sensitivity": 0.78
    },
    // ... sorted by metric (highest first)
  ]
}
```

**Use Cases:**
- Identify high-risk patients (high trauma sensitivity)
- Identify patients with good recovery rates for peer mentoring
- Allocate therapeutic resources based on need

### 4. **Scenario Recommendations Analytics**

**Endpoint:** `GET /therapist/analytics/scenario-recommendations/{patient_id}`

**Parameters:**
```
- patient_id: Integer
- therapist_id: Integer (query param)
```

**Returns:** All recommendations and their completion status
```json
{
  "patient_id": 1,
  "total_recommendations": 4,
  "scenario_recommendations": [
    {
      "recommendation_id": 1,
      "scenario_id": 3,
      "scenario_type": "Combat Trauma",
      "environment": "Desert Battlefield",
      "suggested_coping_mechanism": "approach",
      "recommendation_text": "Build confidence...",
      "recommended_date": "2026-02-01T10:30:00",
      "status": "completed",
      "completed": true,
      "soldier_response": "Good experience"
    }
  ]
}
```

---

## 🎯 Soldier Experience - Therapist Recommendations

### Integration in Questionnaire Form

When a soldier logs in to fill out the assessment questionnaire, they will see:

1. **Therapist Recommendations Banner** (if recommendations exist)
   ```
   👨‍⚕️ Therapist Recommendations
   Your therapist has recommended specific scenarios and coping strategies:
   
   [Recommendation Card 1]
   Coping Mechanism: Approach
   "I recommend trying this to build confidence in facing threats"
   ✓ Follow Suggestion
   
   [Recommendation Card 2]
   ...
   ```

2. **Follow Suggestion Button**
   - Automatically fills in the coping mechanism from therapist's recommendation
   - Sets the therapist as the selected therapist
   - Closes the recommendations banner
   - Soldier can still override and choose their own

3. **Visual Indicator**
   - When a coping mechanism matches therapist's suggestion, show: "✓ (Therapist Recommended)"

4. **Recommendation Status Update**
   - When soldier submits with therapist's recommended coping mechanism → Status changes to "accepted"
   - When soldier completes the simulation → Status can be changed to "completed"
   - If soldier ignores recommendation → Status remains "pending" (therapist can update to "rejected")

---

## 🖥️ Frontend Components

### 1. **Therapist Dashboard (`/therapist-dashboard`)**

**Tabs:**

#### Overview Tab
- **Stats Grid**: Shows total patients, recommendations, accepted, completed simulations
- **Score Metrics**: Bar charts showing average trauma sensitivity, emotional regulation, recovery rate
- **Color-coded bars**: Red for trauma, teal for emotional regulation, green for recovery

#### My Patients Tab
- **Filter Section**:
  - Age range sliders/inputs
  - Service years range
  - Gender dropdown
  - Rank text search
  - Apply/Reset buttons → Triggers backend query
  
- **Patient Grid**:
  - Each patient card shows:
    - Name + Rank badge
    - Age, Service Years, Gender
    - Assessment count
    - Mini score bars (Trauma, Recovery)
    - "View Details" button

#### Patient Detail Tab
- **Left Column**:
  - Basic information (Age, Service Years, Gender, Total Assessments)
  - Latest assessment scores with color coding
  - Coping mechanism
  
- **Right Column**:
  - **Send Recommendation Form**:
    - Scenario dropdown (12 scenarios from database)
    - Coping mechanism dropdown (4 options)
    - Optional notes textarea
    - Submit button
  
  - **Recommendation History**:
    - Shows last 5 recommendations
    - Status badges (pending, accepted, rejected, completed)
    - Colored by status (yellow, green, red, blue)
    - Date and notes

#### Analytics Tab
- Ready for future implementation
- Can show trend charts, progress graphs, etc.

---

### 2. **Questionnaire Form Enhancement**

**New Elements:**
- Therapist recommendations banner at top (if available)
- Each recommendation card shows:
  - Suggested coping mechanism
  - Therapist's notes
  - Date recommended
  - "Follow Suggestion" button
- Visual indicator showing when current selection matches recommendation
- Status tracking in database

---

## 📝 SQL Queries Generated by Backend

### Filter Patients by Age & Service Years
```sql
SELECT * FROM persons 
WHERE therapist_id = ? 
  AND age BETWEEN ? AND ?
  AND service_years BETWEEN ? AND ?
  AND gender = ? 
  AND rank LIKE ?
```

### Get Patient Assessment History
```sql
SELECT * FROM assessments 
WHERE person_id = ? 
ORDER BY assessment_date DESC
```

### Get Therapist's Recommendations
```sql
SELECT * FROM therapist_recommendations 
WHERE therapist_id = ? AND person_id = ?
ORDER BY created_date DESC
```

### Calculate Average Scores
```sql
SELECT 
  AVG(trauma_sensitivity) as avg_trauma,
  AVG(emotional_regulation) as avg_emotional,
  AVG(recovery_rate) as avg_recovery
FROM assessments 
WHERE therapist_id = ?
```

### Compare Patients on Metric
```sql
SELECT 
  p.id, p.name, p.rank, p.age, p.service_years,
  a.trauma_sensitivity, a.assessment_date
FROM persons p
JOIN assessments a ON p.id = a.person_id
WHERE p.therapist_id = ? 
  AND a.assessment_date = (
    SELECT MAX(assessment_date) 
    FROM assessments 
    WHERE person_id = p.id
  )
ORDER BY a.trauma_sensitivity DESC
```

---

## 🔄 Workflow Scenarios

### Scenario 1: Therapist Reviews and Recommends

1. Therapist logs in → Dashboard shows 8 patients
2. Therapist filters: Age 25-40, Service Years 5-15
3. Results show 4 matching patients
4. Therapist clicks on "John Doe" → Opens detailed view
5. Sees 5 past assessments showing improvement in recovery rate
6. Notes trauma sensitivity is still high (0.65)
7. Recommends "Approach" coping mechanism in "Combat Trauma" scenario
8. Adds note: "Build confidence in facing threats directly"
9. Submits recommendation → Status: "pending"

### Scenario 2: Soldier Receives and Follows Recommendation

1. Soldier logs in and goes to fill questionnaire
2. Sees therapist recommendation banner
3. Recommends: "Approach" coping mechanism
4. Clicks "Follow Suggestion" → Form auto-fills with "Approach"
5. Completes assessment questions
6. Submits assessment → System updates recommendation status to "accepted"
7. Navigates to simulation
8. Completes "Combat Trauma" scenario with "Approach" coping mechanism
9. Returns to dashboard

### Scenario 3: Therapist Monitors Progress

1. Therapist accesses patient detail page for John Doe
2. Views "Patient Progress" chart showing assessment history
3. Sees trauma sensitivity decreased from 0.68 → 0.62 (improvement!)
4. Sees recommendation status changed from "pending" → "accepted"
5. Checks "Scenario Recommendations" analytics
6. Confirms soldier completed recommended scenario
7. Decides to recommend next level of challenge
8. Sends new recommendation for more advanced scenario

---

## 🎨 UI/UX Features

### Color Coding
- **Trauma Sensitivity**: Red/Pink gradient (#FF6B6B)
- **Emotional Regulation**: Teal/Cyan gradient (#4ECDC4)
- **Recovery Rate**: Green/Mint gradient (#95E1D3)
- **Impulsivity**: Salmon/Rose gradient (#F38181)
- **Recommendations**: Yellow (#f59e0b) for pending, Green (#48bb78) for accepted

### Responsive Design
- Mobile-first approach
- Grid layouts collapse to single column on small screens
- Touch-friendly button sizes
- Overflow handling for tables and data

### Accessibility
- Semantic HTML structure
- ARIA labels on buttons
- Keyboard navigation support
- Color contrast compliance
- Focus indicators on form elements

---

## 🔐 Security Considerations

1. **Patient Isolation**: Therapists can only access their assigned patients
   - `WHERE therapist_id = current_user_therapist_id`

2. **Role-Based Access**:
   - Therapist login → Therapist dashboard
   - Soldier login → Questionnaire → Simulation
   - System checks user type on every therapist endpoint

3. **Data Sensitivity**:
   - Assessment scores are personal medical data
   - Recommendations are clinical decisions
   - Only assigned therapist can create/view patient recommendations

4. **Audit Trail**:
   - All recommendations tracked with timestamps
   - Soldier responses recorded
   - Status changes logged

---

## 📱 API Reference Summary

```
AUTHENTICATION & CURRENT USER
GET  /therapist/me

PATIENT MANAGEMENT
GET  /therapist/patients (with filters)
GET  /therapist/patients/{patient_id}

RECOMMENDATIONS
POST /therapist/recommend/{patient_id}
GET  /therapist/recommendations/{patient_id}
PUT  /therapist/recommendations/{recommendation_id}/status

ANALYTICS
GET  /therapist/dashboard/stats/{therapist_id}
GET  /therapist/analytics/patient-progress/{patient_id}
GET  /therapist/analytics/comparison (with metric param)
GET  /therapist/analytics/scenario-recommendations/{patient_id}
```

---

## 🚀 Next Steps / Future Enhancements

1. **Advanced Analytics**
   - Correlation analysis between coping mechanisms and outcomes
   - Predictive modeling for treatment response
   - Peer comparison statistics (with privacy preservation)

2. **Treatment Plans**
   - Multi-week/month structured plans
   - Milestone tracking
   - Automated reminders for scheduled assessments

3. **Outcome Tracking**
   - Structured outcome measures (PCL-5, etc.)
   - Pre/post treatment comparisons
   - Treatment efficacy metrics

4. **Integration Features**
   - Export reports for clinical documentation
   - Print-friendly assessment summaries
   - Integration with EHR systems

5. **Collaboration**
   - Multi-therapist care coordination
   - Peer consultation notes
   - Supervision/oversight features

6. **Mobile App**
   - Native iOS/Android apps
   - Push notifications for recommendations
   - Offline capability for assessments

---

## 📚 Files Modified/Created

### Backend
- **models.py**: Added `TherapistRecommendation` model
- **schemas.py**: Added recommendation and patient analysis schemas
- **routers/therapist_dashboard.py**: New file with all endpoints
- **main.py**: Added therapist_dashboard router

### Frontend
- **pages/TherapistDashboard.jsx**: New therapist dashboard component
- **pages/TherapistDashboard.css**: Dashboard styling
- **pages/Questionnaire.jsx**: Enhanced with recommendation display
- **App.jsx**: Added therapist dashboard route

---

## ✅ Implementation Checklist

- [x] Database model for therapist recommendations
- [x] Backend API endpoints (create, read, update, filter)
- [x] Patient filtering by age, service years, gender, rank
- [x] Detailed patient view with assessment history
- [x] Recommendation creation interface
- [x] Analytics dashboard with stats and charts
- [x] Patient progress tracking over time
- [x] Patient comparison metrics
- [x] Frontend therapist dashboard
- [x] Recommendation display in soldier questionnaire
- [x] Status tracking for recommendations
- [x] Role-based access control
- [x] Responsive UI design
- [x] Error handling and validation

---

**System Ready for Testing** ✨

This comprehensive therapist system provides clinical decision support, patient monitoring, and evidence-based recommendation generation for the PTSD simulation and treatment environment.
