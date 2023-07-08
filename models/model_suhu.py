import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class SuhuFuzzyController:
    def __init__(self):
        # Langkah 1: Menentukan Variabel Masukan dan Variabel Keluaran
        # Fuzzifikasi
        suhu = ctrl.Antecedent(np.arange(0, 51, 1), 'suhu')
        kipas = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'kipas')

        suhu['rendah'] = fuzz.trapmf(suhu.universe, [0, 0, 25, 30])
        suhu['sedang'] = fuzz.trimf(suhu.universe, [25, 30, 35])
        suhu['tinggi'] = fuzz.trapmf(suhu.universe, [30, 35, 50, 50])

        kipas['OFF'] = fuzz.trimf(kipas.universe, [0, 0, 1])
        kipas['ON'] = fuzz.trimf(kipas.universe, [0, 1, 1])

        # Rules
        rule1 = ctrl.Rule(suhu['rendah'], [kipas['OFF']])
        rule2 = ctrl.Rule(suhu['sedang'], [kipas['OFF']])
        rule3 = ctrl.Rule(suhu['tinggi'], [kipas['ON']])

        # Menggabungkan aturan fuzzy
        self.sistem_pengambilan_keputusan = ctrl.ControlSystem([rule1, rule2, rule3])

        # Langkah 4: Melakukan Inferensi Fuzzy
        self.pengambilan_keputusan = ctrl.ControlSystemSimulation(self.sistem_pengambilan_keputusan)

    def compute_action(self, nilai_suhu):
        # Input nilai suhu
        self.pengambilan_keputusan.input['suhu'] = nilai_suhu

        # Menjalankan simulasi sistem kontrol fuzzy
        self.pengambilan_keputusan.compute()

        # Defuzzifikasi
        kipas = self.pengambilan_keputusan.output['kipas']
        return kipas


