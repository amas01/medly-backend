from typing import Optional

from sqlalchemy import (
    String,
    Integer,
    Text,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from medly_backend.db.base import Base


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(primary_key=True)
    board_title: Mapped[str] = mapped_column(String)
    qualification: Mapped[str] = mapped_column(String)
    subject_title: Mapped[str] = mapped_column(String)
    subject_id: Mapped[str] = mapped_column(String, index=True)
    type: Mapped[str] = mapped_column(String)
    series: Mapped[str] = mapped_column(String)

    papers: Mapped[list["ExamPaper"]] = relationship(back_populates="exam")


class ExamPaper(Base):
    __tablename__ = "exam_papers"

    id: Mapped[int] = mapped_column(primary_key=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"), index=True)
    paper_id_code: Mapped[str] = mapped_column(String, index=True)
    tier: Mapped[str] = mapped_column(String)
    paper_number: Mapped[str] = mapped_column(String)

    exam: Mapped[Exam] = relationship(back_populates="papers")
    questions: Mapped[list["Question"]] = relationship(back_populates="exam_paper")

    __table_args__ = (UniqueConstraint("paper_id_code", name="uq_exam_paper_id_code"),)


class PracticeSet(Base):
    __tablename__ = "practice_sets"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), index=True)
    unit_index: Mapped[int] = mapped_column(Integer)
    topic_index: Mapped[int] = mapped_column(Integer)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), index=True)

    course: Mapped["Course"] = relationship(back_populates="practice_sets")
    lesson: Mapped["Lesson"] = relationship()
    questions: Mapped[list["Question"]] = relationship(back_populates="practice_set")

    __table_args__ = (
        Index(
            "ix_practiceset_course_unit_topic", "course_id", "unit_index", "topic_index"
        ),
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)

    question_id_code: Mapped[str] = mapped_column(String, index=True)
    origin_type: Mapped[str] = mapped_column(String, index=True)

    exam_paper_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("exam_papers.id"), nullable=True, index=True
    )
    practice_set_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("practice_sets.id"), nullable=True, index=True
    )

    question_number: Mapped[Optional[int]] = mapped_column(Integer)
    question_stem: Mapped[Optional[str]] = mapped_column(Text)
    question_stem_diagram: Mapped[Optional[str]] = mapped_column(Text)
    validation_comment: Mapped[Optional[str]] = mapped_column(Text)
    validation_reason: Mapped[Optional[str]] = mapped_column(Text)

    exam_paper: Mapped[Optional[ExamPaper]] = relationship(back_populates="questions")
    practice_set: Mapped[Optional[PracticeSet]] = relationship(
        back_populates="questions"
    )
    items: Mapped[list["QuestionItem"]] = relationship(back_populates="question")

    __table_args__ = (
        UniqueConstraint(
            "question_id_code", "origin_type", name="uq_question_code_origin"
        ),
        Index("ix_question_code_origin", "question_id_code", "origin_type"),
    )


class QuestionItem(Base):
    __tablename__ = "question_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), index=True)

    question_part: Mapped[int] = mapped_column(Integer)
    question_type: Mapped[str] = mapped_column(String)
    question_text: Mapped[str] = mapped_column(Text)
    markmax: Mapped[int] = mapped_column(Integer)
    markscheme: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[int] = mapped_column(Integer, index=True)

    primary_lesson_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("lessons.id"), nullable=True, index=True
    )

    item_id_code: Mapped[str] = mapped_column(String, index=True)

    question: Mapped[Question] = relationship(back_populates="items")
    primary_lesson: Mapped[Optional["Lesson"]] = relationship(
        back_populates="items_primary"
    )

    extra_lessons: Mapped[list["ItemLessonLink"]] = relationship(back_populates="item")
    chunks: Mapped[list["ItemChunkLink"]] = relationship(back_populates="item")
    provenance: Mapped[list["QuestionItemProvenance"]] = relationship(
        back_populates="item"
    )

    __table_args__ = (UniqueConstraint("item_id_code", name="uq_item_code"),)
