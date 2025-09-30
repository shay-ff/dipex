from pydantic import BaseModel
from datetime import date
from typing import Optional

class Payment(BaseModel):
    """Schema for payment"""
    id: int
    user_id: int
    amount: float
    payment_date: date
    transanction_Id: str
    raw_text: str

class PaymentCreate(BaseModel):
    """Schema for creating a payment"""
    amount: float
    payment_date: date
    transanction_Id: str
    raw_text: str

class PaymentUpdate(BaseModel):
    """Schema for updating a payment"""
    amount: Optional[float] = None
    payment_date: Optional[date] = None
    transanction_Id: Optional[str] = None
    raw_text: Optional[str] = None

    class Config:
        from_attributes = True