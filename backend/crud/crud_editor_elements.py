from datetime import datetime

from sqlalchemy.orm import Session
from crud.base import CRUDBase
import models
import schemas


class CRUDEditorElement(CRUDBase[models.EditorElement, schemas.EditorElementCreate, schemas.EditorElement]):

    @staticmethod
    def create(db: Session, obj_in: schemas.EditorElementCreate) -> schemas.EditorElement:
        db_obj = models.EditorElement()
        db_obj.content = obj_in.content
        db_obj.content_type = obj_in.content_type
        db_obj.position = obj_in.position
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: models.EditorElement, obj_in: schemas.EditorElement) -> schemas.EditorElement:
        if obj_in["content"]:
            db_obj.content = obj_in["content"]
        if obj_in["content_type"]:
            db_obj.content_type = obj_in["content_type"]
        if obj_in["position"]:
            db_obj.position = obj_in["position"]
        db_obj.updated_at = datetime.now()
        db.commit()
        db.refresh(db_obj)
        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)


editor_element = CRUDEditorElement(models.EditorElement)
