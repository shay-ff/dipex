from datetime import date
import pytesseract
from PIL import Image
import re
import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger("ocr_services")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    logger.warning("GOOGLE_API_KEY not found. Gemini integration will be disabled for local/dev runs.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)


def extract_expense_data(image_path: str | None = None) -> dict:
    """Main function to extract expense data from image

    If `image_path` is None or Tesseract not available, this function may return
    simulated/example data for local development.
    """

    # If no image provided, return simulated data for development
    if not image_path or not os.path.exists(image_path):
        logger.info("No image provided or file doesn't exist, returning simulated data")
        return {
            "vendor": "Demo Merchant",
            "amount": "350.00",
            "id": "TXN123456789",
            "date": date.today().isoformat(),
            "category": "Other",
            "payment_method": "UPI",
            "raw_text": "Simulated OCR output"
        }

    # Try to open the image and run OCR
    try:
        image = Image.open(image_path)
    except Exception as e:
        logger.exception("Error opening image for OCR")
        return {}

    # If Google generative model is configured, prefer it (experimental)
    if GOOGLE_API_KEY:
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt = (
                "Extract vendor, amount, transaction id and date from this payment confirmation image."
            )
            response = model.generate_content([prompt, image])
            text = getattr(response, 'text', '')
            logger.info("Gemini response received")
        except Exception:
            logger.exception("Gemini extraction failed, falling back to pytesseract")
            text = pytesseract.image_to_string(image)
    else:
        text = pytesseract.image_to_string(image)

    logger.info("Extracted text length=%d", len(text) if text else 0)

    # Best-effort regex parsing (may fail for some screenshots)
    try:
        vendor = re.search(r'Vendor Name:\s*(.*)', text)
        amount = re.search(r'Amount:\s*([\d.,]+)', text)
        txn_id = re.search(r'Transaction ID:\s*(.*)', text)
        txn_date = re.search(r'Date of Transaction:\s*(.*)', text)

        return {
            "vendor": vendor.group(1).strip() if vendor else "Unknown",
            "amount": amount.group(1).strip() if amount else "0.00",
            "id": txn_id.group(1).strip() if txn_id else "",
            "date": txn_date.group(1).strip() if txn_date else date.today().isoformat(),
            "category": "Other",
            "payment_method": "UPI",
            "raw_text": text
        }
    except Exception:
        logger.exception("Error parsing OCR text")
        return {
            "vendor": "Unknown",
            "amount": "0.00",
            "id": "",
            "date": date.today().isoformat(),
            "category": "Other",
            "payment_method": "UPI",
            "raw_text": text
        }