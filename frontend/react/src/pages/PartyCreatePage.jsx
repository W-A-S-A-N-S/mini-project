import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { createParty, fetchGames } from '../services/api';

const PartyCreatePage = () => {
  const [games, setGames] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    game: '',
    max_members: 4,
    play_time: '',
    duration_hours: 2,
    required_skill: 'any',
    play_style: 'any',
    voice_chat_required: false,
    discord_link: '',
  });
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const getGames = async () => {
      try {
        const response = await fetchGames();
        setGames(response.data.results);
        if (response.data.results.length > 0) {
          setFormData(prev => ({ ...prev, game: response.data.results[0].id }));
        }
      } catch (err) {
        console.error("Failed to fetch games", err);
      }
    };
    getGames();
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await createParty(formData);
      navigate('/parties');
    } catch (err) {
      setError(err.response?.data || { general: 'Failed to create party.' });
      console.error(err);
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-10">
      <h1 className="text-3xl font-bold mb-6 text-center">Create a New Party</h1>
      <form onSubmit={handleSubmit} className="bg-gray-800 p-8 rounded-lg shadow-lg space-y-4">
        
        <div>
          <label className="block text-gray-300 mb-2">Game</label>
          <select name="game" value={formData.game} onChange={handleChange} className="w-full p-2 bg-gray-700 rounded">
            {games.map(game => <option key={game.id} value={game.id}>{game.name}</option>)}
          </select>
        </div>

        <div>
          <label className="block text-gray-300 mb-2">Title</label>
          <input type="text" name="title" value={formData.title} onChange={handleChange} className="w-full p-2 bg-gray-700 rounded" required />
        </div>

        <div>
          <label className="block text-gray-300 mb-2">Description</label>
          <textarea name="description" value={formData.description} onChange={handleChange} className="w-full p-2 bg-gray-700 rounded" required />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-gray-300 mb-2">Play Time</label>
            <input type="datetime-local" name="play_time" value={formData.play_time} onChange={handleChange} className="w-full p-2 bg-gray-700 rounded" required />
          </div>
          <div>
            <label className="block text-gray-300 mb-2">Max Members</label>
            <input type="number" name="max_members" value={formData.max_members} onChange={handleChange} className="w-full p-2 bg-gray-700 rounded" min="2" max="10" required />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-gray-300 mb-2">Required Skill</label>
            <select name="required_skill" value={formData.required_skill} onChange={handleChange} className="w-full p-2 bg-gray-700 rounded">
              <option value="any">Any</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
              <option value="expert">Expert</option>
            </select>
          </div>
          <div>
            <label className="block text-gray-300 mb-2">Play Style</label>
            <select name="play_style" value={formData.play_style} onChange={handleChange} className="w-full p-2 bg-gray-700 rounded">
              <option value="any">Any</option>
              <option value="casual">Casual</option>
              <option value="serious">Serious</option>
              <option value="competitive">Competitive</option>
              <option value="fun">For Fun</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-gray-300 mb-2">Discord Link (Optional)</label>
          <input type="url" name="discord_link" value={formData.discord_link} onChange={handleChange} className="w-full p-2 bg-gray-700 rounded" />
        </div>

        <div className="flex items-center">
          <input type="checkbox" name="voice_chat_required" checked={formData.voice_chat_required} onChange={handleChange} className="h-4 w-4 text-blue-600 bg-gray-700 border-gray-600 rounded" />
          <label className="ml-2 text-gray-300">Voice Chat Required?</label>
        </div>

        <button type="submit" className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-lg mt-4">Create Party</button>
        {error?.general && <p className="text-red-500 text-center mt-4">{error.general}</p>}
      </form>
    </div>
  );
};

export default PartyCreatePage;
