from pydantic import BaseModel
from typing import Optional


class UserRead(BaseModel):
    id: str
    # add more fields as needed later

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    metadata: Optional[dict] = None


class ActivityItem(BaseModel):
    question_id_code: str
    created_at: str
    subject_id: str
    origin_ref: str

    class Config:
        from_attributes = True


class UserActivity(BaseModel):
    user_id: str
    activities: list[ActivityItem]
