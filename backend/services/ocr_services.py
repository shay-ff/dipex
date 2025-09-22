from datetime import date


def simulate_ocr_service() -> dict:
    return {
        "id": "0",
        "vendor": "Starbucks",
        "amount": 350.0,
        "currency": "INR",
        "category": "Food",
        "date": "2025-01-01",
        "payment_method": "card",
        "payment_status": "captured",
        "raw_text": "Starbucks INR 350 2025-01-01",
    }


def extract_expense_data(image_path: str | None = None) -> dict:
    return simulate_ocr_service()