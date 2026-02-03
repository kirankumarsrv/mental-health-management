#!/usr/bin/env python
"""
Quick Start - Run this to test the analysis tools

Usage:
    python quick_start.py
"""

import sys
from person_profile_analyzer import PersonProfileAnalyzer

print("\n" + "="*80)
print("PTSD DATABASE ANALYSIS - QUICK START")
print("="*80 + "\n")

try:
    print("🔄 Initializing analyzer...")
    analyzer = PersonProfileAnalyzer()
    print("✅ Analyzer initialized successfully!\n")
    
    # Get database overview
    print("-" * 80)
    print("DATABASE OVERVIEW")
    print("-" * 80)
    print(f"📊 Total Persons:        {len(analyzer.persons)}")
    print(f"👨‍⚕️ Total Therapists:       {len(analyzer.therapists)}")
    print(f"🎬 Total Scenarios:       {len(analyzer.scenarios)}")
    print(f"⚡ Total Reactions:       {len(analyzer.reactions)}")
    print(f"📄 Total Reports:         {len(analyzer.reports)}")
    print(f"📊 Total Assessments:     {len(analyzer.assessments)}")
    print(f"❓ Total Questionnaires:   {len(analyzer.questionnaires)}")
    print(f"📝 Total Responses:       {len(analyzer.responses)}")
    
    # Get comparison stats
    print("\n" + "-" * 80)
    print("DATABASE STATISTICS")
    print("-" * 80)
    stats = analyzer.get_comparison_stats()
    print(f"Average Age:              {stats['avg_age']:.1f} years")
    print(f"Average Service Years:    {stats['avg_service_years']:.1f} years")
    print(f"Avg Trauma Sensitivity:   {stats['avg_trauma_sensitivity']:.3f}")
    print(f"Avg Emotional Regulation: {stats['avg_emotional_regulation']:.3f}")
    print(f"Avg Recovery Rate:        {stats['avg_recovery_rate']:.3f}")
    print(f"Avg Impulsivity:          {stats['avg_impulsivity']:.3f}")
    
    # Show sample persons
    print("\n" + "-" * 80)
    print("SAMPLE PERSONS (First 5)")
    print("-" * 80)
    persons = analyzer.get_persons_list()[:5]
    for p in persons:
        print(f"  • {p['name']:30} | Rank: {p['rank']:10} | Age: {p['age']:3d} | {p['gender']}")
    
    # Show detailed profile
    if len(persons) > 0:
        print("\n" + "-" * 80)
        print("DETAILED PROFILE EXAMPLE")
        print("-" * 80)
        first_id = analyzer.persons.iloc[0]['id']
        analyzer.print_profile(first_id)
    
    # API usage example
    print("-" * 80)
    print("PYTHON API USAGE EXAMPLES")
    print("-" * 80)
    print("""
# Get person profile as dictionary
profile = analyzer.get_person_profile(person_id=1)

# Search for persons
results = analyzer.search_person("John")

# Pretty print profile
analyzer.print_profile(person_id=1)

# Get all persons
all_persons = analyzer.get_persons_list()

# Get comparison statistics
stats = analyzer.get_comparison_stats()

# Integration with Flask/FastAPI
# See EDA_ANALYSIS_README.md for examples
    """)
    
    print("\n" + "="*80)
    print("✅ ALL SYSTEMS OPERATIONAL")
    print("="*80)
    print("""
NEXT STEPS:

1. Run the Jupyter Notebook:
   jupyter notebook Database_EDA_Analysis.ipynb

2. Review the analysis:
   - Demographics Analysis
   - Assessment Scores
   - Relationship Analysis
   - Person Profiles
   - Summary Report

3. Export CSV results:
   - Check analysis_results/ folder after running notebook

4. Integrate with website:
   - Add analytics_extended.py to backend/routers/
   - Import in main.py:
     from backend.routers.analytics_extended import router as analytics_router
     app.include_router(analytics_router, prefix="/api/analytics")

5. Create person profile dashboard:
   - Use /api/analytics/person/{person_id} endpoint
   - Display in React component

DOCUMENTATION:
   📖 EDA_ANALYSIS_README.md - Complete API reference
   📖 IMPLEMENTATION_GUIDE.md - Integration guide
    """)

except Exception as e:
    print(f"\n❌ Error initializing analyzer: {e}")
    print(f"   Make sure database is running and credentials are correct")
    sys.exit(1)
