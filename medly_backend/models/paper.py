from pydantic import BaseModel


class PaperRead(BaseModel):
    paper_id_code: str
    tier: str
    paper_number: str

    class Config:
        from_attributes = True


class PaperItem(BaseModel):
    item_id_code: str
    question_part: int
    question_text: str
    difficulty: int

    class Config:
        from_attributes = True


class PaperDetail(BaseModel):
    paper: PaperRead
    items: list[PaperItem]
