from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from threading import Lock
from app import db
from app import login
from app import utils

"""
There are two types of users: Admins and Reviewers. 

Admins can create applications and generate the queue for reviewers
to read from. 
"""
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    applications_reviewed = db.Column(db.JSON, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_group(self):
        return self.group

    def get_application(self):
        return self.group.application

    def get_reviewed_applications(self):
        return utils.deserialize(self.applications_reviewed)

    def num_reviewed(self):
        if self.get_reviewed_applications() is None:
            return 0
        return len(self.get_reviewed_applications())
    
    def get_num_remaining(self):
        if self.get_application() is None:
            return -1
        return self.get_application().reviews_per_user - self.num_reviewed()

    def is_owner(self):
        return self.group.owner_id == self.id

    def __repr__(self):
        return '<User: {0} (Group: {1})>'.format(self.username, self.group.group_name) 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# A group of users
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    owner_id = db.Column(db.Integer)
    # define model relationship
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), unique=True)
    users = db.relationship('User', backref='group', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Group {}>'.format(self.group_name)

# A single semester's applications
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.relationship('Group', backref='application', uselist=False)
    semester = db.Column(db.String(64))
    num_apps = db.Column(db.Integer)
    reviews_per_app = db.Column(db.Integer)
    reviews_per_user = db.Column(db.Integer)

    # the list of applications is serialized and stored as a json list
    application_list = db.Column(db.JSON, nullable=True)
    typeform_id = db.Column(db.String(32))

    def is_active(self):
        return self.application_list is not None

    def get_application_queue(self):
        return utils.deserialize(self.application_list)

    def get_num_remaining(self):
        if self.application_list is None:
            return -1 
        return len(self.get_application_queue())

    def __repr__(self):
        return '<Application {}>'.format(self.semester)

