import os

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from upstash_redis import Redis

from api.utils import enviar_mensaje_telegram

# Cargamos variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MY_USER_ID = os.getenv("MY_USER_ID")
TARGET_URL = os.getenv("TARGET_URL")
URL_TELEGRAM = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

redis = Redis(
    url=os.environ.get("UPSTASH_REDIS_REST_URL"),
    token=os.environ.get("UPSTASH_REDIS_REST_TOKEN")
)


def check_power_status():
    # Intentamos conectar con casa
    try:
        response = requests.get(f"https://{TARGET_URL}", timeout=10, verify=False)
        esta_online = (response.status_code == 200)
    except (RequestException, Timeout, ConnectionError):
        esta_online = False

    nuevo_estado = "online" if esta_online else "offline"

    # Control de Reincidencia con Upstash
    estado_anterior = redis.get("estado_luz")

    if nuevo_estado != estado_anterior:
        if nuevo_estado == "offline":
            enviar_mensaje_telegram("*Apagón*: No se puede contactar con la casa.")
        else:
            enviar_mensaje_telegram("*Luz*: Conexión restablecida.")

        redis.set("estado_luz", nuevo_estado)
        return {"status": "changed", "new_state": nuevo_estado}

    return {"status": "unchanged", "state": nuevo_estado}
