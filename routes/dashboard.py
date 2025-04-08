from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from run import db
from models.models import Patient, Result, Imaging, Consult, Order, User

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/api/dashboard/patient-list', methods=['GET'])
def patient_list():
    user_id = 1  # TODO: Replace this with real user auth when ready

    # Get query parameters
    unit = request.args.get('unit')
    service = request.args.get('service')
    acuity = request.args.get('acuity')
    status = request.args.get('status')
    sort_by = request.args.get('sortBy', 'name_asc')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))

    # Base query: join patient with attending user
    query = Patient.query.join(User)

    # Example scoping: filter by unit (optional)
    if unit:
        query = query.filter(Patient.location_bed.ilike(f"%{unit}%"))

    # Example: filter by status
    if status == 'new_admission_24':
        # Placeholder filter – adjust based on real schema
        query = query.filter(Patient.id > 0)

    # Sorting logic
    if sort_by == 'name_asc':
        query = query.order_by(Patient.name.asc())
    elif sort_by == 'location_asc':
        query = query.order_by(Patient.location_bed.asc())

    # Pagination
    total_items = query.count()
    total_pages = (total_items + limit - 1) // limit
    patients = query.offset((page - 1) * limit).limit(limit).all()

    # Status indicators logic
    def get_status_indicators(patient):
        time_window = datetime.utcnow() - timedelta(hours=48)

        return {
            "has_critical_lab": db.session.query(Result).filter_by(
                patient_id=patient.id, is_critical=True, acknowledged_at=None
            ).filter(Result.timestamp > time_window).first() is not None,

            "has_critical_imaging": db.session.query(Imaging).filter_by(
                patient_id=patient.id, is_critical=True, acknowledged_at=None
            ).filter(Imaging.timestamp > time_window).first() is not None,

            "has_unread_consult": db.session.query(Consult).filter_by(
                patient_id=patient.id, assigned_physician_id=user_id,
                status='Completed', read_at=None
            ).first() is not None,

            "has_pending_orders": db.session.query(Order).filter_by(
                patient_id=patient.id, status='PendingSignature',
                responsible_attending_id=user_id
            ).first() is not None
        }

    # Construct response
    results = []
    for p in patients:
        indicators = get_status_indicators(p)
        results.append({
            "mrn": p.mrn,
            "name": p.name,
            "location_bed": p.location_bed,
            "primary_diagnosis_summary": p.primary_diagnosis_summary,
            "attending_name": p.attending.username if p.attending else None,
            "code_status": p.code_status,
            "isolation_status": p.isolation_status,
            "status_indicators": indicators
        })

    return jsonify({
        "patients": results,
        "pagination": {
            "currentPage": page,
            "totalPages": total_pages,
            "totalItems": total_items
        }
    })
