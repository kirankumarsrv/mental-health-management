# Predefined scenario and reaction catalogs used by the simulation router
# ASCII only; keep values concise for UI and backend consumption.

SCENARIO_CATALOG = [
    {
        "key": "urban_ambush",
        "scenario_type": "Urban Ambush",
        "environment": "High noise, crowded, hostile",
        "description": "Busy city street with sporadic gunfire and flashbang effects. High trigger density and intensity.",
        "intensity": "high",
        "recommended_grid": 10,
        "num_triggers": 8,
        "trigger_strength": 12,
    },
    {
        "key": "forest_patrol",
        "scenario_type": "Forest Patrol",
        "environment": "Low light, quiet, suspense",
        "description": "Dense forest with rustling foliage and low visibility. Moderate trigger density, lower intensity per trigger.",
        "intensity": "medium",
        "recommended_grid": 12,
        "num_triggers": 5,
        "trigger_strength": 8,
    },
    {
        "key": "marketplace_crowd",
        "scenario_type": "Marketplace",
        "environment": "Crowded, loud, neutral",
        "description": "Open market with loud vendors and unpredictable movement. Mid-level triggers focused on crowd proximity.",
        "intensity": "medium",
        "recommended_grid": 12,
        "num_triggers": 6,
        "trigger_strength": 9,
    },
    {
        "key": "convoy_escort",
        "scenario_type": "Convoy Escort",
        "environment": "Roadway, sporadic threats",
        "description": "Guarding a convoy through contested roads. Spread out triggers with occasional spikes in intensity.",
        "intensity": "medium-high",
        "recommended_grid": 14,
        "num_triggers": 7,
        "trigger_strength": 10,
    },
    {
        "key": "night_base_alarm",
        "scenario_type": "Night Base Alarm",
        "environment": "Low light, alarms, confusion",
        "description": "Forward operating base during a night alarm. Fewer triggers but strong intensity and disorientation.",
        "intensity": "high",
        "recommended_grid": 10,
        "num_triggers": 5,
        "trigger_strength": 13,
    },
    {
        "key": "ied_roadside",
        "scenario_type": "IED Roadside Blast",
        "environment": "Desert road, explosion aftermath",
        "description": "Simulated roadside improvised explosive device with sudden blast, debris, and smoke. Extremely high intensity triggers mimicking trauma re-exposure.",
        "intensity": "severe",
        "recommended_grid": 8,
        "num_triggers": 12,
        "trigger_strength": 15,
    },
    {
        "key": "casualty_evac",
        "scenario_type": "Casualty Evacuation",
        "environment": "Combat zone, medical emergency",
        "description": "High-stress medical scenario with wounded personnel. Emotional triggers related to responsibility and time pressure.",
        "intensity": "high",
        "recommended_grid": 10,
        "num_triggers": 6,
        "trigger_strength": 11,
    },
    {
        "key": "hostage_rescue",
        "scenario_type": "Hostage Rescue",
        "environment": "Building breach, close quarters",
        "description": "Dynamic building clearance with civilians present. Requires split-second decisions and precise movement in confined space.",
        "intensity": "high",
        "recommended_grid": 10,
        "num_triggers": 9,
        "trigger_strength": 12,
    },
    {
        "key": "defensive_position",
        "scenario_type": "Defensive Position Hold",
        "environment": "Fortified location, sustained attack",
        "description": "Holding defensive perimeter under prolonged assault. Repeated trigger exposures simulating sustained combat stress.",
        "intensity": "medium-high",
        "recommended_grid": 16,
        "num_triggers": 10,
        "trigger_strength": 9,
    },
    {
        "key": "lone_scout",
        "scenario_type": "Lone Scout Recon",
        "environment": "Isolated, enemy territory",
        "description": "Solo reconnaissance mission deep in hostile territory. Isolation and vulnerability create psychological pressure with sparse but high-impact triggers.",
        "intensity": "medium",
        "recommended_grid": 14,
        "num_triggers": 3,
        "trigger_strength": 14,
    },
    {
        "key": "friendly_fire",
        "scenario_type": "Friendly Fire Incident",
        "environment": "Chaos, confusion, betrayal",
        "description": "Complex scenario with unexpected threat from own unit. Tests emotional regulation under traumatic betrayal circumstances.",
        "intensity": "severe",
        "recommended_grid": 10,
        "num_triggers": 7,
        "trigger_strength": 14,
    },
    {
        "key": "misdirection_patrol",
        "scenario_type": "Training Misdirection",
        "environment": "Controlled, unexpected stressors",
        "description": "Training scenario with false alarms and misleading cues. Lower threat level but designed to test discernment and confidence.",
        "intensity": "low-medium",
        "recommended_grid": 10,
        "num_triggers": 4,
        "trigger_strength": 6,
    },
]

# Reaction catalog keyed by soldier status. Each entry provides detailed clinical observations.
REACTION_CATALOG = {
    "Calm": {
        "r_type": "Baseline State",
        "physical_response": "Respirations 12-16/min, controlled and deep; shoulders relaxed; visual scanning methodical and deliberate; muscle tension minimal; cognitive processing clear; situational awareness optimal"
    },
    "Alert": {
        "r_type": "Heightened Vigilance",
        "physical_response": "Heart rate 90-110 bpm; pupils dilated; rapid visual scanning for threats/cover; increased muscle tension in shoulders/neck; breathing shallow 20-24/min; hands near weapon ready position; hypervigilant to environmental cues"
    },
    "Panic": {
        "r_type": "Acute Stress Response",
        "physical_response": "Heart rate 130+ bpm; hyperventilation 30+ breaths/min; tunnel vision with peripheral awareness loss; tremors in extremities; decision-making impaired; disorganized movement patterns; fight-flight-freeze activation; verbal communication difficulty; sweating profuse"
    },
    "Recovered": {
        "r_type": "Post-Stress Stabilization",
        "physical_response": "Controlled breathing exercises initiated; heart rate decreasing; muscle tension releasing; cognitive function restoring; grounding techniques applied; situational reassessment in progress; return to tactical baseline"
    }
}

DEFAULT_TRIGGER_CONFIG = {
    "num_triggers": 5,
    "trigger_strength": 10,
    "recommended_grid": 10,
}


def find_scenario_preset(scenario_type: str):
    """Return preset dict matching a scenario_type (case-insensitive)."""
    if not scenario_type:
        return None
    lowered = scenario_type.lower()
    return next((p for p in SCENARIO_CATALOG if p["scenario_type"].lower() == lowered), None)


def reaction_template_for_status(status: str):
    """Fetch reaction template keyed by soldier status with safe fallback."""
    return REACTION_CATALOG.get(status, REACTION_CATALOG.get("Alert"))
