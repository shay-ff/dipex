from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from ..db.base import Base

class Expense(Base):
    """Expense model for the database"""
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vendor = Column(String, nullable=False)
    amount = Column(Numeric(10,2), nullable=False)
    expense_date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    raw_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Expense(id={self.id}, user_id={self.user_id}, vendor='{self.vendor}', amount={self.amount}, expense_date='{self.expense_date}', category='{self.category}')>"