import os

from fastapi import Request, HTTPException

# Cargamos las variables de entorno
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
AUTHORIZED_USER_ID = os.getenv("MY_USER_ID")


def validate_telegram_request(request: Request, data: dict):
    # Validar que la petición viene de Telegram
    x_telegram_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if x_telegram_token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Origen no autorizado")

    # Validar que el mensaje es de TU ID de usuario
    message = data.get("message") or data.get("callback_query", {}).get("message")

    if not message:
        return True

    # Comprueba que el ID sea el autorizado
    user_id = message.get("from", {}).get("id")
    if str(user_id) != str(AUTHORIZED_USER_ID):
        print(f"Intento de acceso no autorizado")
        raise HTTPException(status_code=403, detail="Usuario no autorizado")

    return True
