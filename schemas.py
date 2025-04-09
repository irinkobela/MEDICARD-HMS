from extensions import ma, db
from models.models import Patient, Admission, User, Result, Imaging, Consult, Order # type: ignore

class BaseSchema(ma.SQLAlchemyAutoSchema):
    """Base schema with common configuration"""
    class Meta:
        model = Patient
        load_instance = True
        sqla_session = db.session
        include_fk = True

class UserSchema(BaseSchema):
    class Meta:
        model = User
        exclude = ('password_hash',)

# Create User schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class PatientSchema(BaseSchema):
    class Meta:
        model = Patient

class AdmissionSchema(BaseSchema):
    class Meta:
        model = Admission
    
    # Optional: If you want to customize fields further or exclude some
    # exclude = ("some_internal_field",) # Fields to exclude from output
    # dump_only = ("id", "created_at") # Fields that are read-only (e.g., generated by DB)

# Create instances of the schema: one for single objects, one for lists
patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)

admission_schema = AdmissionSchema()
admissions_schema = AdmissionSchema(many=True)

class ResultSchema(BaseSchema):
    class Meta:
        model = Result

result_schema = ResultSchema()
results_schema = ResultSchema(many=True)

class ImagingSchema(BaseSchema):
    class Meta:
        model = Imaging

imaging_schema = ImagingSchema()
imagings_schema = ImagingSchema(many=True)

class ConsultSchema(BaseSchema):
    class Meta:
        model = Consult
        load_instance = True
        sqla_session = db.session
        include_fk = True

class OrderSchema(BaseSchema):
    class Meta:
        model = Order
        load_instance = True
        sqla_session = db.session
        include_fk = True

# --- Schema Instances (used in routes/views) ---

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)

admission_schema = AdmissionSchema()
admissions_schema = AdmissionSchema(many=True)

result_schema = ResultSchema()
results_schema = ResultSchema(many=True)

imaging_schema = ImagingSchema()
imagings_schema = ImagingSchema(many=True)

consult_schema = ConsultSchema()
consults_schema = ConsultSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
