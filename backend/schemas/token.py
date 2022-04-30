from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None


class TokenPayload(BaseModel):
    email: str = None
    sub: Optional[int] = None
