# routes/dashboard.py

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user # Ensure these are imported
from datetime import datetime, timedelta
from sqlalchemy import select, distinct, or_ # Import 'select', 'distinct', 'or_'
from sqlalchemy.orm import joinedload # Import eager loading helpers

# Assuming 'db' is imported correctly, either directly or via extensions
from extensions import db
# Import all relevant models
from models.models import Patient, Result, Imaging, Consult, Order, User, Admission, VitalSign

# Define the dashboard blueprint
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/patient-list', methods=['GET'])
@login_required # Ensures user is logged in and current_user is available
def patient_list():
    """
    Retrieves a paginated and filterable list of patients for the dashboard,
    including status indicators based on recent activity.
    """
    try: # Wrap main logic in try/except for robustness
        user_id = current_user.id # Use the current user's ID for relevant indicators

        # --- Get Query Parameters ---
        unit = request.args.get('unit')
        service = request.args.get('service') # Placeholder filter
        acuity = request.args.get('acuity')   # Placeholder filter
        status = request.args.get('status')
        sort_by = request.args.get('sortBy', 'name_asc')
        page = request.args.get('page', 1, type=int)
        limit = min(request.args.get('limit', 20, type=int), 100) # Add max limit

        if page <= 0 or limit <= 0:
             return jsonify({"error": "Invalid 'page' or 'limit' parameter. Must be positive integers."}), 400

        # --- Base Patient Query ---
        # Start with Patient model and eager load the attending User relationship
        query = Patient.query.options(joinedload(Patient.attending))

        # --- Apply Filters ---
        if unit:
            query = query.filter(Patient.location_bed.ilike(f"%{unit}%"))
        # TODO: Implement filters for 'service' and 'acuity'

        if status == 'new_admission_24':
            twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
            subq = db.session.query(Admission.patient_id)\
                .filter(Admission.admission_date >= twenty_four_hours_ago)\
                .distinct()\
                .subquery()
            query = query.join(subq, Patient.id == subq.c.patient_id)

        # --- Apply Sorting ---
        if sort_by == 'name_asc':
            query = query.order_by(Patient.last_name.asc(), Patient.first_name.asc())
        elif sort_by == 'location_asc':
            query = query.order_by(Patient.location_bed.asc())
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
            "pending_orders": set(),
            "abnormal_vitals": set()
        }

        if patient_ids_on_page:
            time_window = datetime.utcnow() - timedelta(hours=48) # Configurable?

            # Query for patient IDs with unacknowledged critical labs
            # *** FIXED: Select Admission.patient_id and explicit join ***
            stmt_lab = select(distinct(Admission.patient_id)).select_from(Result)\
                .join(Admission, Result.admission_id == Admission.id)\
                .where(
                    Admission.patient_id.in_(patient_ids_on_page),
                    Result.is_critical == True,
                    Result.acknowledged_at.is_(None),
                    Result.result_date > time_window
                )
            crit_lab_query = db.session.execute(stmt_lab).scalars().all()
            indicator_patient_ids["critical_lab"] = set(crit_lab_query)

            # Query for patient IDs with unacknowledged critical imaging
            # *** FIXED: Select Admission.patient_id and explicit join ***
            stmt_img = select(distinct(Admission.patient_id)).select_from(Imaging)\
                .join(Admission, Imaging.admission_id == Admission.id)\
                .where(
                    Admission.patient_id.in_(patient_ids_on_page),
                    Imaging.is_critical == True,
                    Imaging.acknowledged_at.is_(None),
                    Imaging.image_date > time_window
                )
            crit_img_query = db.session.execute(stmt_img).scalars().all()
            indicator_patient_ids["critical_imaging"] = set(crit_img_query)

            # Query for patient IDs with unread completed consults for the current user
            # *** FIXED: Select Admission.patient_id and explicit join ***
            stmt_consult = select(distinct(Admission.patient_id)).select_from(Consult)\
                .join(Admission, Consult.admission_id == Admission.id)\
                .where(
                    Admission.patient_id.in_(patient_ids_on_page),
                    Consult.assigned_physician_id == user_id,
                    Consult.status == 'Completed',
                    Consult.read_at.is_(None)
                )
            unread_consult_query = db.session.execute(stmt_consult).scalars().all()
            indicator_patient_ids["unread_consult"] = set(unread_consult_query)

            # Query for patient IDs with pending orders for the current user
            # *** FIXED: Select Admission.patient_id and explicit join ***
            stmt_order = select(distinct(Admission.patient_id)).select_from(Order)\
                .join(Admission, Order.admission_id == Admission.id)\
                .where(
                    Admission.patient_id.in_(patient_ids_on_page),
                    Order.status == 'PendingSignature',
                    Order.responsible_attending_id == user_id
                )
            pending_order_query = db.session.execute(stmt_order).scalars().all()
            indicator_patient_ids["pending_orders"] = set(pending_order_query)

            # Query for patient IDs with recent abnormal vitals (example thresholds)
            # *** FIXED: Select Admission.patient_id and explicit join ***
            stmt_vitals = select(distinct(Admission.patient_id)).select_from(VitalSign)\
                .join(Admission, VitalSign.admission_id == Admission.id)\
                .where(
                    Admission.patient_id.in_(patient_ids_on_page),
                    VitalSign.timestamp > time_window,
                    or_(
                        VitalSign.heart_rate > 120, VitalSign.heart_rate < 50,
                        VitalSign.systolic_bp > 180, VitalSign.systolic_bp < 90,
                        VitalSign.oxygen_saturation < 92.0,
                        VitalSign.temperature > 38.5,
                        VitalSign.respiratory_rate > 24
                    )
                )
            abnormal_vitals_query = db.session.execute(stmt_vitals).scalars().all()
            indicator_patient_ids["abnormal_vitals"] = set(abnormal_vitals_query)

        # --- Construct Response ---
        results = []
        for p in patients_paginated:
            indicators = {
                "has_critical_lab": p.id in indicator_patient_ids["critical_lab"],
                "has_critical_imaging": p.id in indicator_patient_ids["critical_imaging"],
                "has_unread_consult": p.id in indicator_patient_ids["unread_consult"],
                "has_pending_orders": p.id in indicator_patient_ids["pending_orders"],
                "has_abnormal_vitals": p.id in indicator_patient_ids["abnormal_vitals"]
            }
            attending_username = p.attending.username if p.attending else None
            results.append({
                "id": p.id, "mrn": p.mrn,
                "name": f"{p.first_name} {p.last_name}",
                "dob": p.dob.isoformat() if p.dob else None,
                "sex": p.sex, "location_bed": p.location_bed,
                "primary_diagnosis_summary": p.primary_diagnosis_summary,
                "attending_name": attending_username,
                "code_status": p.code_status,
                "isolation_status": p.isolation_status,
                "status_indicators": indicators
            })

        # --- Return JSON Response ---
        return jsonify({
            "patients": results,
            "pagination": {
                "currentPage": page, "perPage": limit,
                "totalPages": total_pages, "totalItems": total_items
            }
        }), 200

    except Exception as e:
        print(f"Error in patient_list dashboard: {e}")
        return jsonify({"error": "An internal server error occurred retrieving patient list"}), 500
