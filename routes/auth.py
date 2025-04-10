# routes/auth.py (Corrected Full Version)

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.models import User   # Import User model
from extensions import db        # Import db instance
from schemas import user_schema  # Import User schema
from marshmallow import ValidationError
from datetime import datetime    # For updating last_login

# Define blueprint
auth_bp = Blueprint('auth', __name__)

# --- Registration Route ---
@auth_bp.route('/register', methods=['POST'])
def register():
    print("--- Entering register() function ---")
    """Register a new user."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    # Validate input and load using UserSchema
    try:
        # load_instance=True returns a User object if validation passes
        # Exclude fields not expected or needed during initial load for registration
        # 'password' is load_only in schema and required=True
        new_user = user_schema.load(json_data, partial=("role", "id", "created_at", "last_login", "is_active"))

    except ValidationError as err:
        # Return validation errors from Marshmallow
        return jsonify({"errors": err.messages}), 400

    # Check if username or email already exists using attributes from the loaded object
    if User.query.filter_by(username=new_user.username).first():
        return jsonify({"error": "Username already exists"}), 409
    if User.query.filter_by(email=new_user.email).first():
        return jsonify({"error": "Email already registered"}), 409

    # Get the raw password *from the original input JSON* for hashing
    raw_password = json_data.get('password')
    if not raw_password:
         # Should be caught by schema validation if password is required=True
         return jsonify({"errors": {"password": ["Password is required."]}}), 400

    # Call the password hashing method ON the loaded User instance
    new_user.set_password(raw_password)
    # Set role if it wasn't part of the schema load or set a default
    if not new_user.role:
        new_user.role = json_data.get('role', 'User') # Default role to 'User'

    # Add the fully prepared user object and commit to database
    try:
        db.session.add(new_user)
        db.session.commit()
        # Return success message and serialize the committed user object
        return jsonify({
            "message": "User registered successfully",
            "user": user_schema.dump(new_user) # Uses dump to exclude password_hash
            }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error during registration commit: {e}")
        return jsonify({"error": "Database error during registration"}), 500


# --- Login Route ---
@auth_bp.route('/login', methods=['POST'])
def login():
    print("--- Entering login() function ---")
    """Logs a user in."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    email = json_data.get('email')
    password = json_data.get('password')

    if not email or not password:
         return jsonify({"error": "Missing email or password"}), 400

    # Find user by email
    user = User.query.filter_by(email=email).first()

    # Check if user exists and password is correct using model method
    if user and user.check_password(password):
        # Check if user account is active (using the is_active field in your model)
        if not user.is_active:
             return jsonify({"error": "User account is inactive"}), 401 # Unauthorized

        # Log the user in using Flask-Login's function
        # The `remember=True` argument can be added if you want "remember me" functionality
        login_user(user) # Add remember=request.json.get('remember', False) if needed

        # Update last_login timestamp
        try:
            user.last_login = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating last_login for user {user.id}: {e}")
            # Log error but proceed with login success response

        # Return success message and user info
        return jsonify({
            "message": "Login successful",
            "user": user_schema.dump(user) # Use schema to serialize output
            }), 200
    else:
        # Incorrect email or password
        return jsonify({"error": "Invalid email or password"}), 401 # Unauthorized


# --- Logout Route ---
@auth_bp.route('/logout', methods=['POST']) # Use POST for logout as it changes state
@login_required # Make sure user is logged in to log out
def logout():
    print("--- Entering logout() function ---")
    """Logs the current user out."""
    try:
        logout_user() # Flask-Login function to clear session
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        print(f"Error during logout: {e}")
        return jsonify({"error": "An error occurred during logout"}), 500


# --- Login Status Route ---
@auth_bp.route('/status', methods=['GET'])
# No login_required here by default, as we want to check status for guests too
def status():
    print("--- Entering status() function ---")
    """Checks if a user is currently logged in and returns user info if they are."""
    if current_user.is_authenticated:
        # current_user is provided by Flask-Login
        return jsonify({
            "is_logged_in": True,
            "user": user_schema.dump(current_user)  # Use schema to serialize output
        }), 200
    else:
        return jsonify({"is_logged_in": False}), 200