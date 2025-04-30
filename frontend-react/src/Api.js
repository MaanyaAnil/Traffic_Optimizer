import axios from 'axios';

const API_URL = 'http://localhost:8000/upload';

export const uploadVideos = async (videos) => {
  const formData = new FormData();
  videos.forEach(video => formData.append('videos', video));

  const response = await axios.post(`${API_URL}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

  return response.data;
};

export const fetchStatus = async () => {
  const response = await axios.get(`${API_URL}/status`);
  return response.data;
};

// You might also have triggerEmergency and clearEmergency functions here