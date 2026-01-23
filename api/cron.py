import os, requests
from requests.exceptions import RequestException, Timeout, ConnectionError

# Cargamos variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MY_USER_ID = os.getenv("MY_USER_ID")
TARGET_URL = os.getenv("TARGET_URL")
URL_TELEGRAM = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def check_power_status():
    try:
        # Intentamos conectar con el puerto de casa
        # Usamos un timeout corto (10 s) para que el cron no se quede colgado
        response = requests.get(f"https://{TARGET_URL}", timeout=10, verify=False)

        # Si responde 200, hay luz. No enviamos nada para no molestar.
        if response.status_code == 200:
            return {"status": "ok", "message": "Conexión estable"}

    except (RequestException, Timeout, ConnectionError):
        # SI FALLA: Enviamos el mensaje de alerta proactivo
        payload = {
            "chat_id": MY_USER_ID,
            "text": "**ALERTA PROACTIVA**: He perdido conexión con tu casa. Posible corte de luz o caída de red."
        }
        requests.post(URL_TELEGRAM, json=payload, timeout=5)
        return {"status": "error", "message": "Alerta enviada"}

    return {"status": "unknown"}
