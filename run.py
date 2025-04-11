# run.py (Restored - Step 1)

import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from extensions import db, migrate, ma, login_manager, bcrypt # Restore imports
from sqlalchemy import text
from flask_cors import CORS # Keep the import 

# --- Load Environment Variables ---
load_dotenv()
print("Loaded environment variables from .env")

# --- Import Necessary Models ---
try:
    from models.models import User # Restore User import
    models_imported = True
    print("Successfully imported: User")
except ImportError as e:
    print(f"FATAL ERROR: Could not import essential models (e.g., User). Error: {e}")
    models_imported = False
    raise SystemExit(f"Failed to import core models: {e}")

# --- Create Flask App Instance ---
app = Flask(__name__)
print("Flask app instance created.")
# === CORRECTED/SPECIFIC CORS CONFIGURATION ===
# Replace the simple CORS(app) with this:
CORS(
    app,                           # Apply CORS to the Flask app
    resources={r"/api/*": {        # Apply CORS rules to routes starting with /api/
        "origins": "http://localhost:5173"  # Allow requests ONLY from your frontend origin
    }},
    supports_credentials=True      # IMPORTANT: Allow cookies (like Flask-Login session) to be sent/received
)
print("CORS enabled for origin http://localhost:5173 on /api/* routes, with credentials support.")
# === END CORS CORRECTION ===

# --- Application Configuration ---
# Restore configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not app.config['SECRET_KEY']:
    raise ValueError("SECRET_KEY is not set in the environment variables or .env file.")
if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise ValueError("DATABASE_URL is not set in the environment variables or .env file.")
print("App configuration loaded.")

# --- Initialize Flask Extensions ---
# Restore extension initializations
try:
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    print("Flask extensions initialized (db, migrate, ma, bcrypt, login_manager).")
except Exception as e:
    print(f"ERROR initializing extensions: {e}")
    raise e

# --- Configure Flask-Login ---
# Restore Flask-Login configuration
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please log in to access this page.'
print(f"Flask-Login configured. Login view set to: {login_manager.login_view}")

# --- User Loader Callback for Flask-Login ---
# Restore user loader
@login_manager.user_loader
def load_user(user_id):
    if not models_imported:
        print("User loader skipped: essential models failed to import.")
        return None
    try:
        user = User.query.get(int(user_id))
        # print(f"User loader attempt for ID {user_id}. Found: {user is not None}") # Debug
        return user
    except Exception as e:
        print(f"ERROR in user loader for ID {user_id}: {e}")
        return None

# --- Register Core Blueprints (like Authentication) ---
# Keep auth_bp registration separate and early
try:
    from routes.auth import auth_bp # This still imports the SIMPLIFIED auth.py
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    print("Successfully registered core blueprint: auth_bp at /api/auth")
except ImportError as e:
    print(f"FATAL ERROR: Could not import or register core blueprint 'auth_bp'. Error: {e}")
    raise SystemExit(f"Failed to register auth_bp: {e}")
except Exception as e:
    print(f"FATAL ERROR: Unexpected error registering 'auth_bp'. Error: {e}")
    raise SystemExit(f"Failed to register auth_bp: {e}")

# --- Register Optional/Other Blueprints ---
# Keep this section commented out for now
# try:
#     # ... (all optional blueprints commented out) ...
#     print("Checked for other optional blueprints.")
# except ImportError as e:
#     print(f"WARNING: Could not import/register optional blueprint(s). Error: {e}")
# except Exception as e:
#     print(f"WARNING: Unexpected error registering optional blueprint(s). Error: {e}")


# --- Basic Test Route ---
@app.route('/')
def index():
    db_status = "Unknown"
    try:
        db.session.execute(text('SELECT 1')) # Test DB connection now
        db_status = "Database Connection OK"
    except Exception as e:
        db_status = f"Database Connection Error: {e}"
    return f"<h1>MEDICARD-HMS Backend Running (Restored Run)</h1><p>{db_status}</p>"


# --- Main Execution ---
# Keep app.run() commented out - use 'flask run' command
# if __name__ == '__main__':
#     pass

print("run.py finished loading.")