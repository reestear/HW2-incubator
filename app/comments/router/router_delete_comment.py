from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.shanyraks.service import Service as shanyraksService
from app.shanyraks.service import get_service as get_service_shanyraks

from ..service import Service, get_service
from . import router


@router.delete("/{shanyrak_id:str}/comments/{comment_id:str}")
def delete_comment(
    shanyrak_id: str,
    comment_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
    svc_shanyraaks: shanyraksService = Depends(get_service_shanyraks),
) -> dict[str, str]:
    svc.repository.delete_comment(comment_id)
    svc_shanyraaks.repository.delete_shanyrak_comment_by_id(shanyrak_id, comment_id)
    return Response(status_code=200)
