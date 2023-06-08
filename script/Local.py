from os import path
from datetime import datetime

from board import D4
from adafruit_dht import DHT22
from mysql import connector

from constants import (
    DEFAULT_TEMPERATURE_HIGH_LIMIT,
    DEFAULT_TEMPERATURE_LOW_LIMIT,
    DEFAULT_HUMIDITY_HIGH_LIMIT,
    DEFAULT_HUMIDITY_LOW_LIMIT,
)
from exceptions_types import *


class Local:
    def __init__(self, settings: dict, releves_file_path: str) -> None:
        if not isinstance(settings, dict):
            raise Exception("le paramètre renseigné doit être de type dict")

        settings_required_properties = (
            ("id_local", int),
            ("seuil_temperature_min", float),
            ("seuil_temperature_max", float),
            ("seuil_humidite_max", float),
            ("seuil_humidite_min", float),
            ("compteur", int),
            ("interval_secondes", float),
        )

        settings_dict = check_properties(settings_required_properties, settings)

        if not path.isfile(releves_file_path):
            raise Exception(f'le fichier "{releves_file_path}" n\'existe pas!')

        self.settings = settings_dict
        self.releves_file_path = releves_file_path

    def __repr__(self) -> str:
        return f"local {self.id}"

    @staticmethod
    def read_sensor_data() -> dict[str, float]:
        dhtDevice = DHT22(D4)

        temperature = dhtDevice.temperature
        humidite = dhtDevice.humidity

        if temperature is None or humidite is None:
            raise Exception("les valeurs recues ne sont pas valides")

        return {"temperature": temperature, "humidite": humidite}

    @property
    def id(self) -> int:
        return self.settings.get("id_local")

    def get_local_name(self, db_info: dict) -> str:
        db_properties = (
            ("host", str),
            ("port", int),
            ("user", str),
            ("password", str),
            ("database", str),
        )

        db_dict = check_properties(db_properties, db_info)

        select_query = """
            SELECT nom_local
            FROM locals
            WHERE id = %s
        """

        try:
            with connector.connect(**db_dict) as cnx:
                with cnx.cursor() as cursor:
                    cursor.execute(select_query, (self.id,))
                    local_name = cursor.fetchone()[0]

            if local_name is None:
                raise Exception("aucun nom n'a été trouvé")

            return local_name

        except connector.Error as e:
            # Créer MySQL Exception
            raise Exception(f"Erreur lors de la récupération du nom du local : {e}")

    def get_last_sensor_reading(
        self,
        keys: tuple = (
            ("horodatage", datetime.fromisoformat),
            ("temperature", float),
            ("humidite", float),
        ),
    ) -> dict:
        return get_last_csv_record(self.releves_file_path, keys)

    def send_sensor_data_to_db(self, db_info: dict):
        db_properties = (
            ("host", str),
            ("port", int),
            ("user", str),
            ("password", str),
            ("database", str),
        )

        db_dict = check_properties(db_properties, db_info)

        dht_info = self.get_last_sensor_reading()
        temperature = dht_info["temperature"]
        humidity = dht_info["humidite"]

        horodatage = datetime.now()

        insert_query = """
            INSERT INTO releves_locals
            (temperature, humidity, horodatage, id_local)
            VALUES (%s, %s, %s, %s)
        """

        try:
            with connector.connect(**db_dict) as cnx:
                with cnx.cursor() as cursor:
                    cursor.execute(
                        insert_query,
                        (
                            temperature,
                            humidity,
                            horodatage.strftime("%Y-%m-%d %H-%M-%S"),
                            self.id,
                        ),
                    )
                    cnx.commit()
        except connector.Error as e:
            # Créer MySQL Exception
            raise Exception(f"Erreur lors de l'insertion des données : {e}")

    def is_above_max_temperature(self, temperature: float) -> bool:
        return temperature > self.settings.get(
            "seuil_temperature_max", DEFAULT_TEMPERATURE_HIGH_LIMIT
        )

    def is_below_min_temperature(self, temperature: float) -> bool:
        return temperature < self.settings.get(
            "seuil_temperature_min", DEFAULT_TEMPERATURE_LOW_LIMIT
        )

    def is_above_max_humidity(self, humidity: float) -> bool:
        return humidity > self.settings.get(
            "seuil_humidite_max", DEFAULT_HUMIDITY_HIGH_LIMIT
        )

    def is_below_min_humidity(self, humidity: float) -> bool:
        return humidity < self.settings.get(
            "seuil_humidite_min", DEFAULT_HUMIDITY_LOW_LIMIT
        )
