import React from 'react';
import { Link } from 'react-router-dom';

const GameCard = ({ game }) => {
  const difficultyColors = {
    'easy': 'bg-green-600',
    'normal': 'bg-blue-600',
    'hard': 'bg-yellow-600',
    'extreme': 'bg-red-600',
  };

  return (
    <Link to={`/games/${game.id}`} className="block bg-gray-800 rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 ease-in-out">
      <img 
        className="w-full h-48 object-cover" 
        src={game.image_url || 'https://via.placeholder.com/400x300?text=No+Image'} 
        alt={`${game.name} cover art`} 
      />
      <div className="p-4">
        <h3 className="text-xl font-bold text-white mb-2 truncate">{game.name}</h3>
        <div className="flex justify-between items-center text-sm text-gray-400">
          <span className="font-semibold capitalize bg-gray-700 px-2 py-1 rounded-full text-xs">{game.genre}</span>
          <div>
            <span>{game.min_players}-{game.max_players} Players</span>
            <span className="ml-2 pl-2 border-l border-gray-600">{game.open_party_count} Parties</span>
          </div>
        </div>
        <div className="mt-3 flex items-center">
          <span className={`text-xs font-semibold mr-2 px-2.5 py-0.5 rounded-full text-white ${difficultyColors[game.difficulty] || 'bg-gray-500'}`}>
            {game.difficulty}
          </span>
        </div>
      </div>
    </Link>
  );
};

export default GameCard;
