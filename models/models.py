# models/models.py

from extensions import db  # <--- CHANGE THIS IMPORT
from datetime import date, datetime # Add if using Date/DateTime below

class User(db.Model):
    __tablename__ = 'user' # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255)) # Increased length to 255
    role = db.Column(db.String(80), nullable=True) # Added role back from run.py example

    def __repr__(self):
        return f'<User {self.username}>'

class Patient(db.Model):
    __tablename__ = 'patients' # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String(64), unique=True, nullable=False, index=True) # Added index
    first_name = db.Column(db.String(100), nullable=False) # Patient's first name
    last_name = db.Column(db.String(100), nullable=False) # Patient's last name
    dob = db.Column(db.Date, nullable=False) # Date of Birth - make sure date is imported
    sex = db.Column(db.String(10)) # e.g., 'Male', 'Female', 'Other'
    location_bed = db.Column(db.String(64), nullable=True)
    primary_diagnosis_summary = db.Column(db.String(256), nullable=True)
    code_status = db.Column(db.String(64), nullable=True)
    isolation_status = db.Column(db.String(64), nullable=True)
    # Correct ForeignKey points to 'user.id' (tablename.columnname)
    attending_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # Define relationship to User
    attending = db.relationship('User', backref=db.backref('patients', lazy=True))

    def __repr__(self):
         # Simple representation including MRN
         return f'<Patient {self.mrn} - {self.name}>'

# Keep the existing User and Patient class definitions above this

# --- ADD THIS NEW CLASS ---
class Admission(db.Model):
    __tablename__ = 'admissions' # Explicit table name
    id = db.Column(db.Integer, primary_key=True) # Unique ID for each admission

    # Foreign Key linking to the Patient table
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)

    # Foreign Key linking to the User table (for admitting physician, nullable if not always known)
    admitting_physician_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    admission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Use DateTime for time too
    discharge_date = db.Column(db.DateTime, nullable=True) # Nullable until discharged
    reason_for_visit = db.Column(db.Text, nullable=True) # Can store longer text
    current_location = db.Column(db.String(100), nullable=True) # e.g., 'ER', 'ICU A', 'Room 402'

    # Define relationship back to Patient (One Patient can have Many Admissions)
    # 'patient' attribute will be added to Admission instances
    # 'admissions' attribute will be added to Patient instances
    patient = db.relationship('Patient', backref=db.backref('admissions', lazy='dynamic')) # Use lazy='dynamic' for query building

    # Define relationship back to User (One User can admit Many Patients) - Optional
    # 'admitting_physician' attribute will be added to Admission instances
    # 'admitted_patients' attribute will be added to User instances
    admitting_physician = db.relationship('User', backref=db.backref('admitted_patients', lazy='dynamic'))

    def __repr__(self):
        return f'<Admission {self.id} for Patient {self.patient_id} on {self.admission_date}>'
# --- END OF NEW CLASS ---


class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Add ForeignKey('patients.id') later
    patient_id = db.Column(db.Integer, nullable=False)
    is_critical = db.Column(db.Boolean, default=False)
    acknowledged_at = db.Column(db.DateTime, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Added default
    # TODO: Add fields for test name, value, units etc.


class Imaging(db.Model):
     __tablename__ = 'imaging'
     id = db.Column(db.Integer, primary_key=True)
     # TODO: Add ForeignKey('patients.id') later
     patient_id = db.Column(db.Integer, nullable=False)
     is_critical = db.Column(db.Boolean, default=False)
     acknowledged_at = db.Column(db.DateTime, nullable=True)
     timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
     # TODO: Add fields for modality, report text, link_to_pacs etc.


class Consult(db.Model):
    __tablename__ = 'consults'
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Add ForeignKey('patients.id') later
    patient_id = db.Column(db.Integer, nullable=False)
    # TODO: Add ForeignKey('user.id') later for requesting/assigned physicians
    assigned_physician_id = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(64)) # e.g., 'Pending', 'Completed'
    read_at = db.Column(db.DateTime, nullable=True)
    # TODO: Add fields for consult question, answer/note etc.


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Add ForeignKey('patients.id') later
    patient_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(64)) # e.g., 'Ordered', 'Completed', 'Cancelled'
    # TODO: Add ForeignKey('user.id') later
    responsible_attending_id = db.Column(db.Integer, nullable=True)
    # TODO: Add fields for order type, details, timestamp etc.