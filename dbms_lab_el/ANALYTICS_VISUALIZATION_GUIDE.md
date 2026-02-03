# Analytics Visualization Implementation Guide

## ✅ What's Been Implemented

### Frontend Analytics Dashboard (Person-Specific)
Your new Analytics page at `http://localhost:5173/analytics` now displays **personalized soldier analytics** with interactive Chart.js visualizations.

### Key Features

#### 1. **Automatic User Detection**
- When you log in as a soldier, the Analytics page automatically loads YOUR data (person-specific, not system-wide)
- Uses authenticated user's `person_id` from the login context
- Falls back gracefully if user profile not found

#### 2. **Interactive Charts**

**A. Radar Chart - Current Psychological Profile**
- Displays 4 key dimensions:
  - **Trauma Sensitivity**: Your sensitivity to trauma-related stimuli
  - **Emotional Regulation**: Ability to manage emotions
  - **Recovery Rate**: Speed of psychological recovery
  - **Impulsivity**: Impulse control capacity
- Shows your current assessment values (0.0-1.0 scale)
- Updated whenever you complete a new assessment

**B. Line Chart - Assessment Progression Over Time**
- Shows how your 4 dimensions change across multiple assessments
- Helps track improvement or decline trends
- Visible only if you have 2+ assessments
- Color-coded for easy distinction:
  - Red: Trauma Sensitivity
  - Green: Emotional Regulation
  - Blue: Recovery Rate
  - Orange: Impulsivity

**C. Bar Chart - Latest PTSD Symptom Severity**
- From your most recent simulation, shows 4 PTSD symptom areas:
  - **Avoidance** (Red): Avoiding trauma-related stimuli
  - **Re-Experiencing** (Orange): Intrusive memories/flashbacks
  - **Negative Alterations** (Yellow): Persistent negative emotions
  - **Hyperarousal** (Purple): Heightened startle response
- Automatically mapped from categorical report data (High/Yes/Moderate/Severe → numeric 0.0-1.0)

**D. Doughnut Chart - Activity Summary**
- Shows total assessments completed
- Shows total simulations run
- Quick visual summary of engagement

**E. Key Metrics Cards**
- Total assessments completed
- Total simulations run
- Current trauma sensitivity score

**F. Assessment History Table**
- Detailed table of all your assessments
- Shows all 4 dimension scores for each assessment
- Includes coping mechanism selected
- Sorted by most recent first

#### 3. **Visual Explanations**
Each chart includes explanatory text describing:
- What the data means
- How to interpret the values
- What actions the numbers suggest

---

## 🔄 Data Flow

```
Soldier Login
    ↓
useAuth() hook provides person_id
    ↓
GET /analytics/person/{person_id}
    ↓
Backend returns:
  - person_name
  - all assessments (with 4 dimension scores)
  - all reports (with PTSD symptom scores)
  - current_profile (latest assessment)
  - assessment_count
  - simulation_count
    ↓
Frontend renders:
  - 4 interactive Chart.js charts
  - Key metrics cards
  - Assessment history table
```

---

## 📊 Technical Details

### Backend Endpoint
```
GET /analytics/person/{person_id}
```
Returns JSON with:
- `person_name`: Soldier's name
- `person_id`: Unique person ID
- `rank`: Military rank
- `assessments`: Array of all assessments with:
  - `id`, `trauma_sensitivity`, `emotional_regulation`, `recovery_rate`, `impulsivity`
  - `coping_mechanism`, `created_at`
- `reports`: Array of all simulation reports with:
  - `avoidance_score`, `re_experiencing_score`, `negative_alterations_score`, `hyperarousal_score`
  - `assessment_id`, `created_at`
- `current_profile`: Latest assessment values
- `assessment_count`: Total assessments
- `simulation_count`: Total simulations

### Frontend Dependencies Added
```json
{
  "chart.js": "^4.4.0",
  "react-chartjs-2": "^5.2.0"
}
```

### Chart.js Components Used
- **Radar**: For psychological profile dimensions
- **Line**: For progression over time
- **Bar**: For PTSD symptom severity
- **Doughnut**: For activity summary

---

## 🎯 How to Use

### As a Soldier

1. **Register & Login**
   ```
   Username: your_username
   Password: your_password
   Role: Soldier
   ```

2. **Complete Assessment**
   - Go to "Take Assessment" (or `/questionnaire`)
   - Answer 20 psychological questions
   - System automatically calculates your profile

3. **Run Simulation**
   - Go to "Run Simulation" (or `/simulation`)
   - Simulation sliders auto-populate from your assessment
   - Simulation runs for 20 steps
   - Recovery Report generated

4. **View Analytics**
   - Go to "Analytics" (or `/analytics`)
   - See personalized charts and metrics
   - Track your psychological profile over time
   - Review symptom severity from latest simulation

### Repeat
- Complete another assessment for new data points
- Run another simulation to generate new reports
- Analytics automatically update with new data

---

## 📈 Example Scenarios

### Scenario 1: First Analytics View
- 1 assessment → Only radar chart shows current profile
- 0 simulations → No bar chart (no PTSD symptoms yet)
- Line chart hidden (need 2+ assessments)
- Activity shows 1 assessment, 0 simulations

### Scenario 2: After 2+ Assessments & 1+ Simulations
- Radar chart shows current profile
- Line chart shows progression trends
- Bar chart shows latest PTSD symptoms
- Doughnut chart shows activity counts
- Table shows all assessment history

### Scenario 3: Improvement Tracking
- Compare line chart trends across multiple assessments
- If trauma_sensitivity drops: Good, less trauma sensitivity
- If emotional_regulation rises: Good, better emotion management
- If hyperarousal in bar chart drops: Good, reduced hypervigilance

---

## 🔐 Security

- All analytics are **person-specific** using authenticated user's person_id
- Soldiers can only see their own analytics (enforced by backend)
- Therapists see system-wide analytics (separate endpoint)
- No sensitive data exposure across users

---

## 🚀 What's Next

### Optional Enhancements
1. **Export Reports**: Add button to download charts as PNG/PDF
2. **Comparison View**: Compare your profile to aggregate data
3. **Prediction**: Predict future severity based on trends
4. **Recommendations**: AI-generated treatment recommendations based on profile
5. **Therapist Insights**: Share specific charts with assigned therapist

### Visualizations Not Yet Implemented
- Confusion matrix (needs ML prediction model)
- Correlation heatmap (requires more diverse data)
- 3D scatter plot of cluster positions

---

## 🐛 Troubleshooting

### "Unable to load analytics: User profile not found"
- **Cause**: Login session lost or profile not loaded
- **Fix**: Log out and log back in

### "No analytics data available"
- **Cause**: Haven't completed any assessments yet
- **Fix**: Go to Questionnaire, complete assessment, then view Analytics

### Charts not showing
- **Cause**: Frontend dependencies not installed
- **Fix**: 
  ```bash
  cd frontend
  npm install chart.js react-chartjs-2
  ```

### "Failed to load analytics data for this soldier"
- **Cause**: Backend endpoint error or connection issue
- **Fix**: 
  1. Check backend is running: `uvicorn backend.main:app --reload`
  2. Check browser console (F12) for specific error
  3. Verify database has assessment data

---

## 📝 Files Modified

1. **frontend/src/pages/Analytics.jsx** - Complete rewrite with:
   - Person-specific analytics loading
   - Chart.js integration
   - 4 interactive visualizations
   - Explanatory text for each chart
   - Assessment history table

2. **frontend/package.json** - Added:
   - `chart.js@^4.4.0`
   - `react-chartjs-2@^5.2.0`

3. **No backend changes needed** - Existing endpoint already supports person-specific queries

---

## ✨ Summary

Your Analytics dashboard is now:
✅ **Person-specific** - Shows only your data when logged in
✅ **Interactive** - 4 different chart types for comprehensive analysis
✅ **Explanatory** - Each visualization includes interpretation guide
✅ **Real-time** - Updates automatically when new assessments/simulations complete
✅ **Responsive** - Works on desktop and mobile devices
✅ **Secure** - Only your data visible to you
