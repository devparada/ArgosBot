from fastapi import FastAPI, Request
import os, requests

from api.security import validate_telegram_request

app = FastAPI(title="ArgosBot")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
URL_TELEGRAM = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    validate_telegram_request(request, data)

    try:
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            texto_recibido = data["message"].get("text", "")

            # Si el usuario escribe /hello, ArgosBot responde
            if texto_recibido == "/hello":
                payload = {
                    "chat_id": chat_id,
                    "text": "¡Hola! Soy ArgosBot. El servidor funciona."
                }
                requests.post(URL_TELEGRAM + "sendMessage", json=payload, timeout=5)

    except KeyError:
        pass

    return {"status": "ok"}

@app.get("/")
async def home():
    return "ArgosBot está activo"
