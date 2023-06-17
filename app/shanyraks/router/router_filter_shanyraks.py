from typing import Any, List

from fastapi import Depends, Response
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class Shanyrak(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    room_count: int
    description: str
    user_id: Any
    media: list[str] = []
    comments: list[Any] = []
    location: Any


class GetShanyraksResponse(AppModel):
    total: int
    shanyraks: List[Shanyrak]


@router.get("/", response_model=GetShanyraksResponse)
def filter_shanyraks(
    limit: int = None,
    offset: int = None,
    type: str = None,
    room_count: int = None,
    price_from: float = None,
    price_untill: float = None,
    latitude: float = None,
    longitude: float = None,
    radius: float = None,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    if latitude is not None or longitude is not None or radius is not None:
        if latitude is None or longitude is None or radius is None:
            return Response(status_code=400)

    filtering = {
        "limit": limit,
        "offset": offset,
        "type": type,
        "room_count": room_count,
        "price_from": price_from,
        "price_untill": price_untill,
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
    }

    result = svc.repository.filter_shanyraks(filtering)
    return result
