import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchParties, joinParty } from '../services/api';
import PartyCard from '../components/PartyCard';

const PartyListPage = () => {
  const [parties, setParties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getParties = async () => {
    try {
      const response = await fetchParties();
      setParties(response.data.results);
    } catch (err) {
      setError('Error fetching parties.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getParties();
  }, []);

  const handleJoinParty = async (partyId) => {
    try {
      await joinParty(partyId);
      // Optimistically update the UI or refetch the list
      // For now, let's refetch to get the most accurate data
      getParties(); 
    } catch (err) {
      console.error("Failed to join party", err);
      alert("Failed to join party. It might be full or you may have already joined.");
    }
  };

  if (loading) return <p className="text-center">Loading parties...</p>;
  if (error) return <p className="text-center text-red-500">{error}</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Available Parties</h1>
        <Link to="/parties/create" className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg">
          Create Party
        </Link>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {parties.length > 0 ? (
          parties.map((party) => (
            <PartyCard key={party.id} party={party} onJoin={handleJoinParty} />
          ))
        ) : (
          <p>No parties found. Why not create one?</p>
        )}
      </div>
    </div>
  );
};

export default PartyListPage;