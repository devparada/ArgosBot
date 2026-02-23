import asyncio

import httpx
from upstash_redis import Redis

from api.config import Config
from api.utils import enviar_mensaje_telegram

redis = Redis(
    url=Config.UPSTASH_URL,
    token=Config.UPSTASH_TOKEN
)


async def check_power_status():
    if not Config.TARGET_URL:
        return {"error": "TARGET_URL no configurada"}

    esta_online = False

    # Intentamos conectar con casa
    async with httpx.AsyncClient(verify=False) as client:
        for i in range(3):
            try:
                response = await client.get(f"https://{Config.TARGET_URL}", timeout=10)
                if response.status_code == 200:
                    esta_online = True
                    break
            except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError):
                if i < 2:  # No esperar en el último intento
                    await asyncio.sleep(2)

    nuevo_estado = "online" if esta_online else "offline"

    # Lógica de Redis
    res_redis = redis.get("estado_luz")
    estado_anterior = res_redis if res_redis else "desconocido"

    if nuevo_estado != estado_anterior:
        if nuevo_estado == "offline":
            texto = "*Apagón*: No se puede contactar con la casa."
        else:
            texto = "*Luz*: Conexión restablecida."

        redis.set("estado_luz", nuevo_estado)
        if Config.MY_USER_ID:
            enviar_mensaje_telegram(texto, Config.MY_USER_ID)
        return {"status": "changed", "new_state": nuevo_estado}

    return {"status": "unchanged", "state": nuevo_estado}
