import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { AlertCircle, Lightbulb, CheckCircle } from 'lucide-react';
import api from '../api';

const likertOptions = [
    { value: '1', label: 'Strongly Disagree' },
    { value: '2', label: 'Disagree' },
    { value: '3', label: 'Neutral' },
    { value: '4', label: 'Agree' },
    { value: '5', label: 'Strongly Agree' }
];

const Questionnaire = () => {
    const navigate = useNavigate();
    const { user } = useAuth();
    const [questions, setQuestions] = useState([]);
    const [responses, setResponses] = useState({});
    const [therapists, setTherapists] = useState([]);
    const [selectedTherapist, setSelectedTherapist] = useState('');
    const [copingMechanism, setCopingMechanism] = useState('avoidance');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [therapistRecommendations, setTherapistRecommendations] = useState([]);
    const [showRecommendations, setShowRecommendations] = useState(false);
    const [scenarios, setScenarios] = useState([]);
    const [selectedRecommendationId, setSelectedRecommendationId] = useState(null);
    const [recommendedScenarioId, setRecommendedScenarioId] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [questionsRes, therapistsRes, scenariosRes] = await Promise.all([
                    api.get('/questionnaires/'),
                    api.get('/therapists/'),
                    api.get('/scenarios/')
                ]);
                setQuestions(questionsRes.data || []);
                setTherapists(therapistsRes.data || []);
                setScenarios(scenariosRes.data || []);
                
                // Auto-set therapist if soldier already has one assigned
                if (user?.person?.therapist_id) {
                    setSelectedTherapist(user.person.therapist_id.toString());
                }
                
                // Load therapist recommendations if user has a therapist assigned
                if ((user?.person_id || user?.person?.id) && user?.person?.therapist_id) {
                    const personId = user?.person_id || user?.person?.id;
                    const therapistId = user?.person?.therapist_id;
                    try {
                        const recsRes = await api.get(
                            `/therapist/recommendations/${personId}?therapist_id=${therapistId}&status=pending`
                        );
                        if (recsRes.data && recsRes.data.length > 0) {
                            setTherapistRecommendations(recsRes.data);
                            setShowRecommendations(true);
                        }
                    } catch (err) {
                        // Recommendations not available, continue without them
                        console.log('No recommendations available');
                    }
                }
            } catch (err) {
                console.error('Failed to fetch questionnaire data', err);
                setError('Failed to load questions. Please try again.');
            }
        };
        fetchData();
    }, [user]);

    const handleResponseChange = (questionId, value) => {
        setResponses(prev => ({ ...prev, [questionId]: value }));
    };

    const applyRecommendation = (recommendation) => {
        setSelectedTherapist(recommendation.therapist_id);
        setCopingMechanism(recommendation.suggested_coping_mechanism);
        setSelectedRecommendationId(recommendation.id);
        setRecommendedScenarioId(recommendation.scenario_id);
        setShowRecommendations(false);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!user?.person?.id && !user?.person_id && !user?.person) {
            setError('No soldier profile linked to this account.');
            return;
        }

        if (!selectedTherapist) {
            setError('Please select a therapist.');
            return;
        }

        const unanswered = questions.filter(q => !responses[q.id]);
        if (unanswered.length > 0) {
            setError('Please answer all questions before submitting.');
            return;
        }

        setLoading(true);

        try {
            const personId = user?.person?.id || user?.person_id || user?.person?.id;
            const responsePayload = {
                person_id: personId,
                therapist_id: parseInt(selectedTherapist, 10),
                coping_mechanism: copingMechanism,
                responses: questions.map(q => ({
                    questionnaire_id: q.id,
                    answer_value: responses[q.id],
                    response_time_seconds: null
                }))
            };

            const res = await api.post('/assessments/', responsePayload);
            const assessment = res.data;

            // If there was a selected recommendation, update its status
            if (selectedRecommendationId) {
                try {
                    await api.put(
                        `/therapist/recommendations/${selectedRecommendationId}/status`,
                        null,
                        { params: { new_status: 'accepted' } }
                    );
                } catch (err) {
                    console.log('Could not update recommendation status');
                }
            }

            const query = new URLSearchParams({
                assessment_id: assessment.id,
                person_id: assessment.person_id
            });
            if (recommendedScenarioId) query.set('scenario_id', recommendedScenarioId);
            if (selectedRecommendationId) query.set('recommendation_id', selectedRecommendationId);

            navigate(`/simulation?${query.toString()}`);
        } catch (err) {
            console.error('Failed to submit assessment', err);
            setError('Failed to submit assessment. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '2rem', maxWidth: '900px', margin: '0 auto' }}>
            <div style={{ marginBottom: '2rem' }}>
                <h1>Psychological Assessment</h1>
                <p style={{ color: 'var(--text-muted)' }}>
                    Answer the questions below to generate your trauma profile. This will be used for simulation.
                </p>
            </div>

            {/* Therapist Recommendations Banner */}
            {showRecommendations && therapistRecommendations.length > 0 && (
                <div style={{
                    padding: '1.5rem',
                    marginBottom: '1.5rem',
                    background: 'linear-gradient(135deg, #fef3c7, #fde68a)',
                    border: '2px solid #f59e0b',
                    borderRadius: '8px',
                    borderLeft: '4px solid #f59e0b'
                }}>
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
                        <Lightbulb size={24} style={{ color: '#d97706', flexShrink: 0, marginTop: '0.25rem' }} />
                        <div style={{ flex: 1 }}>
                            <h3 style={{ margin: '0 0 1rem 0', color: '#92400e' }}>
                                👨‍⚕️ Therapist Recommendations
                            </h3>
                            <p style={{ margin: '0 0 1rem 0', color: '#b45309', fontSize: '0.95rem' }}>
                                Your therapist has recommended specific scenarios and coping strategies for your next session:
                            </p>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                                {therapistRecommendations.slice(0, 3).map((rec, idx) => (
                                    <div key={idx} style={{
                                        background: 'white',
                                        padding: '1rem',
                                        borderRadius: '6px',
                                        borderLeft: '3px solid #f59e0b'
                                    }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                                            <div style={{ flex: 1 }}>
                                                <strong style={{ color: '#2d3748' }}>
                                                    Coping Mechanism: <span style={{ color: '#f59e0b' }}>
                                                        {rec.suggested_coping_mechanism.charAt(0).toUpperCase() + rec.suggested_coping_mechanism.slice(1)}
                                                    </span>
                                                </strong>
                                                {rec.scenario_id && (
                                                    <p style={{ margin: '0.35rem 0 0 0', color: '#4a5568', fontSize: '0.9rem' }}>
                                                        Scenario: {scenarios.find(s => s.id === rec.scenario_id)?.scenario_type || 'Assigned scenario'}
                                                    </p>
                                                )}
                                                {rec.recommendation_text && (
                                                    <p style={{ margin: '0.5rem 0 0 0', color: '#4a5568', fontSize: '0.9rem' }}>
                                                        {rec.recommendation_text}
                                                    </p>
                                                )}
                                                <small style={{ color: '#718096' }}>
                                                    Recommended: {new Date(rec.created_date).toLocaleDateString()}
                                                </small>
                                            </div>
                                            <button
                                                onClick={() => applyRecommendation(rec)}
                                                style={{
                                                    padding: '0.5rem 1rem',
                                                    background: '#f59e0b',
                                                    color: 'white',
                                                    border: 'none',
                                                    borderRadius: '6px',
                                                    cursor: 'pointer',
                                                    fontWeight: '600',
                                                    fontSize: '0.85rem',
                                                    transition: 'all 0.3s ease'
                                                }}
                                                onMouseEnter={(e) => e.currentTarget.style.background = '#d97706'}
                                                onMouseLeave={(e) => e.currentTarget.style.background = '#f59e0b'}
                                            >
                                                ✓ Follow Suggestion
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <p style={{ margin: '1rem 0 0 0', fontSize: '0.85rem', color: '#b45309' }}>
                                You can follow your therapist's suggestion or choose your own coping strategy below.
                            </p>
                        </div>
                    </div>
                </div>
            )}

            {error && (
                <div style={{
                    padding: '1rem',
                    marginBottom: '1.5rem',
                    background: 'rgba(239, 68, 68, 0.1)',
                    border: '1px solid rgba(239, 68, 68, 0.3)',
                    borderRadius: '8px',
                    color: '#f87171'
                }}>
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit}>
                {/* Only show therapist dropdown if soldier doesn't have one assigned */}
                {!user?.person?.therapist_id && (
                    <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                            Select Therapist
                        </label>
                        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '0.75rem' }}>
                            Choose a therapist who will oversee your assessments and provide guidance.
                        </p>
                        <select
                            value={selectedTherapist}
                            onChange={(e) => setSelectedTherapist(e.target.value)}
                            style={{ width: '100%', padding: '0.75rem', borderRadius: '8px' }}
                        >
                            <option value="">Choose a therapist</option>
                            {therapists.map(t => (
                                <option key={t.id} value={t.id}>{t.name} - {t.specialization}</option>
                            ))}
                        </select>
                    </div>
                )}

                {/* Show assigned therapist info if they have one */}
                {user?.person?.therapist_id && (
                    <div className="glass-panel" style={{ 
                        padding: '1.5rem', 
                        marginBottom: '1.5rem',
                        background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%)',
                        border: '1px solid rgba(16, 185, 129, 0.3)'
                    }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                            <CheckCircle size={20} style={{ color: '#10b981' }} />
                            <div>
                                <label style={{ display: 'block', fontWeight: '600', color: '#10b981' }}>
                                    Your Assigned Therapist
                                </label>
                                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', margin: '0.25rem 0 0 0' }}>
                                    {therapists.find(t => t.id === user.person.therapist_id)?.name || 'Loading...'} - 
                                    {therapists.find(t => t.id === user.person.therapist_id)?.specialization || ''}
                                </p>
                            </div>
                        </div>
                    </div>
                )}

                <div className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                        Coping Mechanism
                        {therapistRecommendations.some(r => r.suggested_coping_mechanism === copingMechanism) && (
                            <span style={{ color: '#10b981', marginLeft: '0.5rem', fontSize: '0.85rem' }}>
                                ✓ (Therapist Recommended)
                            </span>
                        )}
                    </label>
                    <select
                        value={copingMechanism}
                        onChange={(e) => setCopingMechanism(e.target.value)}
                        style={{ width: '100%', padding: '0.75rem', borderRadius: '8px' }}
                    >
                        <option value="avoidance">Avoidance (Run away)</option>
                        <option value="approach">Approach (Face threat)</option>
                        <option value="freezing">Freezing (Paralyzed)</option>
                        <option value="suppression">Suppression (Ignore it)</option>
                    </select>
                </div>

                {questions.map((q, index) => (
                    <div key={q.id} className="glass-panel" style={{ padding: '1.5rem', marginBottom: '1.25rem' }}>
                        <div style={{ marginBottom: '1rem' }}>
                            <strong>Q{index + 1}.</strong> {q.question_text}
                            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
                                Dimension: {q.dimension.replace('_', ' ')}
                            </div>
                        </div>

                        <div style={{ 
                            display: 'flex', 
                            gap: '0.5rem', 
                            flexWrap: 'wrap',
                            justifyContent: 'space-between'
                        }}>
                            {likertOptions.map(opt => (
                                <label 
                                    key={opt.value} 
                                    style={{ 
                                        flex: '1 1 auto',
                                        minWidth: '140px',
                                        padding: '0.75rem 1rem',
                                        borderRadius: '8px',
                                        border: responses[q.id] === opt.value 
                                            ? '2px solid var(--primary-color, #3b82f6)' 
                                            : '2px solid rgba(255, 255, 255, 0.1)',
                                        background: responses[q.id] === opt.value 
                                            ? 'rgba(59, 130, 246, 0.15)' 
                                            : 'rgba(255, 255, 255, 0.05)',
                                        cursor: 'pointer',
                                        textAlign: 'center',
                                        transition: 'all 0.2s ease',
                                        fontWeight: responses[q.id] === opt.value ? '600' : '400'
                                    }}
                                    onMouseEnter={(e) => {
                                        if (responses[q.id] !== opt.value) {
                                            e.currentTarget.style.background = 'rgba(255, 255, 255, 0.08)';
                                            e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.2)';
                                        }
                                    }}
                                    onMouseLeave={(e) => {
                                        if (responses[q.id] !== opt.value) {
                                            e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)';
                                            e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                                        }
                                    }}
                                >
                                    <input
                                        type="radio"
                                        name={`q-${q.id}`}
                                        value={opt.value}
                                        checked={responses[q.id] === opt.value}
                                        onChange={(e) => handleResponseChange(q.id, e.target.value)}
                                        style={{ display: 'none' }}
                                    />
                                    <span style={{ fontSize: '0.9rem' }}>{opt.label}</span>
                                </label>
                            ))}
                        </div>
                    </div>
                ))}

                <button className="btn" type="submit" disabled={loading} style={{ width: '100%', padding: '1rem' }}>
                    {loading ? 'Submitting Assessment...' : 'Submit Assessment & Start Simulation'}
                </button>
            </form>
        </div>
    );
};

export default Questionnaire;
