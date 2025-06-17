from sqlalchemy import Boolean, Column, Date, String, Integer

from app.db.models import Base

class Tickets(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_date = Column(Date, nullable=False)
    type = Column(String(50), nullable=True)
    lot_number = Column(String(255), nullable=True)
    matched_count = Column(Integer, nullable=True)
    pay = Column(Integer, nullable=True)
    win = Column(Integer, nullable=True)
    result_updated = Column(Boolean, server_default="false", nullable=False)
