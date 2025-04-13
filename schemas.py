# schemas.py


from extensions import ma, db   # Import Marshmallow and DB instances
# Import ALL models used in this file
from models.models import User, Patient, Admission, Result, Imaging, Consult, Order, VitalSign
from marshmallow import fields  # Import fields for explicit field definition


# --- Define Schemas ---


class UserSchema(ma.SQLAlchemyAutoSchema):
    # Explicitly define password for input validation (load_only means it's not dumped)
    password = fields.String(required=True, load_only=True, validate=fields.validate.Length(min=8))  # Example: add min length validation


    class Meta:
        model = User            # Link to the User model
        load_instance = True    # Creates User instance during loading
        sqla_session = db.session  # Provide the session
        include_fk = True       # Include foreign keys if needed in output
        exclude = ("password_hash",)  # NEVER dump the password hash


# Create instances used in routes
user_schema = UserSchema()
users_schema = UserSchema(many=True)




class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patient         # Link to the Patient model
        load_instance = True
        sqla_session = db.session
        include_fk = True       # Includes attending_id


# Create instances used in routes
patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)



class AdmissionSchema(ma.SQLAlchemyAutoSchema):
    # Example: Format dates/times explicitly if needed
    # admission_date = ma.DateTime(format='%Y-%m-%dT%H:%M:%S')
    # discharge_date = ma.DateTime(format='%Y-%m-%dT%H:%M:%S', allow_none=True)


    class Meta:
        model = Admission       # Link to the Admission model
        load_instance = True
        sqla_session = db.session
        include_fk = True       # Includes patient_id, admitting_physician_id


# Create instances used in routes
admission_schema = AdmissionSchema()
admissions_schema = AdmissionSchema(many=True)




class ResultSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Result          # Link to the Result model
        load_instance = True
        sqla_session = db.session
        include_fk = True       # Includes patient_id


# Create instances used in routes
result_schema = ResultSchema()
results_schema = ResultSchema(many=True)




class ImagingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Imaging         # Link to the Imaging model
        load_instance = True
        sqla_session = db.session
        include_fk = True       # Includes patient_id


# Create instances used in routes
imaging_schema = ImagingSchema()
imagings_schema = ImagingSchema(many=True)




class ConsultSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Consult         # Link to the Consult model
        load_instance = True
        sqla_session = db.session
        include_fk = True       # Includes patient_id, assigned_physician_id


# Create instances used in routes
consult_schema = ConsultSchema()
consults_schema = ConsultSchema(many=True)




class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order           # Link to the Order model
        load_instance = True
        sqla_session = db.session
        include_fk = True       # Includes patient_id, responsible_attending_id


# Create instances used in routes
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


class VitalSignSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VitalSign          # Link to the VitalSign model
        load_instance = True       # Create model instances when loading data
        sqla_session = db.session  # Provide the database session
        include_fk = True          # Include foreign keys (like admission_id, recorded_by_id) in the output

# Create instances for single object and list serialization/deserialization
vital_sign_schema = VitalSignSchema()
vital_signs_schema = VitalSignSchema(many=True)


# --- NO DUPLICATE INSTANCES NEEDED AT THE END ---
