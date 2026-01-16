import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function AuthCallback() {
  const navigate = useNavigate();

  useEffect(() => {
    const hash = window.location.hash;
    const params = new URLSearchParams(hash.replace('#', ''));
    const sessionId = params.get('session_id');

    if (!sessionId) {
      navigate('/login');
      return;
    }

    axios
      .post(`${API}/auth/session`, { session_id: sessionId })
      .then((res) => {
        navigate('/dashboard', { state: { user: res.data } });
      })
      .catch(() => {
        navigate('/login');
      });
  }, [navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <p>Signing you in...</p>
    </div>
  );
}
