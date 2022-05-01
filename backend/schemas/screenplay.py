from typing import Optional, Any, List
from datetime import datetime

from pydantic import BaseModel, Field
from enum import Enum


class ContentType(str, Enum):
    HEADING = 'HEADING'
    ACTION = 'ACTION'
    CHARACTER = 'CHARACTER'
    PARENTHETICAL = 'PARENTHETICAL'
    DIALOGUE = 'DIALOGUE'
    SHOT = 'SHOT'
    TRANSITION = 'TRANSITION'
    TEXT = 'TEXT'


class EditorElement(BaseModel):
    content: str
    content_type: ContentType = ContentType.TEXT
    position: int


class ScreenplayBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool

    class Config:
        orm_mode = True


class ScreenplayCreate(ScreenplayBase):
    owner_id: int
    elements: List[EditorElement] = Field(default_factory=list, example=[
        {'content': 'test', 'content_type': 'HEADING', 'position': 0},
        {'content': 'test', 'content_type': 'TEXT', 'position': 1},
        {'content': 'test', 'content_type': 'TRANSITION', 'position': 2},
        {'content': 'test', 'content_type': 'ACTION', 'position': 3},
        {'content': 'test', 'content_type': 'CHARACTER', 'position': 4},
        {'content': 'test', 'content_type': 'PARENTHETICAL', 'position': 5},
        {'content': 'test', 'content_type': 'DIALOGUE', 'position': 6},
        {'content': 'test', 'content_type': 'SHOT', 'position': 7}])


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

    elements: List[Any] = []
