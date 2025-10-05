// API Configuration
// Update this with your computer's IP address when testing on a physical device

// To find your IP address:
// Mac/Linux: Run `ifconfig` in terminal, look for inet under en0 or wlan0
// Windows: Run `ipconfig` in command prompt, look for IPv4 Address

// IMPORTANT: Use your computer's IP address for both simulator and physical device
// This ensures consistent behavior across all testing scenarios
export const API_BASE_URL = '${process.env.BASE_URL}';

export const API_ENDPOINTS = {
  OCR_EXTRACT: `${API_BASE_URL}/api/v1/ocr/extract`,
  OCR_EXTRACT_AND_SAVE: `${API_BASE_URL}/api/v1/ocr/extract-and-save`,
};
