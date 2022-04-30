from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.base_class import Base


class Screenplay(Base):
    """
    Class that represents the screenplay table in the database.
    """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_public = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="screenplays")
