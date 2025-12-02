import json
from pathlib import Path

from sqlalchemy.orm import Session

from medly_backend.db.models import Course, Unit, Topic, Lesson
from medly_backend.data_importer.util import upsert

# Hardcoded these values, but should come from config
COURSE_VALUES = {
    "subject_id": "aqaGCSEBio",
    "board": "AQA",
    "qualification": "GCSE",
}


def import_course(session: Session, path: str | Path):
    data = json.load(open(path))

    course = upsert(session, Course, ["subject_id"], COURSE_VALUES)

    for unit in data:
        unit_row = upsert(
            session,
            Unit,
            ["course_id", "unit_index"],
            {
                "course_id": course.id,
                "unit_index": unit["unitIndex"],
                "unit_title": unit["unitTitle"],
            },
        )

        for topic in unit["topics"]:
            topic_row = upsert(
                session,
                Topic,
                ["unit_id", "topic_index"],
                {
                    "unit_id": unit_row.id,
                    "topic_index": topic["topicIndex"],
                    "topic_title": topic["topicTitle"],
                },
            )

            for lesson in topic["lessons"]:
                lesson_row = upsert(
                    session,
                    Lesson,
                    ["topic_id", "lesson_index"],
                    {
                        "topic_id": topic_row.id,
                        "lesson_index": lesson["lessonIndex"],
                        "lesson_id_code": lesson["lessonID"],
                        "lesson_title": lesson["lessonTitle"],
                    },
                )
                # No chunks in course JSON
