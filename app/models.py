from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from app import login

# Each group has one admin account that manages all applications
class Administrator(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    applications = db.relationship('Application', backref='group', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Administrator(Group: {})>'.format(self.group_name) 

@login.user_loader
def load_user(id):
    return Administrator.query.get(int(id))

# A single semester's applications
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typeform_link = db.Column(db.String(256))
    reviews_per_app = db.Column(db.Integer)
    semester = db.Column(db.String(64), index=True, unique=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('administrator.id'))

    def __repr__(self):
        return '<Application {}>'.format(self.semester)
