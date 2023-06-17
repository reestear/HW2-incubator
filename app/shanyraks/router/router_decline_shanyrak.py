from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.post("/{shanyrak_id:str}/approve")
def decline_shanyrak(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    if jwt_data.role != "moderator":
        return Response(status_code=403)
    svc.repository.decline_shanyrak_by_id(shanyrak_id)
    return Response(status_code=201)
