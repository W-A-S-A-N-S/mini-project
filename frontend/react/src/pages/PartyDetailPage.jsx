import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiClient, deleteParty } from '../services/api';
import { useAuth } from '../context/AuthContext';

const PartyDetailPage = () => {
  const { id } = useParams();
  const [party, setParty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    const fetchParty = async () => {
      try {
        const response = await apiClient.get(`/parties/${id}/`);
        setParty(response.data);
      } catch (err) {
        setError('Error fetching party details.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchParty();
  }, [id]);

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this party?')) {
      try {
        await deleteParty(id);
        navigate('/parties');
      } catch (err) {
        console.error("Failed to delete party", err);
        alert('Failed to delete party.');
      }
    }
  };

  if (loading) return <p className="text-center">Loading party...</p>;
  if (error) return <p className="text-center text-red-500">{error}</p>;
  if (!party) return <p className="text-center">Party not found.</p>;

  const isCreator = user && user.id === party.creator.id;

  return (
    <div className="max-w-4xl mx-auto mt-10 bg-gray-800 p-8 rounded-lg shadow-lg text-white">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-4xl font-bold mb-2">{party.title}</h1>
          <p className="text-lg text-gray-400">Hosted by {party.creator.username}</p>
        </div>
        {isCreator && (
          <button 
            onClick={handleDelete}
            className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg"
          >
            Delete Party
          </button>
        )}
      </div>

      <div className="mt-6 border-t border-gray-700 pt-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h2 className="text-2xl font-bold mb-4">Party Details</h2>
            <div className="space-y-3">
              <p><span className="font-semibold">Game:</span> {party.game.name}</p>
              <p><span className="font-semibold">Description:</span> {party.description}</p>
              <p><span className="font-semibold">Play Time:</span> {new Date(party.play_time).toLocaleString()}</p>
              <p><span className="font-semibold">Duration:</span> {party.duration_hours} hours</p>
              <p><span className="font-semibold">Status:</span> {party.status}</p>
            </div>
          </div>
          <div>
            <h2 className="text-2xl font-bold mb-4">Requirements</h2>
            <div className="space-y-3">
              <p><span className="font-semibold">Required Skill:</span> {party.required_skill}</p>
              <p><span className="font-semibold">Play Style:</span> {party.play_style}</p>
              <p><span className="font-semibold">Voice Chat:</span> {party.voice_chat_required ? 'Required' : 'Not required'}</p>
              {party.discord_link && <p><span className="font-semibold">Discord:</span> <a href={party.discord_link} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline">{party.discord_link}</a></p>}
            </div>
          </div>
        </div>
      </div>

      <div className="mt-8 border-t border-gray-700 pt-6">
        <h2 className="text-2xl font-bold mb-4">Members ({party.current_members_count} / {party.max_members})</h2>
        <ul className="space-y-2">
          {party.members.map(member => (
            <li key={member.user.id} className="bg-gray-700 p-3 rounded-lg">{member.user.username}</li>
          ))}
        </ul>
      </div>

    </div>
  );
};

export default PartyDetailPage;
