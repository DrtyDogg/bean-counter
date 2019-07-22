import logging
import os
from flask import Flask
from flask_bootstrap import Bootstrap, WebCDN
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

# Local imports
from config import Config

# app.config.from_object(Config)
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.login_view = 'auth.login'
    app.extensions['bootstrap']['cdns']['jquery'] = WebCDN(
                '//cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/')

    if not app.debug and not app.testing:
        if not os.path.exists(app.config['LOG_DIR']):
            os.mkdir(app.config['LOG_DIR'])
        file_handler = RotatingFileHandler(
            app.config['LOG_DIR'] + '/bean-counter.log',
            maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('** Bean Counter Startup **')

    # Import the blueprints
    from app.main import bp as main_bp
    from app.errors import bp as errors_bp
    from app.auth import bp as auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp)

    # Import other files
    with app.app_context():
        from . import filters, models
    return app
