import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class LuxFuzzyController:
    def __init__(self):
        # Langkah 1: Menentukan Variabel Masukan dan Variabel Keluaran
        intensitas_cahaya = ctrl.Antecedent(np.arange(0, 2001, 1), 'intensitas_cahaya')
        aksi = ctrl.Consequent(np.arange(0, 2.1, 0.1), 'aksi')

        # Langkah 2: Menentukan Fungsi Keanggotaan
        intensitas_cahaya['rendah'] = fuzz.trimf(intensitas_cahaya.universe, [0, 0, 400.1])
        intensitas_cahaya['sedang'] = fuzz.trimf(intensitas_cahaya.universe, [400.1, 1000, 1000.1])
        intensitas_cahaya['tinggi'] = fuzz.trimf(intensitas_cahaya.universe, [1000.1, 2000, 2000])

        aksi['nyala'] = fuzz.trimf(aksi.universe, [0, 0, 0.5])
        aksi['biarkan'] = fuzz.trimf(aksi.universe, [0, 1, 1])
        aksi['mati'] = fuzz.trimf(aksi.universe, [1, 1, 2])

        # Langkah 3: Menentukan Aturan Fuzzy Sugeno
        rule1 = ctrl.Rule(intensitas_cahaya['rendah'], aksi['nyala'])
        rule2 = ctrl.Rule(intensitas_cahaya['sedang'], aksi['biarkan'])
        rule3 = ctrl.Rule(intensitas_cahaya['tinggi'], aksi['mati'])

        # Menggabungkan aturan fuzzy Sugeno
        self.sistem_pengambilan_keputusan = ctrl.ControlSystem([rule1, rule2, rule3])

        # Langkah 4: Melakukan Inferensi Fuzzy Sugeno
        self.pengambilan_keputusan = ctrl.ControlSystemSimulation(self.sistem_pengambilan_keputusan)

    def compute_action(self, nilai_intensitas):
        # Input nilai intensitas cahaya
        self.pengambilan_keputusan.input['intensitas_cahaya'] = nilai_intensitas

        # Menjalankan simulasi sistem kontrol fuzzy
        self.pengambilan_keputusan.compute()

        # Defuzzifikasi
        aksi = self.pengambilan_keputusan.output['aksi']
        return aksi
