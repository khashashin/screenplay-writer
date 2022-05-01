from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import crud
import schemas
from api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Screenplay])
def get_screenplay_list(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get screenplay list.
    Allow only if user is owner or superuser.
    """
    if crud.user.is_superuser(current_user):
        screenplays = crud.screenplay.get_multi(db, skip=skip, limit=limit)
    else:
        screenplays = crud.screenplay.get_multi_by_owner(db=db, owner_id=current_user.id, skip=skip, limit=limit)
    return screenplays


@router.post("/", response_model=schemas.Screenplay)
async def create_screenplay(
        *,
        db: Session = Depends(deps.get_db),
        screenplay_in: schemas.ScreenplayCreate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new screenplay.
    Any registered user can create new screenplay.
    """
    data = {
        "name": screenplay_in.name,
        "description": screenplay_in.description,
        "is_public": screenplay_in.is_public,
        "owner_id": current_user.id,
        "elements": screenplay_in.elements
    }
    return await crud.screenplay.create(db=db, obj_in=data)


@router.get("/{screenplay_id}", response_model=schemas.Screenplay)
def get_screenplay(
        *,
        db: Session = Depends(deps.get_db),
        screenplay_id: int,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get screenplay by ID.
    Allow only if user is owner or superuser.
    """
    screenplay = crud.screenplay.get(db=db, id=screenplay_id)
    if not screenplay:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Project not found")
    if not crud.user.is_superuser(current_user) or screenplay.owner_id != current_user.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
    return screenplay


@router.put("/{screenplay_id}", response_model=schemas.Screenplay)
def update_screenplay(
        *,
        db: Session = Depends(deps.get_db),
        screenplay_id: int,
        screenplay_in: schemas.ScreenplayUpdate,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update screenplay.
    Allow only if user is owner or superuser.
    """
    screenplay = crud.screenplay.get(db=db, id=screenplay_id)
    if not screenplay:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Project not found")
    if not crud.user.is_superuser(current_user) or screenplay.owner_id != current_user.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
    return crud.screenplay.update(db=db, db_obj=screenplay, obj_in=screenplay_in)


@router.delete("/{screenplay_id}", response_model=schemas.ScreenplayDelete)
def delete_screenplay(
        *,
        db: Session = Depends(deps.get_db),
        screenplay_id: int,
        current_user: schemas.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete screenplay
    Allow only if user is owner or superuser.
    """
    screenplay = crud.screenplay.get(db=db, id=screenplay_id)
    if not screenplay:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Project not found")
    if not crud.user.is_superuser(current_user) or screenplay.owner_id != current_user.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
    return crud.screenplay.remove(db=db, id=screenplay_id)


@router.get("/public/{screenplay_id}", response_model=schemas.Screenplay)
def get_public_screenplay(
        *,
        db: Session = Depends(deps.get_db),
        screenplay_id: int,
) -> Any:
    """
    Get public screenplay by ID
    """
    screenplay = crud.screenplay.get(db=db, id=screenplay_id)
    if not screenplay or not screenplay.is_public:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return screenplay


@router.get("/public/", response_model=List[schemas.Screenplay])
def get_public_screenplay(
        *,
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get all public screenplays
    """
    screenplay = crud.screenplay.get_multi_public(db=db)
    return screenplay
