// frontend/src/App.jsx
import React from 'react';
import LoginPage from './pages/LoginPage'; // Import the new component
// You can remove the import './App.css' if App.css is empty

function App() {
  // For now, App just renders the LoginPage
  return (
    <div className="App">
      <LoginPage />
    </div>
  );
}

export default App;