# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create extension instances WITHOUT the app object
db = SQLAlchemy()
migrate = Migrate()