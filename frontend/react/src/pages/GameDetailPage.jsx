import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { apiClient } from '../services/api';
import PartyCard from '../components/PartyCard';

const GameDetailPage = () => {
  const { id } = useParams();
  const [game, setGame] = useState(null);
  const [parties, setParties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const gameResponse = await apiClient.get(`/games/${id}/`);
        setGame(gameResponse.data);

        const partiesResponse = await apiClient.get(`/parties/?game=${id}`);
        setParties(partiesResponse.data.results);

      } catch (err) {
        setError('Error fetching game details.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  if (loading) return <p className="text-center">Loading...</p>;
  if (error) return <p className="text-center text-red-500">{error}</p>;
  if (!game) return <p className="text-center">Game not found.</p>;

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white">{game.name}</h1>
        <p className="text-lg text-gray-400 mt-2">Parties for {game.name}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {parties.length > 0 ? (
          parties.map((party) => (
            <PartyCard key={party.id} party={party} />
          ))
        ) : (
          <p className="text-white">No parties found for this game. Why not create one?</p>
        )}
      </div>
    </div>
  );
};

export default GameDetailPage;
