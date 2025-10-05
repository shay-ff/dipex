import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TouchableOpacity, 
  Image, 
  StyleSheet, 
  ActivityIndicator,
  Alert,
  ScrollView
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { ApiService, ExtractedData } from '../../services/apiService';
import { API_BASE_URL, API_ENDPOINTS } from '../../config/api';

export default function App() {
  // STATE MANAGEMENT
  // Think of useState as variables that React watches
  // When they change, the UI automatically updates
  
  const [selectedImage, setSelectedImage] = useState<string | null>(null); // stores the image URI
  const [loading, setLoading] = useState<boolean>(false); // shows spinner when uploading
  const [extractedData, setExtractedData] = useState<ExtractedData | null>(null); // stores OCR results

  // FUNCTION 1: Pick image from gallery
  const pickImage = async () => {
    // Request permission to access photos (required on iOS)
    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
    
    if (permissionResult.granted === false) {
      Alert.alert("Permission Required", "Please allow access to your photos");
      return;
    }

    // Open image picker
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'], // only images, no videos
      allowsEditing: false, // lets user crop
      aspect: [9, 16], // portrait aspect ratio
      quality: 0.8, // compress to 80% quality to save bandwidth
    });

    // If user didn't cancel, save the image URI
    if (!result.canceled) {
      setSelectedImage(result.assets[0].uri);
      // Clear previous results when new image selected
      setExtractedData(null);
    }
  };

  // FUNCTION 2: Upload image to backend
  const uploadImage = async () => {
    if (!selectedImage) {
      Alert.alert("No Image", "Please select a screenshot first");
      return;
    }

    // Debug: Log the configuration being used
    console.log('=== Upload Debug ===');
    console.log('API_BASE_URL:', API_BASE_URL);
    console.log('OCR_EXTRACT endpoint:', API_ENDPOINTS.OCR_EXTRACT);
    console.log('==================');

    setLoading(true); // show spinner

    try {
      // Use API service for cleaner code
      const result = await ApiService.extractFromImage(selectedImage);
      if (result.success && result.data) {
        setExtractedData(result.data);
        Alert.alert("Success", "Payment details extracted!");
      } else {
        Alert.alert("Error", result.error || "Failed to extract data");
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      Alert.alert("Network Error", errorMessage);
      console.error('Upload error:', error);
    } finally {
      setLoading(false); // hide spinner
    }
  };

  // UI RENDERING
  return (
    <ScrollView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Dipex</Text>
        <Text style={styles.subtitle}>Upload Payment Screenshot</Text>
      </View>

      {/* Image Preview */}
      {selectedImage && (
        <View style={styles.imageContainer}>
          <Image 
            source={{ uri: selectedImage }} 
            style={styles.image}
            resizeMode="contain"
          />
        </View>
      )}

      {/* Buttons */}
      <View style={styles.buttonContainer}>
        <TouchableOpacity 
          style={styles.button} 
          onPress={pickImage}
          disabled={loading}
        >
          <Text style={styles.buttonText}>
            {selectedImage ? "Change Screenshot" : "Pick Screenshot"}
          </Text>
        </TouchableOpacity>

        {selectedImage && (
          <TouchableOpacity 
            style={[styles.button, styles.uploadButton]} 
            onPress={uploadImage}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.buttonText}>Extract Data</Text>
            )}
          </TouchableOpacity>
        )}
      </View>

      {/* Results Display */}
      {extractedData && (
        <View style={styles.resultsContainer}>
          <Text style={styles.resultsTitle}>Extracted Details:</Text>
          
          <View style={styles.resultRow}>
            <Text style={styles.label}>Amount:</Text>
            <Text style={styles.value}>₹{extractedData.amount || 'N/A'}</Text>
          </View>

          <View style={styles.resultRow}>
            <Text style={styles.label}>Merchant:</Text>
            <Text style={styles.value}>{extractedData.merchant || 'N/A'}</Text>
          </View>

          <View style={styles.resultRow}>
            <Text style={styles.label}>Date:</Text>
            <Text style={styles.value}>{extractedData.date || 'N/A'}</Text>
          </View>

          <View style={styles.resultRow}>
            <Text style={styles.label}>Transaction ID:</Text>
            <Text style={styles.value}>{extractedData.transaction_id || 'N/A'}</Text>
          </View>
        </View>
      )}

      {/* Instructions */}
      {!selectedImage && (
        <View style={styles.instructions}>
          <Text style={styles.instructionText}>
            📸 Take a screenshot of your UPI payment confirmation
          </Text>
          <Text style={styles.instructionText}>
            📤 Upload it here to automatically track your expense
          </Text>
        </View>
      )}
    </ScrollView>
  );
}

// STYLES (CSS-like styling for React Native)
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  header: {
    marginTop: 50,
    marginBottom: 30,
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#333',
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginTop: 5,
  },
  imageContainer: {
    width: '100%',
    height: 400,
    backgroundColor: '#fff',
    borderRadius: 10,
    overflow: 'hidden',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  image: {
    width: '100%',
    height: '100%',
  },
  buttonContainer: {
    gap: 15,
    marginBottom: 20,
  },
  button: {
    backgroundColor: '#007AFF',
    padding: 16,
    borderRadius: 10,
    alignItems: 'center',
  },
  uploadButton: {
    backgroundColor: '#34C759',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  resultsContainer: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    marginBottom: 20,
  },
  resultsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  resultRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  label: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
  },
  value: {
    fontSize: 14,
    color: '#333',
    fontWeight: '600',
  },
  instructions: {
    padding: 20,
    backgroundColor: '#fff',
    borderRadius: 10,
    gap: 10,
  },
  instructionText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 22,
  },
});