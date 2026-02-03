import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Set token in API headers if it exists
        if (token) {
            api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            // Fetch user profile
            fetchUserProfile();
        } else {
            setLoading(false);
        }
    }, [token]);

    const fetchUserProfile = async () => {
        try {
            const response = await api.get('/auth/me/profile');
            setUser(response.data);
        } catch (error) {
            console.error('Failed to fetch user profile:', error);
            // Token might be invalid, clear it
            logout();
        } finally {
            setLoading(false);
        }
    };

    const login = async (username, password) => {
        try {
            const response = await api.post('/auth/login-json', {
                username,
                password
            });
            
            const { access_token } = response.data;
            
            // Store token
            localStorage.setItem('token', access_token);
            setToken(access_token);
            api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
            
            // Fetch user profile
            await fetchUserProfile();
            
            return { success: true };
        } catch (error) {
            return { 
                success: false, 
                error: error.response?.data?.detail || 'Login failed' 
            };
        }
    };

    const register = async (username, password, role, formData) => {
        try {
            const payload = {
                username,
                password,
                role,
                ...formData  // Spread soldier_name, rank, age, etc.
            };
            
            await api.post('/auth/register', payload);
            
            // Auto-login after registration
            return await login(username, password);
        } catch (error) {
            return { 
                success: false, 
                error: error.response?.data?.detail || 'Registration failed' 
            };
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
        delete api.defaults.headers.common['Authorization'];
    };

    const value = {
        user,
        token,
        loading,
        login,
        register,
        logout,
        isAuthenticated: !!token && !!user
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};
