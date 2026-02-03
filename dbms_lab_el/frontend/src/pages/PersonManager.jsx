import React, { useState, useEffect } from 'react';
import { Plus, Edit2, Trash2, X } from 'lucide-react';
import api from '../api';

const PersonManager = () => {
    const [persons, setPersons] = useState([]);
    const [therapists, setTherapists] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [editingPerson, setEditingPerson] = useState(null);
    const [formData, setFormData] = useState({
        name: '',
        rank: '',
        age: '',
        gender: '',
        service_years: '',
        therapist_id: ''
    });

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            setLoading(true);
            const [personsRes, therapistsRes] = await Promise.all([
                api.get('/persons/'),
                api.get('/therapists/')
            ]);
            setPersons(personsRes.data);
            setTherapists(therapistsRes.data);
            setError(null);
        } catch (err) {
            setError('Failed to fetch data');
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
                age: parseInt(formData.age),
                service_years: parseInt(formData.service_years),
                therapist_id: parseInt(formData.therapist_id)
            };

            if (editingPerson) {
                await api.put(`/persons/${editingPerson.id}`, data);
            } else {
                await api.post('/persons/', data);
            }
            
            fetchData();
            closeModal();
        } catch (err) {
            alert('Failed to save person');
            console.error(err);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this soldier?')) {
            try {
                await api.delete(`/persons/${id}`);
                fetchData();
            } catch (err) {
                alert('Failed to delete person');
                console.error(err);
            }
        }
    };

    const openModal = (person = null) => {
        if (person) {
            setEditingPerson(person);
            setFormData({
                name: person.name,
                rank: person.rank,
                age: person.age.toString(),
                gender: person.gender,
                service_years: person.service_years.toString(),
                therapist_id: person.therapist_id.toString()
            });
        } else {
            setEditingPerson(null);
            setFormData({
                name: '',
                rank: '',
                age: '',
                gender: '',
                service_years: '',
                therapist_id: therapists[0]?.id?.toString() || ''
            });
        }
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
        setEditingPerson(null);
    };

    const getTherapistName = (therapistId) => {
        const therapist = therapists.find(t => t.id === therapistId);
        return therapist ? therapist.name : 'Unknown';
    };

    if (loading) return <div className="container"><p>Loading...</p></div>;
    if (error) return <div className="container"><p style={{ color: 'var(--accent-danger)' }}>{error}</p></div>;

    return (
        <div className="container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Soldiers</h1>
                <button className="btn" onClick={() => openModal()} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Plus size={18} /> Add New Soldier
                </button>
            </div>

            <div className="glass-panel" style={{ padding: '0', overflow: 'hidden' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                    <thead style={{ background: 'rgba(255,255,255,0.05)', borderBottom: '1px solid var(--border-glass)' }}>
                        <tr>
                            <th style={{ padding: '1rem' }}>ID</th>
                            <th style={{ padding: '1rem' }}>Name</th>
                            <th style={{ padding: '1rem' }}>Rank</th>
                            <th style={{ padding: '1rem' }}>Age</th>
                            <th style={{ padding: '1rem' }}>Gender</th>
                            <th style={{ padding: '1rem' }}>Service Years</th>
                            <th style={{ padding: '1rem' }}>Therapist</th>
                            <th style={{ padding: '1rem' }}>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {persons.map(p => (
                            <tr key={p.id} style={{ borderBottom: '1px solid var(--border-glass)' }}>
                                <td style={{ padding: '1rem' }}>#{p.id}</td>
                                <td style={{ padding: '1rem', fontWeight: 'bold' }}>{p.name}</td>
                                <td style={{ padding: '1rem' }}>{p.rank}</td>
                                <td style={{ padding: '1rem' }}>{p.age}</td>
                                <td style={{ padding: '1rem' }}>{p.gender}</td>
                                <td style={{ padding: '1rem' }}>{p.service_years}</td>
                                <td style={{ padding: '1rem' }}>{getTherapistName(p.therapist_id)}</td>
                                <td style={{ padding: '1rem', display: 'flex', gap: '0.5rem' }}>
                                    <button 
                                        className="btn-secondary" 
                                        style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }}
                                        onClick={() => openModal(p)}
                                    >
                                        <Edit2 size={14} /> Edit
                                    </button>
                                    <button 
                                        className="btn-secondary" 
                                        style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem', background: 'var(--accent-danger)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}
                                        onClick={() => handleDelete(p.id)}
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
                        
                        <h2>{editingPerson ? 'Edit Soldier' : 'Add New Soldier'}</h2>
                        
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
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Rank</label>
                                <select 
                                    required
                                    value={formData.rank}
                                    onChange={(e) => setFormData({...formData, rank: e.target.value})}
                                >
                                    <option value="">Select Rank</option>
                                    <option value="Private">Private</option>
                                    <option value="Corporal">Corporal</option>
                                    <option value="Sergeant">Sergeant</option>
                                    <option value="Lieutenant">Lieutenant</option>
                                    <option value="Captain">Captain</option>
                                </select>
                            </div>
                            
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                                <div>
                                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Age</label>
                                    <input 
                                        type="number" 
                                        required
                                        min="18"
                                        max="65"
                                        value={formData.age}
                                        onChange={(e) => setFormData({...formData, age: e.target.value})}
                                    />
                                </div>
                                
                                <div>
                                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Gender</label>
                                    <select 
                                        required
                                        value={formData.gender}
                                        onChange={(e) => setFormData({...formData, gender: e.target.value})}
                                    >
                                        <option value="">Select</option>
                                        <option value="Male">Male</option>
                                        <option value="Female">Female</option>
                                        <option value="Other">Other</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div style={{ marginBottom: '1rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Service Years</label>
                                <input 
                                    type="number" 
                                    required
                                    min="0"
                                    max="40"
                                    value={formData.service_years}
                                    onChange={(e) => setFormData({...formData, service_years: e.target.value})}
                                />
                            </div>
                            
                            <div style={{ marginBottom: '1.5rem' }}>
                                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Assigned Therapist</label>
                                <select 
                                    required
                                    value={formData.therapist_id}
                                    onChange={(e) => setFormData({...formData, therapist_id: e.target.value})}
                                >
                                    <option value="">Select Therapist</option>
                                    {therapists.map(t => (
                                        <option key={t.id} value={t.id}>{t.name}</option>
                                    ))}
                                </select>
                            </div>
                            
                            <div style={{ display: 'flex', gap: '1rem' }}>
                                <button type="submit" className="btn" style={{ flex: 1 }}>
                                    {editingPerson ? 'Update' : 'Create'}
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

export default PersonManager;
