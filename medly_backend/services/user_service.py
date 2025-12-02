from sqlalchemy.orm import Session
from typing import Optional

from medly_backend.db.models import User, UserQuestionAttempt


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, user_id: str) -> Optional[User]:
        return self.session.query(User).filter(User.id == user_id).one_or_none()

    def update_user(self, user: User, update: dict) -> User:
        for key, value in update.items():
            if value is not None:
                setattr(user, key, value)
        self.session.add(user)
        self.session.commit()
        return user

    def get_activity(
        self,
        user_id: str,
        subject: Optional[str] = None,
        paper: Optional[str] = None,
        lesson: Optional[str] = None,
    ) -> list[UserQuestionAttempt]:
        query = self.session.query(UserQuestionAttempt).filter(
            UserQuestionAttempt.user_id == user_id
        )

        if subject:
            query = query.filter(UserQuestionAttempt.subject_id == subject)

        if paper:
            query = query.filter(UserQuestionAttempt.origin_ref.contains(paper))

        if lesson:
            query = query.filter(UserQuestionAttempt.origin_ref.contains(lesson))

        return query.order_by(UserQuestionAttempt.created_at.desc()).limit(50).all()
