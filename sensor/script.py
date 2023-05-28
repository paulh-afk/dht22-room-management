# Modules build-in
from os import path
from time import sleep, time
from datetime import datetime

# Constantes
from constants import *

# Modules créés
from Local import Local
from utils import get_yaml_infos
from mail import send_mail

# Exceptions
from exceptions_types import *

# Chemin fichier de configuration
config_folder_path = path.abspath(
    path.join(path.abspath(__file__), RELATIVE_CONFIG_FOLDER_PATH)
)
config_file_path = path.join(config_folder_path, CONFIG_FILENAME)

# Chemin fichier contenant les releves du capteur
releves_folder_path = path.abspath(
    path.join(path.abspath(__file__), RELATIVE_RELEVES_FOLDER_PATH)
)
releves_file_path = path.join(releves_folder_path, RELEVES_FILENAME)

config_info = get_yaml_infos(config_file_path, ("email",))

settings = config_info.get("settings")
db_info = config_info.get("database")
email_info = config_info.get("email")

count = NO_REPLY_MAX


try:
    local = Local(settings, releves_file_path)
    dht_infos = local.get_last_dht_record()

    while True:
        if count == 0:
            raise NoMeasuresException(
                f"Aucun releves n'a été ajouter dans le fichier {releves_file_path} depuis {NO_REPLY_MAX * 3} secondes."
            )

        horodatage_delayed = datetime.fromtimestamp(time() - MAX_HORODATAGE_GAP)
        horodatage_last_record: datetime = dht_infos.get("horodatage")

        if not isinstance(horodatage_delayed, datetime):
            raise Exception("Le dernier enregistrement ne contient pas d'horodatage")

        if horodatage_delayed.timestamp() > horodatage_last_record.timestamp():
            count -= 1
            sleep(3)
        else:
            break

    # Insertion des derniers données du fichier dans la base de données
    local.send_dht_infos_db(db_info)

    count = local.settings.get("compteur", DEFAULT_COMPTEUR)
    interval = local.settings.get("interval_secondes", DEFAULT_INTERVAL)

    while count >= 1:
        dht_infos = local.get_last_dht_record()

        temperature = dht_infos.get("temperature")
        seuil_temperature_min = False
        seuil_temperature_max = False

        humidity = dht_infos.get("humidite")
        seuil_humidity_min = False
        seuil_humidity_max = False

        # Conditions température
        if local.is_temperature_high(temperature, DEFAULT_TEMPERATURE_HIGH_LIMIT):
            seuil_temperature_max = True

        if local.is_temperature_low(temperature, DEFAULT_TEMPERATURE_LOW_LIMIT):
            seuil_temperature_min = True

        # Conditions humidité
        if local.is_humidity_high(humidity, DEFAULT_HUMIDITY_HIGH_LIMIT):
            seuil_humidity_max = True

        if local.is_humidity_low(humidity, DEFAULT_HUMIDITY_LOW_LIMIT):
            seuil_humidity_min = True

        if (
            not seuil_temperature_min
            and not seuil_temperature_max
            and not seuil_humidity_min
            and not seuil_humidity_max
        ):
            break

        count -= 1
        sleep(interval)

    if count == 0:
        local_name = local.get_localname(db_info)
        horodatage = datetime.now()

        if seuil_temperature_max:
            limit = local.settings.get(
                "seuil_temperature_max", DEFAULT_TEMPERATURE_HIGH_LIMIT
            )
        elif seuil_temperature_min:
            limit = local.settings.get(
                "seuil_temperature_min", DEFAULT_TEMPERATURE_LOW_LIMIT
            )
        elif seuil_humidity_max:
            limit = local.settings.get(
                "seuil_humidite_max", DEFAULT_HUMIDITY_HIGH_LIMIT
            )
        else:
            limit = local.settings.get(
                "seuil_humidite_min", DEFAULT_TEMPERATURE_LOW_LIMIT
            )

        if seuil_temperature_min or seuil_temperature_max:
            temperature_gap = abs(round(temperature - limit, 2))
            subject = "ALERTE TEMPERATURE dans le local " + local_name

            body = (
                f"Le seuil de la température du local {local_name} a été dépassé !\n"
                + f"La température enregistrer depuis {horodatage.strftime('%d/%m/%Y %H:%M:%S')} dépasse le seuil définie.\n"
                + f"Elle est de {str(temperature)} °C, "
                + f"ce qui correspond à un écart de {str(temperature_gap)} °C, "
                + f"avec le seuil de {str(limit)} °C défini.\n"
                + f"L'humiditée relative du local est de {str(humidity)} %."
            )
        else:
            humidity_gap = abs(round(humidity - limit, 2))
            subject = "ALERTE HUMIDITE dans le local " + local_name

            body = (
                f"Le seuil de l'humidité du local {local_name} a été dépassé !\n"
                + f"L'humidité enregistrer depuis {horodatage.strftime('%d/%m/%Y %H:%M:%S')} dépasse le seuil définie.\n"
                + f"Elle est de {str(humidity)} %, "
                + f"ce qui correspond à un écart de {str(humidity_gap)} %, "
                + f"avec le seuil de {str(limit)} % défini.\n"
                + f"La température du local est de {str(temperature)} °C."
            )

        send_mail(email_info, subject, body)


except Exception as err:
    print("Erreur:", err)
