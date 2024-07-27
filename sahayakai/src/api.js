import axios from 'axios';

export const fetchRecommendations = async (keywords) => {
  try {
    const response = await axios.post('http://localhost:5000/recommend', {
      keywords,
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    return [];
  }
};
