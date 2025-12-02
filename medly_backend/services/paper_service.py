from sqlalchemy.orm import Session
from typing import Optional, List

from medly_backend.db.models import ExamPaper, Question, QuestionItem


class PaperService:
    def __init__(self, session: Session):
        self.session = session

    def get_paper(self, paper_id: str) -> Optional[ExamPaper]:
        return (
            self.session.query(ExamPaper)
            .filter(ExamPaper.paper_id_code == paper_id)
            .one_or_none()
        )

    def get_items_for_paper(self, paper_id: str) -> List[QuestionItem]:
        return (
            self.session.query(QuestionItem)
            .join(Question, Question.id == QuestionItem.question_id)
            .join(ExamPaper, ExamPaper.id == Question.exam_paper_id)
            .filter(ExamPaper.paper_id_code == paper_id)
            .order_by(Question.question_number.asc(), QuestionItem.question_part.asc())
            .all()
        )
