import random
from . import schemas

def run_simulation(person: schemas.Person, scenario: schemas.Scenario):
    """
    Core Agent-Based Model Logic.
    Decides reactions based on Person attributes and Scenario details.
    """
    reactions = []
    
    # 1. Determine "Base Stress" based on Scenario
    base_stress = 0
    if "Ambush" in scenario.scenario_type or "High" in scenario.environment:
        base_stress = 80
    elif "Crowd" in scenario.scenario_type:
        base_stress = 50
    else:
        base_stress = 30

    # 2. Adjust based on Person (Agent Rules)
    # Rule: Higher service years -> Better discipline but potentially specific triggers
    stress_modifier = 0
    if person.service_years < 2:
        # Rookie: High stress response to danger
        stress_modifier = +20
    elif person.service_years > 10:
        # Veteran: Controlled response, but might have deep triggers
        stress_modifier = -10
    
    final_stress = base_stress + stress_modifier + random.randint(-10, 10)
    final_stress = max(0, min(100, final_stress))

    # 3. Generate Time-Series Reactions (3 Steps)
    # Step 1: Initial Contact
    r1_type = "Alert" if final_stress < 50 else "Startle"
    reactions.append({
        "reaction_type": r1_type,
        "physical_response": f"Heart Rate {60 + (final_stress // 2)} bpm"
    })

    # Step 2: Mid-Simulation Processing
    if final_stress > 80:
        r2_type = "Panic"
        phys = "Hyperventilation, Trembling"
    elif final_stress > 50:
        r2_type = "Defense Stance"
        phys = "Rapid Breathing, Sweating"
    else:
        r2_type = "Observation"
        phys = "Steady Breathing"
    
    reactions.append({
        "reaction_type": r2_type,
        "physical_response": phys
    })

    # Step 3: Resolution
    if final_stress > 90:
        r3_type = "Avoidance/Flight"
    elif final_stress > 60:
        r3_type = "Aggression/Fight"
    else:
        r3_type = "Calm Down"
    
    reactions.append({
        "reaction_type": r3_type,
        "physical_response": f"Final Stress Level: {final_stress}/100"
    })

    # 4. Generate Report Data
    report_data = {
        "avoidance": "High" if final_stress > 85 else "Low",
        "re_experiencing": "Yes" if person.service_years > 5 and final_stress > 60 else "No",
        "negative_alterations": "Moderate" if final_stress > 40 else "None",
        "hyperarousal": "Severe" if final_stress > 80 else "Mild",
        "recovery_readiness": "Low" if final_stress > 70 else "High"
    }

    return reactions, report_data
