from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from database.base_class import Base


class User(Base):
    """
    Class that represents the user table in the database.
    """

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=True)
    last_name = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    screenplays = relationship("Screenplay", back_populates="owner")
