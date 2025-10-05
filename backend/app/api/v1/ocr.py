from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ....db.session import get_db
from ....services.ocr_services import extract_expense_data
from ....services.expenses_services import create_expense, to_schema as expense_to_schema
from ....services.payments_services import create_payment, to_schema as payment_to_schema
from ....services.auth_services import get_user_by_id
from ....models.user import User
from datetime import datetime
import tempfile
import os
import logging

# Configure module logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


router = APIRouter(prefix="/ocr", tags=["ocr"])


class OCRRequest(BaseModel):
    """Request model for OCR endpoint"""
    user_id: int


@router.post("/extract")
async def extract_from_image(
    file: UploadFile = File(...),
    user_id: int = Form(default=1),  # Default user for testing
    db: Session = Depends(get_db)
):
    """
    Extract expense data from uploaded screenshot
    """
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Save uploaded file temporarily
    temp_file = None
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Extract data using OCR service (pass the file path)
        data = extract_expense_data(temp_file_path)
        
        if not data:
            return {
                "success": False,
                "error": "Could not extract data from image"
            }
        
        # For now, just return the extracted data without saving to DB
        # You can uncomment the DB saving code below when you want to persist data
        
        return {
            "success": True,
            "data": {
                "amount": data.get("amount"),
                "merchant": data.get("vendor"),
                "date": data.get("date"),
                "transaction_id": data.get("id", "N/A"),
                "category": data.get("category", "Other"),
                "payment_method": data.get("payment_method", "UPI"),
                "raw_text": data.get("raw_text", "")
            }
        }
        
    except Exception as e:
        logger.exception("OCR processing failed")
        return {
            "success": False,
            "error": f"Processing failed: {str(e)}"
        }
    
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@router.post("/extract-and-save")
def extract_and_save(request: OCRRequest, db: Session = Depends(get_db)):
    user_id = request.user_id

    user = get_user_by_id(db, user_id)
    if not user:
        # Provide helpful error details without leaking sensitive data
        available_ids = [u.id for u in db.query(User).all()]
        logger.info("User lookup failed for user_id=%s; available_ids=%s", user_id, available_ids)
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

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


