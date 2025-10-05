import { API_ENDPOINTS, API_BASE_URL } from '../config/api';

export interface ExtractedData {
  amount: number;
  merchant: string;
  date: string;
  transaction_id: string;
  category?: string;
  payment_method?: string;
}

export interface ApiResponse {
  success: boolean;
  data?: ExtractedData;
  error?: string;
}

export class ApiService {
  /**
   * Upload image for OCR processing
   */
  static async extractFromImage(imageUri: string): Promise<ApiResponse> {
    try {
      // Create FormData for file upload
      const formData = new FormData();
      
      formData.append('file', {
        uri: imageUri,
        type: 'image/jpeg',
        name: 'payment_screenshot.jpg',
      } as any);

      console.log('API_BASE_URL:', API_BASE_URL);
      console.log('OCR_EXTRACT endpoint:', API_ENDPOINTS.OCR_EXTRACT);
      console.log('Uploading to:', API_ENDPOINTS.OCR_EXTRACT);

      const response = await fetch(API_ENDPOINTS.OCR_EXTRACT, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ApiResponse = await response.json();
      return data;

    } catch (error) {
      console.error('API Error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error occurred'
      };
    }
  }

  /**
   * Test API connection
   */
  static async testConnection(): Promise<boolean> {
    try {
      const response = await fetch(API_ENDPOINTS.OCR_EXTRACT.replace('/ocr/extract', ''), {
        method: 'GET',
      });
      return response.ok;
    } catch (error) {
      console.error('Connection test failed:', error);
      return false;
    }
  }
}