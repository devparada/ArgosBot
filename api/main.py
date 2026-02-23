from fastapi import FastAPI, Request, Header, HTTPException

from api.commands import COMMANDS
from api.cron import check_power_status
from api.security import validate_telegram_request

app = FastAPI(title="ArgosBot")


@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    validate_telegram_request(request, data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        texto = data["message"]["text"]

        # Buscamos si el comando existe en el cargador
        handler = COMMANDS.get(texto)
        if handler:
            handler(chat_id, data)

    return {"status": "ok"}


@app.get("/api/cron_watchdog")
async def cron_watchdog(x_vercel_cron: str = Header(None)):
    """
    Solo permite la ejecución si el header X-Vercel-Cron está presente.
    Vercel lo envía automáticamente en las tareas programadas.
    """
    if x_vercel_cron != "1":
        # Si alguien entra desde el navegador, recibirá un 401
        raise HTTPException(status_code=401, detail="No autorizado: Solo ejecutable por un Cron")

    result = check_power_status()
    return result


@app.get("/")
async def home():
    return "ArgosBot está activo"
