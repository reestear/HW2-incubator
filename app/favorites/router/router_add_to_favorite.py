from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.post("/{shanyrak_id:str}")
def add_to_favorites(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    svc.repository.add_to_favorites(shanyrak_id, jwt_data.user_id)

    return Response(status_code=200)
