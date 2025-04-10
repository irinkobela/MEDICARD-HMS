# routes/consults.py (Corrected)

from flask import Blueprint, request, jsonify
from flask_login import login_required # Import login_required
from sqlalchemy import or_
from extensions import db
from models.models import Consult, Patient, User # Import Patient/User for FK checks
# Ensure ConsultSchema is defined correctly in schemas.py
from schemas import consult_schema, consults_schema
from decorators import roles_required
from constants import Roles
from marshmallow import ValidationError
from datetime import datetime # Import if using DateTime fields like read_at

consults_bp = Blueprint('consults', __name__)

@consults_bp.route('/consults', methods=['POST'])
@login_required
@roles_required(Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT) # Example: Roles allowed to request consults
def create_consult():
    """Create a new consult request."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        # Optional: Check related records exist
        if 'patient_id' not in json_data or not Patient.query.get(json_data['patient_id']):
             return jsonify({"error": "Valid patient_id is required and must exist"}), 400
        # Add checks for requesting_physician_id, assigned_physician_id if they are required/provided
        # json_data['requesting_physician_id'] = current_user.id # Example: Set requesting user automatically

        new_consult = consult_schema.load(json_data, session=db.session)
        db.session.add(new_consult)
        db.session.commit()

        return jsonify({
            "message": "Consult created successfully",
            "consult": consult_schema.dump(new_consult)
        }), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error creating consult: {e}")
        # Standardized error response
        return jsonify({"error": "An internal server error occurred"}), 500

@consults_bp.route('/consults', methods=['GET'])
@login_required
# Example: Broad access to view consult list, maybe filter later by assigned physician
@roles_required(Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT, Roles.NURSE)
def get_consults():
    """Get a list of consults (add pagination/filtering later)."""
    try:
        # Basic version - add pagination/filtering like in patients.py later
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        patient_id_filter = request.args.get('patient_id', None, type=int)
        status_filter = request.args.get('status', None, type=str)
        # Add filter by assigned_physician_id = current_user.id?

        query = Consult.query
        if patient_id_filter:
            query = query.filter_by(patient_id=patient_id_filter)
        if status_filter:
             query = query.filter_by(status=status_filter)

        query = query.order_by(Consult.created_at.desc()) # Order by creation time
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        consults_on_page = pagination.items

        result_list = consults_schema.dump(consults_on_page)

        response = {
            "results": result_list, "page": pagination.page, "per_page": pagination.per_page,
            "total_pages": pagination.pages, "total_items": pagination.total
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Error listing consults: {e}")
        # Standardized error response
        return jsonify({"error": "An internal server error occurred"}), 500

@consults_bp.route('/consults/<int:consult_id>', methods=['GET'])
@login_required
@roles_required(Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT, Roles.NURSE) # Example roles
def get_consult_detail(consult_id):
     """Get details for a single consult."""
     # Add logic here to check if current_user should be allowed to see THIS consult
     try:
          consult = Consult.query.get_or_404(consult_id)
          # Check permissions based on consult details if needed
          # if consult.assigned_physician_id != current_user.id and current_user.role not in [Roles.ADMIN]:
          #     abort(403)
          return consult_schema.dump(consult), 200
     except Exception as e:
          print(f"Error fetching consult {consult_id}: {e}")
          return jsonify({"error": "An internal server error occurred"}), 500

@consults_bp.route('/consults/<int:consult_id>', methods=['PUT'])
@login_required
# Example: Roles allowed to update consult status or add response
@roles_required(Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT)
def update_consult(consult_id):
    """Update an existing consult."""
    # Add logic here to check if the current_user is allowed to update THIS consult
    try:
        consult = Consult.query.get_or_404(consult_id)
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No input data provided"}), 400

        try:
            # Use schema load for validation and partial update
            updated_consult = consult_schema.load(
                 json_data, instance=consult, partial=True, session=db.session
            )
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        # Add checks for FKs if they are updated

        db.session.commit()
        return jsonify({
            "message": "Consult updated successfully",
            "consult": consult_schema.dump(updated_consult)
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error updating consult {consult_id}: {e}")
        # Standardized error response
        return jsonify({"error": "An internal server error occurred"}), 500

@consults_bp.route('/consults/<int:consult_id>', methods=['DELETE'])
@login_required
@roles_required(Roles.ADMIN) # Example: Only Admin can delete consults?
def delete_consult(consult_id):
    """Delete a consult."""
    try:
        consult = Consult.query.get_or_404(consult_id)
        # Add more authorization if needed
        db.session.delete(consult)
        db.session.commit()
        return '', 204 # Use 204 No Content for successful DELETE
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting consult {consult_id}: {e}")
        # Standardized error response
        return jsonify({"error": "An internal server error occurred"}), 500