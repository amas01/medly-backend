import re
import json
from pathlib import Path

from sqlalchemy.orm import Session

from medly_backend.db.models import (
    User,
    UserQuestionAttempt,
    QuestionItem,
    QuestionItemProvenance,
)
from medly_backend.data_importer.util import upsert

FIREBASE_PATH = re.compile(
    r"users/(?P<uid>[^/]+)/subjectsWeb/(?P<subject_id>[^/]+)/"
    r"mocks/(?P<paper_id>[^/]+)/questions/(?P<questionID>[^/]+)"
)


def import_user_data(session: Session, path: str | Path):
    data = json.load(open(path))

    for key, val in data["targets"].items():
        m = FIREBASE_PATH.match(key)
        if not m:
            continue

        uid = m.group("uid")
        questionID = m.group("questionID")
        subject_id = m.group("subject_id")
        origin_ref = key

        user = upsert(session, User, ["id"], {"id": uid})

        # look up QuestionItem
        item = (
            session.query(QuestionItem)
            .filter(QuestionItem.item_id_code == questionID)
            .first()
        )

        # upsert the user attempt
        upsert(
            session,
            UserQuestionAttempt,
            ["user_id", "question_id_code", "created_at"],
            {
                "user_id": uid,
                "question_id_code": questionID,
                "created_at": val["createdAt"],
                "is_marked": val["isMarked"],
                "canvas_maths": val["canvas"]["maths"],
                "canvas_paths": val["canvas"]["paths"],
                "canvas_textboxes": val["canvas"]["textboxes"],
                "subject_id": subject_id,
                "origin_ref": origin_ref,
                "source_file": "user_data.json",
            },
        )

        # provenance for the item (if exists)
        if item:
            upsert(
                session,
                QuestionItemProvenance,
                ["item_id", "source_file", "source_kind"],
                {
                    "item_id": item.id,
                    "source_file": "user_data.json",
                    "source_kind": "user_attempt",
                },
            )
