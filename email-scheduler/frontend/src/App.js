import React, { useState, useEffect } from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useNavigate,
  useLocation,
} from 'react-router-dom';
import axios from 'axios';
import { Toaster } from 'sonner';
import './App.css';
import './index.css';

import LoginPage from './pages/LoginPage';
import UserDashboard from './pages/UserDashboard';
import LoginCallback from './pages/LoginCallback';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

axios.defaults.withCredentials = true;

function ProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.state?.user) {
      setUser(location.state.user);
      setIsAuthenticated(true);
      return;
    }

    const checkAuth = async () => {
      try {
        const response = await axios.get(`${API}/auth/me`);
        setUser(response.data);
        setIsAuthenticated(true);
      } catch {
        setIsAuthenticated(false);
        navigate('/login');
      }
    };

    checkAuth();
  }, [navigate, location]);

  if (isAuthenticated === null) {
    return (
      <div style={{ padding: 40 }}>Loading...</div>
    );
  }

  return isAuthenticated
    ? React.cloneElement(children, { user })
    : null;
}

function AppRouter() {
  const location = useLocation();

  if (location.hash?.includes('session_id=')) {
    return <LoginCallback />;
  }

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <UserDashboard />
          </ProtectedRoute>
        }
      />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppRouter />
      <Toaster position="top-right" richColors />
    </BrowserRouter>
  );
}
