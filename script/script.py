from os import path
from time import sleep

from utils import add_data
from Local import Local

releves_file_path = path.abspath(path.join(path.abspath(__file__), "../.."))
releves_file_path = path.join(releves_file_path, "releves.csv")


INTERVAL = 5.0

while True:
    try:
        dht_info = Local.read_sensor_data()

        add_data(releves_file_path, dht_info["temperature"], dht_info["humidite"], 100)
    except Exception as err:
        print("Erreur:", err)

    sleep(INTERVAL)
