# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow 
from flask_login import LoginManager # type: ignore # <-- Import LoginManager
from flask_bcrypt import Bcrypt # type: ignore # <-- Import Bcrypt
# Create extension instances WITHOUT the app object
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
login_manager = LoginManager() # <-- Add LoginManager instance
bcrypt = Bcrypt()         # <-- Add Bcrypt instance