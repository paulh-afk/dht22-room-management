import csv
from datetime import datetime
import os

from adafruit_dht import DHT22
from board import D4

# changer d'endroit
DATA_FILENAME = 'datas.csv'
FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_PATH = os.path.join(FOLDER_PATH, DATA_FILENAME)

fieldnames = ['horodatage', 'temperature', 'humidite']


def csvfile_to_datas():
    try:
        with open(DATA_FILE_PATH, 'r') as csvfile:
            datas = []
            spamreader = csv.DictReader(csvfile)

            for row in spamreader:
                horodatage = datetime.strptime(
                    row['horodatage'], '%Y-%m-%d %H:%M:%S')

                datas.append({
                    'horodatage': horodatage,
                    'temperature': row['temperature'],
                    'humidite': row['humidite']
                })

            return datas

    except FileNotFoundError:
        print("Fichier non trouvé!")
        print("Fin du programme")
        exit()
    
    except IOError:
        exit()




def add_data(temperature: float, humidite: float, records: int = 30):
    horodatage = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    csv_data = csvfile_to_datas()

    while len(csv_data) >= records:
        csv_data.pop(0)

    csv_data.append({
        'horodatage': horodatage,
        'temperature': temperature,
        'humidite': humidite
    })

    try:
        with open(DATA_FILE_PATH, 'w+', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames)

            csvwriter.writeheader()
            csvwriter.writerows(csv_data)

    except IOError:
        exit()
    
def get_dht_info():
    """

    """
    try:
        dhtDevice = DHT22(D4, use_pulseio=False)

        # dhtDevice.measure()
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
 
        dhtDevice.exit()

        if temperature is None or humidity is None:
            return None

        return {'temperature': round(temperature, 2), 'humidity': round(humidity, 2)}

    except RuntimeError:
        return None