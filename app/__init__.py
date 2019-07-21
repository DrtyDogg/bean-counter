from flask import Flask
from flask_bootstrap import Bootstrap, WebCDN
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Local imports
from config import Config

# app.config.from_object(Config)
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    app.extensions['bootstrap']['cdns']['jquery'] = WebCDN(
                '//cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/')

# Import the blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Import other files
    with app.app_context():
        from . import filters, models
    return app
