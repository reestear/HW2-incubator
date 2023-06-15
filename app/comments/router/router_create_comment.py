from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateCommentRequest(AppModel):
    content: str


@router.post("/{shanyrak_id:str}/comments")
def create_comment(
    shanyrak_id: str,
    input: CreateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    svc.repository.create_comment(jwt_data.user_id, shanyrak_id, input.content)
    return Response(status_code=200)
