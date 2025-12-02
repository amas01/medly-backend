import json
from pathlib import Path
from sqlalchemy.orm import Session
from medly_backend.db.models import (
    Exam,
    ExamPaper,
    Question,
    QuestionItem,
    ItemLessonLink,
    QuestionItemProvenance,
)
from medly_backend.data_importer.util import upsert


def import_exams(session: Session, path: str | Path):
    data = json.load(open(path))

    for exam in data:
        exam_row = upsert(
            session,
            Exam,
            ["subject_id", "series"],
            {
                "board_title": exam["board_title"],
                "qualification": exam["qualification"],
                "subject_title": exam["subject_title"],
                "subject_id": exam["subject_id"],
                "type": exam["type"],
                "series": exam["series"],
            },
        )

        for paper in exam["papers"]:
            paper_row = upsert(
                session,
                ExamPaper,
                ["paper_id_code"],
                {
                    "exam_id": exam_row.id,
                    "paper_id_code": paper["paper_id"],
                    "tier": paper["tier"],
                    "paper_number": paper["paper"],
                },
            )

            for q in paper["questions"]:
                question_row = upsert(
                    session,
                    Question,
                    ["question_id_code", "origin_type"],
                    {
                        "question_id_code": q["question_id"],
                        "origin_type": "exam",
                        "exam_paper_id": paper_row.id,
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
                            "question_id": question_row.id,
                            "question_part": item["question_part"],
                            "question_type": item["question_type"],
                            "question_text": item["question_text"],
                            "markmax": item["markmax"],
                            "markscheme": item["markscheme"],
                            "difficulty": item["difficulty"],
                            "item_id_code": item["questionID"],
                        },
                    )

                    # Handle lessonIDs (may not map)
                    for lid in item.get("lessonIDs", []):
                        lesson = (
                            session.query(Lesson)
                            .filter(Lesson.lesson_id_code == lid)
                            .first()
                        )

                        if lesson:
                            upsert(
                                session,
                                ItemLessonLink,
                                ["item_id", "lesson_id"],
                                {"item_id": item_row.id, "lesson_id": lesson.id},
                            )

                    upsert(
                        session,
                        QuestionItemProvenance,
                        ["item_id", "source_file", "source_kind"],
                        {
                            "item_id": item_row.id,
                            "source_file": "aqaGCSEBio_exams.json",
                            "source_kind": "exam",
                        },
                    )
