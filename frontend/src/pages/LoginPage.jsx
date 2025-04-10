// frontend/src/pages/LoginPage.jsx
import React, { useState } from 'react'; // Import React and the useState hook

// Define the LoginPage component
function LoginPage() {
  // State variables to hold the input values
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(''); // To store any login error messages
  const [loading, setLoading] = useState(false); // To show a loading state on submit

  // Function to handle form submission
  const handleLogin = (event) => {
    event.preventDefault(); // Prevent the browser from doing a full page reload on submit
    setError(''); // Clear previous errors
    setLoading(true); // Indicate loading
    console.log('Attempting login with:', { email, password });

    // --- TODO: Replace this alert with an actual API call using axios ---
    // We will add the axios call in the next step!
    alert('Login form submitted! API call is next.');
    // ---

    // Simulate API call ending (remove this later)
    setLoading(false);
    // setEmail(''); // Optional: Clear fields after submit attempt
    // setPassword('');
  };

  // Return the JSX structure (HTML-like code) for the login page
  return (
    <div>
      <h2>Login Page</h2>
      <form onSubmit={handleLogin}>
        <div>
          {/* Email Input */}
          <label htmlFor="email">ელ.ფოსტა:</label> {/* Georgian for Email */}
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)} // Update email state when user types
            required // HTML5 validation: field must be filled
            disabled={loading} // Disable input while loading
          />
        </div>
        <div>
          {/* Password Input */}
          <label htmlFor="password">პაროლი:</label> {/* Georgian for Password */}
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)} // Update password state when user types
            required // HTML5 validation
            disabled={loading} // Disable input while loading
          />
        </div>
        {/* Display error message if 'error' state is not empty */}
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <div>
          {/* Submit Button */}
          <button type="submit" disabled={loading}>
            {/* Show different text while loading */}
            {loading ? 'Logging in...' : 'შესვლა'}{/* Georgian for Login */}
          </button>
        </div>
      </form>
    </div>
  );
}

// Export the component so App.jsx can import it
export default LoginPage;