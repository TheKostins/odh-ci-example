from fastapi import FastAPI
from routers.main_router import main_router
from config.environment import get_settings

settings = get_settings()

app = FastAPI()
app.include_router(main_router, prefix="/api/v1", tags=["v1"])
