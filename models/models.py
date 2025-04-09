# models/models.py

from extensions import db
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    patient_id = db.Column(db.Integer, nullable=False)
    is_critical = db.Column(db.Boolean, default=False)
    acknowledged_at = db.Column(db.DateTime, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Imaging(db.Model):
    __tablename__ = 'imaging'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    is_critical = db.Column(db.Boolean, default=False)
    acknowledged_at = db.Column(db.DateTime, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Consult(db.Model):
    __tablename__ = 'consults'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    assigned_physician_id = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(64))
    read_at = db.Column(db.DateTime, nullable=True)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(64))
    responsible_attending_id = db.Column(db.Integer, nullable=True)
