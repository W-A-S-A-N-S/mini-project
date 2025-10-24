import { createContext, useState, useContext, useEffect } from 'react';
import { fetchUserProfile } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [tokens, setTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const bootstrapAuth = async () => {
      if (tokens) {
        try {
          const response = await fetchUserProfile();
          setUser(response.data);
        } catch (e) {
          // Invalid token, clear state
          setTokens(null);
          setUser(null);
          localStorage.removeItem('authTokens');
        }
      }
      setLoading(false);
    };
    bootstrapAuth();
  }, [tokens]);

  const login = async (authTokens) => {
    setTokens(authTokens);
    localStorage.setItem('authTokens', JSON.stringify(authTokens));
    try {
      const response = await fetchUserProfile();
      setUser(response.data);
    } catch (e) {
      console.error("Failed to fetch user profile after login", e);
    }
  };

  const logout = () => {
    setTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
  };

  const value = {
    user,
    tokens,
    loading,
    login,
    logout,
  };

  // Render children only after loading is complete
  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};
