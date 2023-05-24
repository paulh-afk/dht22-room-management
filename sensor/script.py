# Modules build-in
from os import path

from datetime import datetime
from time import sleep

# Modules installés
from mysql import connector

# Modules
from utils import get_yaml_infos, get_last_csv_record
from mail import send_mail

# Valeurs par défaut
DEFAULT_TEMPERATURE_LOW_LIMIT = 0.0
DEFAULT_TEMPERATURE_HIGH_LIMIT = 35.0

DEFAULT_HUMIDITY_LOW_LIMIT = 20.0
DEFAULT_HUMIDITY_HIGH_LIMIT = 70.0

DEFAULT_COMPTEUR = 3
DEFAULT_INTERVAL = 20

horodatage = datetime.now()

# Fichier de configuration
CONFIG_FILENAME = "config.yaml"
CONFIG_FOLDER_PATH = path.abspath(path.join(path.abspath(__file__), "../.."))
CONFIG_FILE_PATH = path.join(CONFIG_FOLDER_PATH, CONFIG_FILENAME)

# Fichier de relevés
RELEVES_FILENAME = "releves.csv"
RELEVES_FOLDER_PATH = path.abspath(path.join(path.abspath(__file__), "../.."))
RELEVES_FILE_PATH = path.join(RELEVES_FOLDER_PATH, RELEVES_FILENAME)

CONFIG_INFO = get_yaml_infos(CONFIG_FILE_PATH, ("email",))

import threading
from queue import Queue


class Local:
    __queue_releve = Queue()

    def __init__(self, settings: dict, releves_file: str) -> None:
        try:
            if type(settings) != dict:
                raise Exception("le paramètre renseigné doit être de type dict!")

            settings_properties = (
                ("id_local", int),
                ("seuil_temperature_min", float),
                ("seuil_temperature_max", float),
                ("seuil_humidite_max", float),
                ("seuil_humidite_min", float),
                ("compteur", int),
                ("interval_secondes", float),
            )

            for t in settings_properties:
                t_key = t[0]
                if not t_key in settings:
                    raise Exception(f'la clé "{t_key}" n\'a pas été trouvée!')

            settings_dict = {}

            for t in settings_properties:
                try:
                    t_key = t[0]
                    t_type = t[1]

                    settings_dict[t_key] = t_type(settings.get(t_key))
                except ValueError:
                    raise Exception(f'la clé "{t_key}" n\'est pas de type {t_type}')

            if not path.isfile(releves_file):
                raise Exception(f'le fichier "{releves_file}" n\'existe pas!')

        except Exception as err:
            raise err

        self.settings = settings_dict
        self.releves_file = releves_file

    def get_last_dht_record(
        self,
        lock: threading.Lock,
        keys=(
            ("horodatage", datetime.fromisoformat),
            ("temperature", float),
            ("humidite", float),
        ),
    ) -> dict:
        # implémenter sémaphore dans programme écriture
        try:
            lock.acquire()
            result = get_last_csv_record(self.releves_file, keys)

            self.__queue_releve.put(result)

        except:
            raise Exception("Une erreur s'est produite lors de la lecture du fichier")
        finally:
            lock.release()

        return self.__queue_releve.get()

    # TODO
    def __repr__(self) -> str:
        pass

    @property
    def id(self) -> int:
        return self.settings.get("id_local")

    @property
    def temperature(self) -> float:
        ...

    @property
    def humidite(self) -> float:
        ...


settings = CONFIG_INFO.get("settings")

# TODO ajouter tests unitaire
try:
    lock = threading.Lock()
    local = Local(settings, "../csv_file.csv")
    print(local.get_last_dht_record(lock))
except Exception as err:
    print("error:", err)

# def get_dht_info() -> dict[str, float] | None:
#     """ """

#     # derniers records du fichier releves.csv pour éviter collision avec la sonde

#     try:
#         semaphore.acquire()
#         result = get_last_csv_record(RELEVES_FILE_PATH)

#     except Exception:
#         # Une erreur s'est produite lors de la lecture du fichier
#         result = None

#     finally:
#         semaphore.release()
#         queue_lecture.put(result)


# def insert_dht_datas_db(db_info: dict, datas: dict, id_local: int):
#     """ """

#     cnx = None

#     try:
#         cnx = connector.connect(**db_info)
#         cursor = cnx.cursor()

#         # datas
#         temperature = datas["temperature"]
#         humidity = datas["humidity"]

#         insert_query = """
#               INSERT INTO releves_locals
#               (temperature, humidity, horodatage, id_local)
#               VALUES ({}, {}, '{}', {})""".format(
#             temperature, humidity, horodatage.strftime("%Y-%m-%d %H-%M-%S"), id_local
#         )

#         cursor.execute(insert_query)
#         cnx.commit()

#         cursor.close()
#         cnx.close()

#     except Exception:
#         # exit()
#         # Erreur bdd: aucune insertion en base de données
#         ...

#     finally:
#         if cnx != None:
#             if cnx.is_connected():
#                 cnx.disconnect()


# def select_local_name_by_id(db_info: dict, id_local: int):
#     try:
#         cnx = connector.connect(**db_info)
#         cursor = cnx.cursor()

#         select_query = """
#               SELECT nom_local
#               FROM locals
#               WHERE id = {}""".format(
#             id_local
#         )

#         cursor.execute(select_query)
#         local_name = cursor.fetchone()

#         cursor.close()
#         cnx.close()

#         if local_name is None:
#             return "Local non identifié"

#         return local_name[0]

#     except Exception:
#         if cnx.is_connected():
#             cnx.disconnect()


# count = 0

# if not type(CONFIG_INFO) is dict:
#     # Erreur email non renseignée
#     ...
#     exit()


# while True:
#     queue_lecture = Queue()

#     thread_reader = threading.Thread(target=get_dht_info)
#     thread_reader.start()

#     thread_reader.join()

#     dht_info = queue_lecture.get()

#     if "database" in CONFIG_INFO and "settings" in CONFIG_INFO:
#         insert_dht_datas_db(
#             CONFIG_INFO.get("database"),
#             dht_info,
#             CONFIG_INFO.get("settings").get("id_local"),
#         )
#     else:
#         # Aucune insertion en base de données
#         ...

#     # TODO
#     # ajout info si erreur lors de l'ajout en bdd dans fichier `dht_info.json`

#     try:
#         settings = CONFIG_INFO.get("settings")
#         if settings is None:
#             raise Exception("")
#             # section ["settings"] sensée existé
#             # script édition fichier s'assure que toutes les sections et propriétées existent

#         properties = (
#             "id_local",
#             "seuil_temperature_min",
#             "seuil_temperature_max",
#             "seuil_humidite_max",
#             "seuil_humidite_min",
#             "compteur",
#             "interval_secondes",
#         )

#         for property in settings.keys():
#             if not property in properties:
#                 raise Exception("")
#                 # script édition fichier s'assure que toutes les sections et propriétées existent

#         settings: dict

#         # Aucun identifiant de local
#         id_local = settings.get("id_local", -1)

#         temperature_limit_min = settings.get(
#             "seuil_temperature_min", DEFAULT_TEMPERATURE_LOW_LIMIT
#         )
#         temperature_limit_max = settings.get(
#             "seuil_temperature_max", DEFAULT_TEMPERATURE_HIGH_LIMIT
#         )

#         humidite_limit_min = settings.get(
#             "seuil_humidite_min", DEFAULT_HUMIDITY_LOW_LIMIT
#         )
#         humidite_limit_max = settings.get(
#             "seuil_humidite_max", DEFAULT_HUMIDITY_HIGH_LIMIT
#         )

#         count = settings.get("compteur", DEFAULT_COMPTEUR)
#         interval = settings.get("interval_secondes", DEFAULT_INTERVAL)

#     except Exception as err:
#         # Local sans nom
#         id_local = -1

#         temperature_limit_min = DEFAULT_TEMPERATURE_LOW_LIMIT
#         temperature_limit_max = DEFAULT_TEMPERATURE_HIGH_LIMIT

#         humidite_limit_min = DEFAULT_HUMIDITY_LOW_LIMIT
#         humidite_limit_max = DEFAULT_HUMIDITY_HIGH_LIMIT

#         count = DEFAULT_COMPTEUR
#         interval = DEFAULT_INTERVAL

#     print(count)
#     print(interval)

#     while count >= 0:
#         thread_reader = threading.Thread(target=get_dht_info)
#         thread_reader.start()

#         thread_reader.join()

#         dht_info = queue_lecture.get()

#         print(dht_info)

#         temperature = dht_info["temperature"]
#         seuil_temperature_min = False
#         seuil_temperature_max = False

#         humidity = dht_info["humidity"]
#         seuil_humidity_min = False
#         seuil_humidity_max = False

#         # Conditions température
#         if temperature <= temperature_limit_min:
#             seuil_temperature_min = True

#         if temperature >= temperature_limit_max:
#             seuil_temperature_max = True

#         # Conditions humidité
#         if humidity <= humidite_limit_min:
#             seuil_humidity_min = True

#         if humidity >= humidite_limit_max:
#             seuil_humidity_max = True

#         if (
#             not seuil_temperature_min
#             and not seuil_temperature_max
#             and not seuil_humidity_min
#             and not seuil_humidity_max
#         ):
#             break

#         count -= 1
#         sleep(interval)

#     if count == 0:
#         if id_local == -1:
#             local_name = "LOCAL NON DEFINIE"
#         else:
#             local_name = select_local_name_by_id(CONFIG_INFO.get("database"), id_local)

#         if seuil_temperature_min:
#             limit = temperature_limit_min
#         elif seuil_temperature_max:
#             limit = temperature_limit_max
#         elif seuil_temperature_min:
#             limit = humidite_limit_min
#         else:
#             limit = humidite_limit_max

#         if seuil_temperature_min or seuil_temperature_max:
#             temperature_gap = round(temperature - limit, 2)
#             subject = "ALERTE TEMPERATURE dans le local " + local_name

#             body = (
#                 f"Le seuil de la température du local {local_name} a été dépassé !\n"
#                 + f"La température enregistrer depuis {horodatage.strftime('%d/%m/%Y %H:%M:%S')} dépasse le seuil définie.\n"
#                 + f"Elle est de {str(temperature)} °C, "
#                 + f"ce qui correspond à un écart de {str(temperature_gap)} °C, "
#                 + f"avec le seuil de {str(limit)} °C défini.\n"
#                 + f"L'humiditée relative du local est de {str(humidity)} %."
#             )
#         else:
#             humidity_gap = round(humidity - limit, 2)
#             subject = "ALERTE HUMIDITE dans le local " + local_name

#             body = (
#                 f"Le seuil de l'humidité du local {local_name} a été dépassé !\n"
#                 + f"L'humidité enregistrer depuis {horodatage.strftime('%d/%m/%Y %H:%M:%S')} dépasse le seuil définie.\n"
#                 + f"Elle est de {str(humidity)} %, "
#                 + f"ce qui correspond à un écart de {str(humidity_gap)} %, "
#                 + f"avec le seuil de {str(limit)} % défini.\n"
#                 + f"La température du local est de {str(temperature)} °C."
#             )

#         send_mail(CONFIG_INFO.get("email"), subject, body)

#     break
