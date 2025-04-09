from flask import Blueprint, request, jsonify
from models.models import Patient # type: ignore
from extensions import db
from routes.auth import token_required
from schemas import patient_schema, patients_schema
from marshmallow import ValidationError
from sqlalchemy import or_

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/patients', methods=['GET', 'POST'])
@token_required
def handle_patients(current_user):
    if request.method == 'POST':
        if current_user.role not in ['doctor', 'admin']:
            return jsonify({"error": "Unauthorized"}), 403

        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No input data provided"}), 400

        try:
            new_patient = patient_schema.load(json_data, session=db.session)

            if Patient.query.filter_by(mrn=new_patient.mrn).first():
                return jsonify({"error": f"Patient with MRN {new_patient.mrn} already exists."}), 409

            db.session.add(new_patient)
            db.session.commit()

            return jsonify({
                "message": "Patient created successfully",
                "patient": patient_schema.dump(new_patient)
            }), 201

        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except Exception as e:
            db.session.rollback()
            print(f"Database error creating patient: {e}")
            return jsonify({"error": "Database error occurred"}), 500

    elif request.method == 'GET':
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            search_term = request.args.get('search', None, type=str)

            query = Patient.query

            if search_term:
                search_pattern = f"%{search_term}%"
                query = query.filter(
                    or_(
                        Patient.mrn.ilike(search_pattern),
                        Patient.first_name.ilike(search_pattern),
                        Patient.last_name.ilike(search_pattern)
                    )
                )

            query = query.order_by(Patient.last_name, Patient.first_name)

            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            patients_on_page = pagination.items

            result = patients_schema.dump(patients_on_page)

            response = {
                "results": result,
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total_pages": pagination.pages,
                "total_items": pagination.total
            }
            return jsonify(response), 200

        except Exception as e:
            print(f"Database error listing patients: {e}")
            return jsonify({"error": "An error occurred listing patients"}), 500

@patients_bp.route('/patients/<string:mrn>', methods=['GET'])
@token_required
def get_patient_by_mrn(current_user, mrn):
    try:
        patient = Patient.query.filter_by(mrn=mrn).first_or_404(
            description=f"Patient with MRN {mrn} not found."
        )

        result = patient_schema.dump(patient)
        return jsonify(result), 200

    except Exception as e:
        print(f"Database error fetching patient {mrn}: {e}")
        return jsonify({"error": "An error occurred retrieving patient data"}), 500

@patients_bp.route('/patients/<string:mrn>', methods=['PUT'])
@token_required
def update_patient(current_user, mrn):
    try:
        patient = Patient.query.filter_by(mrn=mrn).first_or_404(
            description=f"Patient with MRN {mrn} not found. Cannot update."
        )

        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No input data provided"}), 400

        try:
            updated_patient = patient_schema.load(
                json_data, instance=patient, partial=True, session=db.session
            )
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

        if 'mrn' in json_data and json_data['mrn'] != mrn:
             if Patient.query.filter(Patient.mrn == json_data['mrn'], Patient.id != patient.id).first():
                 return jsonify({"error": f"Another patient with MRN {json_data['mrn']} already exists."}), 409

        db.session.commit()

        return jsonify({
            "message": "Patient updated successfully",
            "patient": patient_schema.dump(updated_patient)
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Database error updating patient {mrn}: {e}")
        return jsonify({"error": "An error occurred updating patient data"}), 500

@patients_bp.route('/patients/<string:mrn>', methods=['DELETE'])
@token_required
def delete_patient(current_user, mrn):
    try:
        patient = Patient.query.filter_by(mrn=mrn).first_or_404(
            description=f"Patient with MRN {mrn} not found. Cannot delete."
        )

        db.session.delete(patient)
        db.session.commit()

        return jsonify({"message": f"Patient with MRN {mrn} deleted successfully."}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Database error deleting patient {mrn}: {e}")
        return jsonify({"error": "An error occurred deleting patient data"}), 500
