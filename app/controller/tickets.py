from typing import Optional
from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session

from app.db import get_session
from app.db.services.tickets_service import TicketsService
from app.models.base_response_model import BaseResponseModel

router = APIRouter()

@router.get("/tickets")
def get_tickets(
    db: Session = Depends(get_session),
    start_date: Optional[str] = Query(None, alias="startDate", description="Start date in YYYY-MM-DD format", example="2023-01-01"),
    end_date: Optional[str] = Query(None, alias="endDate", description="End date in YYYY-MM-DD format", example="2023-12-31")
):
    tickets_service = TicketsService(db)
    result = tickets_service.get_tickets(start_date=start_date, end_date=end_date)

    return BaseResponseModel.ok(result)
