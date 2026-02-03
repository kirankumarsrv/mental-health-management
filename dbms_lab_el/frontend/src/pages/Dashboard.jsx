import React, { useEffect, useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { Activity, Users, Brain, FlaskConical, FileText, Play, LineChart, CheckCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import api from '../api';

const Dashboard = () => {
    const { user } = useAuth();
    const [stats, setStats] = useState({
        total_persons: 0,
        total_therapists: 0,
        total_scenarios: 0,
        total_reactions: 0,
        total_reports: 0
    });
    const [recentReports, setRecentReports] = useState([]);
    const [recentReactions, setRecentReactions] = useState([]);
    const [hasAssessment, setHasAssessment] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [statsRes, reportsRes, reactionsRes] = await Promise.all([
                api.get('/simulations/stats'),
                api.get('/reports?limit=5'),
                api.get('/reactions?limit=5')
            ]);
            setStats(statsRes.data);
            setRecentReports(Array.isArray(reportsRes.data) ? reportsRes.data : []);
            setRecentReactions(Array.isArray(reactionsRes.data) ? reactionsRes.data : []);
            
            // Check if user has completed assessment
            if (user?.person?.id || user?.person_id) {
                try {
                    const personId = user?.person?.id || user?.person_id;
                    const assessmentsRes = await api.get(`/assessments/?person_id=${personId}`);
                    setHasAssessment(assessmentsRes.data && assessmentsRes.data.length > 0);
                } catch (err) {
                    console.error('Failed to check assessments', err);
                }
            }
        } catch (err) {
            console.error('Failed to fetch dashboard data', err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="container"><p>Loading dashboard...</p></div>;

    // Redirect therapists to therapist dashboard
    if (user?.user?.role === 'therapist') {
        return <Navigate to="/therapist-dashboard" replace />;
    }

    return (
        <div className="container">
            <header style={{ marginBottom: '2rem' }}>
                <h1>Dashboard</h1>
                <p style={{ color: 'var(--text-muted)' }}>Welcome to the PTSD Simulation System</p>
            </header>

            {/* Workflow Guide for Soldiers */}
            {user?.role === 'soldier' && (
                <div className="glass-panel" style={{ 
                    padding: '2rem', 
                    marginBottom: '2rem',
                    background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)'
                }}>
                    <h2 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                        <FileText size={28} style={{ color: 'var(--primary)' }} />
                        Your Assessment Workflow
                    </h2>
                    
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: '1rem' }}>
                        <Link to="/questionnaire" style={{ textDecoration: 'none' }}>
                            <div className="glass-panel" style={{ 
                                padding: '1.5rem', 
                                textAlign: 'center',
                                cursor: 'pointer',
                                border: hasAssessment ? '2px solid var(--accent-success)' : '2px solid var(--primary)'
                            }}>
                                {hasAssessment ? (
                                    <CheckCircle size={40} style={{ color: 'var(--accent-success)', marginBottom: '0.5rem' }} />
                                ) : (
                                    <FileText size={40} style={{ color: 'var(--primary)', marginBottom: '0.5rem' }} />
                                )}
                                <h3>1. Take Assessment</h3>
                                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                    {hasAssessment ? 'Completed ✓' : 'Answer questionnaire'}
                                </p>
                            </div>
                        </Link>

                        <Link to="/scenarios" style={{ textDecoration: 'none' }}>
                            <div className="glass-panel" style={{ 
                                padding: '1.5rem', 
                                textAlign: 'center',
                                cursor: 'pointer',
                                opacity: hasAssessment ? 1 : 0.6
                            }}>
                                <FlaskConical size={40} style={{ color: 'var(--accent-warning)', marginBottom: '0.5rem' }} />
                                <h3>2. Choose Scenario</h3>
                                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                    Select simulation type
                                </p>
                            </div>
                        </Link>

                        <Link to="/simulation" style={{ textDecoration: 'none' }}>
                            <div className="glass-panel" style={{ 
                                padding: '1.5rem', 
                                textAlign: 'center',
                                cursor: 'pointer',
                                opacity: hasAssessment ? 1 : 0.6
                            }}>
                                <Play size={40} style={{ color: 'var(--primary)', marginBottom: '0.5rem' }} />
                                <h3>3. Run Simulation</h3>
                                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                    Execute PTSD model
                                </p>
                            </div>
                        </Link>

                        <Link to="/analytics" style={{ textDecoration: 'none' }}>
                            <div className="glass-panel" style={{ 
                                padding: '1.5rem', 
                                textAlign: 'center',
                                cursor: 'pointer',
                                opacity: hasAssessment ? 1 : 0.6
                            }}>
                                <LineChart size={40} style={{ color: 'var(--accent-success)', marginBottom: '0.5rem' }} />
                                <h3>4. View Analytics</h3>
                                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                    Analyze results
                                </p>
                            </div>
                        </Link>
                    </div>

                    {!hasAssessment && (
                        <div style={{ 
                            marginTop: '1.5rem', 
                            padding: '1rem', 
                            background: 'rgba(56, 189, 248, 0.1)',
                            borderRadius: '8px',
                            border: '1px solid rgba(56, 189, 248, 0.3)'
                        }}>
                            <p style={{ margin: 0, fontSize: '0.95rem' }}>
                                👉 <strong>Get Started:</strong> Complete your psychological assessment questionnaire to begin simulations with personalized trauma profile values.
                            </p>
                        </div>
                    )}
                </div>
            )}

            {/* Stats */}

            <div className="grid-cols-3">
                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
                        <Users size={24} style={{ color: 'var(--primary)' }} />
                        <h3>Soldiers</h3>
                    </div>
                    <h2 style={{ color: 'var(--primary)', fontSize: '2.5rem', margin: 0 }}>{stats.total_persons}</h2>
                </div>
                
                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
                        <Brain size={24} style={{ color: 'var(--accent-success)' }} />
                        <h3>Therapists</h3>
                    </div>
                    <h2 style={{ color: 'var(--accent-success)', fontSize: '2.5rem', margin: 0 }}>{stats.total_therapists}</h2>
                </div>
                
                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
                        <FlaskConical size={24} style={{ color: 'var(--accent-warning)' }} />
                        <h3>Scenarios</h3>
                    </div>
                    <h2 style={{ color: 'var(--accent-warning)', fontSize: '2.5rem', margin: 0 }}>{stats.total_scenarios}</h2>
                </div>
            </div>

            <div className="grid-cols-2" style={{ marginTop: '2rem' }}>
                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
                        <Activity size={24} style={{ color: 'var(--primary)' }} />
                        <h3>Reactions Recorded</h3>
                    </div>
                    <h2 style={{ color: 'var(--primary)', fontSize: '2.5rem', margin: 0 }}>{stats.total_reactions}</h2>
                </div>

                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
                        <Activity size={24} style={{ color: 'var(--accent-success)' }} />
                        <h3>Reports Generated</h3>
                    </div>
                    <h2 style={{ color: 'var(--accent-success)', fontSize: '2.5rem', margin: 0 }}>{stats.total_reports}</h2>
                </div>
            </div>

            {recentReports.length > 0 && (
                <div className="glass-panel" style={{ padding: '1.5rem', marginTop: '2rem' }}>
                    <h3 style={{ marginBottom: '1rem' }}>Recent Assessments (Reports)</h3>
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead style={{ borderBottom: '1px solid var(--border-glass)' }}>
                            <tr>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>ID</th>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Soldier ID</th>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Reaction ID</th>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Therapist ID</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recentReports.map(rep => (
                                <tr key={rep.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                    <td style={{ padding: '0.75rem' }}>#{rep.id}</td>
                                    <td style={{ padding: '0.75rem' }}>#{rep.person_id}</td>
                                    <td style={{ padding: '0.75rem' }}>#{rep.reaction_id}</td>
                                    <td style={{ padding: '0.75rem' }}>#{rep.therapist_id}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {recentReactions.length > 0 && (
                <div className="glass-panel" style={{ padding: '1.5rem', marginTop: '2rem' }}>
                    <h3 style={{ marginBottom: '1rem' }}>Recent Reactions Recorded</h3>
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead style={{ borderBottom: '1px solid var(--border-glass)' }}>
                            <tr>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>ID</th>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Reaction Type</th>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Physical Response</th>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Soldier ID</th>
                                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Scenario ID</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recentReactions.map(rxn => (
                                <tr key={rxn.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                    <td style={{ padding: '0.75rem' }}>#{rxn.id}</td>
                                    <td style={{ padding: '0.75rem' }}>{rxn.r_type}</td>
                                    <td style={{ padding: '0.75rem' }} title={rxn.physical_response}>
                                        {rxn.physical_response.substring(0, 40)}...
                                    </td>
                                    <td style={{ padding: '0.75rem' }}>#{rxn.person_id || 'N/A'}</td>
                                    <td style={{ padding: '0.75rem' }}>#{rxn.scenario_id || 'N/A'}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
