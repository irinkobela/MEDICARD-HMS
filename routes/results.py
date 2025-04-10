# routes/results.py (Corrected)

from flask import Blueprint, request, jsonify
from flask_login import login_required # Import login_required
from sqlalchemy import or_
from extensions import db
from models.models import Result, Patient # Import Patient if checking patient_id exists
# Ensure ResultSchema is defined correctly in schemas.py
from schemas import result_schema, results_schema
from decorators import roles_required
from constants import Roles
from marshmallow import ValidationError

results_bp = Blueprint('results', __name__)

@results_bp.route('/results', methods=['POST'])
@login_required
@roles_required(Roles.ADMIN, Roles.LAB_TECH) # Example roles for creating results
def handle_results_post():
    """Create a new result."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        # Optional: Check if patient_id exists
        if 'patient_id' not in json_data or not Patient.query.get(json_data['patient_id']):
             return jsonify({"error": "Valid patient_id is required and must exist"}), 400

        new_result = result_schema.load(json_data, session=db.session)
        db.session.add(new_result)
        db.session.commit()

        return jsonify({
            "message": "Result created successfully",
            "result": result_schema.dump(new_result)
        }), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error creating result: {e}")
        # Standardized error response
        return jsonify({"error": "An internal server error occurred"}), 500


@results_bp.route('/results', methods=['GET'])
@login_required
@roles_required(Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT, Roles.NURSE, Roles.LAB_TECH) # Example roles for viewing results
def handle_results_get():
    """Get a list of results (add pagination/filtering later)."""
    try:
        # Basic version - add pagination/filtering like in patients.py later
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        patient_id_filter = request.args.get('patient_id', None, type=int)

        query = Result.query
        if patient_id_filter:
            query = query.filter_by(patient_id=patient_id_filter)

        query = query.order_by(Result.timestamp.desc()) # Order by time
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        results_on_page = pagination.items

        result_list = results_schema.dump(results_on_page)

        response = {
            "results": result_list, "page": pagination.page, "per_page": pagination.per_page,
            "total_pages": pagination.pages, "total_items": pagination.total
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Error listing results: {e}")
        # Standardized error response
        return jsonify({"error": "An internal server error occurred"}), 500


@results_bp.route('/results/<int:result_id>', methods=['GET'])
@login_required
@roles_required(Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT, Roles.NURSE, Roles.LAB_TECH) # Example roles
def get_result_detail(result_id):
     """Get details for a single result."""
     try:
          result = Result.query.get_or_404(result_id)
          return result_schema.dump(result), 200
     except Exception as e:
          print(f"Error fetching result {result_id}: {e}")
          return jsonify({"error": "An internal server error occurred"}), 500


@results_bp.route('/results/<int:result_id>', methods=['PUT'])
@login_required
@roles_required(Roles.ADMIN, Roles.LAB_TECH) # Example: Only Admin/LabTech can update?
def modify_result_put(result_id):
    """Update an existing result."""
    try:
        result = Result.query.get_or_404(result_id)
        json_data = request.get_json()
        if not json_data:
             return jsonify({"error": "No input data provided"}), 400

        try:
             # Use schema load for validation and partial update
             updated_result = result_schema.load(
                  json_data, instance=result, partial=True, session=db.session
             )
        except ValidationError as err:
             return jsonify({"errors": err.messages}), 400

        db.session.commit()
        return jsonify({
            "message": "Result updated successfully",
            "result": result_schema.dump(updated_result)
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error updating result {result_id}: {e}")
        # Standardized error response
        return jsonify({"error": "An internal server error occurred"}), 500


@results_bp.route('/results/<int:result_id>', methods=['DELETE'])
@login_required
@roles_required(Roles.ADMIN) # Example: Only Admin can delete results?
def modify_result_delete(result_id):
     """Delete a result."""
     try:
          result = Result.query.get_or_404(result_id)
          db.session.delete(result)
          db.session.commit()
          return '', 204 # Use 204 No Content for successful DELETE
     except Exception as e:
          db.session.rollback()
          print(f"Error deleting result {result_id}: {e}")
          # Standardized error response
          return jsonify({"error": "An internal server error occurred"}), 500