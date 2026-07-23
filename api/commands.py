import requests
from requests import RequestException
from upstash_redis import Redis

from api.config import Config
from api.utils import enviar_mensaje_telegram

r = Redis(
    url=Config.UPSTASH_URL,
    token=Config.UPSTASH_TOKEN
)


def cmd_hello(chat_id, _data=None):
    texto = "¡Hola! Soy ArgosBot. El servidor funciona."
    enviar_mensaje_telegram(texto, chat_id)


def cmd_status(chat_id, _data=None):
    # Verificación activa de conectividad para el comando manual
    try:
        response = requests.get(f"https://{Config.TARGET_URL}", timeout=5)
        conexion_activa = response.status_code == 200
    except (TimeoutError, ConnectionError, RequestException):
        conexion_activa = False

    # Lectura del estado persistido por el ups_handler (SAI / energía)
    estado_ups = r.get("estado_ups") or "online"
    start_time_str = r.get("tiempo_caido")

    if conexion_activa and estado_ups == "online":
        texto = "El sistema está operativo, con red y sin incidencias."
    else:
        duracion_texto = ""
        if start_time_str and start_time_str != "0":
            import time
            downtimes_segundos = int(time.time()) - int(start_time_str)
            minutos = downtimes_segundos // 60
            duracion_texto = f" Tiempo transcurrido: {minutos} minutos."

        if not conexion_activa and estado_ups != "online":
            texto = f"¡ALERTA! Sin conexión a internet y el SAI reporta corte eléctrico.{duracion_texto}"
        elif not conexion_activa:
            texto = f"¡ALERTA! No hay conexión con el objetivo (posible caída de red).{duracion_texto}"
        else:
            texto = f"¡ALERTA! El sistema sigue en estado crítico por corte de luz.{duracion_texto}"

    enviar_mensaje_telegram(texto, chat_id)


COMMANDS = {
    "/hello": cmd_hello,
    "/status": cmd_status
}
