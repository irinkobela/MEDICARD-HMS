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
