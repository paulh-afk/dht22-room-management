from board import D4
from adafruit_dht import DHT22
from time import sleep

COUNT_TOLERANCE_ERROR = 10

def get_dht_info() -> dict | None:
  """_summary_

  Returns:
      _type_: _description_
  """
  try:
    dhtDevice = DHT22(D4, use_pulseio=False)

    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity

    dhtDevice.exit()

    if temperature is None or humidity is None:
      return None

    return {'temperature': round(temperature, 2), 'humidity': round(humidity, 2)}

  except RuntimeError:
    return None
  
count = 0
  
while True:
    dht_info = get_dht_info()

    if count == COUNT_TOLERANCE_ERROR:
        exit()

    # Gestion RuntimeError
    if dht_info is None:
        sleep(1.0)
        count += 1
        continue  