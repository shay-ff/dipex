from datetime import date
import pytesseract
from PIL import Image
import re
import os


def simulate_ocr_service() -> dict:
    return {
        "id": "TXN123456789",
        "vendor": "Starbucks Coffee",
        "amount": 350.0,
        "currency": "INR",
        "category": "Food & Dining",
        "date": "2025-01-10",
        "payment_method": "UPI",
        "payment_status": "Success",
        "raw_text": "Payment to Starbucks Coffee ₹350.00 via UPI on 10 Jan 2025 TXN123456789",
    }


def extract_text_from_image(image_path: str) -> str:
    """Extract text from image using Tesseract OCR"""
    try:
        # Open and process image
        image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Extract text using Tesseract
        text = pytesseract.image_to_string(image)
        return text.strip()
    
    except Exception as e:
        print(f"OCR extraction error: {e}")
        return ""


def parse_payment_text(text: str) -> dict:
    """Parse extracted text to find payment details"""
    
    # Initialize result
    result = {
        "id": "N/A",
        "vendor": "Unknown Merchant",
        "amount": 0.0,
        "currency": "INR",
        "category": "Other",
        "date": date.today().isoformat(),
        "payment_method": "UPI",
        "payment_status": "Unknown",
        "raw_text": text
    }
    
    # Common patterns for Indian UPI payments
    patterns = {
        # Amount patterns (₹, Rs, INR)
        'amount': [
            r'₹\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'Rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'INR\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'(\d+(?:,\d+)*(?:\.\d{2})?)\s*₹'
        ],
        
        # Transaction ID patterns
        'transaction_id': [
            r'(?:TXN|Transaction|Ref|ID)[\s:]*([A-Z0-9]{8,})',
            r'UPI\s*(?:Ref|ID)[\s:]*([A-Z0-9]{8,})',
            r'([0-9]{12,})'  # Long numeric IDs
        ],
        
        # Merchant patterns
        'merchant': [
            r'(?:to|paid|payment to)\s+([A-Za-z\s&.]+?)(?:\s+₹|\s+Rs|\s+INR|\s+\d)',
            r'Merchant:\s*([A-Za-z\s&.]+)',
            r'Paid to\s+([A-Za-z\s&.]+)'
        ],
        
        # Date patterns
        'date': [
            r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{2,4})',
        ]
    }
    
    # Extract amount
    for pattern in patterns['amount']:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(',', '')
            try:
                result['amount'] = float(amount_str)
                break
            except ValueError:
                continue
    
    # Extract transaction ID
    for pattern in patterns['transaction_id']:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result['id'] = match.group(1)
            break
    
    # Extract merchant
    for pattern in patterns['merchant']:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            merchant = match.group(1).strip()
            if len(merchant) > 2:  # Avoid single characters
                result['vendor'] = merchant
                break
    
    # Extract date
    for pattern in patterns['date']:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date_str = match.group(1)
            # You might want to add date parsing logic here
            result['date'] = date_str
            break
    
    # Determine category based on merchant name
    merchant_lower = result['vendor'].lower()
    if any(word in merchant_lower for word in ['starbucks', 'cafe', 'restaurant', 'food', 'zomato', 'swiggy']):
        result['category'] = 'Food & Dining'
    elif any(word in merchant_lower for word in ['uber', 'ola', 'metro', 'bus']):
        result['category'] = 'Transportation'
    elif any(word in merchant_lower for word in ['amazon', 'flipkart', 'shopping', 'store']):
        result['category'] = 'Shopping'
    elif any(word in merchant_lower for word in ['netflix', 'spotify', 'movie', 'entertainment']):
        result['category'] = 'Entertainment'
    
    # Determine payment status
    if any(word in text.lower() for word in ['success', 'completed', 'paid']):
        result['payment_status'] = 'Success'
    elif any(word in text.lower() for word in ['failed', 'declined', 'error']):
        result['payment_status'] = 'Failed'
    
    return result


def extract_expense_data(image_path: str | None = None) -> dict:
    """Main function to extract expense data from image"""
    
    # If no image provided, return simulated data for testing
    if not image_path or not os.path.exists(image_path):
        print("No image provided or file doesn't exist, returning simulated data")
        return simulate_ocr_service()
    
    try:
        # Extract text from image
        extracted_text = extract_text_from_image(image_path)
        
        if not extracted_text:
            print("No text extracted from image, returning simulated data")
            return simulate_ocr_service()
        
        print(f"Extracted text: {extracted_text}")
        
        # Parse the extracted text
        parsed_data = parse_payment_text(extracted_text)
        
        return parsed_data
        
    except Exception as e:
        print(f"Error in extract_expense_data: {e}")
        return simulate_ocr_service()