# routes/admissions.py

from flask import Blueprint, request, jsonify
from models.models import Admission, Patient, User # Import necessary models
from extensions import db                       # Import db instance
from schemas import admission_schema, admissions_schema # Import Admission schemas
from marshmallow import ValidationError
from sqlalchemy import or_ # Keep for potential search later

# Define blueprint
admissions_bp = Blueprint('admissions', __name__) # Different name from patients_bp

# --- Routes for /api/admissions ---

@admissions_bp.route('/admissions', methods=['POST'])
def add_admission():
    """Create a new admission record."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    # Validate and deserialize using schema
    try:
        # Ensure related patient exists (basic check)
        if 'patient_id' not in json_data or not Patient.query.get(json_data['patient_id']):
             return jsonify({"error": "Valid patient_id is required and must exist"}), 400
        # Ensure related user exists if provided (basic check)
        if 'admitting_physician_id' in json_data and json_data['admitting_physician_id'] is not None:
             if not User.query.get(json_data['admitting_physician_id']):
                  return jsonify({"error": "admitting_physician_id does not refer to an existing user"}), 400

        new_admission = admission_schema.load(json_data, session=db.session)
        db.session.add(new_admission)
        db.session.commit()

        return jsonify({
            "message": "Admission created successfully",
            "admission": admission_schema.dump(new_admission)
        }), 201

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Database error creating admission: {e}")
        return jsonify({"error": "Database error occurred"}), 500

@admissions_bp.route('/admissions', methods=['GET'])
def get_admissions():
    """Get a list of admissions with optional filtering, search, pagination."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        patient_id_filter = request.args.get('patient_id', None, type=int)
        # Add more filters or search terms later if needed (e.g., by reason, date range)

        query = Admission.query

        if patient_id_filter:
            query = query.filter_by(patient_id=patient_id_filter)

        # Add ordering, e.g., by admission date descending
        query = query.order_by(Admission.admission_date.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        admissions_on_page = pagination.items

        result = admissions_schema.dump(admissions_on_page)

        response = {
            "results": result,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_pages": pagination.pages,
            "total_items": pagination.total
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Database error listing admissions: {e}")
        return jsonify({"error": "An error occurred listing admissions"}), 500

# --- Routes for /api/admissions/<id> ---

@admissions_bp.route('/admissions/<int:admission_id>', methods=['GET'])
def get_admission_detail(admission_id):
    """Get details for a single admission by its ID."""
    try:
        admission = Admission.query.get_or_404(
            admission_id, description=f"Admission with ID {admission_id} not found."
        )
        result = admission_schema.dump(admission)
        return jsonify(result), 200
    except Exception as e:
        print(f"Database error fetching admission {admission_id}: {e}")
        return jsonify({"error": "An error occurred retrieving admission data"}), 500

@admissions_bp.route('/admissions/<int:admission_id>', methods=['PUT'])
def update_admission(admission_id):
    """Update details for an existing admission by ID."""
    try:
        admission = Admission.query.get_or_404(
            admission_id, description=f"Admission with ID {admission_id} not found. Cannot update."
        )
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No input data provided"}), 400

        try:
            # Validate and load updates onto the existing admission instance
            updated_admission = admission_schema.load(
                json_data, instance=admission, partial=True, session=db.session
            )
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        # Add specific checks if needed (e.g., prevent changing patient_id?)

        db.session.commit()

        return jsonify({
            "message": "Admission updated successfully",
            "admission": admission_schema.dump(updated_admission)
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Database error updating admission {admission_id}: {e}")
        return jsonify({"error": "An error occurred updating admission data"}), 500

@admissions_bp.route('/admissions/<int:admission_id>', methods=['DELETE'])
def delete_admission(admission_id):
    """Delete an admission by ID."""
    try:
        admission = Admission.query.get_or_404(
            admission_id, description=f"Admission with ID {admission_id} not found. Cannot delete."
        )
        db.session.delete(admission)
        db.session.commit()
        return jsonify({"message": f"Admission with ID {admission_id} deleted successfully."}), 200
        # return '', 204 # Alternative 204 response

    except Exception as e:
        db.session.rollback()
        print(f"Database error deleting admission {admission_id}: {e}")
        return jsonify({"error": "An error occurred deleting admission data"}), 500