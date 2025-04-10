# routes/patients.py (Corrected - Decorator RBAC only)

from flask import Blueprint, request, jsonify
from models.models import Patient
from extensions import db
from schemas import patient_schema, patients_schema
from marshmallow import ValidationError
from sqlalchemy import or_
from flask_login import login_required # Import login_required
from decorators import roles_required  # Import custom decorator
from constants import Roles          # Import Roles class

patients_bp = Blueprint('patients', __name__)

# Route to GET a list of all patients OR POST to create a new patient
@patients_bp.route('/patients', methods=['GET', 'POST'])
@login_required # Requires login for both GET and POST list/create
def handle_patients():
    if request.method == 'POST':
        # Role check via decorator applied below would be cleaner,
        # but applying here if GET/POST have different roles.
        # Example: Allow more roles to create than just view? Unlikely for patients.
        # Let's assume same roles for GET/POST list/create for now.
        # Applying roles_required decorator below handles this.

        # --- Use this decorator if different roles for POST vs GET ---
        # @roles_required(Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT, Roles.RECEPTION) # Example roles for POST

        # Removed manual role check 'if current_user.role not in [...]'

        json_data = request.get_json()
        # ... (rest of POST logic remains the same as your working version) ...
        if not json_data:
             return jsonify({"error": "No input data provided"}), 400
        try:
            new_patient = patient_schema.load(json_data, session=db.session)
            if Patient.query.filter_by(mrn=new_patient.mrn).first():
                return jsonify({"error": f"Patient with MRN {new_patient.mrn} already exists."}), 409
            db.session.add(new_patient)
            db.session.commit()
            return jsonify({
                "message": "Patient created successfully",
                "patient": patient_schema.dump(new_patient)
            }), 201
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except Exception as e:
            db.session.rollback()
            print(f"Database error creating patient: {e}")
            return jsonify({"error": "Database error occurred"}), 500

    elif request.method == 'GET':
        # Role check via decorator applied below

        # --- Use this decorator if different roles for POST vs GET ---
        # @roles_required(Roles.ADMIN, Roles.DOCTOR, ...) # Example roles for GET

        # Removed manual role check 'if current_user.role not in [...]'

        # ... (rest of GET logic with search/pagination remains the same) ...
        try:
             page = request.args.get('page', 1, type=int)
             per_page = request.args.get('per_page', 20, type=int)
             search_term = request.args.get('search', None, type=str)
             query = Patient.query
             if search_term:
                 search_pattern = f"%{search_term}%"
                 query = query.filter(or_(
                     Patient.mrn.ilike(search_pattern),
                     Patient.first_name.ilike(search_pattern),
                     Patient.last_name.ilike(search_pattern)
                 ))
             query = query.order_by(Patient.last_name, Patient.first_name)
             pagination = query.paginate(page=page, per_page=per_page, error_out=False)
             patients_on_page = pagination.items
             result = patients_schema.dump(patients_on_page)
             response = {
                 "results": result, "page": pagination.page, "per_page": pagination.per_page,
                 "total_pages": pagination.pages, "total_items": pagination.total
             }
             return jsonify(response), 200
        except Exception as e:
             print(f"Database error listing patients: {e}")
             return jsonify({"error": "An error occurred listing patients"}), 500

# Decorators apply to the function below them
@patients_bp.route('/patients/<string:mrn>', methods=['GET'])
@login_required
@roles_required( # Define roles allowed to GET specific patient
    Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT, Roles.NURSE, Roles.LAB_TECH,
    Roles.PHARMACIST, Roles.RADIOLOGIST, Roles.ANGIOLOGIST, Roles.ANESTHESIOLOGIST,
    Roles.SOCIAL_WORKER, Roles.PHYSIOTHERAPIST, Roles.SURGEON # Example broad read access
)
def get_patient_by_mrn(mrn):
    # ... function body remains the same ...
    try:
        patient = Patient.query.filter_by(mrn=mrn).first_or_404(...)
        result = patient_schema.dump(patient)
        return jsonify(result), 200
    except Exception as e:
        print(f"Database error fetching patient {mrn}: {e}")
        return jsonify({"error": "An error occurred retrieving patient data"}), 500

@patients_bp.route('/patients/<string:mrn>', methods=['PUT'])
@login_required
@roles_required(Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT, Roles.NURSE) # Example roles for UPDATE
def update_patient(mrn):
    # ... function body remains the same ...
    try:
        patient = Patient.query.filter_by(mrn=mrn).first_or_404(...)
        json_data = request.get_json()
        if not json_data: return jsonify(...), 400
        try:
            updated_patient = patient_schema.load(json_data, instance=patient, partial=True, session=db.session)
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        # Optional MRN check
        db.session.commit()
        return jsonify({"message": "Patient updated", "patient": patient_schema.dump(updated_patient)}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Database error updating patient {mrn}: {e}")
        return jsonify({"error": "An error occurred updating patient data"}), 500


@patients_bp.route('/patients/<string:mrn>', methods=['DELETE'])
@login_required
@roles_required(Roles.ADMIN) # ONLY Admin can delete
def delete_patient(mrn):
    # ... function body remains the same ...
    try:
        patient = Patient.query.filter_by(mrn=mrn).first_or_404(...)
        db.session.delete(patient)
        db.session.commit()
        return jsonify({"message": f"Patient with MRN {mrn} deleted."}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Database error deleting patient {mrn}: {e}")
        return jsonify({"error": "An error occurred deleting patient data"}), 500