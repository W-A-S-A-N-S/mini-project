import React from 'react';

const PartyCard = ({ party, onJoin }) => {
  const statusColors = {
    open: 'bg-green-600',
    closed: 'bg-red-600',
    in_progress: 'bg-blue-600',
    completed: 'bg-gray-500',
  };

  return (
    <div className="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      <div className="p-4">
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm text-gray-400">{party.game.name}</p>
            <h3 className="text-lg font-bold text-white mb-2">{party.title}</h3>
          </div>
          <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full text-white ${statusColors[party.status] || 'bg-gray-500'}`}>
            {party.status}
          </span>
        </div>
        
        <div className="text-sm text-gray-400 mt-2">
          <p>Creator: {party.creator.username}</p>
          <p>Play Time: {new Date(party.play_time).toLocaleString()}</p>
        </div>

        <div className="flex items-center justify-between mt-4">
          <div className="flex items-center">
            <span className="text-sm font-bold text-white">{party.current_members_count} / {party.max_members} Members</span>
          </div>
          <button 
            onClick={() => onJoin(party.id)}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-1 px-3 rounded-lg text-sm disabled:bg-gray-500"
            disabled={party.is_full || party.status !== 'open'}
          >
            Join
          </button>
        </div>
      </div>
    </div>
  );
};

export default PartyCard;
