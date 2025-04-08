# run.py (REVISED)
import os
from flask import Flask
from dotenv import load_dotenv
from extensions import db, migrate # Import from extensions file

# Load environment variables FIRST
load_dotenv()

# Import models AFTER extensions are defined but BEFORE they are initialized with app
# This makes them known to SQLAlchemy's metadata
from models.models import User, Patient, Result, Imaging, Consult, Order

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

# --- Define Routes ---
@app.route('/')
def index():
    try:
        db.session.execute(db.text('SELECT 1'))
        db_status = "Database Connection OK"
    except Exception as e:
        db_status = f"Database Connection Error: {e}"
    return f"Hello from MEDICARD-HMS! {db_status}"

# --- Register Blueprints (Make sure routes/dashboard.py exists and defines 'dashboard') ---
try:
    from routes.dashboard import dashboard
    app.register_blueprint(dashboard)
    # Add more blueprint registrations here later
except ImportError:
    # Handle case where blueprint doesn't exist yet gracefully if needed
    print("NOTE: Dashboard blueprint not found or not imported.")
    pass

# --- Main execution block ---
if __name__ == '__main__':
    # Debug mode is handled by FLASK_ENV=development in .env
    app.run()