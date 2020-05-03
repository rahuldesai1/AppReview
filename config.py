import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    # Form configs
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'temporary-key-should-be-changed'
    CSRF_ENABLED = True

    # Database configs
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "postgresql:///appreview_dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

