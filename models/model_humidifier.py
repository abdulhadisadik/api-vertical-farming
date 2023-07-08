import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class HumFuzzyController:
    def __init__(self):
        # Langkah 1: Menentukan Variabel Masukan dan Variabel Keluaran
# Fuzzifikasi
        kelembaban = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembaban')
        aksi_humidifier = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'aksi_humidifier')
        # Definisi fungsi keanggotaan untuk kelembaban
        kelembaban['rendah'] = fuzz.trimf(kelembaban.universe, [0, 0, 70.1])
        kelembaban['sedang'] = fuzz.trimf(kelembaban.universe, [70, 77, 85.1])
        kelembaban['tinggi'] = fuzz.trimf(kelembaban.universe, [86.1, 100, 100.1])

        aksi_humidifier['mati'] = fuzz.trimf(aksi_humidifier.universe, [0, 0, 0.5])
        aksi_humidifier['hidup'] = fuzz.trimf(aksi_humidifier.universe, [0.5, 1, 1])

        # Langkah 3: Menentukan Aturan Fuzzy
        rule1 = ctrl.Rule(kelembaban['rendah'], aksi_humidifier['hidup'])
        rule2 = ctrl.Rule(kelembaban['sedang'], aksi_humidifier['mati'])
        rule3 = ctrl.Rule(kelembaban['tinggi'], aksi_humidifier['mati'])

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
        aksi_humidifier = self.pengambilan_keputusan.output['aksi_humidifier']
        return aksi_humidifier


