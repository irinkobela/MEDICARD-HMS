// frontend/src/pages/DashboardPage.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // We'll need axios again

function DashboardPage() {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null); // To store user data

  // Simulate fetching user data from storage on component mount
  useEffect(() => {
    const storedData = sessionStorage.getItem('userData');
    if (storedData) {
      setUserData(JSON.parse(storedData));
    } else {
      // If no user data found (e.g., user directly navigated here without login)
      // The ProtectedRoute in App.jsx should ideally handle this,
      // but this is an extra safety check.
      console.warn("No user data found in session storage. Redirecting to login.");
      navigate('/login');
    }
  }, [navigate]);

  const handleLogout = async () => {
    try {
      // Call your backend logout endpoint
      await axios.post('http://127.0.0.1:5000/logout'); // Assuming default credentials handling

      // Clear user data from storage
      sessionStorage.removeItem('userData');
      // Optional: Clear other related storage items

      // Redirect to login page
      navigate('/login');

    } catch (error) {
       console.error("Logout failed:", error);
       // Handle logout error (e.g., show a message)
       // Even if logout API fails, attempt to clear local state and redirect
       sessionStorage.removeItem('userData');
       navigate('/login');
    }
  };

  // Display loading or welcome message while user data is loading or missing
  if (!userData) {
    return <div>Loading user data...</div>;
  }

  // --- TODO: Fetch and display patient list here ---
  // We will add the logic to call '/api/dashboard/patient-list'
  // and display the results in the next step.

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Welcome, {userData.username || userData.email}!</p>
      <p>Your Role: {userData.role}</p>

      {/* Add a simple logout button */}
      <button onClick={handleLogout}>Logout (გასვლა)</button>

      <hr />

      <h3>Patient List</h3>
      {/* Placeholder for patient list */}
      <div>
        Patient list will be displayed here... (Fetching data is the next step)
      </div>
    </div>
  );
}

export default DashboardPage;