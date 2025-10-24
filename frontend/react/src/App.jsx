import { Routes, Route, Link, Outlet } from 'react-router-dom';
import HomePage from './pages/HomePage';
import GameListPage from './pages/GameListPage';
import GameDetailPage from './pages/GameDetailPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import PartyListPage from './pages/PartyListPage';
import PartyCreatePage from './pages/PartyCreatePage';
import PartyDetailPage from './pages/PartyDetailPage';
import { useAuth } from './context/AuthContext';

const Layout = () => {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 shadow">
        <nav className="container mx-auto px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="text-xl font-semibold text-white">
              <Link to="/">Steam Party Matcher</Link>
            </div>
            <div className="flex items-center">
              <Link to="/" className="px-3 py-2 rounded text-gray-300 hover:bg-gray-700">Home</Link>
              <Link to="/games" className="px-3 py-2 rounded text-gray-300 hover:bg-gray-700">Games</Link>
              {user ? (
                <>
                  <Link to="/parties" className="px-3 py-2 rounded text-gray-300 hover:bg-gray-700">Parties</Link>
                  <span className="px-3 py-2 text-gray-300">Welcome, {user.username}</span>
                  <button onClick={logout} className="px-3 py-2 rounded text-gray-300 hover:bg-gray-700">Logout</button>
                </>
              ) : (
                <>
                  <Link to="/login" className="px-3 py-2 rounded text-gray-300 hover:bg-gray-700">Login</Link>
                  <Link to="/register" className="px-3 py-2 rounded text-gray-300 hover:bg-gray-700">Register</Link>
                </>
              )}
            </div>
          </div>
        </nav>
      </header>
      <main className="container mx-auto px-6 py-8">
        <Outlet />
      </main>
    </div>
  );
};

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="games" element={<GameListPage />} />
        <Route path="games/:id" element={<GameDetailPage />} />
        <Route path="parties" element={<PartyListPage />} />
        <Route path="parties/create" element={<PartyCreatePage />} />
        <Route path="parties/:id" element={<PartyDetailPage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />
      </Route>
    </Routes>
  );
}

export default App;