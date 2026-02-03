import React, { useEffect, useState } from 'react';
import api from '../api';
import { useAuth } from '../context/AuthContext';
import { Line, Radar, Bar, Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, registerables } from 'chart.js';

ChartJS.register(...registerables);

const Analytics = () => {
    const { user } = useAuth();
    const [analyticsData, setAnalyticsData] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchPersonAnalytics = async () => {
            // Therapists can't view their own analytics, only patients
            if (user?.user?.role === 'therapist') {
                setError('Therapists can view patient analytics from the Therapist Dashboard. Patient-specific analytics are displayed there.');
                setLoading(false);
                return;
            }

            if (!user?.person?.id) {
                setError('Unable to load analytics: User profile not found. Please login again.');
                setLoading(false);
                return;
            }

            try {
                const response = await api.get(`/analytics/person/${user.person.id}`);
                setAnalyticsData(response.data);
            } catch (err) {
                console.error('Failed to fetch analytics', err);
                setError('Failed to load analytics data for this soldier.');
            } finally {
                setLoading(false);
            }
        };
        fetchPersonAnalytics();
    }, [user]);

    if (loading) {
        return (
            <div style={{ padding: '2rem', textAlign: 'center' }}>
                <p>Loading analytics...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div style={{ padding: '2rem' }}>
                <div style={{
                    padding: '1rem',
                    background: 'rgba(239, 68, 68, 0.1)',
                    border: '1px solid rgba(239, 68, 68, 0.3)',
                    borderRadius: '8px',
                    color: '#f87171'
                }}>
                    {error}
                </div>
            </div>
        );
    }

    if (!analyticsData) {
        return (
            <div style={{ padding: '2rem' }}>
                <p>No analytics data available. Complete an assessment and simulation to view your analytics.</p>
            </div>
        );
    }

    const { person_name, current_profile, assessments, reports } = analyticsData;
    const formatScore = (value) => (typeof value === 'number' ? value.toFixed(2) : 'N/A');

    // Chart 1: Profile Radar Chart (Current Assessment)
    const radarData = {
        labels: ['Trauma Sensitivity', 'Emotional Regulation', 'Recovery Rate', 'Impulsivity'],
        datasets: [{
            label: 'Your PTSD Profile',
            data: [
                current_profile?.trauma_sensitivity || 0,
                current_profile?.emotional_regulation || 0,
                current_profile?.recovery_rate || 0,
                current_profile?.impulsivity || 0
            ],
            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            borderColor: 'rgba(59, 130, 246, 1)',
            borderWidth: 2,
            pointBackgroundColor: 'rgba(59, 130, 246, 1)',
            pointBorderColor: '#fff',
            pointBorderWidth: 2
        }]
    };

    // Chart 2: Assessment Progression (Line Chart)
    const assessmentDates = Array.isArray(assessments)
        ? assessments.map(a => new Date(a.created_at || a.assessment_date || Date.now()).toLocaleDateString())
        : [];
    const traumaData = Array.isArray(assessments) ? assessments.map(a => a.trauma_sensitivity ?? 0) : [];
    const emotionalData = Array.isArray(assessments) ? assessments.map(a => a.emotional_regulation ?? 0) : [];
    const recoveryData = Array.isArray(assessments) ? assessments.map(a => a.recovery_rate ?? 0) : [];
    const impulsivityData = Array.isArray(assessments) ? assessments.map(a => a.impulsivity ?? 0) : [];

    const lineChartData = {
        labels: assessmentDates,
        datasets: [
            {
                label: 'Trauma Sensitivity',
                data: traumaData,
                borderColor: 'rgb(239, 68, 68)',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                tension: 0.3
            },
            {
                label: 'Emotional Regulation',
                data: emotionalData,
                borderColor: 'rgb(34, 197, 94)',
                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                tension: 0.3
            },
            {
                label: 'Recovery Rate',
                data: recoveryData,
                borderColor: 'rgb(59, 130, 246)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.3
            },
            {
                label: 'Impulsivity',
                data: impulsivityData,
                borderColor: 'rgb(251, 146, 60)',
                backgroundColor: 'rgba(251, 146, 60, 0.1)',
                tension: 0.3
            }
        ]
    };

    // Chart 3: Latest PTSD Symptom Scores (Bar Chart)
    const latestReport = reports && reports.length ? reports[reports.length - 1] : null;
    const ptsdSymptoms = {
        labels: ['Avoidance', 'Re-Experiencing', 'Negative Alterations', 'Hyperarousal'],
        datasets: [{
            label: 'PTSD Symptom Severity',
            data: [
                latestReport?.avoidance_score || 0,
                latestReport?.re_experiencing_score || 0,
                latestReport?.negative_alterations_score || 0,
                latestReport?.hyperarousal_score || 0
            ],
            backgroundColor: [
                'rgba(239, 68, 68, 0.7)',
                'rgba(251, 146, 60, 0.7)',
                'rgba(234, 179, 8, 0.7)',
                'rgba(168, 85, 247, 0.7)'
            ],
            borderColor: [
                'rgb(239, 68, 68)',
                'rgb(251, 146, 60)',
                'rgb(234, 179, 8)',
                'rgb(168, 85, 247)'
            ],
            borderWidth: 2
        }]
    };

    // Chart 4: Assessment Status Distribution (Doughnut)
    const assessmentCount = Array.isArray(assessments) ? assessments.length : 0;
    const reportCount = Array.isArray(reports) ? reports.length : 0;
    const simulationCount = Array.isArray(reports) ? reports.length : 0; // Each report is from a simulation

    const statusData = {
        labels: [`Assessments (${assessmentCount})`, `Simulations (${simulationCount})`],
        datasets: [{
            data: [assessmentCount, simulationCount],
            backgroundColor: [
                'rgba(59, 130, 246, 0.7)',
                'rgba(34, 197, 94, 0.7)'
            ],
            borderColor: [
                'rgb(59, 130, 246)',
                'rgb(34, 197, 94)'
            ],
            borderWidth: 2
        }]
    };

    const radarOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#9ca3af',
                    usePointStyle: true,
                    padding: 15
                }
            }
        },
        scales: {
            r: {
                beginAtZero: true,
                max: 1,
                min: 0,
                ticks: { 
                    color: '#9ca3af',
                    stepSize: 0.2
                },
                grid: { color: 'rgba(156, 163, 175, 0.1)' },
                pointLabels: {
                    color: '#9ca3af',
                    font: {
                        size: 12
                    }
                }
            }
        }
    };

    const lineOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#9ca3af',
                    usePointStyle: true,
                    padding: 15
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 1,
                ticks: { color: '#9ca3af' },
                grid: { color: 'rgba(156, 163, 175, 0.1)' }
            },
            x: {
                ticks: { color: '#9ca3af' },
                grid: { color: 'rgba(156, 163, 175, 0.1)' }
            }
        }
    };

    const barOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#9ca3af',
                    usePointStyle: true,
                    padding: 15
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 1,
                ticks: { color: '#9ca3af' },
                grid: { color: 'rgba(156, 163, 175, 0.1)' }
            },
            x: {
                ticks: { color: '#9ca3af' },
                grid: { color: 'rgba(156, 163, 175, 0.1)' }
            }
        }
    };

    const doughnutOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#9ca3af',
                    usePointStyle: true,
                    padding: 15
                }
            }
        }
    };

    return (
        <div style={{ padding: '2rem' }}>
            <h1>Your PTSD Analysis Dashboard</h1>
            <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
                Comprehensive psychological profile analysis for <strong>{person_name}</strong>
            </p>

            {/* Key Metrics */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '1.5rem',
                marginBottom: '2rem'
            }}>
                <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'rgb(59, 130, 246)' }}>
                        {assessmentCount}
                    </div>
                    <div style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                        Assessments Completed
                    </div>
                </div>
                <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'rgb(34, 197, 94)' }}>
                        {simulationCount}
                    </div>
                    <div style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                        Simulations Run
                    </div>
                </div>
                <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'rgb(251, 146, 60)' }}>
                        {(current_profile?.trauma_sensitivity || 0).toFixed(2)}
                    </div>
                    <div style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                        Trauma Sensitivity
                    </div>
                </div>
            </div>

            {/* Charts Grid */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))',
                gap: '2rem',
                marginBottom: '2rem'
            }}>
                {/* Radar Chart */}
                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <h3 style={{ marginTop: 0, marginBottom: '1.5rem' }}>
                        Current Psychological Profile
                    </h3>
                    <div style={{ position: 'relative', height: '300px' }}>
                        <Radar data={radarData} options={radarOptions} />
                    </div>
                    <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '1rem' }}>
                        <strong>What this shows:</strong> Your scores across 4 key psychological dimensions. 
                        Higher scores indicate greater psychological distress in each area.
                    </p>
                </div>

                {/* Doughnut Chart */}
                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <h3 style={{ marginTop: 0, marginBottom: '1.5rem' }}>
                        Assessment & Simulation Activity
                    </h3>
                    <div style={{ position: 'relative', height: '300px' }}>
                        <Doughnut data={statusData} options={doughnutOptions} />
                    </div>
                    <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '1rem' }}>
                        <strong>What this shows:</strong> Your engagement with the PTSD simulation program.
                        Track your progress through assessments and simulations.
                    </p>
                </div>
            </div>

            {/* Line Chart - Assessment Progression */}
            {assessments?.length > 1 && (
                <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '2rem' }}>
                    <h3 style={{ marginTop: 0, marginBottom: '1.5rem' }}>
                        Psychological Profile Progression Over Time
                    </h3>
                    <div style={{ position: 'relative', height: '350px' }}>
                        <Line data={lineChartData} options={lineOptions} />
                    </div>
                    <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '1rem' }}>
                        <strong>What this shows:</strong> How your psychological dimensions have changed 
                        across your assessments. Upward trends indicate improvement, downward trends 
                        indicate increased distress.
                    </p>
                </div>
            )}

            {/* Bar Chart - Latest PTSD Symptoms */}
            {latestReport && (
                <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '2rem' }}>
                    <h3 style={{ marginTop: 0, marginBottom: '1.5rem' }}>
                        Latest PTSD Symptom Severity (From Most Recent Simulation)
                    </h3>
                    <div style={{ position: 'relative', height: '350px' }}>
                        <Bar data={ptsdSymptoms} options={barOptions} />
                    </div>
                    <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '1rem' }}>
                        <strong>What this shows:</strong> PTSD symptom severity breakdown from your latest simulation:
                        <br/>• <strong>Avoidance:</strong> Avoiding trauma-related stimuli
                        <br/>• <strong>Re-Experiencing:</strong> Intrusive trauma memories/flashbacks
                        <br/>• <strong>Negative Alterations:</strong> Persistent negative emotions and beliefs
                        <br/>• <strong>Hyperarousal:</strong> Increased startle response and hypervigilance
                    </p>
                </div>
            )}

            {/* Detailed Assessment History */}
            <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <h3 style={{ marginTop: 0, marginBottom: '1.5rem' }}>
                    Assessment History
                </h3>
                {assessments && assessments.length > 0 ? (
                    <div style={{ overflowX: 'auto' }}>
                        <table style={{
                            width: '100%',
                            borderCollapse: 'collapse',
                            color: '#d1d5db'
                        }}>
                            <thead>
                                <tr style={{ borderBottom: '1px solid rgba(156, 163, 175, 0.3)' }}>
                                    <th style={{ padding: '0.75rem', textAlign: 'left', color: '#9ca3af' }}>Date</th>
                                    <th style={{ padding: '0.75rem', textAlign: 'center', color: '#9ca3af' }}>Trauma</th>
                                    <th style={{ padding: '0.75rem', textAlign: 'center', color: '#9ca3af' }}>Emotion</th>
                                    <th style={{ padding: '0.75rem', textAlign: 'center', color: '#9ca3af' }}>Recovery</th>
                                    <th style={{ padding: '0.75rem', textAlign: 'center', color: '#9ca3af' }}>Impulsivity</th>
                                    <th style={{ padding: '0.75rem', textAlign: 'left', color: '#9ca3af' }}>Coping</th>
                                </tr>
                            </thead>
                            <tbody>
                                {assessments.map((assessment, idx) => (
                                    <tr key={idx} style={{ borderBottom: '1px solid rgba(156, 163, 175, 0.2)' }}>
                                        <td style={{ padding: '0.75rem' }}>
                                            {new Date(assessment.created_at).toLocaleDateString()}
                                        </td>
                                        <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                                            {formatScore(assessment.trauma_sensitivity)}
                                        </td>
                                        <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                                            {formatScore(assessment.emotional_regulation)}
                                        </td>
                                        <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                                            {formatScore(assessment.recovery_rate)}
                                        </td>
                                        <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                                            {formatScore(assessment.impulsivity)}
                                        </td>
                                        <td style={{ padding: '0.75rem' }}>
                                            {assessment.coping_mechanism || 'N/A'}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <p style={{ color: 'var(--text-muted)' }}>No assessments yet. Complete your first assessment to see data here.</p>
                )}
            </div>
        </div>
    );
};

export default Analytics;
