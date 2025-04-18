// frontend/src/pages/LoginPage.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import styles from './LoginPage.module.css'; // Import CSS module
import medicardLogo from '../assets/medicard-logo.png'; // Import logo (ensure path/name is correct)

function LoginPage() {
  // State variables for form inputs, error messages, and loading indicator
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  // Hook for programmatic navigation
  const navigate = useNavigate();

  // Function to handle the login form submission
  const handleLogin = async (event) => {
    event.preventDefault(); // Prevent default form submission behavior
    setError(''); // Clear any previous errors
    setLoading(true); // Set loading state to true

    try {
      // Send POST request to the backend login endpoint
      const response = await axios.post('http://127.0.0.1:5000/api/auth/login', { // Correct backend URL
        email: email,
        password: password,
        withCredentials: true, // Include credentials for CORS
      });

      // Login successful: Store user data in sessionStorage
      // Note: For more persistent login, consider localStorage or state management solutions
      sessionStorage.setItem('userData', JSON.stringify(response.data.user));

      // Navigate to the dashboard page upon successful login
      navigate('/dashboard');

    } catch (err) {
      // Handle login errors
      let errorMessage = 'Login failed. Please try again.'; // Default error message

      // Extract more specific error message from backend response if available
      if (err.response?.data?.error) {
        errorMessage = err.response.data.error; // Use error message from backend { "error": "..." }
      } else if (err.response?.data?.errors) {
         // Handle potential validation errors (if backend sends them)
        errorMessage = Object.values(err.response.data.errors).flat().join(' ');
      } else if (err.request) {
        // Handle network errors (request made, no response received)
        errorMessage = 'Cannot connect to the server. Please check network or if server is running.';
      } else {
        // Handle other errors (e.g., setting up the request)
        errorMessage = err.message;
      }
      setError(errorMessage); // Set the error state to display the message
      console.error('Login failed:', err); // Log the full error for debugging

    } finally {
      // This block executes regardless of success or failure
      setLoading(false); // Set loading state back to false
    }
  };

  // Render the login page structure
  return (
    // Apply container styles for background and centering
    <div className={styles.loginPageContainer}>

      {/* Display the logo */}
      <img src={medicardLogo} alt="Medicard Logo" className={styles.logo} />

      {/* Login form with card styling */}
      <form onSubmit={handleLogin} className={styles.loginForm}>
        {/* Form title in Georgian */}
        <h2>შესვლა</h2>

        {/* Email input group */}
        <div className={styles.formGroup}>
          <label htmlFor="email">ელ.ფოსტა:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)} // Update email state on change
            required // HTML5 validation
            disabled={loading} // Disable input while loading
            autoComplete="email" // Browser autofill hint
          />
        </div>

        {/* Password input group */}
        <div className={styles.formGroup}>
          <label htmlFor="password">პაროლი:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)} // Update password state on change
            required // HTML5 validation
            disabled={loading} // Disable input while loading
            autoComplete="current-password" // Browser autofill hint
          />
        </div>

        {/* Display error message if 'error' state is not empty */}
        {error && <p className={styles.errorMessage}>{error}</p>}

        {/* Forgot Password Button/Link (using CSS Modules) */}
        <div className={styles.forgotPasswordContainer}>
          <button
            type="button" // Prevents form submission
            className={styles.forgotPasswordButton} // Apply styles from CSS module
            // Simple alert for now, replace with navigation or modal later if needed
            onClick={() => alert('გთხოვთ დაუკავშირდეთ IT დეპარტამენტს პაროლის აღსადგენად.')}
          >
            დაგავიწყდა პაროლი?
          </button>
        </div>

        {/* Login Submit Button */}
        <button
          type="submit"
          className={styles.loginButton} // Apply styles from CSS module
          disabled={loading} // Disable button while loading
        >
          {/* Show different text based on loading state */}
          {loading ? 'იტვირთება...' : 'შესვლა'}
        </button>
      </form>
    </div>
  );
}

export default LoginPage;