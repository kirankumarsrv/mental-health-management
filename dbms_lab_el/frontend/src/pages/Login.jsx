import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogIn } from 'lucide-react';

const Login = () => {
    const navigate = useNavigate();
    const { login } = useAuth();
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        const result = await login(formData.username, formData.password);
        
        if (result.success) {
            navigate('/questionnaire');
        } else {
            setError(result.error);
        }
        
        setLoading(false);
    };

    return (
        <div style={{ 
            minHeight: '100vh', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            padding: '2rem'
        }}>
            <div className="glass-panel" style={{ 
                maxWidth: '420px', 
                width: '100%',
                padding: '2.5rem'
            }}>
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    <LogIn size={48} style={{ color: 'var(--primary)', marginBottom: '1rem' }} />
                    <h1 style={{ marginBottom: '0.5rem' }}>PTSD Assessment System</h1>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
                        Sign in to continue
                    </p>
                </div>

                <form onSubmit={handleSubmit}>
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label htmlFor="username" style={{ 
                            display: 'block', 
                            marginBottom: '0.5rem',
                            fontWeight: '500'
                        }}>
                            Username
                        </label>
                        <input
                            type="text"
                            id="username"
                            value={formData.username}
                            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                            required
                            placeholder="Enter your username"
                            style={{
                                width: '100%',
                                padding: '0.75rem',
                                borderRadius: '8px',
                                border: '1px solid rgba(255,255,255,0.1)',
                                background: 'rgba(255,255,255,0.05)',
                                color: 'var(--text)',
                                fontSize: '1rem'
                            }}
                        />
                    </div>

                    <div style={{ marginBottom: '1.5rem' }}>
                        <label htmlFor="password" style={{ 
                            display: 'block', 
                            marginBottom: '0.5rem',
                            fontWeight: '500'
                        }}>
                            Password
                        </label>
                        <input
                            type="password"
                            id="password"
                            value={formData.password}
                            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                            required
                            placeholder="Enter your password"
                            style={{
                                width: '100%',
                                padding: '0.75rem',
                                borderRadius: '8px',
                                border: '1px solid rgba(255,255,255,0.1)',
                                background: 'rgba(255,255,255,0.05)',
                                color: 'var(--text)',
                                fontSize: '1rem'
                            }}
                        />
                    </div>

                    {error && (
                        <div style={{
                            padding: '0.75rem',
                            marginBottom: '1.5rem',
                            background: 'rgba(239, 68, 68, 0.1)',
                            border: '1px solid rgba(239, 68, 68, 0.3)',
                            borderRadius: '8px',
                            color: '#f87171',
                            fontSize: '0.9rem'
                        }}>
                            {error}
                        </div>
                    )}

                    <button 
                        type="submit" 
                        className="btn" 
                        disabled={loading}
                        style={{ 
                            width: '100%',
                            padding: '0.875rem',
                            fontSize: '1rem',
                            fontWeight: '600'
                        }}
                    >
                        {loading ? 'Signing in...' : 'Sign In'}
                    </button>

                    <div style={{ 
                        marginTop: '1.5rem', 
                        textAlign: 'center',
                        fontSize: '0.9rem'
                    }}>
                        <span style={{ color: 'var(--text-muted)' }}>
                            Don't have an account?{' '}
                        </span>
                        <Link to="/register" style={{ 
                            color: 'var(--primary)',
                            textDecoration: 'none',
                            fontWeight: '500'
                        }}>
                            Register here
                        </Link>
                    </div>
                </form>

                <div style={{
                    marginTop: '2rem',
                    padding: '1rem',
                    background: 'rgba(59, 130, 246, 0.1)',
                    borderRadius: '8px',
                    fontSize: '0.85rem',
                    color: 'var(--text-muted)'
                }}>
                    <strong>Test Credentials:</strong><br />
                    Username: soldier1<br />
                    Password: password123
                </div>
            </div>
        </div>
    );
};

export default Login;
