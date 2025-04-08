# routes/patients.py (Complete version with Marshmallow)

from flask import Blueprint, request, jsonify
from models.models import Patient  # Import the Patient model
from extensions import db          # Import the db instance
from datetime import date
from sqlalchemy import or_         # Import 'or_' for searching
from schemas import patient_schema, patients_schema # Import Marshmallow schemas
from marshmallow import ValidationError          # Import validation error

# Define blueprint WITHOUT url_prefix here
patients_bp = Blueprint('patients', __name__)

# Route to GET a list of all patients OR POST to create a new patient
@patients_bp.route('/patients', methods=['GET', 'POST'])
def handle_patients():
    if request.method == 'POST':
        # --- Create a new patient using Marshmallow ---
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No input data provided"}), 400

        # Validate and deserialize input using the schema
        try:
            # .load() validates and creates a Patient instance because load_instance=True in schema Meta
            # Pass session for potential uniqueness checks or relationship loading if needed later
            new_patient = patient_schema.load(json_data, session=db.session)

            # Check MRN uniqueness (schema doesn't check DB unique constraints automatically on load)
            # It's safer to do this check before adding to session if MRN isn't the primary key
            if Patient.query.filter_by(mrn=new_patient.mrn).first():
                return jsonify({"error": f"Patient with MRN {new_patient.mrn} already exists."}), 409 # 409 Conflict

            db.session.add(new_patient)
            db.session.commit()

            # Serialize the created patient back to JSON for the response using schema.dump()
            return jsonify({
                "message": "Patient created successfully",
                "patient": patient_schema.dump(new_patient)
            }), 201 # 201 Created status code

        except ValidationError as err:
            # Return validation errors provided by Marshmallow
            return jsonify({"errors": err.messages}), 400 # 400 Bad Request status code
        except Exception as e:
            db.session.rollback()
            print(f"Database error creating patient: {e}") # Log error server-side
            return jsonify({"error": "Database error occurred"}), 500

    elif request.method == 'GET':
        # --- Get list of patients with Search and Pagination using Marshmallow ---
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            search_term = request.args.get('search', None, type=str)

            query = Patient.query

            if search_term:
                search_pattern = f"%{search_term}%"
                query = query.filter(
                    or_(
                        Patient.mrn.ilike(search_pattern),
                        Patient.first_name.ilike(search_pattern),
                        Patient.last_name.ilike(search_pattern)
                    )
                )

            query = query.order_by(Patient.last_name, Patient.first_name)

            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            patients_on_page = pagination.items

            # Serialize the list of patients using the schema (many=True)
            result = patients_schema.dump(patients_on_page)

            response = {
                "results": result, # Use the serialized result
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total_pages": pagination.pages,
                "total_items": pagination.total
            }
            return jsonify(response), 200

        except Exception as e:
            print(f"Database error listing patients: {e}")
            return jsonify({"error": "An error occurred listing patients"}), 500

# Route to GET a specific patient by MRN
@patients_bp.route('/patients/<string:mrn>', methods=['GET'])
def get_patient_by_mrn(mrn):
    """Get details for a single patient by their MRN."""
    try:
        patient = Patient.query.filter_by(mrn=mrn).first_or_404(
            description=f"Patient with MRN {mrn} not found."
        )

        # Serialize the patient object using the schema
        result = patient_schema.dump(patient)
        return jsonify(result), 200

    except Exception as e:
        print(f"Database error fetching patient {mrn}: {e}")
        return jsonify({"error": "An error occurred retrieving patient data"}), 500

# Route to UPDATE a specific patient by MRN
@patients_bp.route('/patients/<string:mrn>', methods=['PUT'])
def update_patient(mrn):
    """Update details for an existing patient by MRN using Marshmallow."""
    try:
        patient = Patient.query.filter_by(mrn=mrn).first_or_404(
            description=f"Patient with MRN {mrn} not found. Cannot update."
        )

        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No input data provided"}), 400

        # Validate and load updates onto the existing patient instance
        # Use partial=True to allow updating only some fields
        try:
            # Marshmallow will update the 'patient' object in-place because load_instance=True
            updated_patient = patient_schema.load(
                json_data, instance=patient, partial=True, session=db.session
            )
        except ValidationError as err:
            # Return validation errors
            return jsonify({"errors": err.messages}), 400

        # Check if MRN is being changed and if the new one conflicts (Optional advanced check)
        # Note: Handling unique constraint changes during update needs care
        if 'mrn' in json_data and json_data['mrn'] != mrn:
             if Patient.query.filter(Patient.mrn == json_data['mrn'], Patient.id != patient.id).first():
                 return jsonify({"error": f"Another patient with MRN {json_data['mrn']} already exists."}), 409

        db.session.commit()

        # Serialize the updated patient for the response
        return jsonify({
            "message": "Patient updated successfully",
            "patient": patient_schema.dump(updated_patient)
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Database error updating patient {mrn}: {e}")
        return jsonify({"error": "An error occurred updating patient data"}), 500

# Route to DELETE a specific patient by MRN
@patients_bp.route('/patients/<string:mrn>', methods=['DELETE'])
def delete_patient(mrn):
    """Delete a patient by MRN."""
    try:
        patient = Patient.query.filter_by(mrn=mrn).first_or_404(
            description=f"Patient with MRN {mrn} not found. Cannot delete."
        )

        db.session.delete(patient)
        db.session.commit()

        # Return success message (or use status 204 No Content)
        return jsonify({"message": f"Patient with MRN {mrn} deleted successfully."}), 200
        # return '', 204

    except Exception as e:
        db.session.rollback()
        print(f"Database error deleting patient {mrn}: {e}")
        return jsonify({"error": "An error occurred deleting patient data"}), 500