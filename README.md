# MEDICARD-HMS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

MEDICARD-HMS is a modern, doctor-centered Hospital Management System (HMS) designed from the ground up to streamline clinical workflows, enhance patient safety, and improve the efficiency of healthcare professionals in demanding environments like Cardiology, ICU, Cath Lab, and Surgery.

This project aims to address common physician pain points by providing an intuitive, fast, and integrated platform for managing patient information, orders, documentation, and communication.

## Core Principles

* **Doctor-Centric Design:** Every feature prioritizes reducing clicks, saving time, presenting information clearly, and preventing errors for clinicians.
* **Modern UI/UX:** Clean, intuitive, minimalist interface with responsive design for various devices (desktops, tablets).
* **Workflow Optimization:** Seamless integration between modules to follow natural clinical processes, from admission to discharge.
* **Safety First:** Robust clinical decision support, clear presentation of critical information (allergies, code status), medication reconciliation tools, and comprehensive auditing.
* **Interoperability:** Designed with HL7/FHIR standards in mind for integration with LIS, RIS/PACS, scheduling, and other hospital systems.

## Key Features (Planned Scope)

1.  **Login & Personalized Doctor Dashboard:**
    * Secure authentication (LDAP/SSO, Local Credentials, MFA).
    * Role-based, customizable dashboard with action-oriented widgets (Patient Lists, Alerts, Schedules, Results Inbox, Consults Queue).
2.  **Intuitive Patient Chart:**
    * Modular, tabbed interface (Overview, Notes, Orders, Results, Meds, Flowsheets).
    * Persistent patient header with critical information (Allergies, Code Status).
    * Integrated views for Labs (trends), Imaging (PACS links), Echo/Cath reports.
3.  **Smart Clinical Documentation:**
    * Specialty-specific templates (SOAP, H&P, Procedure Notes).
    * Potential for AI-assist (autocomplete), voice-to-text integration.
    * Version tracking and auto-population features.
4.  **Efficient CPOE (Computerized Provider Order Entry):**
    * Unified ordering interface (Meds, Labs, Imaging, Consults).
    * Order Sets, Favorites, and robust Clinical Decision Support (Allergies, Interactions, Duplicates, Dosing).
5.  **Real-Time Results & Imaging Access:**
    * Live vitals feed (ICU), graphical trending for labs.
    * Direct links/integration with PACS viewers.
    * Structured display of key Echo/Cath findings.
6.  **Department-Specific Workflows:**
    * **ICU/ED:** Customizable flowsheets, vent integration, scoring systems, Code Blue interface, handover tools.
    * **Cath Lab/Surgery:** Pre-procedure checklists, intra-op documentation, post-procedure order sets, scheduling visibility.
7.  **Medication Management & Reconciliation:**
    * MAR viewing, smart ordering suggestions, interaction checking.
    * Dedicated workflows for Admission, Transfer, and Discharge reconciliation.
8.  **Streamlined Discharge Planning:**
    * Module for discharge summary creation with auto-population.
    * Medication reconciliation, patient instructions, follow-up planning.
    * Secure electronic transmission options.
9.  **Collaboration Tools:**
    * Structured handover tool (SBAR/IPASS).
    * Integrated task management.
    * Internal secure messaging (patient-context aware).
10. **Robust Security & Access Control:**
    * Granular Role-Based Access Control (RBAC).
    * Comprehensive audit trails.
    * Emergency ("break-the-glass") access protocols.
11. **Future Scope Considerations:**
    * AI-assisted decision support.
    * Predictive analytics dashboards.
    * Telehealth integrations.
    * Research data export modules.

## Technology Stack (Planned)

* **Backend:** Python (Flask)
* **Database:** PostgreSQL
* **Frontend:** React
* **API:** RESTful
* **Key Libraries/Concepts:** SQLAlchemy (ORM), Flask-Migrate (Database Migrations), Bcrypt (Hashing), PyJWT (Tokens), python-ldap (LDAP Auth), Celery (Async Tasks), Docker (Containerization).

## Project Status

* **Current Stage:** Planning
* **Next Milestones:**
    * Define core data models and relationships.
    * Set up initial project structure (backend/frontend).
    * Implement basic User model and Authentication endpoints.
    * Establish CI/CD pipeline basics.

## Getting Started

1.  **Prerequisites:**
    * Python 3.10+
    * `pip` and `venv` (included with Python)
    * Node.js (e.g., v18+) and `npm`
    * PostgreSQL (e.g., v14+) running locally or via Docker.
    * Git
2.  **Clone the repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)<your-github-username>/MEDICARD-HMS.git
    cd MEDICARD-HMS
    ```
3.  **Backend Setup:**
    *(Assumes backend code is in the root or a `/backend` directory - adjust as needed)*
    ```bash
    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`

    # Install Python dependencies (ensure requirements.txt exists)
    pip install -r requirements.txt
    ```
    *(You will need to create the `requirements.txt` file as you add dependencies like Flask, SQLAlchemy, etc.)*
4.  **Database Setup:**
    * Ensure your PostgreSQL server is running.
    * Create a database user and an empty database for the project.
        ```sql
        -- Example PSQL commands:
        CREATE DATABASE medicard_hms;
        CREATE USER medicard_user WITH PASSWORD 'your_secure_password';
        GRANT ALL PRIVILEGES ON DATABASE medicard_hms TO medicard_user;
        ```
    * Configure database connection details (see Configuration section).
    * Apply database migrations (using Flask-Migrate or similar):
        ```bash
        # (Run these after setting up Flask-Migrate)
        # flask db init  # Run once initially
        # flask db migrate -m "Initial migration."
        flask db upgrade
        ```
5.  **Configuration:**
    * Copy `.env.example` (you'll need to create this) to `.env`.
    * Update the `.env` file with your `DATABASE_URL`, `SECRET_KEY`, and other necessary settings. Example:
        ```ini
        # .env file contents
        SECRET_KEY=your_very_strong_random_secret_key
        DATABASE_URL=postgresql://medicard_user:your_secure_password@localhost:5432/medicard_hms
        # Add other config like LDAP details, API keys later
        FLASK_APP=run.py # Or your main app file
        FLASK_ENV=development
        ```
6.  **Running the Backend:**
    ```bash
    # Ensure venv is active
    flask run
    ```
    *The backend should now be running, typically on `http://127.0.0.1:5000`.*
7.  **Frontend Setup:**
    *(Assumes frontend code is in a `/frontend` directory - adjust as needed)*
    ```bash
    cd frontend # Or relevant directory
    npm install
    npm start # Or equivalent React start script
    ```
    *The frontend development server should now be running, often on `http://localhost:3000`.*

## Running Tests

*(Assumes pytest is used for backend testing)*

```bash
# Ensure venv is active and test dependencies are installed
pytest
Contributing
Contributions are very welcome! Please follow these guidelines:

Fork the repository.
Create a new branch for your feature or bugfix (git checkout -b feature/your-feature-name).
Follow standard PEP 8 guidelines for Python code. Use type hints where appropriate.
Write unit/integration tests for your changes.
Ensure all tests pass (pytest).
Commit your changes (git commit -m 'Add some feature').
Push to your branch (git push origin feature/your-feature-name).
Open a Pull Request against the main branch.
Clearly describe your changes in the Pull Request.
Please report bugs or suggest features using the GitHub Issues tracker for this repository.

License
This project is licensed under the MIT License.

Copyright (c) 2025 Irine Bakhutashvili

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.   

(See the LICENSE file for the full license text - you still need to create this file)

Contact
Project Contact: Irine Bakhutashvili - irinebakhutashvili@outlook.com
Issue Tracker: https://github.com/<irinkobela>/MEDICARD-HMS/issues 
This README provides initial guidance and will be updated as the project progresses.
Last Updated: April 8, 2025
