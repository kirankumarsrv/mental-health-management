from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from .. import crud, models, schemas, presets
from ..database import get_db
from typing import Optional
import backend.mesa_model

router = APIRouter(
    prefix="/simulations",
    tags=["simulations"],
    responses={404: {"description": "Not found"}},
)

@router.get("/stats")
def get_statistics(db: Session = Depends(get_db)):
    return crud.get_statistics(db)


@router.get("/presets")
def get_presets():
    """Expose scenario and reaction catalogs for the UI."""
    return {
        "scenarios": presets.SCENARIO_CATALOG,
        "reactions": presets.REACTION_CATALOG,
    }

@router.post("/")
def run_simulation(
    request: schemas.SimulationRunRequest,
    db: Session = Depends(get_db)
):
    # 1. Fetch Entities
    person = crud.get_person(db, request.person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    scenario = crud.get_scenario(db, request.scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    # Therapist is optional for soldiers who haven't been assigned yet
    therapist = None
    if person.therapist_id:
        therapist = crud.get_therapist(db, person.therapist_id)
        if not therapist:
            raise HTTPException(status_code=404, detail="Therapist not found")

    # 2. Resolve profile values (assessment or manual sliders)
    used_assessment_id = None
    if request.assessment_id:
        assessment = crud.get_assessment(db, request.assessment_id)
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        if assessment.person_id != request.person_id:
            raise HTTPException(status_code=400, detail="Assessment does not belong to specified person")

        profile_values = {
            "trauma_sensitivity": assessment.trauma_sensitivity,
            "emotional_regulation": assessment.emotional_regulation,
            "recovery_rate": assessment.recovery_rate,
            "impulsivity": assessment.impulsivity,
            "coping_mechanism": assessment.coping_mechanism.value,
        }
        used_assessment_id = request.assessment_id
    else:
        profile_values = {
            "trauma_sensitivity": request.trauma_sensitivity,
            "emotional_regulation": request.emotional_regulation,
            "recovery_rate": request.recovery_rate,
            "impulsivity": request.impulsivity,
            "coping_mechanism": request.coping_mechanism,
        }

    # 3. Configure simulation settings
    grid_size = max(6, min(20, request.grid_size))
    scenario_preset = presets.find_scenario_preset(scenario.scenario_type)
    num_triggers = presets.DEFAULT_TRIGGER_CONFIG["num_triggers"]
    trigger_strength = presets.DEFAULT_TRIGGER_CONFIG["trigger_strength"]
    if scenario_preset:
        num_triggers = scenario_preset.get("num_triggers", num_triggers)
        trigger_strength = scenario_preset.get("trigger_strength", trigger_strength)

    # 4. Run Mesa simulation for 20 steps
    model = backend.mesa_model.PTSDModel(
        width=grid_size,
        height=grid_size,
        soldier_rank=person.rank,
        soldier_years=person.service_years,
        num_triggers=num_triggers,
        trigger_strength=trigger_strength,
        person_obj=person,
        profile_values=profile_values,
    )

    simulation_steps = []
    current_status = None
    reaction_id = None

    for step_index in range(1, 21):
        model.step()
        soldier = model.soldier

        step_data = {
            "step": step_index,
            "soldier_status": soldier.status,
            "soldier_stress": soldier.stress,
            "soldier_pos": list(soldier.pos) if soldier.pos else None,
            "soldier_color": soldier.color,
        }

        # 5. Create reactions based on status changes
        if soldier.status != current_status:
            current_status = soldier.status
            template = presets.reaction_template_for_status(current_status)

            reaction = crud.create_reaction(
                db,
                schemas.ReactionCreate(
                    r_type=template["r_type"],
                    physical_response=(
                        f"{template['physical_response']} | "
                        f"Stress {soldier.stress:.1f} @ {soldier.pos}"
                    ),
                ),
            )

            reaction_id = reaction.id

            crud.create_exhibits(
                db,
                schemas.ExhibitsCreate(
                    person_id=request.person_id,
                    reaction_id=reaction.id,
                ),
            )

            crud.create_triggers(
                db,
                schemas.TriggersCreate(
                    scenario_id=request.scenario_id,
                    reaction_id=reaction.id,
                ),
            )

            if used_assessment_id:
                reaction.assessment_id = used_assessment_id
                db.commit()
                db.refresh(reaction)

            step_data["reaction_id"] = reaction.id
            step_data["reaction_type"] = reaction.r_type
            step_data["physical_response"] = reaction.physical_response

        simulation_steps.append(step_data)

    final_stress = model.soldier.stress

    report_data = {
        "avoidance": "High" if final_stress > 85 else "Low",
        "re_experiencing": "Yes" if person.service_years > 5 and final_stress > 60 else "No",
        "negative_alterations": "Moderate" if final_stress > 40 else "None",
        "hyperarousal": "Severe" if final_stress > 80 else "Mild",
    }

    # 6. Save Report
    if reaction_id:
        report_schema = schemas.ReportCreate(
            person_id=request.person_id,
            therapist_id=person.therapist_id,
            reaction_id=reaction_id,
            assessment_id=used_assessment_id,
            avoidance=report_data["avoidance"],
            re_experiencing=report_data["re_experiencing"],
            negative_alterations=report_data["negative_alterations"],
            hyperarousal=report_data["hyperarousal"],
        )
        crud.create_report(db, report_schema)

    # 7. Return simulation results
    return {
        "person_id": request.person_id,
        "scenario_id": request.scenario_id,
        "grid_size": grid_size,
        "final_stress": final_stress,
        "full_history": simulation_steps,
        "report": report_data,
        "scenario_preset": scenario_preset,
        "assessment_id": used_assessment_id,
        "profile_used": profile_values,
    }
