from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Numeric, Date
from sqlalchemy.sql import func
from ..db.base import Base


class Payment(Base):
    """Payment model for the database"""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(String, nullable=False)
    payment_status = Column(String, nullable=False)
    raw_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return (
            f"<Payment(id={self.id}, user_id={self.user_id}, amount={self.amount}, "
            f"payment_date='{self.payment_date}', method='{self.payment_method}', status='{self.payment_status}')>"
        )


