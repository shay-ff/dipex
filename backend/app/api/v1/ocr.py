from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ....db.session import get_db
from ....services.ocr_services import extract_expense_data
from ....services.expenses_services import create_expense, to_schema as expense_to_schema
from ....services.payments_services import create_payment, to_schema as payment_to_schema
from ....services.auth_services import get_user_by_id
from ....models.user import User
from datetime import datetime


router = APIRouter(prefix="/ocr", tags=["ocr"])


class OCRRequest(BaseModel):
    """Request model for OCR endpoint"""
    user_id: int


@router.post("/extract-and-save")
def extract_and_save(request: OCRRequest, db: Session = Depends(get_db)):
    user_id = request.user_id
    print(f"Looking for user_id: {user_id}")
    
    user = get_user_by_id(db, user_id)
    if not user:
        # Let's also check if the user exists with additional debug info
        all_users = db.query(User).all()
        available_ids = [u.id for u in all_users]
        print(f"Available user IDs in database: {available_ids}")
        raise HTTPException(status_code=404, detail=f"User {user_id} not found. Available IDs: {available_ids}")
    
    print(f"Found user: ID={user.id}, Email={user.email}, Name={user.name}")

    data = extract_expense_data()

    if not data:
        raise HTTPException(status_code=400, detail="No data extracted")

    expense = create_expense(
        db,
        user_id=user_id,
        vendor=data["vendor"],
        amount=float(data["amount"]),
        expense_date=datetime.fromisoformat(data["date"]).date(),
        category=data.get("category", "Other"),
        raw_text=data.get("raw_text", ""),
    )

    payment = create_payment(
        db,
        user_id=user_id,
        amount=float(data["amount"]),
        payment_date=datetime.fromisoformat(data["date"]).date(),
        payment_method=data.get("payment_method", "unknown"),
        payment_status=data.get("payment_status", "unknown"),
        raw_text=data.get("raw_text", ""),
    )

    return {
        "expense": expense_to_schema(expense).model_dump(),
        "payment": payment_to_schema(payment).model_dump(),
    }


