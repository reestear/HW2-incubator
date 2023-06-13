from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class UpdateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.patch("/{shanyrak_id:str}")
def update_shanyrak(
    shanyrak_id: str,
    input: UpdateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    svc.repository.update_shanyrak_by_id(shanyrak_id, input.dict())
    return Response(status_code=200)
