from extensions import db
from datetime import datetime

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    admissions = db.relationship('Admission', backref='patient', lazy='dynamic')

class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    admission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    discharge_date = db.Column(db.DateTime)
    results = db.relationship('Result', backref='admission', lazy='dynamic')
    imagings = db.relationship('Imaging', backref='admission', lazy='dynamic')
    consults = db.relationship('Consult', backref='admission', lazy='dynamic')
    orders = db.relationship('Order', backref='admission', lazy='dynamic')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.Integer, db.ForeignKey('admission.id'), nullable=False)
    test_name = db.Column(db.String(100), nullable=False)
    result_value = db.Column(db.String(100), nullable=False)
    result_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Imaging(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.Integer, db.ForeignKey('admission.id'), nullable=False)
    image_type = db.Column(db.String(100), nullable=False)
    image_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.LargeBinary, nullable=False)

class Consult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.Integer, db.ForeignKey('admission.id'), nullable=False)
    consultant_name = db.Column(db.String(100), nullable=False)
    consult_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    consult_notes = db.Column(db.Text, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.Integer, db.ForeignKey('admission.id'), nullable=False)
    order_name = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    order_notes = db.Column(db.Text, nullable=False)
