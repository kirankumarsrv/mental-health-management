"""
Psychological Profile - Manual Configuration
Holds psychological profile values set by user via UI sliders
"""

from enum import Enum

class CopingMechanism(str, Enum):
    """Different ways soldiers handle stress"""
    APPROACH = "approach"        # Face the threat directly
    AVOIDANCE = "avoidance"      # Run away
    FREEZING = "freezing"        # Become paralyzed
    SUPPRESSION = "suppression"  # Ignore it

class PsychologicalProfile:
    """
    Holds psychological profile values set manually by user.
    Values are provided via UI sliders instead of auto-generation.
    """
    
    def __init__(self, trauma_sensitivity=0.5, emotional_regulation=0.5, 
                 recovery_rate=0.5, impulsivity=0.5, coping_mechanism="avoidance"):
        """
        Args:
            trauma_sensitivity (float): 0.0-1.0, how sensitive to stress
            emotional_regulation (float): 0.0-1.0, ability to manage emotions
            recovery_rate (float): 0.0-1.0, how fast they recover
            impulsivity (float): 0.0-1.0, tendency to act without thinking
            coping_mechanism (str): "avoidance", "approach", "freezing", "suppression"
        """
        # Clamp values to 0-1 range
        self.trauma_sensitivity = max(0.0, min(1.0, trauma_sensitivity))
        self.emotional_regulation = max(0.0, min(1.0, emotional_regulation))
        self.recovery_rate = max(0.0, min(1.0, recovery_rate))
        self.impulsivity = max(0.0, min(1.0, impulsivity))
        self.baseline_anxiety = 0.3  # Keep as default
        
        # Map string to enum
        coping_map = {
            "avoidance": CopingMechanism.AVOIDANCE,
            "approach": CopingMechanism.APPROACH,
            "freezing": CopingMechanism.FREEZING,
            "suppression": CopingMechanism.SUPPRESSION
        }
        self.coping_mechanism = coping_map.get(coping_mechanism.lower(), CopingMechanism.AVOIDANCE)
        
        # 7. STRESS THRESHOLD MODIFIERS
        # When does soldier transition from Calm → Alert → Panic?
        self.calm_threshold = 50 * (1 + (1 - self.emotional_regulation) * 0.4)  # High regulation = higher threshold
        self.alert_threshold = 80 * (1 + (1 - self.emotional_regulation) * 0.3)
    
    def get_modified_stress_increment(self, base_stress):
        """
        Modify stress based on trauma sensitivity
        
        Args:
            base_stress: Raw stress from triggers
            
        Returns:
            Adjusted stress considering psychological profile
        """
        # Trauma sensitivity amplifies or dampens trigger impact
        multiplier = 0.5 + self.trauma_sensitivity  # Range: 0.6 to 1.5
        modified_stress = base_stress * multiplier
        
        # Emotional regulation reduces stress
        regulation_reduction = self.emotional_regulation * base_stress * 0.2
        modified_stress -= regulation_reduction
        
        return max(0, modified_stress)
    
    def get_recovery_amount(self):
        """How much stress decreases when safe"""
        # Default was -2, now varies by profile
        base_recovery = 2
        return base_recovery * (0.5 + self.recovery_rate)  # Range: 1 to 3.6
    
    def get_stress_thresholds(self):
        """Get personalized stress thresholds"""
        return {
            "calm_threshold": self.calm_threshold,
            "alert_threshold": self.alert_threshold,
            "panic_threshold": self.alert_threshold  # Everything above alert is panic
        }
    
    def should_fight_or_flight(self):
        """
        Determine if soldier fights triggers or flees
        Based on coping mechanism and stress level
        """
        if self.coping_mechanism == CopingMechanism.APPROACH:
            return "fight"
        elif self.coping_mechanism == CopingMechanism.AVOIDANCE:
            return "flight"
        elif self.coping_mechanism == CopingMechanism.FREEZING:
            return "freeze"
        else:  # SUPPRESSION
            return "suppress"
