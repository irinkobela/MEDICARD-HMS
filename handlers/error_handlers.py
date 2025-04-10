from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from jwt.exceptions import PyJWTError # type: ignore
from marshmallow import ValidationError

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            "error": "Validation Error",
            "messages": error.messages
        }), 400

    @app.errorhandler(PyJWTError)
    def handle_jwt_error(error):
        return jsonify({
            "error": "Authentication Error",
            "message": str(error)
        }), 401

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        return jsonify({
            "error": "Database Integrity Error",
            "message": str(error.orig)
        }), 409

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        return jsonify({
            "error": "Database Error",
            "message": str(error)
        }), 500

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "error": "Not Found",
            "message": str(error)
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": str(error)
        }), 500

    return app
