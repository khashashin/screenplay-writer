from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from crud.base import CRUDBase
import models
import schemas


class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[models.User]:
        _user = self.get_by_email(db, email=email)
        if not _user:
            return None
        if not verify_password(password, _user.hashed_password):
            return None
        return _user

    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def create(db: Session, *, obj_in: schemas.UserCreate) -> models.User:
        db_obj = models.User()
        db_obj.email = obj_in.email
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db_obj.first_name = obj_in.first_name
        db_obj.last_name = obj_in.last_name
        db_obj.is_superuser = obj_in.is_superuser
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: models.User, obj_in: Union[schemas.UserUpdate, Dict[str, Any]]
    ) -> models.User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    @staticmethod
    def is_active(_user: models.User) -> bool:
        return _user.is_active

    @staticmethod
    def is_superuser(_user: models.User) -> bool:
        return _user.is_superuser


user = CRUDUser(models.User)
