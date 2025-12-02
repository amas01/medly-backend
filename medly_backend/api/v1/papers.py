from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from medly_backend.db.session import get_session
from medly_backend.services.paper_service import PaperService
from medly_backend.models.paper import PaperDetail, PaperRead, PaperItem

router = APIRouter(prefix="/papers")


def get_paper_service(session: Session = Depends(get_session)) -> PaperService:
    return PaperService(session)


@router.get("/{paper_id}", response_model=PaperDetail)
def get_paper(paper_id: str, service: PaperService = Depends(get_paper_service)):
    paper = service.get_paper(paper_id)
    if not paper:
        raise HTTPException(404, "Paper not found")

    items = service.get_items_for_paper(paper_id)

    return PaperDetail(
        paper=PaperRead.model_validate(paper),
        items=[PaperItem.model_validate(i) for i in items],
    )
