from typing import Generator

import jwt
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import crud
import models
import schemas
from core.config import settings
from core.security import OAuth2PasswordBearerCookie, decode_access_token, decode_refresh_token
from database.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearerCookie(
    tokenUrl=f"{settings.API_V1}/auth/login/access-token",
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        access_token = decode_access_token(token["access_token"])
        token_data = schemas.TokenPayload(**access_token)
    except jwt.PyJWTError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong, please try to login again",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Permission denied"
        )
    return current_user


def get_user_with_expired_access_token(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        refresh_token = decode_refresh_token(token["refresh_token"])
        token_data = schemas.TokenPayload(**refresh_token)
    except jwt.PyJWTError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong, please try to login again",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    if not crud.user.is_active(user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Inactive user")

    return user
