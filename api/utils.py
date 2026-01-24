import os

import requests


def enviar_mensaje_telegram(mensaje: str, chat_id: str = None):
    """
    Envía un mensaje de texto a tu chat de Telegram.
    """
    token = os.environ.get("TELEGRAM_TOKEN")
    target_chat = chat_id or os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not target_chat:
        print("Error: No se han configurado las variables de Telegram")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": target_chat,
        "text": mensaje,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")
