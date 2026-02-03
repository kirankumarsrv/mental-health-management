import React, { useState, useEffect } from 'react';
import { Plus, Edit2, Trash2, X } from 'lucide-react';
import api from '../api';

const ScenarioManager = () => {
    const [scenarios, setScenarios] = useState([]);
    const [scenarioPresets, setScenarioPresets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [editingScenario, setEditingScenario] = useState(null);
    const [formData, setFormData] = useState({
        scenario_type: '',
        environment: ''
    });
    const [selectedPresetKey, setSelectedPresetKey] = useState('');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            setLoading(true);
            const [scenarioRes, presetRes] = await Promise.all([
                api.get('/scenarios/'),
                api.get('/simulations/presets')
            ]);
            setScenarios(scenarioRes.data);
            setScenarioPresets(presetRes.data?.scenarios || []);
            setError(null);
        } catch (err) {
            setError('Failed to fetch scenarios');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (editingScenario) {
                await api.put(`/scenarios/${editingScenario.id}`, formData);
            } else {
                await api.post('/scenarios/', formData);
            }
            
            fetchData();
            closeModal();
        } catch (err) {
            alert('Failed to save scenario');
            console.error(err);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this scenario?')) {
            try {
                await api.delete(`/scenarios/${id}`);
                fetchData();
            } catch (err) {
                alert('Failed to delete scenario');
                console.error(err);
            }
        }
    };

    const openModal = (scenario = null) => {
        if (scenario) {
            setEditingScenario(scenario);
            const preset = scenarioPresets.find(p => p.scenario_type.toLowerCase() === scenario.scenario_type.toLowerCase());
            setSelectedPresetKey(preset ? preset.key : '');
            setFormData({
                scenario_type: scenario.scenario_type,
                environment: scenario.environment
            });
        } else {
            setEditingScenario(null);
            const firstPreset = scenarioPresets[0];
            setSelectedPresetKey(firstPreset ? firstPreset.key : '');
            setFormData({
                scenario_type: firstPreset ? firstPreset.scenario_type : '',
                environment: firstPreset ? firstPreset.environment : ''
            });
        }
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
        setEditingScenario(null);
    };

    if (loading) return <div className="container"><p>Loading...</p></div>;
    if (error) return <div className="container"><p style={{ color: 'var(--accent-danger)' }}>{error}</p></div>;

    return (
        <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Scenarios</h1>
                <button className="btn" onClick={() => openModal()} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Plus size={18} /> Add New Scenario
                </button>
            </div>

            <div className="glass-panel" style={{ padding: '0', overflow: 'hidden' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                    <thead style={{ background: 'rgba(255,255,255,0.05)', borderBottom: '1px solid var(--border-glass)' }}>
                        <tr>
                            <th style={{ padding: '1rem' }}>ID</th>
                            <th style={{ padding: '1rem' }}>Scenario Type</th>
                            <th style={{ padding: '1rem' }}>Environment</th>
                            <th style={{ padding: '1rem' }}>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {scenarios.map(s => (
                            <tr key={s.id} style={{ borderBottom: '1px solid var(--border-glass)' }}>
                                <td style={{ padding: '1rem' }}>#{s.id}</td>
                                <td style={{ padding: '1rem', fontWeight: 'bold' }}>{s.scenario_type}</td>
                                <td style={{ padding: '1rem' }}>{s.environment}</td>
                                <td style={{ padding: '1rem', display: 'flex', gap: '0.5rem' }}>
                                    <button 
                                        className="btn-secondary" 
                                        style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}
                                        onClick={() => openModal(s)}
                                    >
                                        <Edit2 size={14} /> Edit
                                    </button>
                                    <button 
                                        className="btn-secondary" 
                                        style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem', background: 'var(--accent-danger)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}
                                        onClick={() => handleDelete(s.id)}
                                    >
                                        <Trash2 size={14} /> Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Modal */}
            {showModal && (
                <div style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: 'rgba(0,0,0,0.7)',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    zIndex: 1000
                }}>
                    <div className="glass-panel" style={{ padding: '2rem', maxWidth: '500px', width: '90%', position: 'relative' }}>
                        <button 
                            onClick={closeModal}
                            style={{ position: 'absolute', top: '1rem', right: '1rem', background: 'none', border: 'none', color: 'white', cursor: 'pointer' }}
                        >
                            <X size={24} />
                        </button>
                        
                        <h2>{editingScenario ? 'Edit Scenario' : 'Add New Scenario'}</h2>
                        
                        <form onSubmit={handleSubmit} style={{ marginTop: '1.5rem' }}>
                            <div style={{ marginBottom: '1rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Scenario Template</label>
                                <select
                                    required
                                    value={selectedPresetKey}
                                    onChange={(e) => {
                                        const key = e.target.value;
                                        setSelectedPresetKey(key);
                                        const preset = scenarioPresets.find(p => p.key === key);
                                        if (preset) {
                                            setFormData({
                                                scenario_type: preset.scenario_type,
                                                environment: preset.environment
                                            });
                                        }
                                    }}
                                >
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

                            <div style={{ marginBottom: '1.5rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Environment</label>
                                <input 
                                    type="text" 
                                    required
                                    value={formData.environment}
                                    readOnly
                                    style={{ background: 'rgba(255,255,255,0.05)' }}
                                />
                            </div>
                            
                            <div style={{ display: 'flex', gap: '1rem' }}>
                                <button type="submit" className="btn" style={{ flex: 1 }}>
                                    {editingScenario ? 'Update' : 'Create'}
                                </button>
                                <button type="button" className="btn-secondary" style={{ flex: 1 }} onClick={closeModal}>
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ScenarioManager;
