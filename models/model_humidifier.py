import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class HumFuzzyController:
    def __init__(self):
        # Langkah 1: Menentukan Variabel Masukan dan Variabel Keluaran
        # Fuzzifikasi Kelembaban
        kelembaban = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembaban')
        humidifier = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'humidifier')

        kelembaban['rendah'] = fuzz.trapmf(kelembaban.universe, [0, 0, 55, 70])
        kelembaban['sedang'] = fuzz.trimf(kelembaban.universe, [55, 70, 85])
        kelembaban['tinggi'] = fuzz.trapmf(kelembaban.universe, [70, 85, 100, 100])

        humidifier['OFF'] = fuzz.trimf(humidifier.universe, [0, 0, 1])
        humidifier['ON'] = fuzz.trimf(humidifier.universe, [0, 1, 1])

        # Rules Kelembaban
        rule1 = ctrl.Rule(kelembaban['rendah'], [humidifier['ON']])
        rule2 = ctrl.Rule(kelembaban['sedang'], [humidifier['OFF']])
        rule3 = ctrl.Rule(kelembaban['tinggi'], [humidifier['OFF']])


        # Menggabungkan aturan fuzzy
        self.sistem_pengambilan_keputusan = ctrl.ControlSystem([rule1, rule2, rule3])

        # Langkah 4: Melakukan Inferensi Fuzzy
        self.pengambilan_keputusan = ctrl.ControlSystemSimulation(self.sistem_pengambilan_keputusan)

    def compute_action(self, nilai_kelembaban):
        # Input nilai kelembaban
        self.pengambilan_keputusan.input['kelembaban'] = nilai_kelembaban

        # Menjalankan simulasi sistem kontrol fuzzy
        self.pengambilan_keputusan.compute()

        # Defuzzifikasi
        humidifier = self.pengambilan_keputusan.output['humidifier']
        return humidifier


