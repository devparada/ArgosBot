from fastapi import APIRouter, Request

from api.commands.hello import cmd_hello
from api.commands.status import cmd_status
from api.security import validate_telegram_request

router = APIRouter()

COMMANDS = {
    "/hello": cmd_hello,
    "/status": cmd_status,
}


@router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    validate_telegram_request(request, data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        texto = data["message"]["text"]

        handler = COMMANDS.get(texto)
        if handler:
            handler(chat_id, data)

    return {"status": "ok"}
