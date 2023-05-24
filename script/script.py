from utils import add_data, get_dht_info
from time import sleep

INTERVAL = 5.0

while True:
    dht_info = get_dht_info()

    # Gestion RuntimeError
    if dht_info is None:
        sleep(1.0)
        continue

    add_data(dht_info['temperature'], dht_info['humidity'], 100)
    sleep(INTERVAL)
