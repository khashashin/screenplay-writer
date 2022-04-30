from typing import Any

from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter()


@router.get("/")
def get_screenplay_list() -> Any:
    """
    Get screenplay list
    """

    return JSONResponse(
        content={"message": "Get screenplay list"},
        status_code=200,
    )
