from typing import Any

from fastapi import Depends
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class FavoriteShanyraksResponse(AppModel):
    shanyrak_id: Any = Field(alias="shanyrak_id")
    address: str = Field(alias="address")


@router.get("/")
def get_favorites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    print(jwt_data.user_id, flush=True)
    favs = svc.repository.get_favorites(jwt_data.user_id)
    ret = []

    for elem in favs:
        ret.append(
            FavoriteShanyraksResponse(
                shanyrak_id=elem["shanyrak_id"], address=elem["address"]
            )
        )

    return ret
