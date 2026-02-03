import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Play } from 'lucide-react';
import api from '../api';

const SimulationRunner = () => {
    const [searchParams] = useSearchParams();
    const assessmentParam = searchParams.get('assessment_id');
    const personParam = searchParams.get('person_id');
    const scenarioParam = searchParams.get('scenario_id');
    const recommendationParam = searchParams.get('recommendation_id');

    const [running, setRunning] = useState(false);
    const [progress, setProgress] = useState(0);
    const [logs, setLogs] = useState([]);
    const [result, setResult] = useState(null);

    const [persons, setPersons] = useState([]);
    const [scenarios, setScenarios] = useState([]);
    const [scenarioPresets, setScenarioPresets] = useState([]);
    const [reactionCatalog, setReactionCatalog] = useState({});
    const [selectedPerson, setSelectedPerson] = useState("");
    const [selectedScenario, setSelectedScenario] = useState("");
    const [selectedPresetKey, setSelectedPresetKey] = useState("");
    const [gridSize, setGridSize] = useState(10);
    const [assessmentId, setAssessmentId] = useState(assessmentParam || "");
    const [profileLocked, setProfileLocked] = useState(false);

    const [currentFrameData, setCurrentFrameData] = useState(null);

    // Psychological Profile Sliders
    const [traumaSensitivity, setTraumaSensitivity] = useState(0.5);
    const [emotionalRegulation, setEmotionalRegulation] = useState(0.5);
    const [recoveryRate, setRecoveryRate] = useState(0.5);
    const [impulsivity, setImpulsivity] = useState(0.5);
    const [copingMechanism, setCopingMechanism] = useState("avoidance");

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [pRes, sRes, presetRes] = await Promise.all([
                    api.get('/persons/'),
                    api.get('/scenarios/'),
                    api.get('/simulations/presets'),
                ]);

                setPersons(pRes.data);
                setScenarios(sRes.data);
                setScenarioPresets(presetRes.data?.scenarios || []);
                setReactionCatalog(presetRes.data?.reactions || {});

                if (personParam) {
                    setSelectedPerson(parseInt(personParam, 10));
                } else if (pRes.data.length > 0) {
                    setSelectedPerson(pRes.data[0].id);
                }

                // If a recommended scenario is provided, select it first
                if (scenarioParam) {
                    const scenarioId = parseInt(scenarioParam, 10);
                    setSelectedScenario(scenarioId);
                    const scenarioMatch = sRes.data.find(s => s.id === scenarioId);
                    if (scenarioMatch) {
                        const presetMatch = (presetRes.data?.scenarios || []).find(
                            p => p.scenario_type.toLowerCase() === scenarioMatch.scenario_type.toLowerCase()
                        );
                        if (presetMatch) {
                            setSelectedPresetKey(presetMatch.key);
                            setGridSize(presetMatch.recommended_grid || 10);
                        }
                    }
                } else {
                    // Default to first preset and its matching scenario
                    const firstPreset = (presetRes.data?.scenarios || [])[0];
                    if (firstPreset) {
                        setSelectedPresetKey(firstPreset.key);
                        setGridSize(firstPreset.recommended_grid || 10);
                        const match = sRes.data.find(s => s.scenario_type.toLowerCase() === firstPreset.scenario_type.toLowerCase());
                        if (match) {
                            setSelectedScenario(match.id);
                        } else if (sRes.data.length > 0) {
                            setSelectedScenario(sRes.data[0].id);
                        }
                    } else if (sRes.data.length > 0) {
                        setSelectedScenario(sRes.data[0].id);
                    }
                }
            } catch (err) {
                console.error("Failed to fetch data", err);
            }
        };
        fetchData();
    }, []);

    useEffect(() => {
        const fetchAssessment = async () => {
            if (!assessmentParam) return;
            try {
                const res = await api.get(`/assessments/${assessmentParam}`);
                const assessment = res.data;
                setAssessmentId(assessment.id);
                setProfileLocked(true);

                setTraumaSensitivity(assessment.trauma_sensitivity);
                setEmotionalRegulation(assessment.emotional_regulation);
                setRecoveryRate(assessment.recovery_rate);
                setImpulsivity(assessment.impulsivity);
                setCopingMechanism(assessment.coping_mechanism);

                if (assessment.person_id) {
                    setSelectedPerson(assessment.person_id);
                }
            } catch (err) {
                console.error("Failed to fetch assessment", err);
            }
        };
        fetchAssessment();
    }, [assessmentParam]);

    const handlePresetChange = (key) => {
        setSelectedPresetKey(key);
        const preset = scenarioPresets.find(p => p.key === key);
        if (preset) {
            setGridSize(preset.recommended_grid || 10);
            const match = scenarios.find(s => s.scenario_type.toLowerCase() === preset.scenario_type.toLowerCase());
            if (match) {
                setSelectedScenario(match.id);
            }
        }
    };

    const handleRun = async () => {
        if (!selectedPerson || !selectedScenario) return;
        setRunning(true);
        setLogs([]);
        setResult(null);
        setCurrentFrameData(null);

        setLogs(prev => [...prev, "Initializing Mesa Model..."]);

        try {
            await new Promise(r => setTimeout(r, 500));

            const response = await api.post('/simulations/', {
                person_id: selectedPerson,
                scenario_id: selectedScenario,
                assessment_id: assessmentId || undefined,
                assigned_date: new Date().toISOString().split('T')[0],
                grid_size: gridSize,
                trauma_sensitivity: traumaSensitivity,
                emotional_regulation: emotionalRegulation,
                recovery_rate: recoveryRate,
                impulsivity: impulsivity,
                coping_mechanism: copingMechanism
            });

            const simData = response.data;
            const history = simData.full_history || [];

            console.log("DEBUG: simData received:", simData);
            console.log("DEBUG: full_history:", history);
            console.log("DEBUG: history.length:", history.length);

            setLogs(prev => [...prev, `Simulation returned ${history.length} steps.`]);

            // Replay History
            history.forEach((stepData, index) => {
                setTimeout(() => {
                    setCurrentFrameData(stepData);
                    setLogs(prev => {
                        let newLog = `Step ${stepData.step}: Status ${stepData.soldier_status} (Stress: ${stepData.soldier_stress.toFixed(1)})`;
                        
                        // Add reaction info if this step has a reaction
                        if (stepData.reaction_id) {
                            newLog += ` | Reaction #${stepData.reaction_id} [${stepData.reaction_type}]: ${stepData.physical_response.substring(0, 60)}...`;
                        }
                        
                        return [...prev, newLog];
                    });
                    
                    // Auto-scroll to bottom
                    setTimeout(() => {
                        const logsDiv = document.querySelector('.simulation-logs');
                        if (logsDiv) logsDiv.scrollTop = logsDiv.scrollHeight;
                    }, 50);
                }, index * 500); // 500ms per step
            });

            // Finish
            setTimeout(() => {
                setLogs(prev => [...prev, "Model Visualization Complete."]);
                setRunning(false);
                setResult(simData);

                if (recommendationParam) {
                    api.put(
                        `/therapist/recommendations/${recommendationParam}/status`,
                        null,
                        { params: { new_status: 'completed' } }
                    ).catch(() => {
                        console.log('Could not update recommendation to completed');
                    });
                }
            }, history.length * 500);

        } catch (err) {
            console.error(err);
            setLogs(prev => [...prev, "Error: Simulation Failed."]);
            setRunning(false);
        }
    };

    return (
        <div className="container">
            <header style={{ marginBottom: '2rem' }}>
                <h1>Simulation Lab</h1>
                <p style={{ color: 'var(--text-muted)' }}>Configure and run Mesa Agent-Based Model.</p>
            </header>

            <div className="grid-cols-2">
                {/* Controls */}
                <div className="glass-panel" style={{ padding: '2rem' }}>
                    <h3>Configuration</h3>
                    <div style={{ marginTop: '1rem', marginBottom: '1rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>Select Soldier</label>
                        <select value={selectedPerson} onChange={e => setSelectedPerson(e.target.value)}>
                            {persons.map(p => <option key={p.id} value={p.id}>{p.name} ({p.rank})</option>)}
                        </select>
                    </div>

                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>Scenario Template</label>
                        <select value={selectedPresetKey} onChange={e => handlePresetChange(e.target.value)}>
                            {scenarioPresets.map(preset => (
                                <option key={preset.key} value={preset.key}>
                                    {preset.scenario_type} ({preset.environment})
                                </option>
                            ))}
                        </select>
                        {selectedPresetKey && (
                            <small style={{ color: 'var(--text-muted)' }}>
                                {scenarioPresets.find(p => p.key === selectedPresetKey)?.description || ''}
                            </small>
                        )}
                    </div>

                    <div style={{ marginBottom: '1.25rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>
                            Grid Size: <strong>{gridSize} x {gridSize}</strong>
                        </label>
                        <input
                            type="range"
                            min="6"
                            max="20"
                            step="1"
                            value={gridSize}
                            onChange={e => setGridSize(parseInt(e.target.value, 10))}
                            style={{ width: '100%' }}
                        />
                        <small style={{ color: 'var(--text-muted)' }}>Environment dimensions (affects trigger density).</small>
                    </div>

                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>
                            Trauma Sensitivity: <strong>{traumaSensitivity.toFixed(2)}</strong>
                        </label>
                        <input 
                            type="range" 
                            min="0" 
                            max="1" 
                            step="0.01" 
                            value={traumaSensitivity} 
                            onChange={e => setTraumaSensitivity(parseFloat(e.target.value))}
                            disabled={profileLocked}
                            style={{ width: '100%' }}
                        />
                        <small style={{ color: 'var(--text-muted)' }}>How sensitive to stress (0=resistant, 1=highly sensitive)</small>
                    </div>

                    {/* Emotional Regulation Slider */}
                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.3rem' }}>
                            Emotional Regulation: <strong>{emotionalRegulation.toFixed(2)}</strong>
                        </label>
                        <input 
                            type="range" 
                            min="0" 
                            max="1" 
                            step="0.01" 
                            value={emotionalRegulation} 
                            onChange={e => setEmotionalRegulation(parseFloat(e.target.value))}
                            disabled={profileLocked}
                            style={{ width: '100%' }}
                        />
                        <small style={{ color: 'var(--text-muted)' }}>Ability to manage emotions (0=poor, 1=excellent)</small>
                    </div>

                    {/* Recovery Rate Slider */}
                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.3rem' }}>
                            Recovery Rate: <strong>{recoveryRate.toFixed(2)}</strong>
                        </label>
                        <input 
                            type="range" 
                            min="0" 
                            max="1" 
                            step="0.01" 
                            value={recoveryRate} 
                            onChange={e => setRecoveryRate(parseFloat(e.target.value))}
                            disabled={profileLocked}
                            style={{ width: '100%' }}
                        />
                        <small style={{ color: 'var(--text-muted)' }}>How fast they recover from stress (0=slow, 1=fast)</small>
                    </div>

                    {/* Impulsivity Slider */}
                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.3rem' }}>
                            Impulsivity: <strong>{impulsivity.toFixed(2)}</strong>
                        </label>
                        <input 
                            type="range" 
                            min="0" 
                            max="1" 
                            step="0.01" 
                            value={impulsivity} 
                            onChange={e => setImpulsivity(parseFloat(e.target.value))}
                            disabled={profileLocked}
                            style={{ width: '100%' }}
                        />
                        <small style={{ color: 'var(--text-muted)' }}>Tendency to act without thinking (0=deliberate, 1=impulsive)</small>
                    </div>

                    {/* Coping Mechanism Dropdown */}
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem' }}>Coping Mechanism</label>
                        <select value={copingMechanism} onChange={e => setCopingMechanism(e.target.value)} disabled={profileLocked}>
                            <option value="avoidance">Avoidance (Run away)</option>
                            <option value="approach">Approach (Face threat)</option>
                            <option value="freezing">Freezing (Paralyzed)</option>
                            <option value="suppression">Suppression (Ignore it)</option>
                        </select>
                    </div>

                    <button className="btn" onClick={handleRun} disabled={running} style={{ width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                        {running ? 'Running Simulation...' : <><Play size={18} style={{ marginRight: '8px' }} /> Start Simulation</>}
                    </button>
                </div>

                {/* Output Visualization */}
                <div className="glass-panel" style={{ padding: '2rem', minHeight: '400px', display: 'flex', flexDirection: 'column' }}>
                    <h3>Mesa Grid Visualization</h3>

                    {/* Grid Container */}
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
                        gap: '2px',
                        background: '#334155',
                        padding: '2px',
                        borderRadius: '4px',
                        aspectRatio: '1/1',
                        margin: '1.5rem 0',
                        width: '320px',
                        alignSelf: 'center'
                    }}>
                        {Array.from({ length: gridSize * gridSize }).map((_, i) => {
                            const x = i % gridSize;
                            const y = Math.floor(i / gridSize);

                            // Check active step data
                            // logs are now just text, we need state. 
                            // Let's rely on 'progress' to roughly map to steps or parse logs?
                            // Better: Store the current frame in state.

                            return (
                                <div key={i} style={{
                                    background: 'rgba(255,255,255,0.05)',
                                    position: 'relative'
                                }}>
                                    {/* Render Agents based on currentFrame state (we need to impl this) */}
                                    <DataGridCell x={x} y={y} frame={currentFrameData} gridSize={gridSize} />
                                </div>
                            )
                        })}
                    </div>

                    {/* Console Logs */}
                    <div className="simulation-logs" style={{
                        flex: 1,
                        background: 'rgba(0,0,0,0.3)',
                        borderRadius: '8px',
                        padding: '1rem',
                        fontFamily: 'monospace',
                        color: '#4ade80',
                        marginBottom: '1rem',
                        overflowY: 'auto',
                        maxHeight: '150px',
                        fontSize: '0.85rem'
                    }}>
                        {logs.length === 0 ? <span style={{ color: '#64748b' }}>// Ready for Model Execution...</span> :
                            logs.map((log, i) => <div key={i}>&gt; {log}</div>)
                        }
                    </div>

                    {/* Result Report */}
                    {result && result.report && (
                        <div style={{ borderTop: '1px solid var(--border-glass)', paddingTop: '1rem', animation: 'fadeIn 1s' }}>
                            <h4 style={{ color: 'white', marginBottom: '0.5rem' }}>Recovery Report</h4>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', fontSize: '0.9rem' }}>
                                <div>Avoidance: <span style={{ color: 'var(--primary)' }}>{result.report.avoidance}</span></div>
                                <div>Re-Experiencing: <span style={{ color: 'var(--accent-secondary)' }}>{result.report.re_experiencing}</span></div>
                                <div>Negative Alterations: <span style={{ color: 'var(--accent-warning)' }}>{result.report.negative_alterations}</span></div>
                                <div>Hyperarousal: <span style={{ color: 'var(--accent-danger)' }}>{result.report.hyperarousal}</span></div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

// Helper to render cell content
const DataGridCell = ({ x, y, frame, gridSize }) => {
    if (!frame) return null;

    // Check Soldier
    // Mesa grid 0,0 is usually bottom-left? Or top-left? 
    // Usually Python Mesa MultiGrid treated 0,0 as Bottom-Left by default?
    // Let's assume standard matrix for now (0,0 top-left) or check coords.
    // If our backend uses default mesas, 0,0 is bottom-left. 
    // We are rendering top-left (0,0) to bottom-right (9,9) in HTML grid.
    // We might need to flip Y. Let's handle Y flip:
    // HTML Grid Row 0 is Top. Mesa Y=9 is Top.
    // So visualY = 9 - mesaY.

    const mesaY = (gridSize - 1) - y;

    const isSoldier = frame.soldier_pos && frame.soldier_pos[0] === x && frame.soldier_pos[1] === mesaY;

    // Check Triggers
    const isTrigger = frame.triggers && frame.triggers.find(t => t.pos[0] === x && t.pos[1] === mesaY);

    if (isSoldier) {
        return <div style={{
            width: '80%', height: '80%', borderRadius: '50%', margin: '10%',
            background: frame.soldier_color,
            boxShadow: `0 0 8px ${frame.soldier_color}`,
            transition: 'all 0.3s'
        }} title={`Stress: ${frame.soldier_stress}`} />;
    }

    if (isTrigger) {
        return <div style={{
            width: '60%', height: '60%', borderRadius: '2px', margin: '20%',
            background: '#ef4444',
            opacity: 0.6
        }} />;
    }

    return null;
};

export default SimulationRunner;
