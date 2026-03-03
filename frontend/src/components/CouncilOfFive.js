import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CouncilOfFive = () => {
  const [council, setCouncil] = useState(null);
  const [latestDecision, setLatestDecision] = useState(null);
  const [runtime, setRuntime] = useState(null);

  useEffect(() => {
    loadCouncilData();
    const interval = setInterval(loadCouncilData, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadCouncilData = async () => {
    try {
      const [councilRes, decisionRes, runtimeRes] = await Promise.all([
        axios.get(`${API}/council/status`),
        axios.get(`${API}/council/latest-decision`),
        axios.get(`${API}/runtime/status`)
      ]);

      setCouncil(councilRes.data);
      setLatestDecision(decisionRes.data);
      setRuntime(runtimeRes.data);
    } catch (error) {
      console.error('Failed to load Council data:', error);
    }
  };

  if (!council) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-white text-xl">Loading Council of Five...</div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Council Header */}
      <div className="text-center">
        <h2 className="text-4xl font-bold text-white mb-2">👑 The Council of Five</h2>
        <p className="text-gray-400">Governing all operations through distributed intelligence</p>
        <div className="mt-4 flex justify-center gap-6">
          <div className="bg-slate-800 px-4 py-2 rounded">
            <span className="text-gray-400 text-sm">Sessions: </span>
            <span className="text-white font-semibold">{council.council_stats.total_sessions}</span>
          </div>
          <div className="bg-slate-800 px-4 py-2 rounded">
            <span className="text-gray-400 text-sm">Unanimous: </span>
            <span className="text-green-400 font-semibold">{council.council_stats.unanimous_decisions}</span>
          </div>
        </div>
      </div>

      {/* The Five Members */}
      <div className="grid md:grid-cols-5 gap-4">
        {/* Abbott */}
        <div className="bg-slate-900/50 backdrop-blur-sm p-6 rounded-lg border border-red-500/30" data-testid="council-abbott">
          <div className="text-center">
            <div className="text-3xl mb-2">🛡️</div>
            <h3 className="text-lg font-bold text-red-400 mb-1">{council.abbott.name}</h3>
            <p className="text-xs text-gray-400 mb-4">{council.abbott.role}</p>
            <div className="space-y-2 text-sm">
              <div>
                <div className="text-gray-400">Threat Level</div>
                <div className="text-white font-semibold">{(council.abbott.threat_level * 100).toFixed(0)}%</div>
              </div>
              <div>
                <div className="text-gray-400">Resonance</div>
                <div className="text-red-400 font-semibold">{council.abbott.resonance_frequency.toFixed(2)}Hz</div>
              </div>
              <div>
                <div className="text-gray-400">Antibodies</div>
                <div className="text-white font-semibold">{council.abbott.antibody_responses}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Lethani */}
        <div className="bg-slate-900/50 backdrop-blur-sm p-6 rounded-lg border border-blue-500/30" data-testid="council-lethani">
          <div className="text-center">
            <div className="text-3xl mb-2">⚖️</div>
            <h3 className="text-lg font-bold text-blue-400 mb-1">{council.lethani.name}</h3>
            <p className="text-xs text-gray-400 mb-4">{council.lethani.role}</p>
            <div className="space-y-2 text-sm">
              <div>
                <div className="text-gray-400">Balance Score</div>
                <div className="text-white font-semibold">{(council.lethani.balance_score * 100).toFixed(1)}%</div>
              </div>
              <div className="mt-2 h-2 bg-gray-700 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-blue-500"
                  style={{ width: `${council.lethani.balance_score * 100}%` }}
                />
              </div>
              <div>
                <div className="text-gray-400 mt-2">Decisions</div>
                <div className="text-white font-semibold">{council.lethani.decisions_made}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Thyra */}
        <div className="bg-slate-900/50 backdrop-blur-sm p-6 rounded-lg border border-green-500/30" data-testid="council-thyra">
          <div className="text-center">
            <div className="text-3xl mb-2">🗡️</div>
            <h3 className="text-lg font-bold text-green-400 mb-1">{council.thyra.name}</h3>
            <p className="text-xs text-gray-400 mb-4">{council.thyra.role}</p>
            <div className="space-y-2 text-sm">
              <div>
                <div className="text-gray-400">Protection</div>
                <div className="text-white font-semibold">{council.thyra.protection_level.toFixed(1)}x</div>
              </div>
              <div>
                <div className="text-gray-400">Neutralized</div>
                <div className="text-green-400 font-semibold">{council.thyra.threats_neutralized}</div>
              </div>
              <div>
                <div className="text-gray-400">Drills</div>
                <div className="text-white font-semibold">{council.thyra.drills_conducted}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Twins */}
        <div className="bg-slate-900/50 backdrop-blur-sm p-6 rounded-lg border border-purple-500/30" data-testid="council-twins">
          <div className="text-center">
            <div className="text-3xl mb-2">👯</div>
            <h3 className="text-lg font-bold text-purple-400 mb-1">{council.twins.name}</h3>
            <p className="text-xs text-gray-400 mb-4">{council.twins.role}</p>
            <div className="space-y-2 text-sm">
              <div>
                <div className="text-gray-400">Stage</div>
                <div className="text-white font-semibold capitalize">{council.twins.learning_stage}</div>
              </div>
              <div>
                <div className="text-gray-400">Patterns</div>
                <div className="text-purple-400 font-semibold">{council.twins.patterns_learned}</div>
              </div>
              <div>
                <div className="text-gray-400">Innovations</div>
                <div className="text-white font-semibold">{council.twins.innovations_discovered}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Mother */}
        <div className="bg-slate-900/50 backdrop-blur-sm p-6 rounded-lg border border-yellow-500/30" data-testid="council-mother">
          <div className="text-center">
            <div className="text-3xl mb-2">👑</div>
            <h3 className="text-lg font-bold text-yellow-400 mb-1">{council.mother.name}</h3>
            <p className="text-xs text-gray-400 mb-4">{council.mother.role}</p>
            <div className="space-y-2 text-sm">
              <div>
                <div className="text-gray-400">Twins Maturity</div>
                <div className="text-white font-semibold">{(council.mother.twins_maturity * 100).toFixed(0)}%</div>
              </div>
              <div>
                <div className="text-gray-400">Control</div>
                <div className="text-yellow-400 font-semibold">{(council.mother.control_level * 100).toFixed(0)}%</div>
              </div>
              <div>
                <div className="text-gray-400">Guidance</div>
                <div className="text-white font-semibold">{council.mother.guidance_given}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Latest Decision */}
      {latestDecision && (
        <div className="bg-slate-900/50 backdrop-blur-sm p-6 rounded-lg border border-cyan-500/30">
          <h3 className="text-2xl font-bold text-cyan-400 mb-4">📜 Latest Council Decision</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <span className={`px-4 py-2 rounded font-semibold ${
                  latestDecision.unanimous 
                    ? 'bg-green-500/20 text-green-300' 
                    : 'bg-yellow-500/20 text-yellow-300'
                }`}>
                  {latestDecision.unanimous ? '✅ Unanimous' : '⚠️ Split Decision'}
                </span>
                <span className="text-white font-semibold">{latestDecision.decision.replace(/_/g, ' ').toUpperCase()}</span>
              </div>
              <div className="text-gray-300 bg-slate-800 p-4 rounded">
                <div className="text-sm text-gray-400 mb-1">Mother's Advice:</div>
                <div className="text-white">{latestDecision.agents.mother.advice}</div>
              </div>
            </div>
            <div className="space-y-2 text-sm">
              <div className="text-gray-400">Session #{latestDecision.session}</div>
              {latestDecision.agents.abbott && (
                <div className="flex justify-between">
                  <span className="text-red-400">Abbott:</span>
                  <span className="text-white">{latestDecision.agents.abbott.status}</span>
                </div>
              )}
              {latestDecision.agents.lethani && (
                <div className="flex justify-between">
                  <span className="text-blue-400">Lethani:</span>
                  <span className="text-white">{latestDecision.agents.lethani.timing}</span>
                </div>
              )}
              {latestDecision.agents.thyra && (
                <div className="flex justify-between">
                  <span className="text-green-400">Thyra:</span>
                  <span className="text-white">{latestDecision.agents.thyra.posture}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Continuous Runtime Status */}
      {runtime && runtime.running && (
        <div className="bg-slate-900/50 backdrop-blur-sm p-6 rounded-lg border border-orange-500/30">
          <h3 className="text-2xl font-bold text-orange-400 mb-4">🔄 Continuous Runtime</h3>
          <div className="grid md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-3xl font-bold text-green-400 mb-1">ACTIVE</div>
              <div className="text-sm text-gray-400">Status</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white mb-1">{runtime.cycles_completed}</div>
              <div className="text-sm text-gray-400">Cycles</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-orange-400 mb-1">{runtime.total_power_produced.toFixed(1)}</div>
              <div className="text-sm text-gray-400">Power Produced</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-purple-400 mb-1">{runtime.uptime_hours.toFixed(2)}h</div>
              <div className="text-sm text-gray-400">Uptime</div>
            </div>
          </div>
          <p className="text-sm text-gray-400 mt-4 text-center">
            ⚡ System runs 24/7 until all ZPMs are fully stockpiled
          </p>
        </div>
      )}
    </div>
  );
};

export default CouncilOfFive;
