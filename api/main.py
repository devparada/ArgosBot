from fastapi import FastAPI

from api.routers import cron, telegram, ups

app = FastAPI(title="ArgosBot")

app.include_router(telegram.router)
app.include_router(cron.router)
app.include_router(ups.router)


@app.get("/")
async def home():
    return "ArgosBot está activo"
