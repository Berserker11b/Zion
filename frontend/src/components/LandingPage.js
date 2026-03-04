import React from 'react';
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950">
      {/* Hero Section */}
      <div className="container mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-white mb-6">
            FluxCore
            <span className="block text-purple-400 mt-2">Advanced Resource Management Platform</span>
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
            Enterprise-grade computational resource optimization. 
            Maximize efficiency through intelligent load balancing and distributed processing.
          </p>
          <div className="flex gap-4 justify-center">
            <button
              onClick={() => navigate('/register')}
              className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-3 rounded-lg text-lg font-semibold transition-all transform hover:scale-105"
              data-testid="get-started-button"
            >
              Get Started
            </button>
            <button
              onClick={() => navigate('/login')}
              className="bg-gray-700 hover:bg-gray-600 text-white px-8 py-3 rounded-lg text-lg font-semibold transition-all"
              data-testid="login-button"
            >
              Login
            </button>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mt-20">
          <div className="bg-slate-900/50 backdrop-blur-sm p-8 rounded-lg border border-purple-500/30">
            <div className="text-4xl mb-4">🛡️</div>
            <h3 className="text-2xl font-bold text-white mb-3">The Six-Walled Fortress</h3>
            <p className="text-gray-300">
              Advanced security that doesn't just block attacks - it converts them into computational power.
            </p>
          </div>

          <div className="bg-slate-900/50 backdrop-blur-sm p-8 rounded-lg border border-purple-500/30">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-2xl font-bold text-white mb-3">The Starheart Engine</h3>
            <p className="text-gray-300">
              Our proprietary system converts entropy and waste into pure computational resources.
            </p>
          </div>

          <div className="bg-slate-900/50 backdrop-blur-sm p-8 rounded-lg border border-purple-500/30">
            <div className="text-4xl mb-4">💎</div>
            <h3 className="text-2xl font-bold text-white mb-3">Credit Marketplace</h3>
            <p className="text-gray-300">
              Purchase computational power credits. The more demand, the more power we generate.
            </p>
          </div>
        </div>

        {/* How It Works */}
        <div className="mt-20 text-center">
          <h2 className="text-4xl font-bold text-white mb-12">How It Works</h2>
          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="bg-purple-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold">1</div>
              <h4 className="text-white font-semibold mb-2">Purchase Credits</h4>
              <p className="text-gray-400 text-sm">Choose a package that fits your needs</p>
            </div>
            <div className="text-center">
              <div className="bg-purple-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold">2</div>
              <h4 className="text-white font-semibold mb-2">Use Resources</h4>
              <p className="text-gray-400 text-sm">Access computational power for your tasks</p>
            </div>
            <div className="text-center">
              <div className="bg-purple-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold">3</div>
              <h4 className="text-white font-semibold mb-2">We Generate More</h4>
              <p className="text-gray-400 text-sm">Your usage creates more power</p>
            </div>
            <div className="text-center">
              <div className="bg-purple-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl font-bold">4</div>
              <h4 className="text-white font-semibold mb-2">Sustainable Cycle</h4>
              <p className="text-gray-400 text-sm">Self-sustaining computational ecosystem</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;