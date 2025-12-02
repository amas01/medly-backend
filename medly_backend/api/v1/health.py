from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from medly_backend.db.session import get_session

router = APIRouter()


@router.get("/health")
def health(session: Session = Depends(get_session)):
    try:
        session.execute("SELECT 1")
        db = "ok"
    except Exception:
        db = "error"

    return {"status": "ok", "database": db}
