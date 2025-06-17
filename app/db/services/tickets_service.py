from collections import defaultdict
from datetime import date
import re
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.tickets import Tickets

class TicketsService:
    def __init__(self, db: Session):
        self.db = db

    def _get_tickets(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Tickets]:
        query = select(
            Tickets
        ).where(
            Tickets.result_updated.is_(True)
        ).order_by(
            Tickets.ticket_date.asc()
        )
        if start_date:
            query = query.where(Tickets.ticket_date >= start_date)
        if end_date:
            query = query.where(Tickets.ticket_date <= end_date)
        result = self.db.execute(query)
        tickets: List[Tickets] = result.scalars().all()
        
        return tickets

    def get_profit_summary(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> dict:
        tickets = self._get_tickets(start_date, end_date)                               
        grouped_data = defaultdict(lambda: {"pay": 0, "win": 0})

        for ticket in tickets:
            ticket_type = ticket.type
            grouped_data[ticket_type]["pay"] += ticket.pay or 0
            grouped_data[ticket_type]["win"] += ticket.win or 0

        result = {}
        for ticket_type, summary in grouped_data.items():
            result[ticket_type] = [
                {
                    "color": "#FF0000",
                    "label": "Total Pay",
                    "value": float(summary["pay"])
                },
                {
                    "color": "#00FF00",
                    "label": "Total Winning",
                    "value": float(summary["win"])
                }
            ]
        
        return result

    def get_matched_results(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[dict]:
        tickets = self._get_tickets(start_date, end_date)
        results = []
        for ticket in tickets:
            results.append({
                "date": ticket.ticket_date,
                "type": ticket.type,
                "count": ticket.matched_count,
            })
        return {
            "data": results,
        }
