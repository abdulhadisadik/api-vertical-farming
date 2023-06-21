from flask import Flask, request
# from models.model_water_level import FuzzyController
from models.model_water_level import FuzzyController

app = Flask(__name__)

@app.route('/water_level', methods=['POST'])
def fuzzy_controller():
    # Ambil nilai ketinggian dari permintaan POST
    data = request.get_json()
    nilai_ketinggian = data['ketinggian']

    # Menghitung aksi menggunakan objek FuzzyController
    controller = FuzzyController()
    aksi = controller.compute_action(nilai_ketinggian)


    # Tentukan respons berdasarkan aksi
    if aksi > 1.0:
        response = 0
    if aksi > 0.5 and aksi <= 1.0:
        response = 1
    if aksi <= 0.5:
        response = 1
     

    return {
        "aksi_pompa": aksi,
        "response": response
    }

if __name__ == '__main__':
    app.run()
