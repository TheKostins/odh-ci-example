from fastapi import FastAPI
from routers.main_router import main_router
from config.environment import get_settings

from contextlib import asynccontextmanager

from alembic.config import Config
from alembic import command
import asyncio

settings = get_settings()

async def run_migrations():
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", str(settings.db_url))
    await asyncio.to_thread(
        command.upgrade,
        config,
        "head",
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_migrations()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(main_router, prefix="/api/v1", tags=["v1"])
