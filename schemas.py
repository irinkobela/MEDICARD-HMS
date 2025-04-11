# schemas.py (Should look like this)

from extensions import ma, db
from models.models import User, Patient # Only import existing models
from marshmallow import fields

class UserSchema(ma.SQLAlchemyAutoSchema):
    password = fields.String(required=True, load_only=True, validate=fields.validate.Length(min=8))
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_fk = True
        exclude = ("password_hash",)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        load_instance = True
        sqla_session = db.session
        include_fk = True
patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)

# --- Schemas for Admission, Result, Imaging, Consult, Order should still be commented out ---
# class AdmissionSchema(...):
# ... etc ...

# print("Schemas for User and Patient defined.") # Optional print