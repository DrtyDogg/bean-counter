from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Local imports
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
mirgrate = Migrate(app, db)

from app import routes, models, filters
