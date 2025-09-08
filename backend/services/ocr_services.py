from typing import List
from pydantic import BaseModel

class OCRService(BaseModel):
    """OCR service for the database"""
    id: int
    user_id: int
    vendor: str
    amount: float
    expense_date: str
    category: str
    raw_text: str

    def __repr__(self):
        return f"<OCRService(id={self.id}, user_id={self.user_id}, vendor='{self.vendor}', amount={self.amount}, expense_date='{self.expense_date}', category='{self.category}', raw_text='{self.raw_text}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vendor": self.vendor,
            "amount": self.amount,
            "expense_date": self.expense_date,
            "category": self.category,
            "raw_text": self.raw_text
        }
    
    def from_dict(self, data: dict):
        return OCRService(
            id=data["id"],
            user_id=data["user_id"],
            vendor=data["vendor"],
            amount=data["amount"],
            expense_date=data["expense_date"],
            category=data["category"],
            raw_text=data["raw_text"]
        )