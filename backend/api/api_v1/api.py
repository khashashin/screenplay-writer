from fastapi import APIRouter

from api.api_v1.endpoints import screenplays, users, auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(screenplays.router, prefix="/screenplays", tags=["screenplays"])
