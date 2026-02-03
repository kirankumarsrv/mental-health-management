from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from .psychological_profile import PsychologicalProfile
import random

class TriggerAgent(Agent):
    """
    An agent representing a stress trigger (e.g., loud noise, danger zone).
    It doesn't move, just exists to cause stress.
    """
    def __init__(self, unique_id, model, intensity):
        super().__init__(model)
        self.unique_id = unique_id
        self.intensity = intensity

    def step(self):
        pass # Triggers are static

class SoldierAgent(Agent):
    """
    The Soldier agent. Moves around the grid.
    If near a Trigger, stress increases.
    Uses psychological profile for individual differences.
    """
    def __init__(self, unique_id, model, rank, service_years, person_obj=None, profile_values=None):
        super().__init__(model)
        self.unique_id = unique_id
        self.rank = rank
        self.service_years = service_years
        self.stress = 0
        self.status = "Calm" # Calm, Alert, Panic
        self.color = "green"
        
        # Create psychological profile from manual slider values
        if profile_values:
            self.psychological_profile = PsychologicalProfile(**profile_values)
        else:
            # Fallback to default values
            self.psychological_profile = PsychologicalProfile()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def avoid(self, triggers):
        """Move AWAY from the nearest trigger."""
        if not triggers:
            self.move()
            return
        
        nearest = triggers[0] 
        
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        
        best_step = possible_steps[0]
        max_dist = -1
        
        for step in possible_steps:
             dist = abs(step[0] - nearest.pos[0]) + abs(step[1] - nearest.pos[1])
             if dist > max_dist:
                 max_dist = dist
                 best_step = step
                 
        self.model.grid.move_agent(self, best_step)

    def step(self):
        # 1. Detect Triggers nearby (radius 2)
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, radius=2)
        triggers = [a for a in neighbors if isinstance(a, TriggerAgent)]
        
        # 2. Calculate Stress Impact (with psychological profile)
        stress_increment = 0
        for t in triggers:
            stress_increment += t.intensity
        
        # Apply psychological modifiers if profile exists
        if self.psychological_profile:
            stress_increment = self.psychological_profile.get_modified_stress_increment(stress_increment)
        else:
            # Fallback to original logic
            resilience = min(5, self.service_years) 
            stress_increment = max(0, stress_increment - resilience)
        
        self.stress += stress_increment
        
        # Decay stress if no triggers
        if not triggers:
            if self.psychological_profile:
                recovery = self.psychological_profile.get_recovery_amount()
            else:
                recovery = 2
            self.stress = max(0, self.stress - recovery)

        # 3. Determine Behavior (using psychological thresholds)
        if self.psychological_profile:
            thresholds = self.psychological_profile.get_stress_thresholds()
            alert_threshold = thresholds["calm_threshold"]
            panic_threshold = thresholds["alert_threshold"]
        else:
            alert_threshold = 50
            panic_threshold = 80
        
        if self.stress > panic_threshold:
            self.status = "Panic"
            self.color = "red"
            coping = self.psychological_profile.should_fight_or_flight() if self.psychological_profile else "flight"
            
            if coping == "flight":
                self.avoid(triggers)
            elif coping == "freeze":
                pass  # Don't move
            elif coping == "fight":
                self.move()  # Move towards threat (not implemented yet)
            else:  # suppress
                self.move()  # Try to move normally
                
        elif self.stress > alert_threshold:
            self.status = "Alert"
            self.color = "orange"
            self.move() 
        else:
            self.status = "Calm"
            self.color = "green"
            self.move()

class PTSDModel(Model):
    """
    A model with some number of triggers and 1 soldier.
    Incorporates psychological profiles for realistic individual differences.
    """
    def __init__(
        self,
        width,
        height,
        soldier_rank,
        soldier_years,
        num_triggers=5,
        trigger_strength=10,
        person_obj=None,
        profile_values=None,
    ):
        super().__init__()
        self.grid = MultiGrid(width, height, True)
        self.running = True
        
        # Create Soldier with psychological profile from slider values
        self.soldier = SoldierAgent(0, self, soldier_rank, soldier_years, person_obj, profile_values)
        # Start in middle
        self.grid.place_agent(self.soldier, (width//2, height//2))
        
        # Create Triggers with configurable count and strength
        for i in range(num_triggers):
            a = TriggerAgent(i+1, self, trigger_strength)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        # Mesa 3.0+ AgentSet approach - agents auto-registered in Model
        if hasattr(self, 'agents') and hasattr(self.agents, 'shuffle'):
            self.agents.shuffle_do("step")
        else:
            # Fallback: manually step soldier
            self.soldier.step()
