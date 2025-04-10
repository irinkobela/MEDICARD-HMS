# run.py (Corrected Version)
import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from extensions import db, migrate, ma, login_manager, bcrypt # Correct single import
from sqlalchemy import text

# Load environment variables FIRST
load_dotenv()

# --- Import Models ---
# Import models AFTER extensions are defined but BEFORE they are initialized with app
# This makes them known to SQLAlchemy's metadata. Wrap in try-except for robustness.
try:
    # Try importing all models you expect to exist
    from models.models import User, Patient, Admission, Result, Imaging, Consult, Order
    models_imported = True
    print("Successfully imported models.")
except ImportError as e:
    print(f"WARNING: Could not import all models from models.models. Error: {e}")
    print("Ensure models/models.py exists and defines User, Patient, Admission, Result, Imaging, Consult, Order.")
    try:
         from models.models import User, Patient, Admission # Import essentials
         print("Imported essential models (User, Patient, Admission).")
         models_imported = True
    except ImportError as inner_e:
         print(f"ERROR: Could not import even essential models. Error: {inner_e}")
         print("Check models/models.py structure and its import of 'db' from 'extensions.py'.")
         models_imported = False
         # raise inner_e # Optional: Crash if core models fail

# Create Flask app instance
app = Flask(__name__)

# --- Application Configuration ---
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Error checking for config (Good practice!)
if not app.config['SECRET_KEY']:
    raise ValueError("SECRET_KEY is not set. Check .env file.")
if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise ValueError("DATABASE_URL is not set. Check .env file.")

# --- Initialize Extensions WITH the app instance ---
db.init_app(app)
migrate.init_app(app, db)
ma.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# --- Configure Flask-Login ---
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please log in to access this page.'

# --- User Loader for Flask-Login ---
@login_manager.user_loader
def load_user(user_id):
    """Flask-Login hook to load a User object given the user ID stored in the session."""
    # Ensure models were imported before trying to query
    if not models_imported:
         return None
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        print(f"Error loading user {user_id}: {e}")
        return None

# --- Define Basic Routes ---
@app.route('/')
def index():
    db_status = "Database Connection Error: Unknown"
    try:
        db.session.execute(text('SELECT 1'))
        db_status = "Database Connection OK"
    except Exception as e:
        db_status = f"Database Connection Error: {e}"
    return f"Hello from MEDICARD-HMS! {db_status}"

# --- Register Blueprints ---
# Use a single try-except block for all blueprint registrations
try:
    # Import your blueprints here (use correct path from 'routes')
    from routes.patients import patients_bp
    from routes.admissions import admissions_bp
    from routes.auth import auth_bp
    from routes.results import results_bp     # Correct import
    from routes.imaging import imaging_bp     # Correct import
    from routes.orders import orders_bp       # Correct import
    from routes.consults import consults_bp   # Correct import
    # from routes.dashboard import dashboard # Keep commented out unless ready

    # Register your blueprints here
    app.register_blueprint(patients_bp, url_prefix='/api')
    app.register_blueprint(admissions_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(results_bp, url_prefix='/api')   # Register with /api prefix
    app.register_blueprint(imaging_bp, url_prefix='/api')   # Register with /api prefix
    app.register_blueprint(orders_bp, url_prefix='/api')    # Register with /api prefix
    app.register_blueprint(consults_bp, url_prefix='/api')  # Register with /api prefix
    # app.register_blueprint(dashboard)

    # Update print statement to include all registered BPs
    print("Successfully registered blueprints: patients_bp, admissions_bp, auth_bp, results_bp, imaging_bp, orders_bp, consults_bp")

except ImportError as e:
    print(f"WARNING: Could not import or register one or more blueprints. Error: {e}")
    pass

# --- Main execution block ---
if __name__ == '__main__':
    app.run()