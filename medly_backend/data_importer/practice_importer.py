import json
from pathlib import Path

from sqlalchemy.orm import Session
from medly_backend.db.models import (
    PracticeSet,
    ItemChunkLink,
    Lesson,
    Question,
    QuestionItem,
    Chunk,
    QuestionItemProvenance,
)
from medly_backend.data_importer.util import upsert


def import_practices(session: Session, path: str | Path):
    data = json.load(open(path))

    for pset in data:
        lesson = (
            session.query(Lesson)
            .filter(Lesson.lesson_id_code == pset["lessonID"])
            .first()
        )

        pset_row = upsert(
            session,
            PracticeSet,
            ["course_id", "lesson_id"],
            {
                "course_id": lesson.topic.unit.course_id,
                "unit_index": pset["unit_index"],
                "topic_index": pset["topic_index"],
                "lesson_id": lesson.id,
            },
        )

        for q in pset["items"]:
            q_row = upsert(
                session,
                Question,
                ["question_id_code", "origin_type"],
                {
                    "question_id_code": q["question_id"],
                    "origin_type": "practice",
                    "practice_set_id": pset_row.id,
                    "question_number": q["question_number"],
                    "question_stem": q["question_stem"],
                    "question_stem_diagram": q["question_stem_diagram"],
                    "validation_comment": q["validation_comment"],
                    "validation_reason": q["validation_reason"],
                },
            )

            for item in q["items"]:
                item_row = upsert(
                    session,
                    QuestionItem,
                    ["item_id_code"],
                    {
                        "question_id": q_row.id,
                        "question_part": item["question_part"],
                        "question_type": item["question_type"],
                        "question_text": item["question_text"],
                        "markmax": item["markmax"],
                        "markscheme": item["markscheme"],
                        "difficulty": item["difficulty"],
                        "item_id_code": item["questionID"],
                        # specification_point == primary_lesson
                        "primary_lesson_id": lesson.id,
                    },
                )

                # chunks
                for ch in pset["chunks_used"]:
                    # Must relate chunk by chunk_index
                    chunk = (
                        session.query(Chunk)
                        .filter(
                            Chunk.lesson_id == lesson.id,
                            Chunk.chunk_index == ch["chunk_index"],
                        )
                        .first()
                    )

                    if chunk:
                        upsert(
                            session,
                            ItemChunkLink,
                            ["item_id", "chunk_id"],
                            {"item_id": item_row.id, "chunk_id": chunk.id},
                        )

                upsert(
                    session,
                    QuestionItemProvenance,
                    ["item_id", "source_file", "source_kind"],
                    {
                        "item_id": item_row.id,
                        "source_file": "aqaGCSEBio_practices.json",
                        "source_kind": "practice",
                    },
                )
