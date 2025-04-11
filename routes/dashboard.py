# dashboard.py

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user # Ensure these are imported
from datetime import datetime, timedelta
from sqlalchemy import select, distinct # Import 'select' and 'distinct'

# Assuming 'db' is imported correctly, either directly or via extensions
# from run import db # If db is directly in run.py (less common with app factory)
from extensions import db # More likely if using extensions.py pattern
from models.models import Patient, Result, Imaging, Consult, Order, User

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/api/dashboard/patient-list', methods=['GET'])
@login_required # Ensures user is logged in and current_user is available
def patient_list():
    try: # Wrap main logic in try/except for robustness
        user_id = current_user.id # Use the current user's ID

        # --- Get Query Parameters ---
        unit = request.args.get('unit')
        service = request.args.get('service')
        acuity = request.args.get('acuity')
        status = request.args.get('status')
        sort_by = request.args.get('sortBy', 'name_asc')
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)

        # --- Base Patient Query ---
        # Start with Patient model
        query = Patient.query
        # Example: Explicitly join with User for attending info if needed for filtering/sorting
        # query = query.outerjoin(User, Patient.attending_id == User.id)

        # --- Apply Filters (Placeholders - Implement based on your schema) ---
        if unit:
            query = query.filter(Patient.location_bed.ilike(f"%{unit}%"))
        # if service: query = query.filter(...) # Add filter based on service field
        # if acuity: query = query.filter(...) # Add filter based on acuity field
        if status == 'new_admission_24':
            from models.models import Admission # Import only if needed
            twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
            # Requires joining with Admission and filtering on admission_date
            query = query.join(Admission, Patient.id == Admission.patient_id)\
                         .filter(Admission.admission_date >= twenty_four_hours_ago)

        # --- Apply Sorting ---
        if sort_by == 'name_asc':
            query = query.order_by(Patient.last_name.asc(), Patient.first_name.asc())
        elif sort_by == 'location_asc':
            query = query.order_by(Patient.location_bed.asc())
        # Add other sorting options here
        else: # Default sort
             query = query.order_by(Patient.last_name.asc(), Patient.first_name.asc())

        # --- Pagination ---
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        patients_paginated = pagination.items
        total_items = pagination.total
        total_pages = pagination.pages

        # --- Optimization: Fetch Indicators Efficiently ---
        patient_ids_on_page = [p.id for p in patients_paginated]
        indicator_patient_ids = {
            "critical_lab": set(),
            "critical_imaging": set(),
            "unread_consult": set(),
            "pending_orders": set()
        }

        if patient_ids_on_page: # Only query indicators if there are patients
            time_window = datetime.utcnow() - timedelta(hours=48) # Configurable?

            # Query for patient IDs with critical labs
            crit_lab_query = db.session.execute(
                select(distinct(Result.patient_id)).where(
                    Result.patient_id.in_(patient_ids_on_page),
                    Result.is_critical == True,
                    Result.acknowledged_at.is_(None),
                    Result.timestamp > time_window
                )
            ).scalars().all()
            indicator_patient_ids["critical_lab"] = set(crit_lab_query)

            # Query for patient IDs with critical imaging
            crit_img_query = db.session.execute(
                select(distinct(Imaging.patient_id)).where(
                    Imaging.patient_id.in_(patient_ids_on_page),
                    Imaging.is_critical == True,
                    Imaging.acknowledged_at.is_(None),
                    Imaging.timestamp > time_window
                )
            ).scalars().all()
            indicator_patient_ids["critical_imaging"] = set(crit_img_query)

            # Query for patient IDs with unread consults for the current user
            unread_consult_query = db.session.execute(
                select(distinct(Consult.patient_id)).where(
                    Consult.patient_id.in_(patient_ids_on_page),
                    Consult.assigned_physician_id == user_id,
                    Consult.status == 'Completed', # Ensure this status exists
                    Consult.read_at.is_(None)
                )
            ).scalars().all()
            indicator_patient_ids["unread_consult"] = set(unread_consult_query)

            # Query for patient IDs with pending orders for the current user
            pending_order_query = db.session.execute(
                select(distinct(Order.patient_id)).where(
                    Order.patient_id.in_(patient_ids_on_page),
                    Order.status == 'PendingSignature', # Ensure this status exists
                    Order.responsible_attending_id == user_id
                )
            ).scalars().all()
            indicator_patient_ids["pending_orders"] = set(pending_order_query)

        # --- Construct Response ---
        results = []
        for p in patients_paginated:
            # Efficiently check indicators using the pre-fetched sets
            indicators = {
                "has_critical_lab": p.id in indicator_patient_ids["critical_lab"],
                "has_critical_imaging": p.id in indicator_patient_ids["critical_imaging"],
                "has_unread_consult": p.id in indicator_patient_ids["unread_consult"],
                "has_pending_orders": p.id in indicator_patient_ids["pending_orders"]
            }

            # Make sure the patient object has the attending relationship loaded
            # If not already loaded by the query (e.g., via joinedload), access might trigger queries.
            # Consider adding options(joinedload(Patient.attending)) to the main query if needed.
            attending_username = None
            if hasattr(p, 'attending') and p.attending:
                 attending_username = p.attending.username

            results.append({
                "mrn": p.mrn,
                "name": f"{p.first_name} {p.last_name}", # Assumes first/last name exist
                "location_bed": p.location_bed,
                "primary_diagnosis_summary": p.primary_diagnosis_summary,
                "attending_name": attending_username, # Use fetched username
                "code_status": p.code_status,
                "isolation_status": p.isolation_status,
                "status_indicators": indicators
            })

        # --- Return JSON Response ---
        return jsonify({
            "patients": results,
            "pagination": {
                "currentPage": page,
                "totalPages": total_pages,
                "totalItems": total_items
            }
        }), 200

    except Exception as e:
        # Log the error for debugging
        # current_app.logger.error(f"Error in patient_list dashboard: {e}", exc_info=True) # If using app logger
        print(f"Error in patient_list dashboard: {e}") # Basic print for now
        return jsonify({"error": "An internal server error occurred retrieving patient list"}), 500