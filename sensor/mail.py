import smtplib
from email.message import EmailMessage


def send_mail(email_info: dict, subject: str, body: str) -> None:
    """Envoie d'email

    Args:
        email_info (dict): Informations du compte
        subject (str): Sujet de l'email
        body (str): Contenu du corps de l'email
    """

    with smtplib.SMTP(
        email_info.get("server_addr"), email_info.get("server_port")
    ) as server:
        server.starttls()
        server.login(email_info.get("sender").original, email_info.get("password"))

        msg = EmailMessage()
        msg["Subject"] = subject

        msg["From"] = email_info.get("sender")
        msg["To"] = ", ".join(email_info.get("destinations"))
        msg.set_content(body)

        server.send_message(msg)
