from datetime import timedelta, datetime
from typing import Union, Any, Optional

import jwt
from fastapi import HTTPException
from fastapi.openapi.models import OAuthFlows, SecurityBase
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

import crud
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def create_access_token(
    user_id: int, expires_delta: timedelta = None, db: Session = None
) -> str:
    return encode_auth_data(
        user_id, db, expires_delta, settings.ACCESS_TOKEN_EXPIRE_MINUTES, settings.JWT_ACCESS_TOKEN_SECRET)


def create_refresh_token(
    user_id: int, expires_delta: timedelta = None, db: Session = None
) -> str:
    return encode_auth_data(user_id, db, expires_delta)


def decode_access_token(token: str) -> Union[dict, Any]:
    return decode_token(token, settings.JWT_ACCESS_TOKEN_SECRET, verify_signature=True)


def decode_refresh_token(token: str) -> Union[dict, Any]:
    return decode_token(token)


def decode_token(
        token: str, secret: str = settings.JWT_REFRESH_TOKEN_SECRET, verify_signature: bool = False
) -> Union[dict, Any]:
    try:
        payload = jwt.decode(
            jwt=token, key=secret, algorithms=[ALGORITHM], options={'verify_signature': verify_signature})
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="Token is expired",
        )


def encode_auth_data(
        user_id: int,
        db: Session = None,
        expires_delta: timedelta = None,
        default_exp_time: int = settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        secret: str = settings.JWT_REFRESH_TOKEN_SECRET
) -> str:
    if not db:
        raise Exception("No database session provided")
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=default_exp_time
        )
    if secret == settings.JWT_REFRESH_TOKEN_SECRET:
        token_type = "refresh"
    else:
        token_type = "access"
    user = crud.user.get(db, id=user_id)
    if not user:
        raise Exception("User not found")
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": expire,
        "sub": user.id,
        "type": token_type,
    }
    encoded_jwt = jwt.encode(payload, secret, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlows(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("refresh_token")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        param = {
            "access_token":  header_param if header_scheme.lower() == "bearer" else '',
            "refresh_token": cookie_param if cookie_scheme.lower() == "bearer" else ''
        }

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme

        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param


class BasicAuth(SecurityBase):
    def __init__(self, scheme_name: str = None, auto_error: bool = True):
        super().__init__()
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "basic":
            if self.auto_error:
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param
