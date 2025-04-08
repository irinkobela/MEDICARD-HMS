# routes/patients.py (Restored Logic with Correct Routing)

from flask import Blueprint, request, jsonify
from models.models import Patient  # Import the Patient model
from extensions import db          # Import the db instance
from datetime import date

# Define blueprint WITHOUT url_prefix here
patients_bp = Blueprint('patients', __name__)

# Route to GET a list of all patients OR POST to create a new patient
# Define route path EXPLICITLY as '/patients'
@patients_bp.route('/patients', methods=['GET', 'POST'])
def handle_patients():
    if request.method == 'POST':
        # --- Create a new patient ---
        data = request.get_json()

        required_fields = ['mrn', 'first_name', 'last_name', 'dob', 'sex']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields (mrn, first_name, last_name, dob, sex)"}), 400

        try:
            dob_date = date.fromisoformat(data['dob'])
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid date format for dob. Use YYYY-MM-DD."}), 400

        if Patient.query.filter_by(mrn=data['mrn']).first():
             return jsonify({"error": f"Patient with MRN {data['mrn']} already exists."}), 409

        new_patient = Patient(
            mrn=data['mrn'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            dob=dob_date,
            sex=data['sex'],
            # Add optional fields if needed:
            # name=data.get('name'), # If using combined name field
            location_bed=data.get('location_bed'),
            primary_diagnosis_summary=data.get('primary_diagnosis_summary'),
            code_status=data.get('code_status'),
            isolation_status=data.get('isolation_status'),
            attending_id=data.get('attending_id')
        )

        try:
            db.session.add(new_patient)
            db.session.commit()
            # Return the created patient's data
            return jsonify({
                "message": "Patient created successfully",
                "patient": {
                    "id": new_patient.id,
                    "mrn": new_patient.mrn,
                    # "name": new_patient.name, # If using combined name
                    "first_name": new_patient.first_name,
                    "last_name": new_patient.last_name,
                    "dob": new_patient.dob.isoformat(),
                    "sex": new_patient.sex,
                    "location_bed": new_patient.location_bed # Example optional field
                }
            }), 201
        except Exception as e:
            db.session.rollback()
            print(f"Database error: {e}") # Print error to console
            return jsonify({"error": "Database error occurred"}), 500

    elif request.method == 'GET':
        # --- Get list of all patients ---
        try:
            all_patients = Patient.query.order_by(Patient.last_name, Patient.first_name).all()
            patient_list = []
            for patient in all_patients:
                patient_list.append({
                    "id": patient.id,
                    "mrn": patient.mrn,
                    # "name": patient.name, # If using combined name
                    "first_name": patient.first_name,
                    "last_name": patient.last_name,
                    "dob": patient.dob.isoformat(),
                    "sex": patient.sex,
                    "location_bed": patient.location_bed # Example optional field
                })
            return jsonify(patient_list), 200
        except Exception as e:
            print(f"Database error: {e}") # Print error to console
            return jsonify({"error": "Database error occurred"}), 500


@patients_bp.route('/patients/<string:mrn>', methods=['GET'])
def get_patient_by_mrn(mrn):
    """Get details for a single patient by their MRN."""
    try:
        # Query the database for a patient with the matching MRN.
        # .first_or_404() is convenient: it gets the first result or automatically
        # triggers a 404 Not Found error if no patient matches.
        patient = Patient.query.filter_by(mrn=mrn).first_or_404(
            description=f"Patient with MRN {mrn} not found."
        )

        # If found, format the patient's data into a dictionary
        patient_data = {
            "id": patient.id,
            "mrn": patient.mrn,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "dob": patient.dob.isoformat(), # Format date as string
            "sex": patient.sex,
            "location_bed": patient.location_bed,
            "primary_diagnosis_summary": patient.primary_diagnosis_summary,
            "code_status": patient.code_status,
            "isolation_status": patient.isolation_status,
            "attending_id": patient.attending_id
            # Add other fields from your Patient model as needed
        }
        # Return the data as JSON with a 200 OK status
        return jsonify(patient_data), 200

    except Exception as e:
        # Log the error on the server for debugging
        print(f"Database error fetching patient {mrn}: {e}")
        # Return a generic error response to the client
        return jsonify({"error": "An error occurred retrieving patient data"}), 500
    
# --- ADD THIS NEW FUNCTION FOR UPDATING (PUT) ---
@patients_bp.route('/patients/<string:mrn>', methods=['PUT'])
def update_patient(mrn):
    """Update details for an existing patient by MRN."""
    try:
        # Find the existing patient, raise 404 if not found
        patient = Patient.query.filter_by(mrn=mrn).first_or_404(
            description=f"Patient with MRN {mrn} not found. Cannot update."
        )

        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Update fields using data.get() to allow partial updates
        patient.first_name = data.get('first_name', patient.first_name)
        patient.last_name = data.get('last_name', patient.last_name)
        patient.sex = data.get('sex', patient.sex)
        patient.location_bed = data.get('location_bed', patient.location_bed)
        patient.primary_diagnosis_summary = data.get('primary_diagnosis_summary', patient.primary_diagnosis_summary)
        patient.code_status = data.get('code_status', patient.code_status)
        patient.isolation_status = data.get('isolation_status', patient.isolation_status)
        patient.attending_id = data.get('attending_id', patient.attending_id) # Note: Add validation/permission checks later if needed

        # Handle date conversion if DOB is provided
        if 'dob' in data:
            try:
                dob_date = date.fromisoformat(data['dob'])
                patient.dob = dob_date
            except (ValueError, TypeError):
                return jsonify({"error": "Invalid date format for dob. Use YYYY-MM-DD."}), 400

        # Commit the session to save changes to the database
        db.session.commit()

        # Return the updated patient data
        patient_data = {
             "id": patient.id, "mrn": patient.mrn, "first_name": patient.first_name,
             "last_name": patient.last_name, "dob": patient.dob.isoformat(), "sex": patient.sex,
             "location_bed": patient.location_bed, "primary_diagnosis_summary": patient.primary_diagnosis_summary,
             "code_status": patient.code_status, "isolation_status": patient.isolation_status,
             "attending_id": patient.attending_id
        }
        return jsonify({"message": "Patient updated successfully", "patient": patient_data}), 200

    except Exception as e:
        db.session.rollback() # Roll back changes on error
        print(f"Database error updating patient {mrn}: {e}")
        return jsonify({"error": "An error occurred updating patient data"}), 500
# --- END OF UPDATE FUNCTION ---


# --- ADD THIS NEW FUNCTION FOR DELETING (DELETE) ---
@patients_bp.route('/patients/<string:mrn>', methods=['DELETE'])
def delete_patient(mrn):
    """Delete a patient by MRN."""
    try:
        # Find the existing patient, raise 404 if not found
        patient = Patient.query.filter_by(mrn=mrn).first_or_404(
            description=f"Patient with MRN {mrn} not found. Cannot delete."
        )

        # Delete the patient object from the session
        db.session.delete(patient)
        # Commit the transaction to remove from database
        db.session.commit()

        # Return a success message, status 200 OK or 204 No Content
        return jsonify({"message": f"Patient with MRN {mrn} deleted successfully."}), 200
        # Alternatively, for DELETE, often a 204 No Content response is used:
        # return '', 204

    except Exception as e:
        db.session.rollback() # Roll back changes on error
        print(f"Database error deleting patient {mrn}: {e}")
        return jsonify({"error": "An error occurred deleting patient data"}), 500
# --- END OF DELETE FUNCTION ---

    
# You can add more routes here later, like getting a specific patient
# @patients_bp.route('/patients/<string:mrn>', methods=['GET'])
# def get_patient_by_mrn(mrn):
#     # ... implementation ...