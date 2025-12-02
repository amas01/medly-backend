from datetime import datetime, timezone

from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from medly_backend.db.base import Base


class QuestionItemProvenance(Base):
    __tablename__ = "question_item_provenance"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("question_items.id"), index=True)
    source_file: Mapped[str] = mapped_column(String)
    source_kind: Mapped[str] = mapped_column(String)

    first_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    item: Mapped["QuestionItem"] = relationship(back_populates="provenance")

    __table_args__ = (
        UniqueConstraint(
            "item_id", "source_file", "source_kind", name="uq_item_source"
        ),
        Index("ix_prov_item", "item_id"),
    )
