from sqlalchemy import (
    ForeignKey,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from medly_backend.db.base import Base


class ItemLessonLink(Base):
    __tablename__ = "item_lesson_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("question_items.id"), index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), index=True)

    item: Mapped["QuestionItem"] = relationship(back_populates="extra_lessons")
    lesson: Mapped["Lesson"] = relationship(back_populates="items_extra")

    __table_args__ = (Index("ix_itemlesson_item_lesson", "item_id", "lesson_id"),)


class ItemChunkLink(Base):
    __tablename__ = "item_chunk_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("question_items.id"), index=True)
    chunk_id: Mapped[int] = mapped_column(ForeignKey("chunks.id"), index=True)

    item: Mapped["QuestionItem"] = relationship(back_populates="chunks")
    chunk: Mapped["Chunk"] = relationship(back_populates="items")

    __table_args__ = (Index("ix_itemchunk_item_chunk", "item_id", "chunk_id"),)
