from PIL import Image
import pytesseract
import cv2
import numpy as np


def simulate_ocr_service() -> dict:
    return {
        "id": "0",
        "vendor": "Starbucks",
        "amount": 350,
        "currency": "INR",
        "category": "Food",
        "date": "2025-01-01"
    }

def extract_expense_data(image_path: str) -> dict:
    return simulate_ocr_service()