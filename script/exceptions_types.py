class InvalidEmailException(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        message = f'l\'adresse e-mail "{email}" est invalide'
        super().__init__(message)


class MissingKeyException(Exception):
    def __init__(self, key) -> None:
        self.key = key
        message = f'la clé "{key}" n\'est pas présente'
        super().__init__(message)


class InvalidEmailDestinationsException(Exception):
    def __init__(self, email: str) -> None:
        message = f"l'adresse email \"{email}\" n'existe pas"
        super().__init__(message)


class EmailUndeliverableException(Exception):
    def __init__(self, email: str) -> None:
        message = f"l'adresse email \"{email}\" n'est pas délivrable"
        super().__init__(message)


class NoMeasuresException(Exception):
    def __init__(self, err_msg: str) -> None:
        message = (
            err_msg
            + "\nAssurez-vous d'avoir lancé le script d'acquisition des données du capteur DHT22"
        )
        super().__init__(message)
