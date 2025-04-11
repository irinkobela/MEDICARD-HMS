# routes/auth.py (Fully Restored)

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.models import User  # Import User model
from extensions import db       # Import db instance
from schemas import user_schema # <<<=== RESTORE SCHEMA IMPORT
from marshmallow import ValidationError
from datetime import datetime   # For updating last_login

# Define blueprint
auth_bp = Blueprint('auth', __name__)

# --- Registration Route ---
@auth_bp.route('/register', methods=['POST'])
def register():
    print("--- Entering register() function ---")
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    # === RESTORE SCHEMA USAGE ===
    try:
        # Validate and load data using UserSchema
        new_user = user_schema.load(json_data, partial=("role", "id", "created_at", "last_login", "is_active"))
    except ValidationError as err:
        # Return validation errors
        return jsonify({"errors": err.messages}), 400
    # === END SCHEMA USAGE RESTORE ===

    # Check if username or email already exists (using loaded user object)
    # Note: These checks might be redundant if schema validation handles uniqueness,
    # but good to have explicit checks here too.
    if User.query.filter_by(username=new_user.username).first():
        return jsonify({"error": "Username already exists"}), 409
    if User.query.filter_by(email=new_user.email).first():
        return jsonify({"error": "Email already registered"}), 409

    # Get raw password from original JSON to hash it (schema has load_only=True)
    raw_password = json_data.get('password')
    if not raw_password: # Should be caught by schema's required=True
         return jsonify({"errors": {"password": ["Password is required."]}}), 400

    # Hash the password using the model's method
    new_user.set_password(raw_password)
    # Set role if not provided (or use schema default if configured)
    if not new_user.role:
        new_user.role = json_data.get('role', 'User') # Default role

    # Add user to database
    try:
        db.session.add(new_user)
        db.session.commit()
        # === RESTORE SCHEMA USAGE ===
        # Serialize the committed user object for the response (excluding password hash)
        return jsonify({
            "message": "User registered successfully",
            "user": user_schema.dump(new_user) # Use schema dump
            }), 201
        # === END SCHEMA USAGE RESTORE ===
    except Exception as e:
        db.session.rollback()
        print(f"Error during registration commit: {e}")
        return jsonify({"error": "Database error during registration"}), 500


# --- Login Route ---
@auth_bp.route('/login', methods=['POST'])
def login():
    print("--- Entering login() function ---")
    json_data = request.get_json()
    if not json_data: return jsonify({"error": "No input data provided"}), 400

    email = json_data.get('email')
    password = json_data.get('password')

    if not email or not password: return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        if not user.is_active:
            return jsonify({"error": "User account is inactive"}), 401

        login_user(user) # Log user in (Flask-Login sets session cookie)

        try: # Update last_login timestamp
            user.last_login = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating last_login for user {user.id}: {e}")

        # === RESTORE SCHEMA USAGE ===
        # Return success message and serialized user info
        return jsonify({
            "message": "Login successful",
            "user": user_schema.dump(user) # Use schema dump
            }), 200
        # === END SCHEMA USAGE RESTORE ===
    else:
        # Incorrect email or password
        return jsonify({"error": "Invalid email or password"}), 401


# --- Logout Route ---
@auth_bp.route('/logout', methods=['POST'])
@login_required # Requires user to be logged in
def logout():
    print("--- Entering logout() function ---")
    try:
        logout_user() # Clears user session
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        print(f"Error during logout: {e}")
        return jsonify({"error": "An error occurred during logout"}), 500


# --- Login Status Route ---
@auth_bp.route('/status', methods=['GET'])
def status():
    print("--- Entering status() function ---")
    if current_user.is_authenticated:
        # === RESTORE SCHEMA USAGE ===
        return jsonify({
            "is_logged_in": True,
            "user": user_schema.dump(current_user) # Use schema dump
            }), 200
        # === END SCHEMA USAGE RESTORE ===
    else:
        return jsonify({"is_logged_in": False}), 200