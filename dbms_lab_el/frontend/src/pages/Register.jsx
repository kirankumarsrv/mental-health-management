import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { UserPlus } from 'lucide-react';

const Register = () => {
    const navigate = useNavigate();
    const { register } = useAuth();
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        role: 'soldier',
        // Soldier fields
        soldier_name: '',
        rank: 'Private',
        age: '',
        gender: 'Male',
        service_years: '',
        // Therapist fields
        therapist_name: '',
        qualification: '',
        specialization: 'General',
        years_of_experience: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        // Convert numeric fields
        const payload = {
            ...formData,
            age: formData.age ? parseInt(formData.age, 10) : null,
            service_years: formData.service_years ? parseInt(formData.service_years, 10) : null,
            years_of_experience: formData.years_of_experience ? parseInt(formData.years_of_experience, 10) : null
        };

        const result = await register(
            formData.username,
            formData.password,
            formData.role,
            payload
        );

        if (result.success) {
            navigate(formData.role === 'soldier' ? '/questionnaire' : '/dashboard');
        } else {
            setError(result.error);
        }
        
        setLoading(false);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    return (
        <div style={{ 
            minHeight: '100vh', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
            padding: '2rem'
        }}>
            <div className="glass-panel" style={{ 
                maxWidth: '520px', 
                width: '100%',
                padding: '2.5rem'
            }}>
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    <UserPlus size={48} style={{ color: 'var(--primary)', marginBottom: '1rem' }} />
                    <h1 style={{ marginBottom: '0.5rem' }}>Create Account</h1>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
                        Register as a soldier or therapist
                    </p>
                </div>

                <form onSubmit={handleSubmit}>
                    {/* Username */}
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                            Username
                        </label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            required
                            placeholder="Choose a username"
                            style={{
                                width: '100%',
                                padding: '0.75rem',
                                borderRadius: '8px',
                                border: '1px solid rgba(255,255,255,0.1)',
                                background: 'rgba(255,255,255,0.05)',
                                color: 'var(--text)',
                                fontSize: '1rem',
                                boxSizing: 'border-box'
                            }}
                        />
                    </div>

                    {/* Password */}
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                            Password
                        </label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            placeholder="Choose a password"
                            style={{
                                width: '100%',
                                padding: '0.75rem',
                                borderRadius: '8px',
                                border: '1px solid rgba(255,255,255,0.1)',
                                background: 'rgba(255,255,255,0.05)',
                                color: 'var(--text)',
                                fontSize: '1rem',
                                boxSizing: 'border-box'
                            }}
                        />
                    </div>

                    {/* Account Type */}
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                            Account Type
                        </label>
                        <select
                            name="role"
                            value={formData.role}
                            onChange={handleChange}
                            style={{
                                width: '100%',
                                padding: '0.75rem',
                                borderRadius: '8px',
                                border: '1px solid rgba(255,255,255,0.1)',
                                background: 'rgba(255,255,255,0.05)',
                                color: 'var(--text)',
                                fontSize: '1rem',
                                boxSizing: 'border-box'
                            }}
                        >
                            <option value="soldier">Soldier</option>
                            <option value="therapist">Therapist</option>
                        </select>
                    </div>

                    {/* Soldier Details */}
                    {formData.role === 'soldier' && (
                        <>
                            <div style={{ marginBottom: '1.5rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                                    Full Name
                                </label>
                                <input
                                    type="text"
                                    name="soldier_name"
                                    value={formData.soldier_name}
                                    onChange={handleChange}
                                    placeholder="Enter your full name"
                                    style={{
                                        width: '100%',
                                        padding: '0.75rem',
                                        borderRadius: '8px',
                                        border: '1px solid rgba(255,255,255,0.1)',
                                        background: 'rgba(255,255,255,0.05)',
                                        color: 'var(--text)',
                                        fontSize: '1rem',
                                        boxSizing: 'border-box'
                                    }}
                                />
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
                                <div>
                                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                                        Rank
                                    </label>
                                    <select
                                        name="rank"
                                        value={formData.rank}
                                        onChange={handleChange}
                                        style={{
                                            width: '100%',
                                            padding: '0.75rem',
                                            borderRadius: '8px',
                                            border: '1px solid rgba(255,255,255,0.1)',
                                            background: 'rgba(255,255,255,0.05)',
                                            color: 'var(--text)',
                                            fontSize: '1rem',
                                            boxSizing: 'border-box'
                                        }}
                                    >
                                        <option value="Private">Private</option>
                                        <option value="Corporal">Corporal</option>
                                        <option value="Sergeant">Sergeant</option>
                                        <option value="Lieutenant">Lieutenant</option>
                                        <option value="Captain">Captain</option>
                                    </select>
                                </div>

                                <div>
                                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                                        Age
                                    </label>
                                    <input
                                        type="number"
                                        name="age"
                                        value={formData.age}
                                        onChange={handleChange}
                                        placeholder="Age"
                                        min="18"
                                        max="80"
                                        style={{
                                            width: '100%',
                                            padding: '0.75rem',
                                            borderRadius: '8px',
                                            border: '1px solid rgba(255,255,255,0.1)',
                                            background: 'rgba(255,255,255,0.05)',
                                            color: 'var(--text)',
                                            fontSize: '1rem',
                                            boxSizing: 'border-box'
                                        }}
                                    />
                                </div>
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
                                <div>
                                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                                        Gender
                                    </label>
                                    <select
                                        name="gender"
                                        value={formData.gender}
                                        onChange={handleChange}
                                        style={{
                                            width: '100%',
                                            padding: '0.75rem',
                                            borderRadius: '8px',
                                            border: '1px solid rgba(255,255,255,0.1)',
                                            background: 'rgba(255,255,255,0.05)',
                                            color: 'var(--text)',
                                            fontSize: '1rem',
                                            boxSizing: 'border-box'
                                        }}
                                    >
                                        <option value="Male">Male</option>
                                        <option value="Female">Female</option>
                                        <option value="Other">Other</option>
                                    </select>
                                </div>

                                <div>
                                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                                        Years of Service
                                    </label>
                                    <input
                                        type="number"
                                        name="service_years"
                                        value={formData.service_years}
                                        onChange={handleChange}
                                        placeholder="Years"
                                        min="0"
                                        max="50"
                                        style={{
                                            width: '100%',
                                            padding: '0.75rem',
                                            borderRadius: '8px',
                                            border: '1px solid rgba(255,255,255,0.1)',
                                            background: 'rgba(255,255,255,0.05)',
                                            color: 'var(--text)',
                                            fontSize: '1rem',
                                            boxSizing: 'border-box'
                                        }}
                                    />
                                </div>
                            </div>
                        </>
                    )}

                    {/* Therapist Details */}
                    {formData.role === 'therapist' && (
                        <>
                            <div style={{ marginBottom: '1.5rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                                    Full Name
                                </label>
                                <input
                                    type="text"
                                    name="therapist_name"
                                    value={formData.therapist_name}
                                    onChange={handleChange}
                                    placeholder="Enter your full name"
                                    style={{
                                        width: '100%',
                                        padding: '0.75rem',
                                        borderRadius: '8px',
                                        border: '1px solid rgba(255,255,255,0.1)',
                                        background: 'rgba(255,255,255,0.05)',
                                        color: 'var(--text)',
                                        fontSize: '1rem',
                                        boxSizing: 'border-box'
                                    }}
                                />
                            </div>

                            <div style={{ marginBottom: '1.5rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                                    Qualification
                                </label>
                                <input
                                    type="text"
                                    name="qualification"
                                    value={formData.qualification}
                                    onChange={handleChange}
                                    placeholder="e.g., PhD Clinical Psychology"
                                    style={{
                                        width: '100%',
                                        padding: '0.75rem',
                                        borderRadius: '8px',
                                        border: '1px solid rgba(255,255,255,0.1)',
                                        background: 'rgba(255,255,255,0.05)',
                                        color: 'var(--text)',
                                        fontSize: '1rem',
                                        boxSizing: 'border-box'
                                    }}
                                />
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
                                <div>
                                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                                        Specialization
                                    </label>
                                    <input
                                        type="text"
                                        name="specialization"
                                        value={formData.specialization}
                                        onChange={handleChange}
                                        placeholder="e.g., Trauma"
                                        style={{
                                            width: '100%',
                                            padding: '0.75rem',
                                            borderRadius: '8px',
                                            border: '1px solid rgba(255,255,255,0.1)',
                                            background: 'rgba(255,255,255,0.05)',
                                            color: 'var(--text)',
                                            fontSize: '1rem',
                                            boxSizing: 'border-box'
                                        }}
                                    />
                                </div>

                                <div>
                                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                                        Years of Experience
                                    </label>
                                    <input
                                        type="number"
                                        name="years_of_experience"
                                        value={formData.years_of_experience}
                                        onChange={handleChange}
                                        placeholder="Years"
                                        min="0"
                                        max="80"
                                        style={{
                                            width: '100%',
                                            padding: '0.75rem',
                                            borderRadius: '8px',
                                            border: '1px solid rgba(255,255,255,0.1)',
                                            background: 'rgba(255,255,255,0.05)',
                                            color: 'var(--text)',
                                            fontSize: '1rem',
                                            boxSizing: 'border-box'
                                        }}
                                    />
                                </div>
                            </div>
                        </>
                    )}

                    {/* Error Message */}
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

                    {/* Submit Button */}
                    <button 
                        type="submit" 
                        className="btn" 
                        disabled={loading}
                        style={{ width: '100%', padding: '0.875rem', fontSize: '1rem' }}
                    >
                        {loading ? 'Creating account...' : 'Create Account'}
                    </button>

                    {/* Sign In Link */}
                    <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.9rem' }}>
                        <span style={{ color: 'var(--text-muted)' }}>Already have an account? </span>
                        <Link to="/login" style={{ color: 'var(--primary)', textDecoration: 'none' }}>
                            Sign in
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Register;
