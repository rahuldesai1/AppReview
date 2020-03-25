import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    # Form configs
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'temporary-key'

    # Database configs
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

