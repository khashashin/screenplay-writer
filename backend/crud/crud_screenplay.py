from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from crud.base import CRUDBase
import models
import schemas


class CRUDScreenplay(CRUDBase[models.Screenplay, schemas.ScreenplayBase, schemas.ScreenplayBase]):

    @staticmethod
    def create(db: Session, *, obj_in: schemas.ScreenplayCreate) -> models.Screenplay:
        db_obj = models.Screenplay()
        db_obj.name = obj_in.name
        db_obj.description = obj_in.description
        db_obj.is_public = obj_in.is_public
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: models.Screenplay, obj_in: schemas.ScreenplayBase) -> models.Screenplay:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["name"]:
            db_obj.name = update_data["name"]
        if update_data["description"]:
            db_obj.description = update_data["description"]

        db_obj.updated_at = datetime.now()
        return super().update(db=db, db_obj=db_obj, obj_in=update_data)

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.Screenplay]:
        return (
            db.query(self.model)
            .filter(models.Screenplay.owner_id == owner_id, models.Screenplay.deleted_at is None)
            .offset(skip)
            .limit(limit)
            .all()
        )


screenplay = CRUDScreenplay(models.Screenplay)
