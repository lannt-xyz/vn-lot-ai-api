from collections import defaultdict
from datetime import date
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.tickets import Tickets

class TicketsService:
    def __init__(self, db: Session):
        self.db = db

    def _get_tickets(self, start_date: Optional[date] = None, end_date: Optional[date] = None, result_updated: Optional[bool] = True) -> List[Tickets]:
        query = select(
            Tickets
        ).order_by(
            Tickets.ticket_date.asc()
        )
        if result_updated:
            query = query.where(Tickets.result_updated.is_(result_updated))
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

    def get_tickets(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Tickets]:
        tickets = self._get_tickets(start_date, end_date, False)
        result = [
            {
                "date": ticket.ticket_date,
                "cityCode": "xsmb",
                "type": ticket.type,
                "lotNumber": ticket.lot_number,
                "matchedCount": ticket.matched_count,
                "pay": ticket.pay,
                "win": ticket.win,
            } for ticket in tickets
        ]
        return sorted(result, key=lambda x: x["date"], reverse=True)

    def get_matched_by_algorithm(self) -> List[dict]:
        # for the tickets has result_updated = True, count all matched_count by type
        query = select(
            Tickets.type,
            func.sum(Tickets.matched_count).label("matched_count"),
            func.sum(Tickets.pay).label("total_pay"),
            func.sum(Tickets.win).label("total_win")
        ).where(
            Tickets.result_updated.is_(True)
        ).group_by(
            Tickets.type
        ).order_by(
            Tickets.type.asc()
        )
        result = self.db.execute(query)
        matched_results = result.all()
        result = []
        for ticket_type, matched_count, total_pay, total_win in matched_results:
            result.append({
                "type": ticket_type,
                "count": matched_count,
                "profit": total_win - total_pay,
            })
        return result

    def get_today_results(self) -> List[Tickets]:
        today = date.today()
        return self._get_tickets(start_date=today, end_date=today, result_updated=True)
