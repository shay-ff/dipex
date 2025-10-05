#!/usr/bin/env python3
"""
Simple script to test if the backend is accessible
"""
import requests
import sys

def test_backend_connection():
    base_url = "http://192.168.29.12:8000"
    
    print(f"Testing backend connection to: {base_url}")
    
    try:
        # Test root endpoint
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint status: {response.status_code}")
        print(f"Root endpoint response: {response.json()}")
        
        # Test OCR endpoint (should return method not allowed for GET)
        ocr_response = requests.get(f"{base_url}/api/v1/ocr/extract")
        print(f"OCR endpoint status: {ocr_response.status_code}")
        
        if response.status_code == 200:
            print("✅ Backend is accessible!")
            return True
        else:
            print("❌ Backend returned error")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure:")
        print("1. Backend server is running")
        print("2. Server is bound to 0.0.0.0:8000 (not just localhost)")
        print("3. Firewall allows connections on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_backend_connection()
    sys.exit(0 if success else 1)