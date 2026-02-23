import requests
from requests import RequestException

from api.config import Config
from api.utils import enviar_mensaje_telegram

URL_TELEGRAM = f"https://api.telegram.org/bot{Config.TELEGRAM_TOKEN}/sendMessage"


def cmd_hello(chat_id, _data=None):
    texto = "¡Hola! Soy ArgosBot. El servidor funciona."
    enviar_mensaje_telegram(texto, chat_id)


def cmd_status(chat_id, _data=None):
    # Aquí es donde verificaremos si hay internet/luz
    try:
        # Hacemos una petición rápida para ver si hay conexión
        response = requests.get(f"https://{Config.TARGET_URL}", timeout=2)

        if response.status_code == 200:
            status = "Todo normal. El dispositivo está online."
        else:
            status = f"Respuesta inusual del servidor: {response.status_code}"
    except (TimeoutError, ConnectionError, RequestException):
        status = "¡ALERTA! No hay conexión con el objetivo (Posible corte de luz)."

    enviar_mensaje_telegram(status, chat_id)


# Diccionario que mapea el texto del comando a la función
COMMANDS = {
    "/hello": cmd_hello,
    "/status": cmd_status
}
