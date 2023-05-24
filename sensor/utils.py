import yaml
import csv
from mysql import connector


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


def get_last_csv_record(filename: str) -> dict | None:
    try:
        with open(filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            last_record = list(reader)[-1]
            return {
                "horodatate": last_record["horodatage"],
                "temperature": float(last_record["temperature"]),
                "humidity": float(last_record["humidite"]),
            }

    except Exception:
        # Une erreur s'est produite lors de la lecture du fichier
        return None


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
