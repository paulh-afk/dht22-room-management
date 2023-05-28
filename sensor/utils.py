import yaml
import csv

from datetime import datetime
from mysql import connector
from email_validator import validate_email, EmailUndeliverableError, EmailSyntaxError


from exceptions_types import *


class Email:
    def __init__(self, email_str: str) -> None:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_str):
            raise TypeError(f"le mail {email_str} n'est pas valide")

        email_split = email_str.split("@")

        self.id = email_split[0]
        self.provider = email_split[1]


def check_properties(properties: tuple[tuple], settings: dict) -> dict:
    for t in properties:
        t_key = t[0]
        if not t_key in settings:
            raise Exception(f'la clé "{t_key}" n\'a pas été trouvée!')

    result = {}

    for t in properties:
        try:
            t_key = t[0]
            t_type = t[1]

            result[t_key] = t_type(settings.get(t_key))

        except EmailSyntaxError:
            raise InvalidEmailException(settings.get(t_key))

        except ValueError:
            raise TypeError(
                f'la valeur de la clé "{t_key}" n\'est pas de type {t_type}'
            )

    return result


def get_yaml_infos(file_path: str, fields: tuple) -> dict | None:
    """Récupération des informations d'un fichier YAML et désérialisation des données dans un objet `dict`

    Args:
        @params file_path (str): Nom du fichier YAML
        category (str): Selection du dictionnaire du fichier

    Returns:
        dict: Dictionnaire correspondant a `category` en objet `dict` YAML -> `dict`
    """

    try:
        with open(file_path) as yaml_file:
            config = yaml.safe_load(yaml_file)

        if type(config) != dict:
            return None

        for field in fields:
            if config.get(field) == None:
                return None

        return config

    except FileNotFoundError:
        # "Le fichier de configuration n'a pas été trouvé"
        return None
    except Exception:
        # "Erreur lors de la lecture du fichier YAML"
        return None


def get_last_csv_record(filename: str, releves_properties: tuple) -> dict:
    try:
        with open(filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            last_record = list(reader)[-1]

            for t in releves_properties:
                t_key = t[0]
                if not t_key in last_record.keys():
                    raise Exception(f'la clé "{t_key}" n\'a pas été trouvée!')

            releves_dict = {}

            for t in releves_properties:
                try:
                    t_key = t[0]
                    t_type = t[1]

                    releves_dict[t_key] = t_type(last_record.get(t_key))
                except ValueError:
                    raise Exception(f'la clé "{t_key}" n\'est pas de type {t_type}')

            return releves_dict

    except FileNotFoundError:
        raise Exception("Le fichier spécifier n'existe pas!")

    except Exception as err:
        raise err


def csvfile_to_datas(filename: str):
    try:
        with open(filename, "r") as csvfile:
            datas = []
            spamreader = csv.DictReader(csvfile)

            for record in spamreader:
                horodatage = datetime.strptime(
                    record["horodatage"], "%Y-%m-%d %H:%M:%S"
                )

                datas.append(
                    {
                        "horodatage": horodatage,
                        "temperature": record["temperature"],
                        "humidite": record["humidite"],
                    }
                )

            return datas

    except FileNotFoundError:
        raise Exception("fichier non trouvé")

    except Exception:
        raise Exception(f"erreur lors de la lecture du fichier {filename}")


def add_data(
    filename: str,
    temperature: float,
    humidite: float,
    fieldnames: list = ["horodatage", "temperature", "humidite"],
    records: int = 30,
):
    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_data = csvfile_to_datas()

    while len(csv_data) >= records:
        csv_data.pop(0)

    csv_data.append(
        {"horodatage": horodatage, "temperature": temperature, "humidite": humidite}
    )

    try:
        with open(filename, "w+", newline="") as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames)

            csvwriter.writeheader()
            csvwriter.writerows(csv_data)

    except FileNotFoundError:
        raise Exception("fichier non trouvé")

    except Exception:
        raise Exception(f"erreur lors de la lecture du fichier {filename}")


# TODO review function
def update_db_info(db_info: dict) -> bool:
    db_dict = {
        "host": db_info.get("host"),
        "port": db_info.get("port", "3306"),
        "user": db_info.get("user"),
        "password": db_info.get("password"),
        "database": db_info.get("database"),
    }

    if None in db_dict.values():
        print("Une ou plusieurs valeurs renseignées sont incorrectes!")
        return False

    # Try to connect db & table
    try:
        db = connector.connect(**db_dict)
        cursor = db.cursor()

        select_query = """
            SELECT count(*)
            FROM information_schema.tables
            WHERE table_schema = 's1_projet_cours'
            AND table_name = 'data_local'
        """

        cursor.execute(select_query)
        res = cursor.fetchall()

        if db.is_connected():
            db.disconnect()

        if not int(res[0][0]):
            print("Une ou plusieurs informations entrées ne sont pas valide(s)!")
            exit()

    except connector.DataError:
        print("Erreur lors de l'envoie des données!")
        exit()
    except connector.NotSupportedError:
        print("La base de données utilisé n'est pas compatible avec cette application!")
        exit()
    except connector.OperationalError:
        print("Erreur lors de l'opération sur la base de données!")
        exit()
    except connector.DatabaseError:
        print(
            "Une erreur est survenu lors de la connexion à la base de données, vérifier que l'adresse de la base de données renseigner soit bien valide"
        )
        exit()

    try:
        with open(auth_file, "w") as file:
            if file.writable():
                file.write("database:\n")
                file.writelines([f"{item[0]}: {item[1]}\n" for item in db_dict.items()])

    except Exception as err:
        print(err)
        raise err
