import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import NexusCore from './NexusCore';
import CouncilOfFive from './CouncilOfFive';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [walls, setWalls] = useState([]);
  const [starheart, setStarheart] = useState(null);
  const [packages, setPackages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUserData();
    loadWallStatus();
    loadStarheartStatus();
    loadPackages();

    // Refresh data every 5 seconds
    const interval = setInterval(() => {
      loadWallStatus();
      loadStarheartStatus();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getAuthHeaders = () => {
    const token = localStorage.getItem('fluxcore_token');
    return { headers: { Authorization: `Bearer ${token}` } };
  };

  const loadUserData = async () => {
    try {
      const response = await axios.get(`${API}/user/profile`, getAuthHeaders());
      setUser(response.data);
    } catch (error) {
      console.error('Failed to load user:', error);
      if (error.response?.status === 401) {
        localStorage.removeItem('fluxcore_token');
        navigate('/login');
      }
    }
  };

  const loadWallStatus = async () => {
    try {
      const response = await axios.get(`${API}/monitor/walls`);
      setWalls(response.data);
    } catch (error) {
      console.error('Failed to load walls:', error);
    }
  };

  const loadStarheartStatus = async () => {
    try {
      const response = await axios.get(`${API}/monitor/starheart`);
      setStarheart(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load starheart:', error);
      setLoading(false);
    }
  };

  const loadPackages = async () => {
    try {
      const response = await axios.get(`${API}/marketplace/packages`);
      setPackages(response.data);
    } catch (error) {
      console.error('Failed to load packages:', error);
    }
  };

  const handlePurchase = async (packageId) => {
    try {
      await axios.post(
        `${API}/marketplace/purchase`,
        { package_id: packageId, user_id: user.id },
        getAuthHeaders()
      );
      alert('Purchase successful!');
      loadUserData(); // Refresh credits
    } catch (error) {
      alert('Purchase failed: ' + (error.response?.data?.detail || 'Unknown error'));
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('fluxcore_token');
    localStorage.removeItem('fluxcore_user');
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 flex items-center justify-center">
        <div className="text-white text-2xl">Loading FluxCore...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950">
      {/* Header */}
      <div className="bg-slate-900/50 backdrop-blur-sm border-b border-purple-500/30">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-white">FluxCore</h1>
            <p className="text-sm text-gray-400">{user?.email}</p>
          </div>
          <div className="flex items-center gap-6">
            <div className="text-right">
              <p className="text-sm text-gray-400">Available Credits</p>
              <p className="text-2xl font-bold text-purple-400" data-testid="user-credits">{user?.credits?.toFixed(2) || '0.00'}</p>
            </div>
            <button
              onClick={handleLogout}
              className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition-all"
              data-testid="logout-button"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-8">
        {/* The Six-Walled Fortress */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-white mb-6">🛡️ The Six-Walled Fortress</h2>
          <div className="grid md:grid-cols-3 gap-4">
            {walls.map((wall) => (
              <div
                key={wall.wall_number}
                className={`bg-slate-900/50 backdrop-blur-sm p-6 rounded-lg border ${
                  wall.status === 'fortified'
                    ? 'border-green-500/50'
                    : wall.active_threats > 0
                    ? 'border-red-500/50'
                    : 'border-purple-500/30'
                }`}
                data-testid={`wall-${wall.wall_number}`}
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <div className="text-sm text-gray-400">Wall {wall.wall_number}</div>
                    <div className="text-lg font-bold text-white">{wall.name?.split(' - ')[1] || `Wall ${wall.wall_number}`}</div>
                  </div>
                  <div
                    className={`px-2 py-1 rounded text-xs font-semibold ${
                      wall.status === 'fortified'
                        ? 'bg-green-500/20 text-green-300'
                        : wall.active_threats > 0
                        ? 'bg-red-500/20 text-red-300'
                        : 'bg-purple-500/20 text-purple-300'
                    }`}
                  >
                    {wall.status}
                  </div>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Threats Blocked:</span>
                    <span className="text-white font-semibold">{wall.total_blocked}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Entropy Generated:</span>
                    <span className="text-purple-400 font-semibold">{wall.entropy_generated?.toFixed(2)} ⚡</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Council of Five */}
        <CouncilOfFive />

        {/* Nexus Core Engine System */}
        <NexusCore />

        {/* Marketplace */}
        <div>
          <h2 className="text-3xl font-bold text-white mb-6">💎 Credit Marketplace</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {packages.map((pkg) => (
              <div
                key={pkg.id}
                className={`bg-slate-900/50 backdrop-blur-sm p-8 rounded-lg border ${
                  pkg.popular ? 'border-purple-500 ring-2 ring-purple-500/50' : 'border-purple-500/30'
                }`}
                data-testid={`package-${pkg.id}`}
              >
                {pkg.popular && (
                  <div className="bg-purple-600 text-white text-xs font-bold px-3 py-1 rounded-full inline-block mb-4">
                    MOST POPULAR
                  </div>
                )}
                <h3 className="text-2xl font-bold text-white mb-2">{pkg.name}</h3>
                <div className="text-4xl font-bold text-purple-400 mb-4">${pkg.price}</div>
                <div className="text-gray-300 mb-4">{pkg.credits} Credits</div>
                <p className="text-sm text-gray-400 mb-6">{pkg.description}</p>
                <button
                  onClick={() => handlePurchase(pkg.id)}
                  className="w-full bg-purple-600 hover:bg-purple-700 text-white px-4 py-3 rounded-lg font-semibold transition-all"
                  data-testid={`purchase-${pkg.id}`}
                >
                  Purchase
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
