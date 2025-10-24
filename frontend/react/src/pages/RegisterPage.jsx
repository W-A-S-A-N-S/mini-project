import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser } from '../services/api';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    steam_id: '',
    password: '',
    password2: '',
  });
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (formData.password !== formData.password2) {
      setError({ password: 'Passwords do not match.' });
      return;
    }

    try {
      await registerUser(formData);
      navigate('/login'); // Redirect to login page on successful registration
    } catch (err) {
      setError(err.response?.data || { general: 'Failed to register.' });
      console.error(err);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-3xl font-bold mb-6 text-center">Create Account</h1>
      <form onSubmit={handleSubmit} className="bg-gray-800 p-8 rounded-lg shadow-lg">
        <div className="mb-4">
          <label className="block text-gray-300 mb-2" htmlFor="username">Username</label>
          <input type="text" name="username" value={formData.username} onChange={handleChange} className="w-full px-3 py-2 bg-gray-700 rounded" required />
          {error?.username && <p className="text-red-500 text-xs mt-1">{error.username}</p>}
        </div>
        <div className="mb-4">
          <label className="block text-gray-300 mb-2" htmlFor="email">Email</label>
          <input type="email" name="email" value={formData.email} onChange={handleChange} className="w-full px-3 py-2 bg-gray-700 rounded" required />
          {error?.email && <p className="text-red-500 text-xs mt-1">{error.email}</p>}
        </div>
        <div className="mb-4">
          <label className="block text-gray-300 mb-2" htmlFor="steam_id">Steam ID</label>
          <input type="text" name="steam_id" value={formData.steam_id} onChange={handleChange} className="w-full px-3 py-2 bg-gray-700 rounded" required />
          {error?.steam_id && <p className="text-red-500 text-xs mt-1">{error.steam_id}</p>}
        </div>
        <div className="mb-4">
          <label className="block text-gray-300 mb-2" htmlFor="password">Password</label>
          <input type="password" name="password" value={formData.password} onChange={handleChange} className="w-full px-3 py-2 bg-gray-700 rounded" required />
          {error?.password && <p className="text-red-500 text-xs mt-1">{error.password}</p>}
        </div>
        <div className="mb-6">
          <label className="block text-gray-300 mb-2" htmlFor="password2">Confirm Password</label>
          <input type="password" name="password2" value={formData.password2} onChange={handleChange} className="w-full px-3 py-2 bg-gray-700 rounded" required />
        </div>
        {error?.general && <p className="text-red-500 text-center mb-4">{error.general}</p>}
        <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg">Register</button>
      </form>
    </div>
  );
};

export default RegisterPage;