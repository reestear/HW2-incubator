from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.shanyraks.service import Service as shanyrakService
from app.shanyraks.service import get_service as shanyrak_get_service
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class UpdateCommentRequest(AppModel):
    content: str


@router.patch("/{shanyrak_id:str}/comments/{comment_id:str}")
def update_comment(
    shanyrak_id: str,
    comment_id: str,
    input: UpdateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
    shanyrak_svc: shanyrakService = Depends(shanyrak_get_service),
) -> dict[str, str]:
    svc.repository.update_comment(comment_id, input.content)
    shanyrak_svc.repository.update_shanyrak_comment_by_id(
        shanyrak_id, comment_id, input.content
    )
    return Response(status_code=200)
