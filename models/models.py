# models/models.py

from extensions import db
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # Import UserMixin
# from constants import Roles # Roles constant not typically needed in the model itself

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # Should not be nullable
    role = db.Column(db.String(80), nullable=True) # e.g., 'Admin', 'Doctor', 'Nurse' etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True) # Used by Flask-Login

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        # Ensure hash exists before checking
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    # __repr__ needs correct indentation
    def __repr__(self):
        return f'<User {self.username}>'

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String(64), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(10))
    location_bed = db.Column(db.String(64), nullable=True)
    primary_diagnosis_summary = db.Column(db.String(256), nullable=True)
    code_status = db.Column(db.String(64), nullable=True)
    isolation_status = db.Column(db.String(64), nullable=True)
    attending_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    attending = db.relationship('User', backref=db.backref('patients', lazy=True))

    def __repr__(self):
        return f'<Patient {self.mrn} - {self.first_name} {self.last_name}>'

class Admission(db.Model):
    __tablename__ = 'admissions'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)
    admitting_physician_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    admission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    discharge_date = db.Column(db.DateTime, nullable=True)
    reason_for_visit = db.Column(db.Text, nullable=True)
    current_location = db.Column(db.String(100), nullable=True)

    patient = db.relationship('Patient', backref=db.backref('admissions', lazy='dynamic'))
    admitting_physician = db.relationship('User', backref=db.backref('admitted_patients', lazy='dynamic'))

    def __repr__(self):
        return f'<Admission {self.id} for Patient {self.patient_id} on {self.admission_date}>'

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False) # Added FK
    test_name = db.Column(db.String(100), nullable=False) # Example field
    value = db.Column(db.String(100)) # Example field
    units = db.Column(db.String(50)) # Example field
    is_critical = db.Column(db.Boolean, default=False)
    acknowledged_at = db.Column(db.DateTime, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    patient = db.relationship('Patient', backref=db.backref('results', lazy='dynamic')) # Added relationship


class Imaging(db.Model):
    __tablename__ = 'imaging'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False) # Added FK
    modality = db.Column(db.String(50)) # Example: CT, MRI, X-Ray
    body_part = db.Column(db.String(100)) # Example
    report = db.Column(db.Text) # Example
    is_critical = db.Column(db.Boolean, default=False)
    acknowledged_at = db.Column(db.DateTime, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    patient = db.relationship('Patient', backref=db.backref('imaging_studies', lazy='dynamic')) # Added relationship


class Consult(db.Model):
    __tablename__ = 'consults'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False) # Added FK
    requesting_physician_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Example
    assigned_physician_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Example
    consult_service = db.Column(db.String(100)) # Example: Cardiology, Neurology
    reason = db.Column(db.Text) # Example
    status = db.Column(db.String(64)) # e.g., Pending, Completed
    read_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True) # Example
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Example

    patient = db.relationship('Patient', backref=db.backref('consults', lazy='dynamic')) # Added relationship
    # Add relationships for requesting/assigned physicians if needed


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False) # Added FK
    order_type = db.Column(db.String(50)) # Example: Medication, Lab, Radiology
    order_details = db.Column(db.Text) # Example
    status = db.Column(db.String(64)) # e.g., Ordered, Completed, Cancelled
    ordering_physician_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Example
    responsible_attending_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Example - maybe just one physician ID needed?
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Example

    patient = db.relationship('Patient', backref=db.backref('orders', lazy='dynamic')) # Added relationship
    # Add relationships for physicians if needed