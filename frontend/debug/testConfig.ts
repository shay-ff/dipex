// Debug script to test API configuration
import { API_BASE_URL, API_ENDPOINTS } from '../config/api';

console.log('=== API Configuration Debug ===');
console.log('API_BASE_URL:', API_BASE_URL);
console.log('OCR_EXTRACT:', API_ENDPOINTS.OCR_EXTRACT);
console.log('OCR_EXTRACT_AND_SAVE:', API_ENDPOINTS.OCR_EXTRACT_AND_SAVE);
console.log('================================');

export const debugConfig = () => {
  return {
    baseUrl: API_BASE_URL,
    endpoints: API_ENDPOINTS
  };
};