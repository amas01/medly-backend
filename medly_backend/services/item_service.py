from sqlalchemy.orm import Session
from typing import Optional, List

from medly_backend.db.models import QuestionItem, Question, ExamPaper


class ItemService:
    def __init__(self, session: Session):
        self.session = session

    def get_item(self, item_id: str) -> Optional[QuestionItem]:
        return (
            self.session.query(QuestionItem)
            .filter(QuestionItem.item_id_code == item_id)
            .one_or_none()
        )

    def get_appearances(self, item_id: str) -> List[dict]:
        return (
            self.session.query(Question, ExamPaper)
            .join(QuestionItem, QuestionItem.question_id == Question.id)
            .outerjoin(ExamPaper, ExamPaper.id == Question.exam_paper_id)
            .filter(QuestionItem.item_id_code == item_id)
            .all()
        )
