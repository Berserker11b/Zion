import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const NexusCore = () => {
  const [nexusStatus, setNexusStatus] = useState(null);
  const [engines, setEngines] = useState(null);
  const [zpms, setZpms] = useState([]);
  const [busNetwork, setBusNetwork] = useState(null);
  const [cyberWorms, setCyberWorms] = useState(null);

  useEffect(() => {
    loadNexusData();
    const interval = setInterval(loadNexusData, 3000);
    return () => clearInterval(interval);
  }, []);

  const loadNexusData = async () => {
    try {
      const [statusRes, enginesRes, zpmsRes, busRes, wormsRes] = await Promise.all([
        axios.get(`${API}/nexus/status`),
        axios.get(`${API}/nexus/engines`),
        axios.get(`${API}/nexus/zpms`),
        axios.get(`${API}/nexus/bus-network`),
        axios.get(`${API}/nexus/cyber-worms`)
      ]);

      setNexusStatus(statusRes.data);
      setEngines(enginesRes.data);
      setZpms(zpmsRes.data.batteries);
      setBusNetwork(busRes.data);
      setCyberWorms(wormsRes.data);
    } catch (error) {
      console.error('Failed to load Nexus Core data:', error);
    }
  };

  if (!nexusStatus || !engines) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-white text-xl">Loading Nexus Core...</div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Engines Section */}
      <div data-testid="nexus-engines">
        <h2 className="text-3xl font-bold text-white mb-6">⚙️ Power Generation Engines</h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          {/* Turbine Engine */}
          <div className="bg-slate-900/50 backdrop-blur-sm p-6 rounded-lg border border-orange-500/30" data-testid="turbine-engine">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-orange-400">Turbine Engine</h3>
              <span className="px-3 py-1 rounded bg-orange-500/20 text-orange-300 text-sm font-semibold">
                {engines.turbine.status.toUpperCase()}
              </span>
            </div>
            
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Base Efficiency:</span>
                <span className="text-white font-semibold">{(engines.turbine.base_efficiency * 100).toFixed(0)}%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Total Processed:</span>
                <span className="text-orange-400 font-semibold">{engines.turbine.total_processed.toFixed(2)} units</span>
              </div>
              <div className="mt-4 h-2 bg-gray-700 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-orange-500 to-orange-400"
                  style={{ width: `${engines.turbine.base_efficiency * 100}%` }}
                />
              </div>
              <p className="text-xs text-gray-400 mt-2">Always available • Lower efficiency • Reliable baseline</p>
            </div>
          </div>

          {/* Starheart Engine */}
          <div className={`bg-slate-900/50 backdrop-blur-sm p-6 rounded-lg border ${
            engines.starheart.status === 'active' ? 'border-purple-500 ring-2 ring-purple-500/50' :
            engines.starheart.status === 'warming' ? 'border-yellow-500/30' :
            'border-gray-500/30'
          }`} data-testid="starheart-engine">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-purple-400">Starheart Engine</h3>
              <span className={`px-3 py-1 rounded text-sm font-semibold ${
                engines.starheart.status === 'active' ? 'bg-purple-500/20 text-purple-300' :
                engines.starheart.status === 'warming' ? 'bg-yellow-500/20 text-yellow-300' :
                'bg-gray-500/20 text-gray-300'
              }`}>
                {engines.starheart.status.toUpperCase()}
              </span>
            </div>
            
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Peak Efficiency:</span>
                <span className="text-white font-semibold">{(engines.starheart.efficiency * 100).toFixed(0)}%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Gravity Strength:</span>
                <span className="text-purple-400 font-semibold">{(engines.starheart.gravity_strength * 100).toFixed(0)}%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Ignition Progress:</span>
                <span className="text-white font-semibold">{engines.starheart.ignition_progress.toFixed(0)}%</span>
              </div>
              <div className="mt-4 h-2 bg-gray-700 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-purple-600 to-purple-400"
                  style={{ width: `${engines.starheart.ignition_progress}%` }}
                />
              </div>
              {engines.starheart.status === 'active' && (
                <p className="text-xs text-purple-300 mt-2">⚡ IGNITED! Self-sustaining with gravitational pull</p>
              )}
              {engines.starheart.status === 'warming' && (
                <p className="text-xs text-yellow-300 mt-2">🔥 Warming up... {(50 - engines.starheart.total_processed).toFixed(1)} units to ignition</p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* ZPM Batteries */}
      <div data-testid="zpm-batteries">
        <h2 className="text-3xl font-bold text-white mb-6">🔋 ZPM Storage Batteries</h2>
        
        <div className="grid md:grid-cols-5 gap-4">
          {zpms.map((zpm) => (
            <div 
              key={zpm.id}
              className={`bg-slate-900/50 backdrop-blur-sm p-4 rounded-lg border ${
                zpm.status === 'charged' ? 'border-green-500' :
                zpm.status === 'filling' ? 'border-blue-500/50' :
                'border-gray-500/30'
              }`}
              data-testid={`zpm-${zpm.id}`}
            >
              <div className="text-center">
                <div className="text-sm text-gray-400 mb-2">{zpm.id}</div>
                <div className="text-3xl font-bold text-white mb-2">{zpm.fill_percentage.toFixed(0)}%</div>
                <div className="h-2 bg-gray-700 rounded-full overflow-hidden mb-3">
                  <div 
                    className={`h-full ${
                      zpm.status === 'charged' ? 'bg-green-500' :
                      zpm.status === 'filling' ? 'bg-blue-500' :
                      'bg-gray-600'
                    }`}
                    style={{ width: `${zpm.fill_percentage}%` }}
                  />
                </div>
                <div className="text-xs">
                  <div className="text-gray-400">Compression: {zpm.compression_level.toFixed(2)}x</div>
                  <div className={`font-semibold mt-1 ${
                    zpm.status === 'charged' ? 'text-green-400' :
                    zpm.status === 'filling' ? 'text-blue-400' :
                    'text-gray-400'
                  }`}>
                    {zpm.status.toUpperCase()}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        <p className="text-sm text-gray-400 mt-4">
          💡 Compressed energy storage using advanced compression algorithms. Deploy when charged to convert to credits.
        </p>
      </div>

      {/* Bus Network & Cyber Worms */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Bus Network */}
        {busNetwork && (
          <div className="bg-slate-900/50 backdrop-blur-sm p-6 rounded-lg border border-cyan-500/30" data-testid="bus-network">
            <h3 className="text-2xl font-bold text-cyan-400 mb-4">🌐 Nexus Bus Network</h3>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Current Throughput:</span>
                <span className="text-cyan-400 font-semibold">{busNetwork.throughput.toFixed(2)} units/s</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Total Routed:</span>
                <span className="text-white font-semibold">{busNetwork.total_routed.toFixed(2)} units</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Filter Efficiency:</span>
                <span className="text-green-400 font-semibold">{(busNetwork.filter_efficiency * 100).toFixed(0)}%</span>
              </div>
              <p className="text-xs text-gray-400 mt-4">
                Secure tunnel with filtering • Routes entropy from walls to engines
              </p>
            </div>
          </div>
        )}

        {/* Cyber Worms */}
        {cyberWorms && (
          <div className="bg-slate-900/50 backdrop-blur-sm p-6 rounded-lg border border-pink-500/30" data-testid="cyber-worms">
            <h3 className="text-2xl font-bold text-pink-400 mb-4">🐛 Cyber Worms</h3>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Total Active:</span>
                <span className="text-white font-semibold">{cyberWorms.total_worms} worms</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Feeder Worms:</span>
                <span className="text-purple-400 font-semibold">{cyberWorms.feeder_worms}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Compressor Worms:</span>
                <span className="text-blue-400 font-semibold">{cyberWorms.compressor_worms}</span>
              </div>
              <p className="text-xs text-gray-400 mt-4">
                {cyberWorms.starheart_active 
                  ? '⚡ Split mode: Feeding Starheart + Compressing for ZPMs'
                  : '🔄 All worms compressing energy into ZPM batteries'}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default NexusCore;
