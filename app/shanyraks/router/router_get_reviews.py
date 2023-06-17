from typing import Any

from fastapi import Depends, Response
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class Shanyrak(AppModel):
    id: Any = Field(alias="_id")
    type: str = Field(alias="type")
    price: int = Field(alias="price")
    address: str = Field(alias="address")
    area: float = Field(alias="area")
    room_count: int = Field(alias="room_count")


@router.get("/review")
def get_review(
    offset: int = None,
    limit: int = None,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    if jwt_data.role != "moderator":
        return Response(status_code=403)
    result = svc.repository.get_review(offset, limit)
    reviews = []

    for item in result["review"]:
        reviews.append(Shanyrak(**item))

    return {"total": result["total"], "reviews": reviews}
