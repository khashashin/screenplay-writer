from typing import Optional, Any
from datetime import datetime

from pydantic import BaseModel


class ScreenplayBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool

    class Config:
        orm_mode = True


class ScreenplayCreate(ScreenplayBase):
    pass


class ScreenplayUpdate(ScreenplayBase):
    pass


class ScreenplayDelete(ScreenplayBase):
    deleted_at: Optional[Any] = None


class Screenplay(ScreenplayBase):
    id: int
    owner_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[Any] = None
