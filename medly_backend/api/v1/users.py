from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from medly_backend.db.session import get_session
from medly_backend.services.user_service import UserService
from medly_backend.models.user import UserRead, UserUpdate, UserActivity, ActivityItem

router = APIRouter(prefix="/users")


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(session)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return UserRead.model_validate(user)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str,
    update: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    updated = service.update_user(user, update.dict())
    return UserRead.model_validate(updated)


@router.get("/{user_id}/activity", response_model=UserActivity)
def activity(
    user_id: str,
    subject: str | None = None,
    paper: str | None = None,
    lesson: str | None = None,
    service: UserService = Depends(get_user_service),
):
    items = service.get_activity(user_id, subject, paper, lesson)
    return UserActivity(
        user_id=user_id,
        activities=[ActivityItem.model_validate(a) for a in items],
    )
