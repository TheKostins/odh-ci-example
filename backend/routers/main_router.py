from fastapi import APIRouter
from .topic_router import topic_router

main_router = APIRouter()

main_router.include_router(topic_router, tags=["topics"])
