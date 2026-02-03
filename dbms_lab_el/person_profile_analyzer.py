"""
Person Profile Analyzer - Quick Analysis Tool
Provides functions to analyze and display individual person profiles from the database
Useful for integrating with web dashboard to show person-specific analysis
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "ptsd_simulation_db")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)


class PersonProfileAnalyzer:
    """Analyze and generate comprehensive profiles for individual persons"""
    
    def __init__(self):
        """Initialize data from database"""
        self.persons = pd.read_sql("SELECT * FROM persons", engine)
        self.therapists = pd.read_sql("SELECT * FROM therapists", engine)
        self.scenarios = pd.read_sql("SELECT * FROM scenarios", engine)
        self.reactions = pd.read_sql("SELECT * FROM reactions", engine)
        self.reports = pd.read_sql("SELECT * FROM reports", engine)
        self.assessments = pd.read_sql("SELECT * FROM assessments", engine)
        self.participates = pd.read_sql("SELECT * FROM participates", engine)
        self.exhibits = pd.read_sql("SELECT * FROM exhibits", engine)
        self.questionnaires = pd.read_sql("SELECT * FROM questionnaires", engine)
        self.responses = pd.read_sql("SELECT * FROM responses", engine)
    
    def get_person_profile(self, person_id):
        """Get comprehensive profile for a specific person
        
        Args:
            person_id: ID of the person to analyze
            
        Returns:
            dict: Comprehensive profile data
        """
        person = self.persons[self.persons['id'] == person_id]
        if person.empty:
            return {"error": f"Person with ID {person_id} not found"}
        
        person_data = person.iloc[0]
        profile = {
            "basic_info": {
                "id": person_data['id'],
                "name": person_data['name'],
                "rank": person_data['rank'],
                "age": person_data['age'],
                "gender": person_data['gender'],
                "service_years": person_data['service_years']
            },
            "therapist": self._get_therapist_info(person_data['therapist_id']),
            "assessments": self._get_assessment_data(person_id),
            "scenarios": self._get_scenarios_data(person_id),
            "reactions": self._get_reactions_data(person_id),
            "reports": self._get_reports_data(person_id),
            "statistics": self._calculate_statistics(person_id)
        }
        return profile
    
    def _get_therapist_info(self, therapist_id):
        """Get therapist information"""
        if pd.isna(therapist_id):
            return {"assigned": False}
        
        therapist = self.therapists[self.therapists['id'] == therapist_id]
        if therapist.empty:
            return {"assigned": False}
        
        t = therapist.iloc[0]
        return {
            "assigned": True,
            "id": t['id'],
            "name": t['name'],
            "specialization": t['specialization'],
            "experience_years": t['years_of_experience']
        }
    
    def _get_assessment_data(self, person_id):
        """Get assessment scores and data"""
        person_assessments = self.assessments[self.assessments['person_id'] == person_id]
        
        if person_assessments.empty:
            return {"count": 0, "assessments": []}
        
        assessments_list = []
        for _, assess in person_assessments.iterrows():
            assessments_list.append({
                "id": assess['id'],
                "date": str(assess['assessment_date']),
                "trauma_sensitivity": float(assess['trauma_sensitivity']),
                "emotional_regulation": float(assess['emotional_regulation']),
                "recovery_rate": float(assess['recovery_rate']),
                "impulsivity": float(assess['impulsivity']),
                "coping_mechanism": assess['coping_mechanism']
            })
        
        # Get latest assessment
        latest = person_assessments.iloc[-1] if not person_assessments.empty else None
        
        return {
            "count": len(person_assessments),
            "latest": {
                "trauma_sensitivity": float(latest['trauma_sensitivity']) if latest is not None else None,
                "emotional_regulation": float(latest['emotional_regulation']) if latest is not None else None,
                "recovery_rate": float(latest['recovery_rate']) if latest is not None else None,
                "impulsivity": float(latest['impulsivity']) if latest is not None else None,
                "coping_mechanism": latest['coping_mechanism'] if latest is not None else None
            } if latest is not None else None,
            "assessments": assessments_list
        }
    
    def _get_scenarios_data(self, person_id):
        """Get scenario participation data"""
        person_scenarios = self.participates[self.participates['person_id'] == person_id]
        
        if person_scenarios.empty:
            return {"count": 0, "scenarios": []}
        
        scenarios_list = []
        for _, ps in person_scenarios.iterrows():
            scenario = self.scenarios[self.scenarios['id'] == ps['scenario_id']]
            if not scenario.empty:
                s = scenario.iloc[0]
                scenarios_list.append({
                    "id": s['id'],
                    "type": s['scenario_type'],
                    "environment": s['environment'],
                    "assigned_date": str(s['assigned_date']) if pd.notna(s['assigned_date']) else None
                })
        
        return {
            "count": len(scenarios_list),
            "scenarios": scenarios_list
        }
    
    def _get_reactions_data(self, person_id):
        """Get reaction data"""
        person_reactions = self.exhibits[self.exhibits['person_id'] == person_id]
        
        if person_reactions.empty:
            return {"count": 0, "reactions": []}
        
        reactions_list = []
        for _, pr in person_reactions.iterrows():
            reaction = self.reactions[self.reactions['id'] == pr['reaction_id']]
            if not reaction.empty:
                r = reaction.iloc[0]
                reactions_list.append({
                    "id": r['id'],
                    "type": r['r_type'],
                    "physical_response": r['physical_response']
                })
        
        return {
            "count": len(reactions_list),
            "reactions": reactions_list
        }
    
    def _get_reports_data(self, person_id):
        """Get clinical reports"""
        person_reports = self.reports[self.reports['person_id'] == person_id]
        
        if person_reports.empty:
            return {"count": 0, "reports": []}
        
        reports_list = []
        for idx, report in person_reports.iterrows():
            reports_list.append({
                "id": report['id'],
                "avoidance": report['avoidance'],
                "re_experiencing": report['re_experiencing'],
                "negative_alterations": report['negative_alterations'],
                "hyperarousal": report['hyperarousal']
            })
        
        return {
            "count": len(reports_list),
            "reports": reports_list
        }
    
    def _calculate_statistics(self, person_id):
        """Calculate statistics for the person"""
        person = self.persons[self.persons['id'] == person_id].iloc[0]
        person_assessments = self.assessments[self.assessments['person_id'] == person_id]
        
        stats = {
            "total_scenarios": len(self.participates[self.participates['person_id'] == person_id]),
            "total_reactions": len(self.exhibits[self.exhibits['person_id'] == person_id]),
            "total_assessments": len(person_assessments),
            "total_reports": len(self.reports[self.reports['person_id'] == person_id])
        }
        
        if not person_assessments.empty:
            stats["assessment_trends"] = {
                "avg_trauma_sensitivity": float(person_assessments['trauma_sensitivity'].mean()),
                "avg_emotional_regulation": float(person_assessments['emotional_regulation'].mean()),
                "avg_recovery_rate": float(person_assessments['recovery_rate'].mean()),
                "avg_impulsivity": float(person_assessments['impulsivity'].mean())
            }
        
        return stats
    
    def get_persons_list(self):
        """Get list of all persons"""
        return self.persons[['id', 'name', 'rank', 'age', 'gender']].to_dict('records')
    
    def search_person(self, query):
        """Search for person by name or rank"""
        results = self.persons[
            (self.persons['name'].str.contains(query, case=False, na=False)) |
            (self.persons['rank'].str.contains(query, case=False, na=False))
        ]
        return results[['id', 'name', 'rank', 'age', 'gender']].to_dict('records')
    
    def get_comparison_stats(self):
        """Get database-wide statistics for comparison"""
        person_assessments = self.persons.merge(self.assessments, left_on='id', right_on='person_id')
        
        return {
            "avg_age": float(self.persons['age'].mean()),
            "avg_service_years": float(self.persons['service_years'].mean()),
            "avg_trauma_sensitivity": float(person_assessments['trauma_sensitivity'].mean()),
            "avg_emotional_regulation": float(person_assessments['emotional_regulation'].mean()),
            "avg_recovery_rate": float(person_assessments['recovery_rate'].mean()),
            "avg_impulsivity": float(person_assessments['impulsivity'].mean()),
            "total_persons": len(self.persons),
            "total_assessments": len(self.assessments)
        }
    
    def print_profile(self, person_id):
        """Pretty print a person's profile"""
        profile = self.get_person_profile(person_id)
        
        if "error" in profile:
            print(f"❌ {profile['error']}")
            return
        
        basic = profile['basic_info']
        therapist = profile['therapist']
        assessments = profile['assessments']
        stats = profile['statistics']
        
        print("=" * 80)
        print(f"PROFILE: {basic['name'].upper()}")
        print("=" * 80)
        print(f"\n📋 BASIC INFORMATION:")
        print(f"  • ID: {basic['id']}")
        print(f"  • Rank: {basic['rank']}")
        print(f"  • Age: {basic['age']} years")
        print(f"  • Gender: {basic['gender']}")
        print(f"  • Service Years: {basic['service_years']}")
        
        if therapist['assigned']:
            print(f"\n👨‍⚕️ THERAPIST:")
            print(f"  • Name: {therapist['name']}")
            print(f"  • Specialization: {therapist['specialization']}")
            print(f"  • Experience: {therapist['experience_years']} years")
        else:
            print(f"\n👨‍⚕️ THERAPIST: Not assigned")
        
        if assessments['latest']:
            print(f"\n📊 LATEST ASSESSMENT:")
            latest = assessments['latest']
            print(f"  • Trauma Sensitivity: {latest['trauma_sensitivity']:.3f}")
            print(f"  • Emotional Regulation: {latest['emotional_regulation']:.3f}")
            print(f"  • Recovery Rate: {latest['recovery_rate']:.3f}")
            print(f"  • Impulsivity: {latest['impulsivity']:.3f}")
            print(f"  • Coping Mechanism: {latest['coping_mechanism']}")
            print(f"  • Total Assessments: {assessments['count']}")
        
        print(f"\n📈 ENGAGEMENT STATISTICS:")
        print(f"  • Scenarios Participated: {stats['total_scenarios']}")
        print(f"  • Reactions Exhibited: {stats['total_reactions']}")
        print(f"  • Clinical Reports: {stats['total_reports']}")
        
        if 'assessment_trends' in stats:
            print(f"\n📊 ASSESSMENT AVERAGES:")
            trends = stats['assessment_trends']
            print(f"  • Avg Trauma Sensitivity: {trends['avg_trauma_sensitivity']:.3f}")
            print(f"  • Avg Emotional Regulation: {trends['avg_emotional_regulation']:.3f}")
            print(f"  • Avg Recovery Rate: {trends['avg_recovery_rate']:.3f}")
            print(f"  • Avg Impulsivity: {trends['avg_impulsivity']:.3f}")
        
        print("=" * 80 + "\n")


if __name__ == "__main__":
    # Example usage
    analyzer = PersonProfileAnalyzer()
    
    # Print first person's profile
    print("All Persons in Database:")
    persons_list = analyzer.get_persons_list()
    for p in persons_list[:5]:
        print(f"  ID {p['id']}: {p['name']} ({p['rank']})")
    
    # Get detailed profile for first person
    if len(persons_list) > 0:
        first_person_id = persons_list[0]['id']
        analyzer.print_profile(first_person_id)
        
        # Get comparison stats
        print("\n" + "=" * 80)
        print("DATABASE COMPARISON STATISTICS")
        print("=" * 80)
        stats = analyzer.get_comparison_stats()
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"  • {key.replace('_', ' ').title()}: {value:.3f}")
            else:
                print(f"  • {key.replace('_', ' ').title()}: {value}")
