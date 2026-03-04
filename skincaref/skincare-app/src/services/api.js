import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Disease Detection API
export const detectDisease = async (imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);

  const response = await axios.post(`${API_BASE_URL}/disease/analyze`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

// Skincare Analysis API
export const analyzeSkincareWithQuestionnaire = async (imageFile, questionnaire) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('questionnaire', JSON.stringify(questionnaire));

  const response = await axios.post(`${API_BASE_URL}/skincare/analyze`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

// Chatbot API
export const chatWithBot = async (message, skinType = null) => {
  const response = await api.post('/chatbot/chat', {
    message,
    skin_type: skinType,
  });

  return response.data;
};

// Health Check
export const checkHealth = async () => {
  const response = await axios.get('http://localhost:5000/health');
  return response.data;
};

export default api;