from pydantic import BaseModel
from typing import Optional


class ItemRead(BaseModel):
    item_id_code: str
    question_text: str
    markmax: int
    difficulty: int

    class Config:
        from_attributes = True


class ItemAppearance(BaseModel):
    origin_type: str
    paper_id_code: Optional[str]
    practice_set_id: Optional[int]


class ItemDetail(BaseModel):
    item: ItemRead
    appearances: list[ItemAppearance]
