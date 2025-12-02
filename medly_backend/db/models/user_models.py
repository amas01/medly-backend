from datetime import datetime
from typing import Any

from sqlalchemy import (
    String,
    Boolean,
    Text,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from medly_backend.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    attempts: Mapped[list["UserQuestionAttempt"]] = relationship(back_populates="user")


class UserQuestionAttempt(Base):
    __tablename__ = "user_question_attempts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)

    question_id_code: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_marked: Mapped[bool] = mapped_column(Boolean)

    canvas_maths: Mapped[dict[str, Any]] = mapped_column(JSONB)
    canvas_paths: Mapped[dict[str, Any]] = mapped_column(JSONB)
    canvas_textboxes: Mapped[dict[str, Any]] = mapped_column(JSONB)

    subject_id: Mapped[str] = mapped_column(String, index=True)
    origin_ref: Mapped[str] = mapped_column(Text)
    source_file: Mapped[str] = mapped_column(String)

    user: Mapped[User] = relationship(back_populates="attempts")

    __table_args__ = (
        UniqueConstraint(
            "user_id", "question_id_code", "created_at", name="uq_user_question_attempt"
        ),
        Index("ix_attempt_user_question", "user_id", "question_id_code"),
        Index("ix_attempt_question", "question_id_code"),
        Index("ix_attempt_created", "created_at"),
    )
