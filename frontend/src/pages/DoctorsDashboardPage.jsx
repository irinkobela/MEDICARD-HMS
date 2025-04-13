// frontend/src/pages/DoctorsDashboardPage.jsx

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './DoctorsDashboardPage.module.css'; // Import the final CSS module

function DashboardPage() {
    const navigate = useNavigate();
    const [userData, setUserData] = useState(null);
    const [showGreetingToast, setShowGreetingToast] = useState(true);
    const [patients, setPatients] = useState([]);
    const [isLoadingPatients, setIsLoadingPatients] = useState(false);
    const [patientError, setPatientError] = useState(null);
    const [theme, setTheme] = useState('light');

    useEffect(() => {
        const storedData = sessionStorage.getItem('userData');
        if (storedData) {
            try {
                setUserData(JSON.parse(storedData));
            } catch (error) {
                console.error("Failed parse user data", error);
                sessionStorage.removeItem('userData');
                navigate('/login');
            }
        } else {
            console.warn("No user data. Redirecting.");
            navigate('/login');
        }
    }, [navigate]);

    useEffect(() => {
        if (showGreetingToast) {
            const timerId = setTimeout(() => setShowGreetingToast(false), 30000);
            return () => clearTimeout(timerId);
        }
    }, [showGreetingToast]);

    useEffect(() => {
        if (userData) {
            const fetchPatients = async () => {
                setIsLoadingPatients(true);
                setPatientError(null);
                try {
                    const response = await axios.get('http://127.0.0.1:5000/api/dashboard/patient-list', { withCredentials: true });
                    setPatients(response.data.patients || []);
                } catch (err) {
                    let errorMessage = "Could not load patient data.";
                    if (err.response) {
                        errorMessage = `Error ${err.response.status}: ${err.response.data?.error || err.response.statusText}`;
                    } else if (err.request) {
                        errorMessage = "Cannot reach server.";
                    } else {
                        errorMessage = `Unexpected error: ${err.message}`;
                    }
                    setPatientError(errorMessage);
                    setPatients([]);
                } finally {
                    setIsLoadingPatients(false);
                }
            };
            fetchPatients();
        }
    }, [userData]);

    const handleLogout = async () => {
        try {
            await axios.post('http://127.0.0.1:5000/api/auth/logout', {}, { withCredentials: true });
        } catch (error) {
            console.error("Logout API call failed:", error);
        } finally {
            sessionStorage.removeItem('userData');
            navigate('/login');
        }
    };

    const toggleTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
        document.documentElement.setAttribute('data-theme', newTheme);
    };

    if (!userData) {
        return <div className={styles.dashboardContainer}>მონაცემები იტვირთება...</div>;
    }

    const firstName = userData.firstName || '';
    const lastName = userData.lastName || '';
    const displayName = (firstName || lastName) ? `${firstName} ${lastName}`.trim() : (userData.username || userData.email);

    const renderStatusIndicators = (indicators) => {
        if (!indicators) return <td>-</td>;
        const icons = [];
        if (indicators.has_critical_lab) icons.push(
            <span key="lab" className={`${styles.iconWithTooltip}`}>🧪<span className={styles.tooltipText}>კრიტიკული ლაბორატორია</span></span>
        );
        if (indicators.has_critical_imaging) icons.push(
            <span key="img" className={`${styles.iconWithTooltip}`}>☢️<span className={styles.tooltipText}>კრიტიკული კვლევა</span></span>
        );
        if (indicators.has_unread_consult) icons.push(
            <span key="consult" className={`${styles.iconWithTooltip}`}>✉️<span className={styles.tooltipText}>წაუკითხავი კონსულტაცია</span></span>
        );
        if (indicators.has_pending_orders) icons.push(
            <span key="order" className={`${styles.iconWithTooltip}`}>⏳<span className={styles.tooltipText}>მოლოდინშია ხელმოწერა</span></span>
        );
        return <td>{icons.length > 0 ? icons : '-'}</td>;
    };

    return (
        <div className={styles.dashboardContainer}>

            {showGreetingToast && (
                <div className={styles.greetingToast}>
                    <span>გამარჯობა {displayName}, ბედნიერ დღეს გისურვებ!</span>
                    <button onClick={() => setShowGreetingToast(false)} className={styles.toastCloseButton} title="დახურვა">&times;</button>
                </div>
            )}

            <button onClick={handleLogout} className={styles.logoutButton}>გასვლა</button>
            <button onClick={toggleTheme} className={styles.themeToggle}>🌓</button>

            <section className={styles.section}>
                <h2>ჩემი პაციენტები</h2>
                <div className={styles.filters}>
                    <select><option>განყოფილება</option></select>
                    <select><option>სერვისი</option></select>
                    <select><option>სიმძიმე</option></select>
                    <select><option>გაწერა</option></select>
                    <select><option>ახალი მიღებები</option></select>
                </div>

                <div className={styles.patientListContainer}>
                    {isLoadingPatients && <p className={styles.placeholderText}>პაციენტების სია იტვირთება...</p>}
                    {patientError && <p className={styles.errorMessage}>{patientError}</p>}
                    {!isLoadingPatients && !patientError && (
                        <table className={styles.patientTable}>
                            <thead>
                                <tr>
                                    <th>სახელი</th><th>MRN</th><th>ადგილი</th><th>დიაგნოზი</th><th>ექიმი</th><th>სტატუსი</th>
                                </tr>
                            </thead>
                            <tbody>
                                {patients.length > 0 ? (
                                    patients.map((patient) => (
                                        <tr key={patient.mrn}>
                                            <td>{patient.name}</td>
                                            <td>{patient.mrn}</td>
                                            <td>{patient.location_bed || '-'}</td>
                                            <td>{patient.primary_diagnosis_summary || '-'}</td>
                                            <td>{patient.attending_name || '-'}</td>
                                            {renderStatusIndicators(patient.status_indicators)}
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan="6" className={styles.placeholderText}>პაციენტები ვერ მოიძებნა.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    )}
                </div>
            </section>

            <section className={styles.section}>
                <h2>პაციენტის ძებნა</h2>
                <input type="text" placeholder="მოიძიე პაციენტი სახელი, MRN, დიაგნოზით..." className={styles.searchBar} />
            </section>

            <section className={styles.section}>
                <h2><span role="img" aria-label="განგაში" title="განგაში">🚨</span></h2>
                <div className={styles.alertsBox}>
                    <div className={styles.alertCritical}>🛑 კრიტიკული შედეგები</div>
                    <div className={styles.alertRoutine}>ℹ️ რუტინული განახლებები</div>
                </div>
            </section>

            <section className={styles.section}>
                <h2>ICU</h2>
                <div className={styles.widgetBox}>📈 მაღალი რისკის პაციენტების მონიტორინგი</div>
            </section>

            <nav className={styles.bottomNav}>
                <button>ლაბორატორია</button>
                <button>CATH ლაბი</button>
                <button>ქირურგია</button>
                <button>ინსტრუმენტული კვლევები</button>
                <button>მედიკამენტები</button>
                <button>კონსულტაციები</button>
            </nav>

        </div>
    );
}

export default DashboardPage;