# routes/imaging.py (Corrected)

from flask import Blueprint, request, jsonify
from flask_login import login_required # Import login_required
from sqlalchemy import or_
from extensions import db
from models.models import Imaging, Patient # Import Patient for FK check
# Ensure ImagingSchema is defined correctly in schemas.py
from schemas import imaging_schema, imagings_schema
from decorators import roles_required
from constants import Roles
from marshmallow import ValidationError

imaging_bp = Blueprint('imaging', __name__)

@imaging_bp.route('/imaging', methods=['POST'])
@login_required
@roles_required(Roles.ADMIN, Roles.RADIOLOGIST, Roles.LAB_TECH) # Example: Roles allowed to add imaging results
def create_imaging():
    """Create a new imaging record."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        # Optional: Check if patient_id exists
        if 'patient_id' not in json_data or not Patient.query.get(json_data['patient_id']):
             return jsonify({"error": "Valid patient_id is required and must exist"}), 400

        new_imaging = imaging_schema.load(json_data, session=db.session)
        db.session.add(new_imaging)
        db.session.commit()

        return jsonify({
            "message": "Imaging record created successfully",
            "imaging": imaging_schema.dump(new_imaging)
        }), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error creating imaging record: {e}")
        # Standardized error response
        return jsonify({"error": "An internal server error occurred"}), 500

@imaging_bp.route('/imaging', methods=['GET'])
@login_required
@roles_required(Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT, Roles.NURSE, Roles.RADIOLOGIST) # Example: Roles allowed to view list
def get_imagings():
    """Get a list of imaging records (add pagination/filtering later)."""
    try:
        # Basic version - add pagination/filtering like in patients.py later
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        patient_id_filter = request.args.get('patient_id', None, type=int)
        # Add search later if needed

        query = Imaging.query
        if patient_id_filter:
            query = query.filter_by(patient)
    except Exception as e:
        print(f"Error fetching imaging records: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500