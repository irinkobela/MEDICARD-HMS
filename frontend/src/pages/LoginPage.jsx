// frontend/src/pages/LoginPage.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import styles from './LoginPage.module.css';
import medicardLogo from '../assets/medicard-logo.png';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    // ... handleLogin function remains the same ...
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:5000/login', {
        email: email,
        password: password,
      });
      sessionStorage.setItem('userData', JSON.stringify(response.data.user));
      navigate('/dashboard');
    } catch (err) {
      let errorMessage = 'Login failed. Please try again.';
      if (err.response?.data?.error) {
        errorMessage = err.response.data.error;
      } else if (err.response?.data?.errors) {
        errorMessage = Object.values(err.response.data.errors).flat().join(' ');
      } else if (err.request) {
        errorMessage = 'Cannot connect to the server.';
      } else {
        errorMessage = err.message;
      }
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.loginPageContainer}>
      <img src={medicardLogo} alt="Medicard Logo" className={styles.logo} />

      <form onSubmit={handleLogin} className={styles.loginForm}>
        <h2>შესვლა</h2>

        <div className={styles.formGroup}>
          <label htmlFor="email">ელ.ფოსტა:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
            autoComplete="email"
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="password">პაროლი:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
            autoComplete="current-password"
          />
        </div>

        {/* Display Error Message */}
        {error && <p className={styles.errorMessage}>{error}</p>}

        {/* --- START: Add Forgot Password Snippet Here --- */}
        <div style={{ textAlign: 'center', marginTop: '0px', marginBottom: '15px' }}> {/* Adjusted margins */}
          <button
            type="button" // Important: type="button" prevents form submission
            style={{
              background: 'none',
              border: 'none',
              color: '#007b8a', // Use theme color
              textDecoration: 'underline',
              cursor: 'pointer',
              fontSize: '0.9rem' // Slightly smaller font
            }}
            // Alert message in Georgian
            onClick={() => alert('Გთხოვთ დაუკავშირდეთ ადმინისტრატორს პაროლის აღსადგენად.')}
          >
            დაგავიწყდა პაროლი?
          </button>
        </div>
        {/* --- END: Add Forgot Password Snippet Here --- */}


        <button type="submit" className={styles.loginButton} disabled={loading}>
          {loading ? 'იტვირთება...' : 'შესვლა'}
        </button>
      </form>
    </div>
  );
}

export default LoginPage;