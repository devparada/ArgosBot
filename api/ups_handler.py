import logging
import time

from fastapi import HTTPException
from upstash_redis.asyncio import Redis

from api.config import Config
from api.utils import enviar_mensaje_telegram

logger = logging.getLogger(__name__)

r = Redis(
    url=Config.UPSTASH_URL,
    token=Config.UPSTASH_TOKEN
)


async def procesar_cambio_ups(data: dict, authorization: str):
    # Validación de seguridad
    expected_token = f"Bearer {Config.SECRET_TOKEN}"
    if authorization != expected_token:
        raise HTTPException(status_code=401, detail="No autorizado")

    estado_ups = data.get("estado_ups")
    if not estado_ups:
        raise HTTPException(status_code=400, detail="Falta el campo estado_ups")

    estado_anterior = await r.get("estado_ups") or "online"

    # Control de reincidencia
    if estado_ups == estado_anterior:
        logger.info("Estado idéntico al actual. Abortando envío para evitar spam.")
        return {"status": "ignored", "estado": estado_ups}

    await r.set("estado_ups", estado_ups.lower())

    # Obtener Chat ID de forma segura y flexible
    chat_id = getattr(Config, 'TELEGRAM_CHAT_ID', getattr(Config, 'MY_USER_ID', None))
    if not chat_id:
        logger.error("Chat ID no definido. Imposible notificar a Telegram.")
        return {"status": "error", "detail": "Missing Chat ID"}

    # Evaluación de estados y notificaciones
    if estado_ups == "ONBATT":
        await r.set("tiempo_caido", str(int(time.time())))
        enviar_mensaje_telegram(
            "*¡ALERTA:* Corte de luz detectado en casa!\n El SAI ha entrado en baterías.",
            chat_id
        )

    elif estado_ups == "ONLINE":
        start_time_str = await r.get("tiempo_caido")
        duracion_texto = ""

        if start_time_str and start_time_str != "0":
            downtimes_segundos = int(time.time()) - int(start_time_str)
            minutos = downtimes_segundos // 60
            duracion_texto = f"⏱️Tiempo sin servicio: {minutos} minutos."

        await r.set("tiempo_caido", "0")
        enviar_mensaje_telegram(
            f"*¡AVISO:* La energía eléctrica ha sido restaurada.\n{duracion_texto}",
            chat_id
        )

    elif estado_ups == "LOWBATT":
        enviar_mensaje_telegram(
            "🚨 *¡CRÍTICO:* Batería baja en el SAI!\nApagado de emergencia en curso.",
            chat_id
        )

    return {"status": "received", "estado": estado_ups}
