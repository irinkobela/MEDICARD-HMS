// frontend/src/pages/DashboardPage.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './DashboardPage.module.css'; // <<< 1. Import the CSS module

function DashboardPage() {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const storedData = sessionStorage.getItem('userData');
    if (storedData) {
      try {
        const parsedData = JSON.parse(storedData);
        setUserData(parsedData);
      } catch (error) {
        console.error("Failed to parse user data from sessionStorage", error);
        sessionStorage.removeItem('userData');
        navigate('/login');
      }
    } else {
      console.warn("No user data found in session storage. Redirecting to login.");
      navigate('/login');
    }
  }, [navigate]);

  const handleLogout = async () => {
    try {
      await axios.post('http://127.0.0.1:5000/api/auth/logout', {}, {
           withCredentials: true
      });
      console.log("Logout API call successful");
    } catch (error) {
       console.error("Logout API call failed:", error);
    } finally {
       sessionStorage.removeItem('userData');
       navigate('/login');
    }
  };

  if (!userData) {
    // Consider adding a loading CSS class here too
    return <div>მომხმარებლის მონაცემები იტვირთება...</div>;
  }

  const firstName = userData.firstName || '';
  const lastName = userData.lastName || '';
  const displayName = (firstName || lastName) ? `${firstName} ${lastName}`.trim() : (userData.username || userData.email);

  // === 2. Apply CSS classes using className ===
  return (
    <div className={styles.dashboardContainer}> {/* Apply container style */}

      {/* Apply greeting style */}
      <h2 className={styles.greeting}>
        გამარჯობა {displayName}, ბედნიერ დღეს გისურვებ!
      </h2>

      {/* Apply user info style */}
      <p className={styles.userInfo}>
        თქვენი როლი: {userData.role || 'N/A'}
      </p>

      {/* Apply button style */}
      <button onClick={handleLogout} className={styles.logoutButton}>
        გასვლა
      </button>

      {/* Apply separator style */}
      <hr className={styles.separator} />

      {/* Apply section title style */}
      <h3 className={styles.sectionTitle}>
        პაციენტების სია
      </h3>

      {/* Apply placeholder text style */}
      <div className={styles.placeholderText}>
        პაციენტების სია აქ გამოჩნდება... (მონაცემების ჩატვირთვა შემდეგი ნაბიჯია)
      </div>

      {/* --- TODO: Add Patient List Fetching and Rendering Logic Here --- */}
      {/* We will add patient list container/table styles later */}

    </div>
  );
}

export default DashboardPage;