from os import path
from datetime import datetime

# from board import D4
# from adafruit_dht import DHT22
from mysql import connector
from email_validator import validate_email, EmailUndeliverableError, EmailSyntaxError

from utils import get_yaml_infos, get_last_csv_record, check_properties
from mail import send_mail

from exceptions_types import *


class Local:
    def __init__(self, settings: dict, releves_file: str) -> None:
        if not isinstance(settings, dict):
            raise Exception("le paramètre renseigné doit être de type dict")

        settings_required_properties = (
            ("id_local", int),
            # ("seuil_temperature_min", float),
            # ("seuil_temperature_max", float),
            # ("seuil_humidite_max", float),
            # ("seuil_humidite_min", float),
            # ("compteur", int),
            # ("interval_secondes", float),
        )

        settings_dict = check_properties(settings_required_properties, settings)

        if not path.isfile(releves_file):
            raise Exception(f'le fichier "{releves_file}" n\'existe pas!')

        self.settings = settings_dict
        self.releves_file = releves_file

    def __repr__(self) -> str:
        return f"local {self.id}"

    @property
    def id(self) -> int:
        return self.settings.get("id_local")

    def get_last_dht_record(
        self,
        keys: tuple = (
            ("horodatage", datetime.fromisoformat),
            ("temperature", float),
            ("humidite", float),
        ),
    ) -> dict:
        return get_last_csv_record(self.releves_file, keys)

    def read_dht_infos(self) -> dict[str, float]:
        dhtDevice = DHT22(D4)

        temperature = dhtDevice.temperature
        humidite = dhtDevice.humidity

        if temperature is None or humidite is None:
            raise Exception("les valeurs recues ne sont pas valides")

        return {"temperature": temperature, "humidite": humidite}

    def is_temperature_high(self, temperature: float, default_value: float) -> bool:
        return temperature > self.settings.get("seuil_temperature_max", default_value)

    def is_temperature_low(self, temperature: float, default_value: float) -> bool:
        return temperature < self.settings.get("seuil_temperature_min", default_value)

    def is_humidity_high(self, humidity: float, default_value: float) -> bool:
        return humidity > self.settings.get("seuil_humidite_max", default_value)

    def is_humidity_low(self, humidity: float, default_value: float) -> bool:
        return humidity < self.settings.get("seuil_humidite_min", default_value)

    def send_dht_infos(self, db_info: dict):
        db_properties = (
            ("host", str),
            ("port", int),
            ("user", str),
            ("password", str),
            ("database", str),
        )

        db_dict = check_properties(db_properties, db_info)

        dht_info = self.get_last_dht_record()
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

    def get_localname(self, db_info: dict) -> str:
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

    def send_email_alert(self, email_info: dict, subject: str, body: str) -> None:
        email_properties = (
            ("sender", validate_email),
            ("password", str),
            ("server_addr", str),
            ("server_port", int),
        )
        email_destinations_key_name = "destinations"
        email_destinations = email_info.get(email_destinations_key_name)

        if email_destinations == None:
            raise MissingKeyException(email_destinations_key_name)

        if not isinstance(email_destinations, list):
            raise TypeError(
                f'La valeur de "{email_destinations_key_name}" n\' est pas une liste'
            )

        destinations_emails = []

        try:
            for destination_email in email_destinations:
                validate_email(destination_email)
                destinations_emails.append(destination_email)
        except EmailSyntaxError:
            raise InvalidEmailDestinationsException(destination_email)
        except EmailUndeliverableError:
            raise EmailUndeliverableException(destination_email)

        email_dict = check_properties(email_properties, email_info)
        email_dict["destinations"] = destinations_emails

        send_mail(email_dict, subject, body)
