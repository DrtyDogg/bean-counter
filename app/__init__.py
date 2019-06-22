from flask import Flask
from flask_bootstrap import Bootstrap, WebCDN
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Local imports
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
mirgrate = Migrate(app, db)
bootstrap = Bootstrap(app)

#  Use JQuery 3 loaded via flask-bootstrap
app.extensions['bootstrap']['cdns']['jquery'] = WebCDN(
        '//cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/'
)

from app import models, filters, routes
