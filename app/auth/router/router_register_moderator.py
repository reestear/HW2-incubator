from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class RegisterModeratorRequest(AppModel):
    email: str
    password: str


class RegisterModeratorResponse(AppModel):
    email: str


@router.post(
    "/moderators",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterModeratorResponse,
)
def register_moderator(
    input: RegisterModeratorRequest,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    if svc.repository.get_user_by_email(input.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already taken.",
        )

    svc.repository.create_moderator(input.dict())

    return RegisterModeratorResponse(email=input.email)
