import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'My-default-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CONTEXT_ROUTE = os.environ.get('CONTEXT_ROUTE') or ''
    LOG_DIR = os.environ.get('LOG_DIR') or 'logs'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or None
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or None
