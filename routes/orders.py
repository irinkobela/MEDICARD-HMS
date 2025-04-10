# routes/orders.py (Corrected)

from flask import Blueprint, request, jsonify
from flask_login import login_required # Import login_required
from sqlalchemy import or_
from extensions import db
from models.models import Order, Patient, User # Import Patient/User for FK checks
# Ensure OrderSchema is defined correctly in schemas.py
from schemas import order_schema, orders_schema
from decorators import roles_required
from constants import Roles
from marshmallow import ValidationError

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['POST'])
@login_required
@roles_required(Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT) # Example: Roles allowed to create orders
def create_order():
    """Create a new order."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        # Optional: Check related records exist
        if 'patient_id' not in json_data or not Patient.query.get(json_data['patient_id']):
             return jsonify({"error": "Valid patient_id is required and must exist"}), 400
        if 'ordering_physician_id' in json_data and json_data['ordering_physician_id'] is not None:
             if not User.query.get(json_data['ordering_physician_id']):
                  return jsonify({"error": "ordering_physician_id does not refer to an existing user"}), 400
        # Add check for responsible_attending_id if needed

        new_order = order_schema.load(json_data, session=db.session)
        db.session.add(new_order)
        db.session.commit()

        return jsonify({
            "message": "Order created successfully",
            "order": order_schema.dump(new_order)
        }), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error creating order: {e}")
        # Standardized error response
        return jsonify({"error": "An internal server error occurred"}), 500

@orders_bp.route('/orders', methods=['GET'])
@login_required
@roles_required(Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT, Roles.NURSE, Roles.PHARMACIST) # Example: Roles allowed to view orders
def get_orders():
    """Get a list of orders (add pagination/filtering later)."""
    try:
        # Basic version - add pagination/filtering like in patients.py later
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        patient_id_filter = request.args.get('patient_id', None, type=int)
        # Add search later if needed

        query = Order.query
        if patient_id_filter:
            query = query.filter_by(patient_id=patient_id_filter)

        query = query.order_by(Order.created_at.desc()) # Order by creation time
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        orders_on_page = pagination.items

        result_list = orders_schema.dump(orders_on_page)

        response = {
            "results": result_list, "page": pagination.page, "per_page": pagination.per_page,
            "total_pages": pagination.pages, "total_items": pagination.total
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Error listing orders: {e}")
        # Standardized error response
        return jsonify({"error": "An internal server error occurred"}), 500

@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
@login_required
@roles_required(Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT, Roles.NURSE, Roles.PHARMACIST) # Example roles
def get_order_detail(order_id):
     """Get details for a single order."""
     try:
          order = Order.query.get_or_404(order_id)
          return order_schema.dump(order), 200
     except Exception as e:
          print(f"Error fetching order {order_id}: {e}")
          return jsonify({"error": "An internal server error occurred"}), 500

@orders_bp.route('/orders/<int:order_id>', methods=['PUT'])
@login_required
@roles_required(Roles.ADMIN, Roles.DOCTOR, Roles.RESIDENT) # Example: Roles allowed to update orders (e.g., change status)
def update_order(order_id):
    """Update an existing order."""
    try:
        order = Order.query.get_or_404(order_id)
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No input data provided"}), 400

        try:
            # Use schema load for validation and partial update
            updated_order = order_schema.load(
                 json_data, instance=order, partial=True, session=db.session
            )
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        # Add checks for FKs if they are updated

        db.session.commit()
        return jsonify({
            "message": "Order updated successfully",
            "order": order_schema.dump(updated_order)
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error updating order {order_id}: {e}")
        # Standardized error response
        return jsonify({"error": "An internal server error occurred"}), 500

@orders_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@login_required
@roles_required(Roles.ADMIN) # Example: Only Admin can delete orders? Or maybe ordering physician?
def delete_order(order_id):
    """Delete an order."""
    # Add logic here to check if the current_user is allowed to delete THIS specific order
    try:
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()
        return '', 204 # Use 204 No Content for successful DELETE
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting order {order_id}: {e}")
        # Standardized error response
        return jsonify({"error": "An internal server error occurred"}), 500