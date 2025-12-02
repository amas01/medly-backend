from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from medly_backend.db.session import get_session
from medly_backend.services.item_service import ItemService
from medly_backend.schemas.item import ItemDetail, ItemRead, ItemAppearance

router = APIRouter(prefix="/items")


def get_item_service(session: Session = Depends(get_session)) -> ItemService:
    return ItemService(session)


@router.get("/{item_id}", response_model=ItemDetail)
def get_item(item_id: str, service: ItemService = Depends(get_item_service)):
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    appearances_raw = service.get_appearances(item_id)

    appearances = []
    for q, paper in appearances_raw:
        appearances.append(
            ItemAppearance(
                origin_type=q.origin_type,
                paper_id_code=paper.paper_id_code if paper else None,
                practice_set_id=q.practice_set_id,
            )
        )

    return ItemDetail(
        item=ItemRead.model_validate(item),
        appearances=appearances,
    )
