from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from medly_backend.db.session import get_session
from medly_backend.services.lesson_service import LessonService
from medly_backend.models.lesson import LessonRead, LessonDetail, PracticeItemSummary

router = APIRouter(prefix="/lessons")


def get_lesson_service(session: Session = Depends(get_session)) -> LessonService:
    return LessonService(session)


@router.get("/{lesson_id}", response_model=LessonDetail)
def get_lesson(lesson_id: str, service: LessonService = Depends(get_lesson_service)):
    lesson = service.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    items = service.get_practice_items_for_lesson(lesson_id)

    return LessonDetail(
        lesson=LessonRead.model_validate(lesson),
        practice_items=[PracticeItemSummary.model_validate(i) for i in items],
    )
