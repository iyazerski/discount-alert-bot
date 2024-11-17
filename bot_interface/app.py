import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from bot_interface.processors import bot, db


@asynccontextmanager
async def lifespan(_: FastAPI):
    asyncio.create_task(bot.start())
    yield
    await bot.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    try:
        db.healthcheck()
    except RuntimeError:
        return {"status": "unhealthy"}

    return {"status": "healthy"}
