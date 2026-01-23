import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
URL_TELEGRAM = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
TARGET_URL = os.getenv("TARGET_URL")

def cmd_hello(chat_id):
    payload = {"chat_id": chat_id, "text": "¡Hola! Soy ArgosBot. El servidor funciona."}
    requests.post(URL_TELEGRAM, json=payload, timeout=5)

def cmd_status(chat_id):
    # Aquí es donde verificaremos si hay internet/luz
    try:
        # Hacemos una petición rápida para ver si hay conexión
        response = requests.get(f"https://{TARGET_URL}", timeout=2)

        if response.status_code == 200:
            status = "Todo normal. El dispositivo está online."
        else:
            status = f"Respuesta inusual del servidor: {response.status_code}"
    except (TimeoutError, ConnectionError):
        status = "¡ALERTA! No hay conexión con el objetivo (Posible corte de luz)."

    payload = {"chat_id": chat_id, "text": status}
    requests.post(URL_TELEGRAM, json=payload, timeout=5)

# Diccionario que mapea el texto del comando a la función
COMMANDS = {
    "/hello": cmd_hello,
    "/status": cmd_status
}