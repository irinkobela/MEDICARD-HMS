# models/models.py

from extensions import db  # <--- CHANGE THIS IMPORT
from datetime import date, datetime # Add if using Date/DateTime below

class User(db.Model):
    __tablename__ = 'user' # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(80), nullable=True) # Added role back from run.py example

    def __repr__(self):
        return f'<User {self.username}>'

class Patient(db.Model):
    __tablename__ = 'patients' # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String(64), unique=True, nullable=False, index=True) # Added index
    name = db.Column(db.String(128), nullable=False) # Combined first/last for now, adjust if needed
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