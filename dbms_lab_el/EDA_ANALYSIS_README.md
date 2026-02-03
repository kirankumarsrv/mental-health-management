# PTSD Simulation Database - EDA & Analysis Tools

Complete analysis toolkit for the PTSD Simulation Database with comprehensive exploratory data analysis (EDA), visualizations, and person-specific profile generation.

## 📊 Files Overview

### 1. **Database_EDA_Analysis.ipynb** (Main Analysis Notebook)
Comprehensive Jupyter notebook with complete database analysis including:

- **Database Overview**: All tables, relationships, and data types
- **Demographics Analysis**: Age, rank, gender, service years distribution
- **Assessment Scores**: Trauma sensitivity, emotional regulation, recovery rate, impulsivity distributions
- **Reports Analysis**: PTSD symptom patterns (avoidance, re-experiencing, etc.)
- **Scenario & Reaction Analysis**: Engagement patterns and reaction distributions
- **Therapist Performance**: Workload metrics, experience, specialization analysis
- **Individual Person Profiles**: Detailed profiles for each participant
- **Questionnaire Analysis**: Response patterns by dimension and question type
- **Relationship Analysis**: Correlations between age, service years, and assessment scores
- **Interactive Visualizations**: Plotly-based interactive charts and dashboards
- **Summary Report**: Key findings and recommendations
- **Data Export**: CSV exports for presentations and external reporting

### 2. **person_profile_analyzer.py** (Person Profile Tool)
Python utility class for programmatic access to person profiles:

```python
from person_profile_analyzer import PersonProfileAnalyzer

analyzer = PersonProfileAnalyzer()

# Get comprehensive profile
profile = analyzer.get_person_profile(person_id=1)

# Pretty print profile
analyzer.print_profile(person_id=1)

# Search for person
results = analyzer.search_person("John")

# Get database statistics
stats = analyzer.get_comparison_stats()
```

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn sqlalchemy pymysql plotly python-dotenv
```

### Running the Notebook

1. Open `Database_EDA_Analysis.ipynb` in Jupyter
2. Run cells sequentially to generate analysis
3. Exported data will be saved to `analysis_results/` directory

### Using the Profile Analyzer

```python
# Import the analyzer
from person_profile_analyzer import PersonProfileAnalyzer

# Initialize
analyzer = PersonProfileAnalyzer()

# Get person's profile as dictionary
profile = analyzer.get_person_profile(person_id=1)

# Access components
basic_info = profile['basic_info']
assessments = profile['assessments']
scenarios = profile['scenarios']
statistics = profile['statistics']
```

## 📈 Analysis Sections

### Demographics
- Age range, distribution, and statistics
- Rank and gender breakdown
- Service years analysis
- Therapist assignment coverage

### Psychological Assessment Scores
- **Trauma Sensitivity**: How sensitive to trauma-related triggers
- **Emotional Regulation**: Ability to manage emotions
- **Recovery Rate**: Speed of psychological recovery
- **Impulsivity**: Behavioral impulse control

### Clinical Reports
- PTSD symptom dimensions:
  - Avoidance behaviors
  - Re-experiencing symptoms
  - Negative cognitive/mood alterations
  - Hyperarousal/hypervigilance

### Scenarios
- Simulation types and environments
- Participant engagement rates
- Reaction triggering patterns

### Therapist Metrics
- Patient caseloads
- Assigned scenarios
- Experience levels
- Specializations

## 📊 Key Visualizations

1. **Demographics Distribution**: Age, service years, rank, gender
2. **Assessment Score Distributions**: Histograms with means
3. **Correlation Heatmaps**: Score relationships
4. **Interactive Scatter Plots**: Age vs scores with interactive filtering
5. **Box Plots**: Score distributions by demographic groups
6. **Scenario Analysis**: Participants and reactions per scenario
7. **Therapist Workload**: Patient and scenario assignments
8. **Response Patterns**: Questionnaire dimensions and types
9. **Relationship Trends**: Age/service years vs recovery metrics
10. **Interactive Dashboards**: Plotly-based exploration tools

## 💾 Data Export

The notebook automatically exports analysis results to `analysis_results/` directory:

- `persons_with_assessments.csv` - Person demographics with latest scores
- `assessment_by_demographics.csv` - Statistics grouped by gender and rank
- `therapist_performance.csv` - Therapist workload and metrics
- `scenario_analysis.csv` - Scenario participation and reaction data
- `responses_by_dimension.csv` - Assessment response statistics
- `reports_summary.csv` - Clinical report summaries

## 🔍 Using Profiles for Web Dashboard

The `PersonProfileAnalyzer` is designed to integrate with your web application:

### Example: Flask Integration
```python
from flask import Flask, jsonify
from person_profile_analyzer import PersonProfileAnalyzer

app = Flask(__name__)
analyzer = PersonProfileAnalyzer()

@app.route('/api/person/<int:person_id>')
def get_person_profile(person_id):
    profile = analyzer.get_person_profile(person_id)
    return jsonify(profile)

@app.route('/api/persons')
def list_persons():
    return jsonify(analyzer.get_persons_list())

@app.route('/api/search')
def search_persons():
    query = request.args.get('q', '')
    results = analyzer.search_person(query)
    return jsonify(results)

@app.route('/api/stats')
def get_stats():
    return jsonify(analyzer.get_comparison_stats())
```

### Example: FastAPI Integration
```python
from fastapi import FastAPI
from person_profile_analyzer import PersonProfileAnalyzer

app = FastAPI()
analyzer = PersonProfileAnalyzer()

@app.get("/api/person/{person_id}")
async def get_person(person_id: int):
    return analyzer.get_person_profile(person_id)

@app.get("/api/persons")
async def list_persons():
    return analyzer.get_persons_list()
```

## 📋 Person Profile Structure

```python
{
    "basic_info": {
        "id": 1,
        "name": "John Doe",
        "rank": "Captain",
        "age": 35,
        "gender": "Male",
        "service_years": 12
    },
    "therapist": {
        "assigned": True,
        "id": 1,
        "name": "Dr. Smith",
        "specialization": "PTSD",
        "experience_years": 15
    },
    "assessments": {
        "count": 3,
        "latest": {
            "trauma_sensitivity": 0.65,
            "emotional_regulation": 0.72,
            "recovery_rate": 0.68,
            "impulsivity": 0.45,
            "coping_mechanism": "approach"
        },
        "assessments": [...]
    },
    "scenarios": {
        "count": 5,
        "scenarios": [...]
    },
    "reactions": {
        "count": 8,
        "reactions": [...]
    },
    "reports": {
        "count": 2,
        "reports": [...]
    },
    "statistics": {
        "total_scenarios": 5,
        "total_reactions": 8,
        "total_assessments": 3,
        "total_reports": 2,
        "assessment_trends": {...}
    }
}
```

## 🎯 Use Cases

1. **Clinical Dashboard**: Display individual person profiles for therapists
2. **Progress Tracking**: Monitor assessment score trends over time
3. **Population Analysis**: Understand cohort demographics and patterns
4. **Report Generation**: Export data for clinical reports and presentations
5. **Research**: Statistical analysis of PTSD treatment outcomes
6. **Quality Assurance**: Monitor therapist workload and performance

## 📝 Notes

- The notebook is designed for presentation to external stakeholders
- All visualizations are publication-ready
- Data exports are CSV format for easy use in Excel/PowerPoint
- Person profiles can be cached for performance
- Analysis assumes all relationships are properly set up in the database

## 🔧 Troubleshooting

**Database Connection Error**
- Ensure MySQL is running
- Check `.env` file for correct credentials
- Verify database name matches `MYSQL_DATABASE` variable

**Missing Data in Profiles**
- Check if foreign keys are properly set
- Verify related records exist in database
- Some fields may be NULL in your data

**Performance Issues**
- Limit analysis to specific date ranges for large datasets
- Use database indexes on frequently queried columns
- Cache results for repeated queries

## 📞 Support

For questions about analysis or integration:
1. Check database schema documentation
2. Review the notebook cells for detailed explanations
3. Examine `person_profile_analyzer.py` source code for API details

---

**Created**: February 2026  
**Database**: PTSD Simulation DB  
**Purpose**: Comprehensive EDA and Clinical Analysis
