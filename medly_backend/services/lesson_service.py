from sqlalchemy.orm import Session
from typing import Optional

from medly_backend.db.models import Lesson, QuestionItem, ItemLessonLink


class LessonService:
    def __init__(self, session: Session):
        self.session = session

    def get_lesson(self, lesson_id: str) -> Optional[Lesson]:
        return (
            self.session.query(Lesson)
            .filter(Lesson.lesson_id_code == lesson_id)
            .one_or_none()
        )

    def get_practice_items_for_lesson(self, lesson_id: str) -> list[QuestionItem]:
        return (
            self.session.query(QuestionItem)
            .join(ItemLessonLink, ItemLessonLink.item_id == QuestionItem.id)
            .join(Lesson, Lesson.id == ItemLessonLink.lesson_id)
            .filter(Lesson.lesson_id_code == lesson_id)
            .order_by(QuestionItem.difficulty.asc())
            .all()
        )
