from pydantic import BaseModel
from typing import List


class LessonRead(BaseModel):
    lesson_id_code: str
    lesson_title: str

    class Config:
        from_attributes = True


class PracticeItemSummary(BaseModel):
    item_id_code: str
    question_text: str
    difficulty: int

    class Config:
        from_attributes = True


class LessonDetail(BaseModel):
    lesson: LessonRead
    practice_items: List[PracticeItemSummary]
