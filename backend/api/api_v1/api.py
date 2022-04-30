from fastapi import APIRouter

from api.api_v1.endpoints import screenplays

api_router = APIRouter()
api_router.include_router(screenplays.router, prefix="/screenplays", tags=["screenplays"])
