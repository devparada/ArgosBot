from fastapi import APIRouter, Header, Request

from api.services.ups import procesar_cambio_ups

router = APIRouter()


@router.post("/api/webhook/ups")
async def recibir_webhook_ups(request: Request, authorization: str = Header(None)):
    data = await request.json()
    return await procesar_cambio_ups(data, authorization)
