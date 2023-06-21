import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyController:
    def __init__(self):
        # Langkah 1: Menentukan Variabel Masukan dan Variabel Keluaran
        ketinggian_air = ctrl.Antecedent(np.arange(0, 600, 1), 'ketinggian')
        aksi = ctrl.Consequent(np.arange(0, 2.1, 0.1), 'aksi')

        # Langkah 2: Menentukan Fungsi Keanggotaan
        ketinggian_air['rendah'] = fuzz.trimf(ketinggian_air.universe, [0, 0, 299.1])
        ketinggian_air['sedang'] = fuzz.trimf(ketinggian_air.universe, [299.1, 400, 450.1])
        ketinggian_air['tinggi'] = fuzz.trimf(ketinggian_air.universe, [450.1, 600, 600])

        aksi['pompa'] = fuzz.trimf(aksi.universe, [0, 0, 0.5])
        aksi['biarkan'] = fuzz.trimf(aksi.universe, [0, 1, 1])
        aksi['matikan'] = fuzz.trimf(aksi.universe, [1, 1, 2])



        # Langkah 3: Menentukan Aturan Fuzzy Sugeno
        rule1 = ctrl.Rule(ketinggian_air['rendah'], aksi['pompa'])
        rule2 = ctrl.Rule(ketinggian_air['sedang'], aksi['biarkan'])
        rule3 = ctrl.Rule(ketinggian_air['tinggi'], aksi['matikan'])

        # Menggabungkan aturan fuzzy Sugeno
        self.sistem_pengambilan_keputusan = ctrl.ControlSystem([rule1, rule2, rule3])

        # Langkah 4: Melakukan Inferensi Fuzzy Sugeno
        self.pengambilan_keputusan = ctrl.ControlSystemSimulation(self.sistem_pengambilan_keputusan)

  



    def compute_action(self, nilai_ketinggian):
    # Input nilai ketinggian
        self.pengambilan_keputusan.input['ketinggian'] = nilai_ketinggian

        # Menjalankan simulasi sistem kontrol fuzzy
        self.pengambilan_keputusan.compute()

        # Defuzzifikasi
        aksi = self.pengambilan_keputusan.output['aksi']
        print(aksi)  # Output: nilai crisp hasil perhitungan
        return aksi