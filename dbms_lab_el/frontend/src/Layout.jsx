import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Users, UserPlus, FileVideo, Activity, FileText, LogOut, LineChart } from 'lucide-react';
import { useAuth } from './context/AuthContext';

const NavItem = ({ to, icon: Icon, label, active }) => (
    <Link to={to} style={{ textDecoration: 'none' }}>
        <div className={`glass-panel`} style={{
            display: 'flex',
            alignItems: 'center',
            padding: '1rem',
            marginBottom: '0.8rem',
            backgroundColor: active ? 'rgba(56, 189, 248, 0.15)' : 'transparent',
            borderColor: active ? 'var(--primary)' : 'transparent',
            color: active ? 'var(--primary)' : 'var(--text-muted)'
        }}>
            <Icon size={20} style={{ marginRight: '0.8rem' }} />
            <span style={{ fontWeight: 500 }}>{label}</span>
        </div>
    </Link>
);

const Layout = ({ children }) => {
    const location = useLocation();
    const { logout, user } = useAuth();

    return (
        <div style={{ display: 'flex', minHeight: '100vh' }}>
            {/* Sidebar */}
            <aside style={{
                width: '260px',
                padding: '2rem',
                borderRight: '1px solid var(--border-glass)',
                background: 'rgba(15, 23, 42, 0.4)'
            }}>
                <div style={{ marginBottom: '3rem', display: 'flex', alignItems: 'center', color: 'var(--primary)' }}>
                    <Activity size={32} />
                    <h2 style={{ margin: '0 0 0 10px', fontSize: '1.4rem' }}>MindSim</h2>
                </div>

                <nav>
                    {user?.user?.role === 'therapist' ? (
                        // Therapist Navigation
                        <>
                            <NavItem to="/therapist-dashboard" icon={LayoutDashboard} label="Dashboard" active={location.pathname === '/therapist-dashboard'} />
                            <NavItem to="/analytics" icon={LineChart} label="Analytics" active={location.pathname === '/analytics'} />
                        </>
                    ) : (
                        // Soldier Navigation
                        <>
                            <NavItem to="/" icon={LayoutDashboard} label="Dashboard" active={location.pathname === '/'} />
                            <NavItem to="/questionnaire" icon={FileText} label="Take Assessment" active={location.pathname === '/questionnaire'} />
                            <NavItem to="/simulation" icon={Activity} label="Run Simulation" active={location.pathname === '/simulation'} />
                            <NavItem to="/scenarios" icon={FileVideo} label="Scenarios" active={location.pathname === '/scenarios'} />
                            <NavItem to="/analytics" icon={LineChart} label="Analytics" active={location.pathname === '/analytics'} />
                        </>
                    )}
                </nav>

                <div style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '1px solid var(--border-glass)' }}>
                    <div style={{ marginBottom: '0.75rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                        Logged in as: {user?.user?.username || user?.user?.email || 'User'}
                    </div>
                    <button
                        onClick={logout}
                        className="btn"
                        style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                    >
                        <LogOut size={18} style={{ marginRight: '8px' }} /> Log Out
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main style={{ flex: 1, padding: '2rem', overflowY: 'auto' }}>
                {children}
            </main>
        </div>
    );
};

export default Layout;
