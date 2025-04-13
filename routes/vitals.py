# routes/vitals.py

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.models import VitalSign, Admission # Import Admission to check if it exists
from schemas import vital_sign_schema, vital_signs_schema
from marshmallow import ValidationError
from decorators import roles_required # Assuming you have this decorator
from constants import Roles        # Assuming you have Roles defined (e.g., Roles.NURSE, Roles.DOCTOR)
from datetime import datetime      # Import datetime for potential use

# Define the blueprint for vital signs routes
vitals_bp = Blueprint('vitals', __name__)

# --- Route to CREATE a new Vital Sign record for an Admission ---
@vitals_bp.route('/admissions/<int:admission_id>/vitals', methods=['POST'])
@login_required
@roles_required(Roles.NURSE, Roles.DOCTOR, Roles.RESIDENT) # Example: Define roles allowed to record vitals
def add_vital_sign(admission_id):
    """Adds a new vital sign record associated with a specific admission."""
    # Check if the admission exists
    admission = Admission.query.get(admission_id)
    if not admission:
        return jsonify({"error": f"Admission with id {admission_id} not found."}), 404

    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        # Load and validate data using the schema
        # Note: We set admission_id and recorded_by_id after loading
        new_vital = vital_sign_schema.load(
            json_data,
            session=db.session,
            partial=("admission_id", "recorded_by_id", "timestamp") # Exclude fields set manually/by default
        ) # Returns a VitalSign instance because of load_instance=True

        # Set fields not loaded from JSON directly onto the new_vital object
        new_vital.admission_id = admission_id
        new_vital.recorded_by_id = current_user.id

        # Handle optional timestamp override (apply to the loaded instance)
        if 'timestamp' in json_data:
             try:
                 # Attempt to parse timestamp if provided by client
                 new_vital.timestamp = datetime.fromisoformat(json_data['timestamp'])
             except (ValueError, TypeError):
                 # If parsing fails or not provided, rely on DB default (utcnow)
                 pass # No need to explicitly set if relying on DB default

        # Add the instance created by schema.load() to the session
        db.session.add(new_vital)
        db.session.commit()

        return jsonify({
            "message": "Vital sign recorded successfully",
            "vital": vital_sign_schema.dump(new_vital) # Dump the same instance
        }), 201 # 201 Created status

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400 # Validation errors
    except Exception as e:
        db.session.rollback()
        print(f"Error adding vital sign: {e}") # Log the error server-side
        return jsonify({"error": "An unexpected error occurred while adding vital sign."}), 500


# --- Route to GET all Vital Sign records for an Admission (with Pagination & Filtering) ---
@vitals_bp.route('/admissions/<int:admission_id>/vitals', methods=['GET'])
@login_required
@roles_required(Roles.NURSE, Roles.DOCTOR, Roles.RESIDENT, Roles.ADMIN) # Example: Broader read access
def get_vital_signs_for_admission(admission_id):
    """
    Retrieves vital sign records for a specific admission,
    with optional time filtering and pagination.
    Query Params:
        page (int): Page number for pagination (default: 1).
        per_page (int): Items per page (default: 20, max: 100).
        start_time (str): ISO 8601 format timestamp (e.g., YYYY-MM-DDTHH:MM:SS).
        end_time (str): ISO 8601 format timestamp (e.g., YYYY-MM-DDTHH:MM:SS).
    """
    # Check if the admission exists
    admission = Admission.query.get(admission_id)
    if not admission:
        return jsonify({"error": f"Admission with id {admission_id} not found."}), 404

    # --- Pagination Parameters ---
    try:
        page = request.args.get('page', 1, type=int)
        # Set a max limit for per_page for performance reasons
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        if page <= 0 or per_page <= 0:
            raise ValueError("Page and per_page must be positive integers.")
    except (TypeError, ValueError):
         return jsonify({"error": "Invalid 'page' or 'per_page' parameter. Must be positive integers."}), 400

    # --- Filtering Parameters ---
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')
    start_time_obj = None
    end_time_obj = None

    try:
        if start_time_str:
            start_time_obj = datetime.fromisoformat(start_time_str)
        if end_time_str:
            end_time_obj = datetime.fromisoformat(end_time_str)
    except ValueError:
        return jsonify({"error": "Invalid date format for 'start_time' or 'end_time'. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)."}), 400

    # --- Database Query ---
    try:
        query = VitalSign.query.filter(VitalSign.admission_id == admission_id)

        # Apply time filters if provided
        if start_time_obj:
            query = query.filter(VitalSign.timestamp >= start_time_obj)
        if end_time_obj:
            query = query.filter(VitalSign.timestamp <= end_time_obj)

        # Apply ordering (most recent first)
        query = query.order_by(VitalSign.timestamp.desc())

        # Apply pagination
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        vitals_on_page = pagination.items

        # Serialize results
        result = vital_signs_schema.dump(vitals_on_page)

        # Prepare response with pagination metadata
        response = {
            "vitals": result,
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total_pages": pagination.pages,
                "total_items": pagination.total,
                "has_prev": pagination.has_prev,
                "has_next": pagination.has_next,
                "prev_page_num": pagination.prev_num if pagination.has_prev else None,
                "next_page_num": pagination.next_num if pagination.has_next else None
            }
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Error retrieving vital signs: {e}") # Log the error server-side
        return jsonify({"error": "An unexpected error occurred while retrieving vital signs."}), 500
