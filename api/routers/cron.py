from fastapi import APIRouter, Header, HTTPException

from api.services.watchdog import check_power_status

router = APIRouter()


@router.get("/api/cron_watchdog")
async def cron_watchdog(x_vercel_cron: str = Header(None)):
    """
    Solo permite la ejecución si el header X-Vercel-Cron está presente.
    Vercel lo envía automáticamente en las tareas programadas.
    """
    if x_vercel_cron != "1":
        raise HTTPException(status_code=401, detail="No autorizado: Solo ejecutable por un Cron")

    return await check_power_status()
