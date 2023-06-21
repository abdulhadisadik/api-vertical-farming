import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class SuhuFuzzyController:
    def __init__(self):
        # Langkah 1: Menentukan Variabel Masukan dan Variabel Keluaran
        suhu = ctrl.Antecedent(np.arange(0, 101, 1), 'suhu')
        aksi_kipas = ctrl.Consequent(np.arange(0, 2, 1), 'aksi_kipas')

        # Langkah 2: Menentukan Fungsi Keanggotaan
        suhu['rendah'] = fuzz.trimf(suhu.universe, [0, 0, 20.1])
        suhu['sedang'] = fuzz.trimf(suhu.universe, [20.1, 26, 33.1])
        suhu['tinggi'] = fuzz.trimf(suhu.universe, [33.1, 50, 50])

        aksi_kipas['mati'] = fuzz.trimf(aksi_kipas.universe, [0, 0, 0])
        aksi_kipas['hidup'] = fuzz.trimf(aksi_kipas.universe, [1, 1, 1])

        # Langkah 3: Menentukan Aturan Fuzzy
        rule1 = ctrl.Rule(suhu['rendah'], aksi_kipas['mati'])
        rule2 = ctrl.Rule(suhu['sedang'], aksi_kipas['mati'])
        rule3 = ctrl.Rule(suhu['tinggi'], aksi_kipas['hidup'])

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
        aksi_kipas = self.pengambilan_keputusan.output['aksi_kipas']
        return aksi_kipas


