import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token
apiClient.interceptors.request.use(
  (config) => {
    const authTokens = localStorage.getItem('authTokens') 
      ? JSON.parse(localStorage.getItem('authTokens')) 
      : null;

    if (authTokens) {
      config.headers.Authorization = `Bearer ${authTokens.access}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);


export const fetchGames = () => {
  return apiClient.get('/games/');
};

export const loginUser = (credentials) => {
  return apiClient.post('/auth/login/', credentials);
};

export const registerUser = (userData) => {
  return apiClient.post('/auth/register/', userData);
};

export const fetchUserProfile = () => {
  return apiClient.get('/users/profile/');
};

export const fetchParties = () => {
  return apiClient.get('/parties/');
};

export const createParty = (partyData) => {
  return apiClient.post('/parties/', partyData);
};

export const joinParty = (partyId) => {
  return apiClient.post(`/parties/${partyId}/join/`);
};

export const leaveParty = (partyId) => {
  return apiClient.post(`/parties/${partyId}/leave/`);
};
