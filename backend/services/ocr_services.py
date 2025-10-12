from datetime import date
import pytesseract
from PIL import Image
import re
import os
import google.generativeai as genai
from dotenv import load_dotenv

load dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in a .env file or your environment variables.")

genai.configure(api_key=GOOGLE_API_KEY)

def extract_expense_data(image_path: str | None = None) -> dict:
    """Main function to extract expense data from image"""
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Open and prepare the image
    try:
        image = Image.open(file_path)
    except FileNotFoundError:
        return f"Error: Image file not found at {file_path}"
    
    # Create a structured prompt to extract the specific fields
    prompt = """
    This is a payment confirmation image. 
    Please extract the following information and return it only in the format:
    Vendor Name: [Extracted Vendor Name]
    Amount: [Extracted Amount with currency symbol]
    Transaction ID: [Extracted UPI transaction ID]
    Date of Transaction: [Extracted Date of transaction]
    """
    
    # Generate response from Gemini
    # Pass the prompt and the image to the generate_content method
    response = model.generate_content([prompt, image])
    print(response.text.strip())
    return {
        "vendor": re.search(r'Vendor Name:\s*(.*)', response.text).group(1).strip(),
        "amount": re.search(r'Amount:\s*([\d.,]+)', response.text).group(1).strip(),
        "id": re.search(r'Transaction ID:\s*(.*)', response.text).group(1).strip(),
        "date": re.search(r'Date of Transaction:\s*(.*)', response.text).group(1).strip(),
        "category": "Other",  # Placeholder, can be improved with more context
        "payment_method": "UPI",  # Assuming UPI for payment confirmation images
        "raw_text": response.text.strip()
    }