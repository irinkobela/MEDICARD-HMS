# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow 

# Create extension instances WITHOUT the app object
db = SQLAlchemy()
migrate = Migrate()
ma= Marshmallow()