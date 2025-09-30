from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Numeric, Date
from sqlalchemy.sql import func
from ..db.base import Base


class Payment(Base):
    """Payment model for the database"""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payement_date = Column(Date, nullable=False)
    transanction_Id = Column(String, nullable=True)
    raw_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return (
            f"<Payment(id={self.id}, user_id={self.user_id}, amount={self.amount}, "
            f"payement_date='{self.payement_date}', transanction_Id='{self.transanction_Id}')>"
        )


