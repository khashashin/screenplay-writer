import enum
from sqlalchemy import Enum
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base_class import Base


class ContentType(str, enum.Enum):
    HEADING = 'HEADING'
    ACTION = 'ACTION'
    CHARACTER = 'CHARACTER'
    PARENTHETICAL = 'PARENTHETICAL'
    DIALOGUE = 'DIALOGUE'
    SHOT = 'SHOT'
    TRANSITION = 'TRANSITION'
    TEXT = 'TEXT'


class EditorElement(Base):
    """
    Class that represents the Heading table of Screenplay in the database.
    """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    content = Column(String, nullable=True)
    content_type = Column(Enum(ContentType), nullable=True, default='TEXT')
    position = Column(Integer, nullable=True)

    screenplay_id = Column(Integer, ForeignKey('screenplays.id', ondelete="CASCADE"), nullable=False)

    screenplay = relationship("Screenplay", back_populates="elements")
