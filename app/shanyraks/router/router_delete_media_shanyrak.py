from typing import List

from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class DeleteShanyrakMediaRequest(AppModel):
    media: List[str]


@router.delete("/{shanyrak_id:str}/media", response_model=DeleteShanyrakMediaRequest)
def delete_shanyrak_media(
    inpu: DeleteShanyrakMediaRequest,
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    for med in inpu.media:
        svc.repository.delete_shanyrak_media_by_id(shanyrak_id, med)
    # svc.repository.delete_shanyrak_media_by_id(shanyrak_id, "med")

    return Response(status_code=200)
