# run.py (Corrected Version)
import os
from flask import Flask, jsonify # Added jsonify for potential future API use
from dotenv import load_dotenv
from extensions import db, migrate, ma # Import from extensions file
from sqlalchemy import text # Import text for raw SQL execution

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
    # Attempt to import only essential models if others fail, or handle differently
    try:
         from models.models import User, Patient, Admission # Import essentials
         print("Imported essential models (User, Patient, Admission).")
         models_imported = True # Or set a flag indicating partial import
    except ImportError as inner_e:
         print(f"ERROR: Could not import even essential models. Error: {inner_e}")
         print("Check models/models.py structure and its import of 'db' from 'extensions.py'.")
         models_imported = False
         # Decide if the app should crash if core models fail
         # raise inner_e

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
# Do this AFTER configuration is set and BEFORE routes/blueprints are defined/registered
db.init_app(app)
migrate.init_app(app, db)

# --- Define Basic Routes ---
@app.route('/')
def index():
    db_status = "Database Connection Error: Unknown" # Default status
    try:
        # Use text() correctly for raw SQL execution within a session
        db.session.execute(text('SELECT 1'))
        db_status = "Database Connection OK"
    except Exception as e:
        # Capture specific error for better debugging
        db_status = f"Database Connection Error: {e}"
    return f"Hello from MEDICARD-HMS! {db_status}"

# --- Register Blueprints ---
# Use a single try-except block for all blueprint registrations
try:
    # Import your blueprints here
    from routes.patients import patients_bp
    from routes.admissions import admissions_bp # Import admissions blueprint
    # from routes.dashboard import dashboard # Keep commented out unless routes/dashboard.py is ready

    # Register your blueprints here
    app.register_blueprint(patients_bp, url_prefix='/api')
    app.register_blueprint(admissions_bp, url_prefix='/api')
    # app.register_blueprint(dashboard) # Register dashboard later if needed

    print("Successfully registered blueprints: patients_bp, admissions_bp") # Confirmation

except ImportError as e:
    print(f"WARNING: Could not import or register one or more blueprints. Error: {e}")
    # Allow app to run even if some blueprints are missing during development,
    # but routes defined in those blueprints won't work.
    pass

# --- Main execution block ---
if __name__ == '__main__':
    # Debug mode is handled by FLASK_ENV=development in .env
    # The port can also be set via environment variable PORT or defaults to 5000
    app.run()