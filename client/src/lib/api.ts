// API service for making requests to the backend
import config from './config';

// Get API URL from configuration
const API_URL = config.apiUrl;

/**
 * Fetch data from the API with error handling
 */
async function fetchFromApi(endpoint: string) {
  try {
    const response = await fetch(`${API_URL}${endpoint}`);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

// API endpoints
export const api = {
  // Health check
  getHealth: () => fetchFromApi('/health'),

  // User endpoints
  getUsers: () => fetchFromApi('/api/v1/users/'),
  getUser: (id: number) => fetchFromApi(`/api/v1/users/${id}`),
};

export default api;