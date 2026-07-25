import os
import smtplib
import urllib.parse
import urllib.request
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


def alertas_activas():
    valor = os.getenv(
        "ALERTAS_ACTIVAS",
        "false"
    ).lower()

    return valor in [
        "true",
        "1",
        "yes",
        "si",
        "sí"
    ]


def enviar_alerta_telegram(mensaje: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        return {
            "canal": "telegram",
            "enviado": False,
            "detalle": "Telegram no configurado"
        }

    try:
        url = (
            "https://api.telegram.org/"
            f"bot{token}/sendMessage"
        )

        datos = urllib.parse.urlencode(
            {
                "chat_id": chat_id,
                "text": mensaje
            }
        ).encode("utf-8")

        solicitud = urllib.request.Request(
            url,
            data=datos
        )

        with urllib.request.urlopen(
            solicitud,
            timeout=10
        ) as respuesta:
            return {
                "canal": "telegram",
                "enviado": respuesta.status == 200,
                "codigo": respuesta.status,
                "detalle": (
                    "Mensaje enviado por Telegram"
                )
            }

    except Exception as error:
        return {
            "canal": "telegram",
            "enviado": False,
            "detalle": str(error)
        }


def enviar_alerta_correo(
    asunto: str,
    mensaje: str
):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(
        os.getenv("SMTP_PORT", "587")
    )
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM")
    smtp_to = os.getenv("SMTP_TO")

    if not all(
        [
            smtp_host,
            smtp_user,
            smtp_password,
            smtp_from,
            smtp_to
        ]
    ):
        return {
            "canal": "correo",
            "enviado": False,
            "detalle": "Correo no configurado"
        }

    try:
        correo = EmailMessage()
        correo["Subject"] = asunto
        correo["From"] = smtp_from
        correo["To"] = smtp_to
        correo.set_content(mensaje)

        with smtplib.SMTP(
            smtp_host,
            smtp_port,
            timeout=10
        ) as servidor:
            servidor.starttls()
            servidor.login(
                smtp_user,
                smtp_password
            )
            servidor.send_message(correo)

        return {
            "canal": "correo",
            "enviado": True,
            "detalle": (
                "Correo enviado correctamente"
            )
        }

    except Exception as error:
        return {
            "canal": "correo",
            "enviado": False,
            "detalle": str(error)
        }


def enviar_alerta(
    mensaje: str,
    asunto: str = "Alerta NetAdmin API"
):
    if not alertas_activas():
        return {
            "alertas_activas": False,
            "detalle": (
                "Las alertas están desactivadas"
            )
        }

    canal = os.getenv(
        "ALERTA_CANAL",
        "telegram"
    ).lower()

    resultados = []

    if canal in ["telegram", "ambos"]:
        resultados.append(
            enviar_alerta_telegram(mensaje)
        )

    if canal in [
        "correo",
        "email",
        "ambos"
    ]:
        resultados.append(
            enviar_alerta_correo(
                asunto,
                mensaje
            )
        )

    return {
        "alertas_activas": True,
        "canal_configurado": canal,
        "resultados": resultados
    }