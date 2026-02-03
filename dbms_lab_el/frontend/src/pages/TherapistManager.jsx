import React, { useState, useEffect } from 'react';
import { Plus, Edit2, Trash2, X } from 'lucide-react';
import api from '../api';

const TherapistManager = () => {
    const [therapists, setTherapists] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [editingTherapist, setEditingTherapist] = useState(null);
    const [formData, setFormData] = useState({
        name: '',
        qualification: '',
        specialization: '',
        years_of_experience: ''
    });

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            setLoading(true);
            const response = await api.get('/therapists/');
            setTherapists(response.data);
            setError(null);
        } catch (err) {
            setError('Failed to fetch therapists');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = {
                ...formData,
                years_of_experience: parseInt(formData.years_of_experience)
            };

            if (editingTherapist) {
                await api.put(`/therapists/${editingTherapist.id}`, data);
            } else {
                await api.post('/therapists/', data);
            }
            
            fetchData();
            closeModal();
        } catch (err) {
            alert('Failed to save therapist');
            console.error(err);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this therapist?')) {
            try {
                await api.delete(`/therapists/${id}`);
                fetchData();
            } catch (err) {
                alert('Failed to delete therapist');
                console.error(err);
            }
        }
    };

    const openModal = (therapist = null) => {
        if (therapist) {
            setEditingTherapist(therapist);
            setFormData({
                name: therapist.name,
                qualification: therapist.qualification,
                specialization: therapist.specialization,
                years_of_experience: therapist.years_of_experience.toString()
            });
        } else {
            setEditingTherapist(null);
            setFormData({
                name: '',
                qualification: '',
                specialization: '',
                years_of_experience: ''
            });
        }
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
        setEditingTherapist(null);
    };

    if (loading) return <div className="container"><p>Loading...</p></div>;
    if (error) return <div className="container"><p style={{ color: 'var(--accent-danger)' }}>{error}</p></div>;

    return (
        <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Therapists</h1>
                <button className="btn" onClick={() => openModal()} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Plus size={18} /> Add New Therapist
                </button>
            </div>

            <div className="glass-panel" style={{ padding: '0', overflow: 'hidden' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                    <thead style={{ background: 'rgba(255,255,255,0.05)', borderBottom: '1px solid var(--border-glass)' }}>
                        <tr>
                            <th style={{ padding: '1rem' }}>ID</th>
                            <th style={{ padding: '1rem' }}>Name</th>
                            <th style={{ padding: '1rem' }}>Qualification</th>
                            <th style={{ padding: '1rem' }}>Specialization</th>
                            <th style={{ padding: '1rem' }}>Experience (Years)</th>
                            <th style={{ padding: '1rem' }}>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {therapists.map(t => (
                            <tr key={t.id} style={{ borderBottom: '1px solid var(--border-glass)' }}>
                                <td style={{ padding: '1rem' }}>#{t.id}</td>
                                <td style={{ padding: '1rem', fontWeight: 'bold' }}>{t.name}</td>
                                <td style={{ padding: '1rem' }}>{t.qualification}</td>
                                <td style={{ padding: '1rem' }}>{t.specialization}</td>
                                <td style={{ padding: '1rem' }}>{t.years_of_experience}</td>
                                <td style={{ padding: '1rem', display: 'flex', gap: '0.5rem' }}>
                                    <button 
                                        className="btn-secondary" 
                                        style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}
                                        onClick={() => openModal(t)}
                                    >
                                        <Edit2 size={14} /> Edit
                                    </button>
                                    <button 
                                        className="btn-secondary" 
                                        style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem', background: 'var(--accent-danger)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}
                                        onClick={() => handleDelete(t.id)}
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
                        
                        <h2>{editingTherapist ? 'Edit Therapist' : 'Add New Therapist'}</h2>
                        
                        <form onSubmit={handleSubmit} style={{ marginTop: '1.5rem' }}>
                            <div style={{ marginBottom: '1rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Name</label>
                                <input 
                                    type="text" 
                                    required
                                    value={formData.name}
                                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                                />
                            </div>
                            
                            <div style={{ marginBottom: '1rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Qualification</label>
                                <input 
                                    type="text" 
                                    required
                                    placeholder="e.g., PhD Clinical Psychology"
                                    value={formData.qualification}
                                    onChange={(e) => setFormData({...formData, qualification: e.target.value})}
                                />
                            </div>
                            
                            <div style={{ marginBottom: '1rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Specialization</label>
                                <select 
                                    required
                                    value={formData.specialization}
                                    onChange={(e) => setFormData({...formData, specialization: e.target.value})}
                                >
                                    <option value="">Select Specialization</option>
                                    <option value="Trauma">Trauma</option>
                                    <option value="PTSD">PTSD</option>
                                    <option value="Cognitive Behavioral">Cognitive Behavioral</option>
                                    <option value="EMDR">EMDR</option>
                                    <option value="General">General</option>
                                </select>
                            </div>
                            
                            <div style={{ marginBottom: '1.5rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Years of Experience</label>
                                <input 
                                    type="number" 
                                    required
                                    min="0"
                                    max="50"
                                    value={formData.years_of_experience}
                                    onChange={(e) => setFormData({...formData, years_of_experience: e.target.value})}
                                />
                            </div>
                            
                            <div style={{ display: 'flex', gap: '1rem' }}>
                                <button type="submit" className="btn" style={{ flex: 1 }}>
                                    {editingTherapist ? 'Update' : 'Create'}
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

export default TherapistManager;
