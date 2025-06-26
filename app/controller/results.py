from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db import get_session
from app.db.services.tickets_service import TicketsService
from app.models.base_response_model import BaseResponseModel

router = APIRouter()

@router.get("/results/today")
def get_algorithms(
    db: Session = Depends(get_session),
):
    tickets_service = TicketsService(db)
    result = tickets_service.get_today_results()
    if not result:
        return BaseResponseModel.no_content()

    return BaseResponseModel.ok(result)
