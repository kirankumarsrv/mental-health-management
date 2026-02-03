import React, { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './Layout';
import ErrorBoundary from './components/ErrorBoundary';
import Dashboard from './pages/Dashboard';
import ScenarioManager from './pages/ScenarioManager';
import SimulationRunner from './pages/SimulationRunner';
import TherapistDashboard from './pages/TherapistDashboard';
const Analytics = lazy(() => import('./pages/Analytics'));
import Login from './pages/Login';
import Register from './pages/Register';
import Questionnaire from './pages/Questionnaire';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ErrorBoundary>
          <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout>
                  <Dashboard />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/scenarios"
            element={
              <ProtectedRoute>
                <Layout>
                  <ScenarioManager />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/questionnaire"
            element={
              <ProtectedRoute>
                <Layout>
                  <Questionnaire />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/therapist-dashboard"
            element={
              <ProtectedRoute>
                <Layout>
                  <TherapistDashboard />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/simulation"
            element={
              <ProtectedRoute>
                <Layout>
                  <SimulationRunner />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/analytics"
            element={
              <ProtectedRoute>
                <Layout>
                  <Suspense fallback={<div style={{ padding: '2rem' }}>Loading analytics...</div>}>
                    <Analytics />
                  </Suspense>
                </Layout>
              </ProtectedRoute>
            }
          />
          </Routes>
        </ErrorBoundary>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
