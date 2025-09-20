from pydantic import BaseModel
from datetime import date
from typing import Optional

class Expense(BaseModel):
    """Schema for expense"""
    id: int
    user_id: int
    vendor: str
    amount: float
    expense_date: date
    category: str
    raw_text: str

class ExpenseCreate(BaseModel):
    """Schema for creating an expense"""
    vendor: str
    amount: float
    expense_date: date
    category: str
    raw_text: str

class ExpenseUpdate(BaseModel):
    """Schema for updating an expense"""
    vendor: Optional[str] = None
    amount: Optional[float] = None
    expense_date: Optional[date] = None
    category: Optional[str] = None
    raw_text: Optional[str] = None

    class Config:
        from_attributes = True

