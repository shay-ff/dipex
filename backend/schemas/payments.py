from pydantic import BaseModel
from datetime import date
from typing import Optional

class Payment(BaseModel):
    """Schema for payment"""
    id: int
    user_id: int
    amount: float
    payment_date: date
    payment_method: str
    payment_status: str
    raw_text: str

class PaymentCreate(BaseModel):
    """Schema for creating a payment"""
    amount: float
    payment_date: date
    payment_method: str
    payment_status: str
    raw_text: str

class PaymentUpdate(BaseModel):
    """Schema for updating a payment"""
    amount: Optional[float] = None
    payment_date: Optional[date] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None
    raw_text: Optional[str] = None

    class Config:
        from_attributes = True