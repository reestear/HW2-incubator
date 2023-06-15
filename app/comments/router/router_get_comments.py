from fastapi import Depends, status

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.get("/{shanyrak_id:str}/comments", status_code=status.HTTP_201_CREATED)
def get_comments(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    return svc.repository.get_comments(shanyrak_id)
