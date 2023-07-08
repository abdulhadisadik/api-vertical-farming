import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class TanahFuzzyController:
    def __init__(self):
        # Step 1: Define Input and Output Variables
        soil_pH = ctrl.Antecedent(np.arange(0, 14.1, 0.1), 'soil_pH')
        action = ctrl.Consequent(np.arange(0, 2.1, 0.1), 'action')

              # Step 2: Define Membership Functions
        soil_pH['asam'] = fuzz.trimf(soil_pH.universe, [0, 5, 6])
        soil_pH['optimal'] = fuzz.trimf(soil_pH.universe, [5, 6.5, 8])
        soil_pH['basa'] = fuzz.trimf(soil_pH.universe, [7, 8, 14])

        action['solenoid_on'] = fuzz.trimf(action.universe, [0, 0, 1])
        action['solenoid_op'] = fuzz.trimf(action.universe, [1 ,1 ,1]) 
        action['solenoid_off'] = fuzz.trimf(action.universe, [1, 2, 2])

        # Step 3: Define Fuzzy Rules
        rule1 = ctrl.Rule(soil_pH['asam'], action['solenoid_on'])
        rule2 = ctrl.Rule(soil_pH['optimal'], action['solenoid_op'])
        rule3 = ctrl.Rule(soil_pH['basa'], action['solenoid_off'])

        # Combine fuzzy rules
        self.decision_system = ctrl.ControlSystem([rule1, rule2, rule3])

        # Step 4: Create Fuzzy Inference System
        self.decision_simulation = ctrl.ControlSystemSimulation(self.decision_system)

    def compute_action(self, soil_pH_value):
        # Input soil pH value
        self.decision_simulation.input['soil_pH'] = soil_pH_value

        # Run fuzzy control system simulation
        self.decision_simulation.compute()

        # Defuzzification
        action = self.decision_simulation.output['action']
        print(action)  # Output: crisp value after computation
        return action


