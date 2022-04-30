from sqlalchemy.orm import Session

import crud
import schemas
from core.config import settings
from database import base  # noqa: F401


def init_db(db: Session) -> None:

    user = crud.user.get_by_email(db, email=settings.PROJECT_ADMIN_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.PROJECT_ADMIN_EMAIL,
            password=settings.PROJECT_ADMIN_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
