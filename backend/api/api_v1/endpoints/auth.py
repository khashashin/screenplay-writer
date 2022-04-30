from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

import crud
import schemas
from api import deps
from api.deps import get_current_active_user, get_user_with_expired_access_token
from core import security
from core.config import settings

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    response: Response,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    stay_logged_in: bool = False
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    if stay_logged_in:
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = security.create_refresh_token(
            user.id, expires_delta=refresh_token_expires, db=db
        ),
        response.set_cookie(
            key="refresh_token",
            value=f"Bearer {refresh_token}",
            httponly=True,
            max_age=int(refresh_token_expires.total_seconds()),
        )
    else:
        access_token_expires = access_token_expires + timedelta(hours=12)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires, db=db
        ),
    }


@router.post("/login/refresh-token",
             response_model=schemas.Token, dependencies=[Depends(get_user_with_expired_access_token)])
def login_refresh_token(
    request: Request, response: Response, db: Session = Depends(deps.get_db)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    cookie_authorization: str = request.cookies.get("refresh_token")
    cookie_scheme, cookie_param = get_authorization_scheme_param(
        cookie_authorization
    )

    if not cookie_scheme.lower() == "bearer":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    refresh_token = cookie_param
    payload = security.decode_refresh_token(refresh_token)
    if not payload:
        response.delete_cookie("refresh_token")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    user = crud.user.get(db, id=payload.get("user_id"))
    if not user or not crud.user.is_active(user):
        response.delete_cookie("refresh_token")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires, db=db
        ),
    }


@router.post("/login/remove-token", dependencies=[Depends(get_current_active_user)])
def remove_token(
    response: Response
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    response.delete_cookie("refresh_token")
    return {}


@router.get("/login/check-token", dependencies=[Depends(get_current_active_user)])
def check_access_token_validity() -> Any:
    return {}
