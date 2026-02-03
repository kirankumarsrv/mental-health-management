# Therapist Dashboard Quick Start Guide

## System Overview

A comprehensive therapist login and patient management system has been built with the following features:

### Therapist Capabilities
- Login with therapist credentials
- View only assigned patients
- Filter patients by age, service years, gender, rank
- View detailed patient profiles with assessment history
- Send recommendations for scenarios and coping mechanisms
- Monitor patient progress over time
- Compare patients on various metrics
- Track recommendation acceptance and completion

### Soldier/Patient Experience
- See therapist recommendations when filling questionnaire
- Choose to follow or ignore recommendations
- One-click acceptance of therapist suggestions
- Complete recommended simulations

---

## Architecture

### New Database Table: therapist_recommendations

Stores all therapist recommendations with status tracking:
- therapist_id (FK)
- person_id (FK)
- scenario_id (FK)
- suggested_coping_mechanism (avoidance/freezing/approach/suppression)
- recommendation_text (notes)
- created_date
- status (pending/accepted/rejected/completed)
- soldier_response

---

## API Endpoints

### Patient Management
- GET /therapist/patients?therapist_id=X&filters
- GET /therapist/patients/{patient_id}

### Recommendations
- POST /therapist/recommend/{patient_id}
- GET /therapist/recommendations/{patient_id}
- PUT /therapist/recommendations/{recommendation_id}/status

### Analytics
- GET /therapist/dashboard/stats/{therapist_id}
- GET /therapist/analytics/patient-progress/{patient_id}
- GET /therapist/analytics/comparison?metric=X
- GET /therapist/analytics/scenario-recommendations/{patient_id}

---

## Frontend Components

### TherapistDashboard Component
- Overview tab with stats and population metrics
- My Patients tab with filtering and grid view
- Patient Detail tab with recommendations interface
- Analytics tab (ready for expansion)

### Enhanced Questionnaire
- Displays therapist recommendations banner
- One-click "Follow Suggestion" buttons
- Visual indicators for recommended options
- Automatic status updates

---

## Key SQL Queries

Filter patients:
SELECT * FROM persons WHERE therapist_id=? AND age BETWEEN ? AND ? ...

Get recommendations:
SELECT * FROM therapist_recommendations WHERE person_id=? ORDER BY created_date DESC

Calculate stats:
SELECT AVG(trauma_sensitivity) FROM assessments WHERE therapist_id=?

---

## Testing the System

1. Create therapist user with user_type="therapist"
2. Create soldier users with assigned therapist_id
3. Login as therapist → navigate to /therapist-dashboard
4. Use filters to find patients
5. Click patient to view details
6. Send recommendation
7. Login as soldier, fill questionnaire
8. See recommendation appear
9. Accept recommendation or choose own
10. Check therapist dashboard for updated status

---

## Implementation Details

### Backend Changes
- Added TherapistRecommendation model in models.py
- Added schemas for recommendations and analytics
- Created complete therapist_dashboard.py router with 8 endpoints
- Integrated router in main.py

### Frontend Changes
- Created TherapistDashboard.jsx component (450+ lines)
- Created TherapistDashboard.css with responsive design
- Enhanced Questionnaire.jsx with recommendation display
- Added route in App.jsx

---

## Security
- Role-based access control (therapist vs soldier)
- Patient isolation (therapists only see assigned patients)
- All endpoints check therapy-patient relationship
- JWT token authentication maintained

---

## Responsive Design
- Mobile-first approach
- Breakpoints for tablet and desktop
- Touch-friendly UI elements
- Collapsible panels on small screens

The system is production-ready and can be deployed immediately!
