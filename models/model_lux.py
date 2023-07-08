import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class LuxFuzzyController:
    def __init__(self):
        # Fuzzifikasi
        intensitas_cahaya = ctrl.Antecedent(np.arange(0, 1001, 1), 'intensitas_cahaya')
        aksi = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'led')

        intensitas_cahaya['sangat rendah'] = fuzz.trapmf(intensitas_cahaya.universe, [0, 0, 200, 300])
        intensitas_cahaya['rendah'] = fuzz.trimf(intensitas_cahaya.universe, [200, 300, 400])
        intensitas_cahaya['normal'] = fuzz.trapmf(intensitas_cahaya.universe, [300, 400, 600, 700])
        intensitas_cahaya['tinggi'] = fuzz.trimf(intensitas_cahaya.universe, [600, 700, 800])
        intensitas_cahaya['sangat tinggi'] = fuzz.trapmf(intensitas_cahaya.universe, [700, 800, 1000, 1000])

        aksi['OFF'] = fuzz.trimf(aksi.universe, [0, 0, 1])
        aksi['ON'] = fuzz.trimf(aksi.universe, [0, 1, 1])

        # Rules
        rule1 = ctrl.Rule(intensitas_cahaya['sangat rendah'], aksi['ON'])
        rule2 = ctrl.Rule(intensitas_cahaya['rendah'], aksi['ON'])
        rule3 = ctrl.Rule(intensitas_cahaya['normal'], aksi['OFF'])
        rule4 = ctrl.Rule(intensitas_cahaya['tinggi'], aksi['OFF'])
        rule5 = ctrl.Rule(intensitas_cahaya['sangat tinggi'], aksi['OFF'])


        # Kontrol System
        self.sistem_pengambilan_keputusan= ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
        self.pengambilan_keputusan = ctrl.ControlSystemSimulation(self.sistem_pengambilan_keputusan)


    def compute_action(self, nilai_intensitas):
        # Input nilai intensitas cahaya
        self.pengambilan_keputusan.input['intensitas_cahaya'] = nilai_intensitas

        # Menjalankan simulasi sistem kontrol fuzzy
        self.pengambilan_keputusan.compute()

        # Defuzzifikasi
        aksi = self.pengambilan_keputusan.output['led']
        return aksi
