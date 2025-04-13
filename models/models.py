# models/models.py


from extensions import db
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # Import UserMixin  
from constants import Roles 
from sqlalchemy import Boolean, Integer, String, DateTime, ForeignKey, Text


# === User Model ===
class User(db.Model, UserMixin):
    __tablename__ = 'user' # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # Increased length, ensure not nullable
    role = db.Column(db.String(80), nullable=True) # e.g., 'Admin', 'Doctor', 'Nurse' etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True) # Used by Flask-Login

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# === Patient Model ===
class Patient(db.Model):
    __tablename__ = 'patients' # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String(64), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(10)) # Consider Enum or fixed values
    location_bed = db.Column(db.String(64), nullable=True)
    primary_diagnosis_summary = db.Column(db.String(256), nullable=True)
    code_status = db.Column(db.String(64), nullable=True) # Consider Enum
    isolation_status = db.Column(db.String(64), nullable=True) # Consider Enum
    attending_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # FK to User table

    # Relationship to the attending physician (User)
    attending = db.relationship('User', backref=db.backref('assigned_patients', lazy='dynamic')) # Changed backref name for clarity

    # Relationship to Admissions (One-to-Many: One Patient -> Many Admissions)
    admissions = db.relationship('Admission', backref='patient', lazy='dynamic')

    def __repr__(self):
        return f'<Patient {self.mrn} - {self.first_name} {self.last_name}>'


# === Admission Model ===
class Admission(db.Model):
    # No explicit tablename, defaults to 'admission'
    id = db.Column(db.Integer, primary_key=True)
    # *** IMPORTANT: ForeignKey updated to match Patient's tablename 'patients' ***
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    admission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    discharge_date = db.Column(db.DateTime, nullable=True) # Nullable is correct

    # Relationships (One-to-Many: One Admission -> Many Results/Imagings/Consults/Orders)
    results = db.relationship('Result', backref='admission', lazy='dynamic')
    imagings = db.relationship('Imaging', backref='admission', lazy='dynamic')
    consults = db.relationship('Consult', backref='admission', lazy='dynamic')
    orders = db.relationship('Order', backref='admission', lazy='dynamic')

    def __repr__(self):
        return f'<Admission id={self.id} patient_id={self.patient_id} date={self.admission_date}>'


# === Result Model ===
class Result(db.Model):
    # No explicit tablename, defaults to 'result'
    id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.Integer, db.ForeignKey('admission.id'), nullable=False) # FK to Admission table
    test_name = db.Column(db.String(100), nullable=False)
    result_value = db.Column(db.String(100), nullable=False) # Consider Text for longer results
    result_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

 # --- Fields needed for Dashboard Indicators ---
    is_critical = db.Column(Boolean, default=False, nullable=False) # Flag for critical results
    acknowledged_at = db.Column(db.DateTime, nullable=True) # Timestamp when acknowledged
    acknowledged_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Optional: User who acknowledged

    # Relationship for acknowledged_by (optional)
    acknowledged_by = db.relationship('User', foreign_keys=[acknowledged_by_id])

    def __repr__(self):
        return f'<Result id={self.id} test={self.test_name}>'


# === Imaging Model ===
class Imaging(db.Model):
    # No explicit tablename, defaults to 'imaging'
    id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.Integer, db.ForeignKey('admission.id'), nullable=False) # FK to Admission table
    image_type = db.Column(db.String(100), nullable=False) # e.g., 'X-Ray', 'CT', 'MRI'
    image_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Storing large files directly in DB isn't always ideal. Consider storing a path (String) instead.
    image_file = db.Column(db.LargeBinary, nullable=True) # Making nullable if path is used later
    image_report = db.Column(db.Text, nullable=True) # Added field for radiologist's report

# --- Fields needed for Dashboard Indicators ---
    is_critical = db.Column(Boolean, default=False, nullable=False) # Flag for critical imaging results
    acknowledged_at = db.Column(db.DateTime, nullable=True) # Timestamp when acknowledged
    acknowledged_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Optional: User who acknowledged

    # Relationship for acknowledged_by (optional)
    acknowledged_by = db.relationship('User', foreign_keys=[acknowledged_by_id])

    def __repr__(self):
        return f'<Imaging id={self.id} type={self.image_type}>'


# === Consult Model ===
class Consult(db.Model):
    # No explicit tablename, defaults to 'consult'
    id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.Integer, db.ForeignKey('admission.id'), nullable=False) # FK to Admission table
    consultant_name = db.Column(db.String(100), nullable=False) # Or link to User table? consultant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    consult_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    consult_notes = db.Column(db.Text, nullable=False)

  # --- Fields needed for Dashboard Indicators ---
    # Consider replacing consultant_name with a foreign key
    assigned_physician_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True) # User assigned to read/action consult
    status = db.Column(db.String(50), default='Pending', nullable=False) # e.g., 'Pending', 'Completed', 'Cancelled'
    read_at = db.Column(db.DateTime, nullable=True) # Timestamp when assigned physician read it

    # Relationship to assigned physician
    assigned_physician = db.relationship('User', foreign_keys=[assigned_physician_id])
    def __repr__(self):
        return f'<Consult id={self.id} consultant={self.consultant_name}>'


# === Order Model ===
class Order(db.Model):
    # No explicit tablename, defaults to 'order'
    id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.Integer, db.ForeignKey('admission.id'), nullable=False) # FK to Admission table
    order_type = db.Column(db.String(50), nullable=False) # e.g., 'Medication', 'Lab', 'Imaging', 'Procedure'
    order_name = db.Column(db.String(100), nullable=False) # e.g., 'Complete Blood Count', 'Chest X-Ray', 'Aspirin 81mg'
    order_details = db.Column(db.Text, nullable=True) # e.g., dosage, frequency, reason
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending') # e.g., 'Pending', 'Completed', 'Cancelled'

  # --- Fields needed for Dashboard Indicators ---
    responsible_attending_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True) # User responsible for signing/actioning

    # Relationship to responsible attending
    responsible_attending = db.relationship('User', foreign_keys=[responsible_attending_id])


    def __repr__(self):
        return f'<Order id={self.id} type={self.order_type} name={self.order_name}>'
    
class VitalSign(db.Model):
    __tablename__ = 'vital_signs'
    id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.Integer, db.ForeignKey('admission.id'), nullable=False, index=True)
    recorded_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # User who recorded
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True) # Renamed from recorded_at

    # --- Core Vitals ---
    heart_rate = db.Column(db.Integer, nullable=True) # Renamed from pulse (bpm)
    systolic_bp = db.Column(db.Integer, nullable=True) # Renamed from blood_pressure_systolic (mmHg)
    diastolic_bp = db.Column(db.Integer, nullable=True) # Renamed from blood_pressure_diastolic (mmHg)
    mean_arterial_pressure = db.Column(db.Float, nullable=True) # MAP (mmHg)
    respiratory_rate = db.Column(db.Integer, nullable=True) # (breaths/min)
    temperature = db.Column(db.Float, nullable=True) # (e.g., Celsius)
    oxygen_saturation = db.Column(db.Float, nullable=True) # SpO2 (%)

    # --- Additional Measurements ---
    pain_score = db.Column(db.Integer, nullable=True) # e.g., 0-10 scale
    blood_glucose = db.Column(db.Float, nullable=True) # (e.g., mg/dL)
    height = db.Column(db.Float, nullable=True) # (e.g., cm) - Usually recorded once
    weight = db.Column(db.Float, nullable=True) # (e.g., kg)
    bmi = db.Column(db.Float, nullable=True) # Body Mass Index - Can be calculated

    # --- Neurological / Consciousness ---
    level_of_consciousness = db.Column(db.String(50), nullable=True) # e.g., AVPU, GCS Score (as string or link to GCS model?)
    intracranial_pressure = db.Column(db.Float, nullable=True) # ICP (mmHg)
    cerebral_perfusion_pressure = db.Column(db.Float, nullable=True) # CPP (mmHg)

    # --- Fluid Balance ---
    urine_output = db.Column(db.Float, nullable=True) # (e.g., mL over a period) - Need context for period?
    central_venous_pressure = db.Column(db.Float, nullable=True) # CVP (mmHg or cmH2O)

    # --- Advanced Hemodynamics / Respiratory ---
    pap_systolic = db.Column(db.Integer, nullable=True) # Pulmonary Artery Pressure Systolic (mmHg)
    pap_diastolic = db.Column(db.Integer, nullable=True) # Pulmonary Artery Pressure Diastolic (mmHg)
    cardiac_output = db.Column(db.Float, nullable=True) # (L/min)
    svo2 = db.Column(db.Float, nullable=True) # Mixed venous oxygen saturation (%)
    etco2 = db.Column(db.Float, nullable=True) # End-tidal CO2 (mmHg)
    pao2_fio2_ratio = db.Column(db.Float, nullable=True) # PaO2/FiO2 Ratio

    # --- General ---
    notes = db.Column(db.Text, nullable=True)

    # --- Relationships --- (Already defined in previous attempt, ensure consistent)
    # admission = db.relationship('Admission', backref=...) # Handled by backref in Admission likely
    recorded_by = db.relationship('User', backref=db.backref('recorded_vitals', lazy='dynamic'))

    def __repr__(self):
        return f'<VitalSign id={self.id} admission_id={self.admission_id} time={self.timestamp}>'

