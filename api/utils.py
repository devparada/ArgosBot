import os

import requests


def enviar_mensaje_telegram(mensaje: str, chat_id):
    """
    Envía un mensaje de texto a tu chat de Telegram.
    """
    token = os.environ.get("TELEGRAM_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": mensaje,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")
