import smtplib
from email.message import EmailMessage
from email_validator import (
    validate_email,
    EmailSyntaxError,
    EmailUndeliverableError,
)

from exceptions_types import *
from utils import check_properties


def send_mail(email_info: dict, subject: str, body: str) -> None:
    """Envoie d'email

    Args:
        email_info (dict): Informations du compte
        subject (str): Sujet de l'email
        body (str): Contenu du corps de l'email
    """

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

    with smtplib.SMTP(
        email_info.get("server_addr"), email_info.get("server_port")
    ) as server:
        server.starttls()
        server.login(email_dict.get("sender").original, email_dict.get("password"))

        msg = EmailMessage()
        msg["Subject"] = subject

        msg["From"] = email_dict.get("sender").original
        msg["To"] = ", ".join(email_dict.get("destinations"))
        msg.set_content(body)

        server.send_message(msg)
