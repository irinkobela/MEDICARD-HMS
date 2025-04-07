import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv # Import dotenv

# Load environment variables from .env file at the start
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# --- Application Configuration ---
# Load secret key from environment variable
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# Load database URI from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# Optional: Disable modification tracking overhead (recommended)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Initialize Extensions ---
# Initialize database extension (SQLAlchemy)
db = SQLAlchemy(app)
# Initialize migration extension (Migrate)
migrate = Migrate(app, db)

# --- Define Database Models (We'll add the first one in the next step) ---
# Example structure:
# class YourModelName(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     # other columns...

# --- Define Routes ---
@app.route('/')
def index():
    # Example: Try a basic database query to check connection
    try:
        # Execute a simple SQL query to test connection
        db.session.execute(db.text('SELECT 1'))
        db_status = "Database Connection OK"
    except Exception as e:
        db_status = f"Database Connection Error: {e}" # Show error if connection fails
    return f"Hello from MEDICARD-HMS! {db_status}" # Display status

# --- Main execution block ---
if __name__ == '__main__':
    # Flask run command will handle debug based on FLASK_ENV in .env
    app.run()