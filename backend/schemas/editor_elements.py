from enum import Enum
from typing import Optional, Any
from datetime import datetime

from pydantic import BaseModel


class ContentType(str, Enum):
    HEADING = 'HEADING'
    ACTION = 'ACTION'
    CHARACTER = 'CHARACTER'
    PARENTHETICAL = 'PARENTHETICAL'
    DIALOGUE = 'DIALOGUE'
    SHOT = 'SHOT'
    TRANSITION = 'TRANSITION'
    TEXT = 'TEXT'


class EditorElementBase(BaseModel):
    content: str
    content_type: ContentType
    position: int

    class Config:
        orm_mode = True


class EditorElementCreate(EditorElementBase):
    pass


class EditorElementDelete(EditorElementBase):
    deleted_at: Optional[Any] = None


class EditorElement(EditorElementBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[Any] = None
