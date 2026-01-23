from fastapi import FastAPI, Request
from api.commands import COMMANDS
from api.security import validate_telegram_request

app = FastAPI(title="ArgosBot")

@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    validate_telegram_request(request, data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        texto = data["message"]["text"]

        # Buscamos si el comando existe en nuestro cargador
        handler = COMMANDS.get(texto)
        if handler:
            handler(chat_id, data)

    return {"status": "ok"}

@app.get("/")
async def home():
    return "ArgosBot está activo"
