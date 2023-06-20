import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyController:
    def __init__(self):
        # Membuat variabel input
        ketinggian = ctrl.Antecedent(np.arange(0, 601, 1), 'ketinggian')
        ketinggian['rendah'] = fuzz.trimf(ketinggian.universe, [0, 0, 449])
        ketinggian['tinggi'] = fuzz.trimf(ketinggian.universe, [449, 450, 599])

        # Membuat variabel output
        aksi_pompa = ctrl.Consequent(np.arange(0, 2, 1), 'aksi_pompa')
        aksi_pompa['nyala'] = fuzz.trimf(aksi_pompa.universe, [0, 0, 0.5])
        aksi_pompa['mati'] = fuzz.trimf(aksi_pompa.universe, [0.5, 1, 1])

        # Aturan fuzzy
        aturan = ctrl.Rule(ketinggian['rendah'], aksi_pompa['nyala'])
        aturan2 = ctrl.Rule(ketinggian['tinggi'], aksi_pompa['mati'])

        # Membuat sistem kontrol fuzzy
        self.simulasi = ctrl.ControlSystem([aturan, aturan2])
        self.hasil = ctrl.ControlSystemSimulation(self.simulasi)

    def compute_action(self, nilai_ketinggian):
        # Input nilai ketinggian
        self.hasil.input['ketinggian'] = nilai_ketinggian

        # Menjalankan simulasi sistem kontrol fuzzy
        self.hasil.compute()

        # Mendapatkan aksi pada variabel output
        aksi = self.hasil.output['aksi_pompa']

        return aksi
