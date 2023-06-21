from flask import Flask, request
# from models.model_water_level import FuzzyController
from models.model_water_level import WaterFuzzyController
from models.model_lux import LuxFuzzyController
from models.model_suhu import SuhuFuzzyController
from models.model_humidifier import HumFuzzyController
from models.Model_pHTanah import TanahFuzzyController

app = Flask(__name__)

# API WATER LEVEL
@app.route('/water_level', methods=['POST'])
def water_fuzzy_controller():
    # Ambil nilai ketinggian dari permintaan POST
    data = request.get_json()
    nilai_ketinggian = data['ketinggian']

    # Menghitung aksi menggunakan objek FuzzyController
    controller = WaterFuzzyController()
    aksi = controller.compute_action(nilai_ketinggian)


    # Tentukan respons berdasarkan aksi
    if aksi > 1.0:
        response = 0
    if aksi > 0.5 and aksi <= 1.0:
        response = 1
    if aksi <= 0.5:
        response = 1
     

    return {
        "aksi_selenoid": aksi,
        "response": response
    }


# API LUX
@app.route('/lux_level', methods=['POST'])
def lux_fuzzy_controller():
    # Ambil nilai lux level dari permintaan POST
    data = request.get_json()
    nilai_lux = data["lux"]
    
    # Menghitung aksi menggunakan objek FuzzyController
    controller = LuxFuzzyController()
    aksi = controller.compute_action(nilai_lux)
    # Tentukan respon berdasarakn aksi
    if aksi > 1.0:
        response = 0
    if aksi > 0.5 and aksi <= 1.0:
        response = 0
    if aksi <= 0.5:
        response = 1

    return {
        "aksi_cahaya": aksi,
        "response": response
    }


# API Suhu
@app.route('/suhu_level', methods=['POST'])
def suhu_fuzzy_controller():
    # Ambil nilai ketinggian dari permintaan POST
    data = request.get_json()
    nilai_suhu = data['suhu']
 
    # Menghitung aksi menggunakan objek FuzzyController
    controller = SuhuFuzzyController()
    aksi = controller.compute_action(nilai_suhu)


    # Tentukan respons berdasarkan aksi
    if aksi > 0.5:
        response = 1
    else:
        response = 0
     

    return {
        "aksi_kipas": aksi,
        "response": response
    }


# API Hum
@app.route('/hum_level', methods=['POST'])
def hum_fuzzy_controller():
    # Ambil nilai ketinggian dari permintaan POST
    data = request.get_json()
    nilai_kelembaban = data['kelembaban']
 
    # Menghitung aksi menggunakan objek FuzzyController
    controller = HumFuzzyController()
    aksi = controller.compute_action(nilai_kelembaban)


    # Tentukan respons berdasarkan aksi
    if aksi > 0.5:
        response = 1
    else:
        response = 0
     
    return {
        "aksi_hum": aksi,
        "response": response
    }


#API PhTanah
@app.route('/phtanah', methods=['POST'])
def tanah_fuzzy_controller():
    # Ambil nilai ketinggian dari permintaan POST
    data = request.get_json()
    nilai_tanah = data['tanah']
 
    # Menghitung aksi menggunakan objek FuzzyController
    controller = TanahFuzzyController()
    aksi = controller.compute_action(nilai_tanah)


    # Tentukan respons berdasarkan aksi
    if aksi < 1:
        response = 1
    else:
        response = 0
     
    return {
        "aksi_selenoid": aksi,
        "response": response
    }


if __name__ == '__main__':
    app.run()
