import React, { useState, useEffect } from 'react';
import {
    Users, BarChart3, TrendingUp, Filter, Plus, ChevronDown,
    Calendar, Activity, CheckCircle, AlertCircle, Eye, Send
} from 'lucide-react';
import API from '../api';
import './TherapistDashboard.css';

const TherapistDashboard = () => {
    const [activeTab, setActiveTab] = useState('overview');
    const [therapistId, setTherapistId] = useState(null);
    const [dashboardStats, setDashboardStats] = useState(null);
    const [patients, setPatients] = useState([]);
    const [selectedPatient, setSelectedPatient] = useState(null);
    const [patientDetails, setPatientDetails] = useState(null);
    const [scenarios, setScenarios] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Filter state
    const [filters, setFilters] = useState({
        min_age: '',
        max_age: '',
        min_service_years: '',
        max_service_years: '',
        gender: '',
        rank: ''
    });

    // Recommendation form state
    const [recommendationForm, setRecommendationForm] = useState({
        scenario_id: '',
        suggested_coping_mechanism: '',
        recommendation_text: ''
    });

    // Initialize - Get therapist info and load data
    useEffect(() => {
        const loadTherapistData = async () => {
            try {
                setLoading(true);
                const therapistResponse = await API.get('/therapist/me');
                setTherapistId(therapistResponse.data.id);
                
                // Load dashboard stats
                const statsResponse = await API.get(`/therapist/dashboard/stats/${therapistResponse.data.id}`);
                setDashboardStats(statsResponse.data);
                
                // Load patients
                const patientsResponse = await API.get(`/therapist/patients?therapist_id=${therapistResponse.data.id}`);
                setPatients(patientsResponse.data.patients);
                
                // Load scenarios
                const scenariosResponse = await API.get('/scenarios');
                setScenarios(scenariosResponse.data);
                
                setError('');
            } catch (err) {
                setError('Failed to load therapist data: ' + err.message);
            } finally {
                setLoading(false);
            }
        };

        loadTherapistData();
    }, []);

    // Handle filter changes
    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilters(prev => ({ ...prev, [name]: value }));
    };

    // Apply filters
    const handleApplyFilters = async () => {
        try {
            setLoading(true);
            const queryParams = new URLSearchParams();
            
            Object.entries(filters).forEach(([key, value]) => {
                if (value) queryParams.append(key, value);
            });
            
            queryParams.append('therapist_id', therapistId);
            
            const response = await API.get(`/therapist/patients?${queryParams.toString()}`);
            setPatients(response.data.patients);
            setError('');
        } catch (err) {
            setError('Failed to apply filters: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    // Reset filters
    const handleResetFilters = async () => {
        setFilters({
            min_age: '',
            max_age: '',
            min_service_years: '',
            max_service_years: '',
            gender: '',
            rank: ''
        });
        
        try {
            const response = await API.get(`/therapist/patients?therapist_id=${therapistId}`);
            setPatients(response.data.patients);
        } catch (err) {
            setError('Failed to load patients: ' + err.message);
        }
    };

    // Load patient details
    const handleSelectPatient = async (patientId) => {
        try {
            setLoading(true);
            const response = await API.get(`/therapist/patients/${patientId}?therapist_id=${therapistId}`);
            setPatientDetails(response.data);
            setSelectedPatient(patientId);
            setActiveTab('patient-detail');
            setError('');
        } catch (err) {
            setError('Failed to load patient details: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    // Submit recommendation
    const handleSubmitRecommendation = async () => {
        try {
            if (!recommendationForm.scenario_id || !recommendationForm.suggested_coping_mechanism) {
                setError('Please select a scenario and coping mechanism');
                return;
            }
            
            setLoading(true);
            const payload = {
                scenario_id: parseInt(recommendationForm.scenario_id),
                suggested_coping_mechanism: recommendationForm.suggested_coping_mechanism,
                recommendation_text: recommendationForm.recommendation_text,
                person_id: selectedPatient
            };
            await API.post(
                `/therapist/recommend/${selectedPatient}?therapist_id=${therapistId}`,
                payload
            );
            
            // Reload patient details
            const response = await API.get(`/therapist/patients/${selectedPatient}?therapist_id=${therapistId}`);
            setPatientDetails(response.data);
            
            // Reset form
            setRecommendationForm({
                scenario_id: '',
                suggested_coping_mechanism: '',
                recommendation_text: ''
            });
            
            setError('');
            alert('Recommendation sent successfully!');
        } catch (err) {
            setError('Failed to submit recommendation: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    if (loading && !dashboardStats) {
        return <div className="therapist-dashboard loading">Loading therapist dashboard...</div>;
    }

    return (
        <div className="therapist-dashboard">
            <div className="dashboard-header">
                <h1>👨‍⚕️ Therapist Dashboard</h1>
                <p>Manage patients, monitor progress, and provide recommendations</p>
            </div>

            {error && <div className="error-banner">{error}</div>}

            {/* Navigation Tabs */}
            <div className="dashboard-tabs">
                <button
                    className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
                    onClick={() => setActiveTab('overview')}
                >
                    <BarChart3 size={20} /> Overview
                </button>
                <button
                    className={`tab-btn ${activeTab === 'patients' ? 'active' : ''}`}
                    onClick={() => setActiveTab('patients')}
                >
                    <Users size={20} /> My Patients
                </button>
                <button
                    className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`}
                    onClick={() => setActiveTab('analytics')}
                >
                    <TrendingUp size={20} /> Analytics
                </button>
            </div>

            {/* OVERVIEW TAB */}
            {activeTab === 'overview' && dashboardStats && (
                <div className="tab-content">
                    <div className="stats-grid">
                        <div className="stat-card">
                            <Users size={32} />
                            <div>
                                <h3>{dashboardStats.total_patients}</h3>
                                <p>Total Patients</p>
                            </div>
                        </div>

                        <div className="stat-card">
                            <Send size={32} />
                            <div>
                                <h3>{dashboardStats.total_recommendations}</h3>
                                <p>Recommendations Sent</p>
                            </div>
                        </div>

                        <div className="stat-card">
                            <CheckCircle size={32} />
                            <div>
                                <h3>{dashboardStats.accepted_recommendations}</h3>
                                <p>Accepted</p>
                            </div>
                        </div>

                        <div className="stat-card">
                            <Activity size={32} />
                            <div>
                                <h3>{dashboardStats.completed_simulations}</h3>
                                <p>Simulations Completed</p>
                            </div>
                        </div>
                    </div>

                    <div className="scores-section">
                        <h2>Patient Population Averages</h2>
                        <div className="score-metrics">
                            <div className="metric-bar">
                                <label>Avg Trauma Sensitivity</label>
                                <div className="progress-bar">
                                    <div
                                        className="progress-fill trauma"
                                        style={{ width: `${dashboardStats.average_trauma_sensitivity * 100}%` }}
                                    ></div>
                                </div>
                                <span>{dashboardStats.average_trauma_sensitivity.toFixed(2)}</span>
                            </div>

                            <div className="metric-bar">
                                <label>Avg Emotional Regulation</label>
                                <div className="progress-bar">
                                    <div
                                        className="progress-fill emotional"
                                        style={{ width: `${dashboardStats.average_emotional_regulation * 100}%` }}
                                    ></div>
                                </div>
                                <span>{dashboardStats.average_emotional_regulation.toFixed(2)}</span>
                            </div>

                            <div className="metric-bar">
                                <label>Avg Recovery Rate</label>
                                <div className="progress-bar">
                                    <div
                                        className="progress-fill recovery"
                                        style={{ width: `${dashboardStats.average_recovery_rate * 100}%` }}
                                    ></div>
                                </div>
                                <span>{dashboardStats.average_recovery_rate.toFixed(2)}</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* PATIENTS TAB */}
            {activeTab === 'patients' && (
                <div className="tab-content">
                    {/* Filters Section */}
                    <div className="filters-section">
                        <h2><Filter size={24} /> Advanced Filters</h2>
                        <div className="filter-grid">
                            <div className="filter-group">
                                <label>Min Age</label>
                                <input
                                    type="number"
                                    name="min_age"
                                    placeholder="e.g., 20"
                                    value={filters.min_age}
                                    onChange={handleFilterChange}
                                />
                            </div>

                            <div className="filter-group">
                                <label>Max Age</label>
                                <input
                                    type="number"
                                    name="max_age"
                                    placeholder="e.g., 50"
                                    value={filters.max_age}
                                    onChange={handleFilterChange}
                                />
                            </div>

                            <div className="filter-group">
                                <label>Min Service Years</label>
                                <input
                                    type="number"
                                    name="min_service_years"
                                    placeholder="e.g., 5"
                                    value={filters.min_service_years}
                                    onChange={handleFilterChange}
                                />
                            </div>

                            <div className="filter-group">
                                <label>Max Service Years</label>
                                <input
                                    type="number"
                                    name="max_service_years"
                                    placeholder="e.g., 20"
                                    value={filters.max_service_years}
                                    onChange={handleFilterChange}
                                />
                            </div>

                            <div className="filter-group">
                                <label>Gender</label>
                                <select name="gender" value={filters.gender} onChange={handleFilterChange}>
                                    <option value="">All</option>
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                </select>
                            </div>

                            <div className="filter-group">
                                <label>Rank</label>
                                <input
                                    type="text"
                                    name="rank"
                                    placeholder="e.g., Captain"
                                    value={filters.rank}
                                    onChange={handleFilterChange}
                                />
                            </div>
                        </div>

                        <div className="filter-buttons">
                            <button className="btn-primary" onClick={handleApplyFilters}>
                                Apply Filters
                            </button>
                            <button className="btn-secondary" onClick={handleResetFilters}>
                                Reset
                            </button>
                        </div>
                    </div>

                    {/* Patients List */}
                    <div className="patients-list-section">
                        <h2>My Patients ({patients.length})</h2>
                        <div className="patients-grid">
                            {patients.map(patient => (
                                <div key={patient.id} className="patient-card" onClick={() => handleSelectPatient(patient.id)}>
                                    <div className="patient-header">
                                        <h3>{patient.name}</h3>
                                        <span className="rank-badge">{patient.rank}</span>
                                    </div>

                                    <div className="patient-info">
                                        <div className="info-row">
                                            <span>Age:</span>
                                            <strong>{patient.age}</strong>
                                        </div>
                                        <div className="info-row">
                                            <span>Service:</span>
                                            <strong>{patient.service_years} yrs</strong>
                                        </div>
                                        <div className="info-row">
                                            <span>Gender:</span>
                                            <strong>{patient.gender}</strong>
                                        </div>
                                        <div className="info-row">
                                            <span>Assessments:</span>
                                            <strong>{patient.assessment_count}</strong>
                                        </div>
                                    </div>

                                    {patient.latest_trauma_sensitivity && (
                                        <div className="patient-scores">
                                            <div className="score-indicator">
                                                <span>Trauma</span>
                                                <div className="mini-bar" style={{
                                                    width: `${patient.latest_trauma_sensitivity * 100}%`
                                                }}></div>
                                            </div>
                                            <div className="score-indicator">
                                                <span>Recovery</span>
                                                <div className="mini-bar recovery" style={{
                                                    width: `${patient.latest_recovery_rate * 100}%`
                                                }}></div>
                                            </div>
                                        </div>
                                    )}

                                    <button className="btn-view">
                                        <Eye size={16} /> View Details
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* PATIENT DETAIL TAB */}
            {activeTab === 'patient-detail' && patientDetails && (
                <div className="tab-content patient-detail-view">
                    <div className="patient-detail-header">
                        <div className="back-btn" onClick={() => setActiveTab('patients')}>
                            ← Back to Patients
                        </div>
                        <h2>{patientDetails.name} - {patientDetails.rank}</h2>
                    </div>

                    <div className="detail-grid">
                        {/* Left Column - Patient Info */}
                        <div className="detail-section">
                            <h3>Patient Information</h3>
                            <div className="info-block">
                                <div className="info-item">
                                    <span>Age</span>
                                    <strong>{patientDetails.age}</strong>
                                </div>
                                <div className="info-item">
                                    <span>Service Years</span>
                                    <strong>{patientDetails.service_years}</strong>
                                </div>
                                <div className="info-item">
                                    <span>Gender</span>
                                    <strong>{patientDetails.gender}</strong>
                                </div>
                                <div className="info-item">
                                    <span>Total Assessments</span>
                                    <strong>{patientDetails.assessment_count}</strong>
                                </div>
                            </div>

                            {patientDetails.last_assessment_date && (
                                <>
                                    <h3 style={{ marginTop: '2rem' }}>Latest Assessment</h3>
                                    <div className="assessment-block">
                                        <div className="assessment-score">
                                            <span>Trauma Sensitivity</span>
                                            <div className="score-value" style={{ color: '#FF6B6B' }}>
                                                {patientDetails.latest_trauma_sensitivity?.toFixed(2)}
                                            </div>
                                        </div>
                                        <div className="assessment-score">
                                            <span>Emotional Regulation</span>
                                            <div className="score-value" style={{ color: '#4ECDC4' }}>
                                                {patientDetails.latest_emotional_regulation?.toFixed(2)}
                                            </div>
                                        </div>
                                        <div className="assessment-score">
                                            <span>Recovery Rate</span>
                                            <div className="score-value" style={{ color: '#95E1D3' }}>
                                                {patientDetails.latest_recovery_rate?.toFixed(2)}
                                            </div>
                                        </div>
                                        <div className="assessment-score">
                                            <span>Impulsivity</span>
                                            <div className="score-value" style={{ color: '#F38181' }}>
                                                {patientDetails.latest_impulsivity?.toFixed(2)}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="info-item" style={{ marginTop: '1rem' }}>
                                        <span>Coping Mechanism</span>
                                        <strong>{patientDetails.latest_coping_mechanism}</strong>
                                    </div>
                                </>
                            )}
                        </div>

                        {/* Right Column - Recommendations */}
                        <div className="detail-section">
                            <h3>Send Recommendation</h3>
                            <div className="recommendation-form">
                                <div className="form-group">
                                    <label>Select Scenario</label>
                                    <select
                                        value={recommendationForm.scenario_id}
                                        onChange={(e) => setRecommendationForm({
                                            ...recommendationForm,
                                            scenario_id: parseInt(e.target.value)
                                        })}
                                    >
                                        <option value="">Choose a scenario...</option>
                                        {scenarios.map(scenario => (
                                            <option key={scenario.id} value={scenario.id}>
                                                {scenario.scenario_type} - {scenario.environment}
                                            </option>
                                        ))}
                                    </select>
                                </div>

                                <div className="form-group">
                                    <label>Recommended Coping Mechanism</label>
                                    <select
                                        value={recommendationForm.suggested_coping_mechanism}
                                        onChange={(e) => setRecommendationForm({
                                            ...recommendationForm,
                                            suggested_coping_mechanism: e.target.value
                                        })}
                                    >
                                        <option value="">Choose mechanism...</option>
                                        <option value="avoidance">Avoidance</option>
                                        <option value="freezing">Freezing</option>
                                        <option value="approach">Approach</option>
                                        <option value="suppression">Suppression</option>
                                    </select>
                                </div>

                                <div className="form-group">
                                    <label>Notes (Optional)</label>
                                    <textarea
                                        placeholder="Why you're recommending this scenario..."
                                        value={recommendationForm.recommendation_text}
                                        onChange={(e) => setRecommendationForm({
                                            ...recommendationForm,
                                            recommendation_text: e.target.value
                                        })}
                                    ></textarea>
                                </div>

                                <button className="btn-primary full-width" onClick={handleSubmitRecommendation}>
                                    <Plus size={18} /> Send Recommendation
                                </button>
                            </div>

                            {/* Recent Recommendations */}
                            {patientDetails.recommendations.length > 0 && (
                                <>
                                    <h3 style={{ marginTop: '2rem' }}>Recommendation History</h3>
                                    <div className="recommendations-list">
                                        {patientDetails.recommendations.slice(0, 5).map(rec => (
                                            <div key={rec.id} className="recommendation-item">
                                                <div className="rec-header">
                                                    <strong>{rec.status.toUpperCase()}</strong>
                                                    <span className={`status-badge ${rec.status}`}>{rec.status}</span>
                                                </div>
                                                <p>{rec.recommendation_text}</p>
                                                <small>
                                                    {new Date(rec.created_date).toLocaleDateString()}
                                                </small>
                                            </div>
                                        ))}
                                    </div>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* ANALYTICS TAB */}
            {activeTab === 'analytics' && (
                <div className="tab-content">
                    <h2>Patient Analytics & Trends</h2>
                    
                    {dashboardStats && (
                        <>
                            {/* Overview Stats */}
                            <div style={{ 
                                display: 'grid', 
                                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
                                gap: '1.5rem',
                                marginTop: '2rem',
                                marginBottom: '2rem'
                            }}>
                                <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
                                    <Users size={32} style={{ color: 'var(--primary)', marginBottom: '0.5rem' }} />
                                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--primary)' }}>
                                        {dashboardStats.total_patients}
                                    </div>
                                    <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Total Patients</div>
                                </div>
                                
                                <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
                                    <BarChart3 size={32} style={{ color: '#10b981', marginBottom: '0.5rem' }} />
                                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#10b981' }}>
                                        {dashboardStats.total_recommendations}
                                    </div>
                                    <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Total Recommendations</div>
                                </div>
                                
                                <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
                                    <CheckCircle size={32} style={{ color: '#f59e0b', marginBottom: '0.5rem' }} />
                                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#f59e0b' }}>
                                        {dashboardStats.accepted_recommendations}
                                    </div>
                                    <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Accepted Recommendations</div>
                                </div>
                                
                                <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
                                    <Activity size={32} style={{ color: '#8b5cf6', marginBottom: '0.5rem' }} />
                                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#8b5cf6' }}>
                                        {dashboardStats.completed_simulations}
                                    </div>
                                    <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Completed Simulations</div>
                                </div>
                            </div>

                            {/* Average Assessment Scores */}
                            <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem' }}>
                                <h3 style={{ marginBottom: '1.5rem' }}>Average Patient Assessment Scores</h3>
                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
                                    <div>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                            <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Trauma Sensitivity</span>
                                            <strong style={{ color: '#ef4444' }}>{(dashboardStats.average_trauma_sensitivity || 0).toFixed(2)}</strong>
                                        </div>
                                        <div style={{ 
                                            height: '8px', 
                                            background: 'rgba(239, 68, 68, 0.2)', 
                                            borderRadius: '4px',
                                            overflow: 'hidden'
                                        }}>
                                            <div style={{ 
                                                width: `${(dashboardStats.average_trauma_sensitivity || 0) * 100}%`, 
                                                height: '100%', 
                                                background: '#ef4444',
                                                transition: 'width 0.3s ease'
                                            }}></div>
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                            <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Emotional Regulation</span>
                                            <strong style={{ color: '#3b82f6' }}>{(dashboardStats.average_emotional_regulation || 0).toFixed(2)}</strong>
                                        </div>
                                        <div style={{ 
                                            height: '8px', 
                                            background: 'rgba(59, 130, 246, 0.2)', 
                                            borderRadius: '4px',
                                            overflow: 'hidden'
                                        }}>
                                            <div style={{ 
                                                width: `${(dashboardStats.average_emotional_regulation || 0) * 100}%`, 
                                                height: '100%', 
                                                background: '#3b82f6',
                                                transition: 'width 0.3s ease'
                                            }}></div>
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                            <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Recovery Rate</span>
                                            <strong style={{ color: '#10b981' }}>{(dashboardStats.average_recovery_rate || 0).toFixed(2)}</strong>
                                        </div>
                                        <div style={{ 
                                            height: '8px', 
                                            background: 'rgba(16, 185, 129, 0.2)', 
                                            borderRadius: '4px',
                                            overflow: 'hidden'
                                        }}>
                                            <div style={{ 
                                                width: `${(dashboardStats.average_recovery_rate || 0) * 100}%`, 
                                                height: '100%', 
                                                background: '#10b981',
                                                transition: 'width 0.3s ease'
                                            }}></div>
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                            <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Impulsivity</span>
                                            <strong style={{ color: '#f59e0b' }}>{(dashboardStats.average_impulsivity || 0).toFixed(2)}</strong>
                                        </div>
                                        <div style={{ 
                                            height: '8px', 
                                            background: 'rgba(245, 158, 11, 0.2)', 
                                            borderRadius: '4px',
                                            overflow: 'hidden'
                                        }}>
                                            <div style={{ 
                                                width: `${(dashboardStats.average_impulsivity || 0) * 100}%`, 
                                                height: '100%', 
                                                background: '#f59e0b',
                                                transition: 'width 0.3s ease'
                                            }}></div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Recommendation Effectiveness */}
                            <div className="glass-panel" style={{ padding: '2rem' }}>
                                <h3 style={{ marginBottom: '1rem' }}>Recommendation Effectiveness</h3>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
                                    <div style={{ flex: 1 }}>
                                        <div style={{ marginBottom: '1rem' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                                <span>Acceptance Rate</span>
                                                <strong style={{ color: '#10b981' }}>
                                                    {dashboardStats.total_recommendations > 0 
                                                        ? ((dashboardStats.accepted_recommendations / dashboardStats.total_recommendations) * 100).toFixed(1)
                                                        : 0}%
                                                </strong>
                                            </div>
                                            <div style={{ 
                                                height: '12px', 
                                                background: 'rgba(16, 185, 129, 0.2)', 
                                                borderRadius: '6px',
                                                overflow: 'hidden'
                                            }}>
                                                <div style={{ 
                                                    width: `${dashboardStats.total_recommendations > 0 ? (dashboardStats.accepted_recommendations / dashboardStats.total_recommendations) * 100 : 0}%`, 
                                                    height: '100%', 
                                                    background: '#10b981',
                                                    transition: 'width 0.3s ease'
                                                }}></div>
                                            </div>
                                        </div>
                                        
                                        <div>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                                <span>Completion Rate</span>
                                                <strong style={{ color: '#8b5cf6' }}>
                                                    {dashboardStats.total_recommendations > 0 
                                                        ? ((dashboardStats.completed_simulations / dashboardStats.total_recommendations) * 100).toFixed(1)
                                                        : 0}%
                                                </strong>
                                            </div>
                                            <div style={{ 
                                                height: '12px', 
                                                background: 'rgba(139, 92, 246, 0.2)', 
                                                borderRadius: '6px',
                                                overflow: 'hidden'
                                            }}>
                                                <div style={{ 
                                                    width: `${dashboardStats.total_recommendations > 0 ? (dashboardStats.completed_simulations / dashboardStats.total_recommendations) * 100 : 0}%`, 
                                                    height: '100%', 
                                                    background: '#8b5cf6',
                                                    transition: 'width 0.3s ease'
                                                }}></div>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div style={{ 
                                        textAlign: 'center',
                                        padding: '1.5rem',
                                        background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)',
                                        borderRadius: '8px',
                                        minWidth: '150px'
                                    }}>
                                        <TrendingUp size={40} style={{ color: 'var(--primary)', marginBottom: '0.5rem' }} />
                                        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                            {dashboardStats.accepted_recommendations} of {dashboardStats.total_recommendations}
                                        </div>
                                        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>recommendations followed</div>
                                    </div>
                                </div>
                            </div>
                        </>
                    )}
                </div>
            )}
        </div>
    );
};

export default TherapistDashboard;
