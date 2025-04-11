// frontend/src/App.jsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom'; // Import necessary components
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage'; // Import the new dashboard page

// --- Mock Authentication Check (Replace with real logic later) ---
// This is a placeholder. In a real app, you'd check for a stored token
// or use context state to determine if the user is logged in.
const isAuthenticated = () => {
  // For now, let's assume the user is logged in if there's *any* user info in sessionStorage
  // You'll replace this with a more robust check based on how you store login state
  return sessionStorage.getItem('userData') !== null;
};

// --- Protected Route Component ---
// This component checks authentication before rendering the requested page
// If not authenticated, it redirects to the login page.
function ProtectedRoute({ children }) {
  if (!isAuthenticated()) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to. This allows us to send them along to that page after login.
    return <Navigate to="/login" replace />;
  }
  return children; // Render the component if authenticated
}
// ---

function App() {
  return (
    <div className="App">
      <Routes>
        {/* Public Route: Login Page */}
        <Route path="/login" element={<LoginPage />} />

        {/* Protected Route: Dashboard Page */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />

        {/* Default Route */}
        {/* If authenticated, go to dashboard, otherwise go to login */}
        <Route
          path="/"
          element={isAuthenticated() ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />}
        />

        {/* Optional: Catch-all route for 404 Not Found */}
        {/* <Route path="*" element={<NotFoundPage />} /> */}
      </Routes>
    </div>
  );
}

export default App;