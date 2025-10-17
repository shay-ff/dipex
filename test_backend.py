#!/usr/bin/env python3
"""
Simple script to test if the backend is accessible
"""
import requests
import sys
import logging

logger = logging.getLogger("test_backend")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def test_backend_connection():
    base_url = "http://127.0.0.1:8000"
    
    logger.info("Testing backend connection to: %s", base_url)
    
    try:
        # Test root endpoint
        response = requests.get(f"{base_url}/")
        logger.info("Root endpoint status: %s", response.status_code)
        try:
            logger.info("Root endpoint response: %s", response.json())
        except Exception:
            logger.info("Root endpoint returned non-json response")
        
        # Test OCR endpoint (should return method not allowed for GET)
        ocr_response = requests.get(f"{base_url}/api/v1/ocr/extract")
        logger.info("OCR endpoint status: %s", ocr_response.status_code)
        
        if response.status_code == 200:
            logger.info("✅ Backend is accessible!")
            return True
        else:
            logger.error("❌ Backend returned error")
            return False
            
    except requests.exceptions.ConnectionError:
        logger.error("❌ Cannot connect to backend. Make sure the server is running and network settings are correct")
        return False
    except Exception as e:
        logger.exception("❌ Error testing backend: %s", e)
        return False


if __name__ == "__main__":
    success = test_backend_connection()
    sys.exit(0 if success else 1)