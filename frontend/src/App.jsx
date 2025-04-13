// frontend/src/App.jsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
// --- Import specific dashboard components ---
// Make sure the filename matches exactly (case-sensitive)
import DoctorsDashboardPage from './pages/DoctorsDashboardPage' ;
// import NurseDashboardPage from './pages/NurseDashboardPage'; // For later
// import AdminDashboardPage from './pages/AdminDashboardPage'; // For later
// import DefaultDashboardPage from './pages/DefaultDashboardPage'; // Optional fallback

// --- Authentication Check ---
// Checks if userData exists in sessionStorage
function isAuthenticated() {
  return sessionStorage.getItem('userData') !== null;
}

// --- Protected Route Component (Modified for Role-Based Rendering) ---
// This component now handles both AuthN (is user logged in?)
// and AuthZ (which dashboard should this user see?)
function ProtectedRoute() { // Removed 'children' prop as it decides what to render
  const userDataString = sessionStorage.getItem('userData');

  // 1. Check if authenticated
  if (!userDataString) {
    // Not logged in, redirect to login
    return <Navigate to="/login" replace />;
  }

  // 2. If authenticated, parse data and check role
  try {
    const userData = JSON.parse(userDataString);
    const userRole = userData.role; // Get role from stored data

    // === Role-Based Rendering Logic ===
    // IMPORTANT: Make sure the role strings ('Doctor', 'Nurse', etc.) exactly match
    // what your backend sends in the user object upon login.
    if (userRole === 'Doctor') {
        return <DoctorsDashboardPage />;
    }
    // --- Add other roles later ---
    // else if (userRole === 'Nurse') {
    //     // Make sure NurseDashboardPage component exists and is imported
    //     // return <NurseDashboardPage />;
    //     return <div> сестринское табло (Nurse Dashboard Placeholder)</div>; // Placeholder
    // }
    // else if (userRole === 'Admin') {
    //     // Make sure AdminDashboardPage component exists and is imported
    //     // return <AdminDashboardPage />;
    //      return <div> ადმინისტრაციის პანელი (Admin Dashboard Placeholder)</div>; // Placeholder
    // }
    else {
        // Fallback for unknown roles or a default dashboard
        console.warn(`Unknown or unhandled user role: ${userRole}`);
        // Optionally return a default dashboard or an access denied message
        // return <DefaultDashboardPage />;
        return <div> წვდომა შეზღუდულია / როლი უცნობია (Access Denied / Unknown Role)</div>;
    }
    // ===================================

  } catch (error) {
      // Handle error parsing user data (e.g., corrupted data)
      console.error("Error parsing user data in ProtectedRoute:", error);
      sessionStorage.removeItem('userData'); // Clear corrupted data
      return <Navigate to="/login" replace />; // Redirect to login
  }
}
// --- End ProtectedRoute ---

function App() {
  // Helper function to check auth status for the root redirect
  const checkAuth = () => isAuthenticated();

  return (
    <div className="App">
      <Routes>
        {/* Public Route: Login Page */}
        <Route path="/login" element={<LoginPage />} />

        {/* Protected Route: Dashboard Area */}
        {/* The ProtectedRoute component itself now handles which dashboard to show */}
        <Route
          path="/dashboard"
          element={<ProtectedRoute />}
        />

        {/* Default Route: Redirect based on auth status */}
        <Route
          path="/"
          element={checkAuth() ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />}
        />

        {/* Optional: Catch-all 404 Not Found Route */}
        {/* <Route path="*" element={<NotFoundPage />} /> */}
      </Routes>
    </div>
  );
}

export default App;