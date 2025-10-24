import { useState, useEffect } from 'react';
import { fetchGames } from '../services/api';

import GameCard from '../components/GameCard';

const GameListPage = () => {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getGames = async () => {
      try {
        const response = await fetchGames();
        setGames(response.data.results);
      } catch (err) {
        setError('Error fetching games. Is the backend server running?');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    getGames();
  }, []);

  if (loading) return <p className="text-center">Loading games...</p>;
  if (error) return <p className="text-center text-red-500">{error}</p>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Games</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {games.length > 0 ? (
          games.map((game) => (
            <GameCard key={game.id} game={game} />
          ))
        ) : (
          <p>No games found.</p>
        )}
      </div>
    </div>
  );
};


export default GameListPage;