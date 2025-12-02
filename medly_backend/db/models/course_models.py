from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from medly_backend.db.base import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[str] = mapped_column(String, index=True)
    board: Mapped[str] = mapped_column(String)
    qualification: Mapped[str] = mapped_column(String)

    units: Mapped[list["Unit"]] = relationship(back_populates="course")
    practice_sets: Mapped[list["PracticeSet"]] = relationship(back_populates="course")


class Unit(Base):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), index=True)
    unit_index: Mapped[int] = mapped_column(Integer)
    unit_title: Mapped[str] = mapped_column(String)

    course: Mapped[Course] = relationship(back_populates="units")
    topics: Mapped[list["Topic"]] = relationship(back_populates="unit")

    __table_args__ = (
        UniqueConstraint("course_id", "unit_index", name="uq_unit_course_index"),
        Index("ix_unit_course_unitindex", "course_id", "unit_index"),
    )


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), index=True)
    topic_index: Mapped[int] = mapped_column(Integer)
    topic_title: Mapped[str] = mapped_column(String)

    unit: Mapped[Unit] = relationship(back_populates="topics")
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="topic")

    __table_args__ = (
        UniqueConstraint("unit_id", "topic_index", name="uq_topic_unit_index"),
        Index("ix_topic_unit_topicindex", "unit_id", "topic_index"),
    )


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), index=True)
    lesson_index: Mapped[int] = mapped_column(Integer)
    lesson_id_code: Mapped[str] = mapped_column(String, index=True)
    lesson_title: Mapped[str] = mapped_column(String)

    topic: Mapped[Topic] = relationship(back_populates="lessons")
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="lesson")

    items_primary: Mapped[list["QuestionItem"]] = relationship(
        back_populates="primary_lesson"
    )
    items_extra: Mapped[list["ItemLessonLink"]] = relationship(back_populates="lesson")

    __table_args__ = (
        UniqueConstraint("topic_id", "lesson_index", name="uq_lesson_topic_index"),
        Index("ix_lesson_topic_lessonindex", "topic_id", "lesson_index"),
        Index("ix_lesson_code", "lesson_id_code"),
    )


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer)
    chunk_title: Mapped[str] = mapped_column(String)

    lesson: Mapped[Lesson] = relationship(back_populates="chunks")
    items: Mapped[list["ItemChunkLink"]] = relationship(back_populates="chunk")

    __table_args__ = (
        UniqueConstraint("lesson_id", "chunk_index", name="uq_chunk_lesson_index"),
        Index("ix_chunk_lesson_chunkindex", "lesson_id", "chunk_index"),
    )
