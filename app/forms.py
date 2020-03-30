from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange
from app.models import User, Group

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign in")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Username does not exist.')
        
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

class GroupJoinForm(FlaskForm):
    group_name = StringField("Group Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Join")

    def validate_group_name(self, group_name):
        group = Group.query.filter_by(group_name=group_name.data).first()
        if group is None:
            raise ValidationError('Group does not exist.')

class GroupRegistrationForm(FlaskForm):
    group_name = StringField("Group Name", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Group')

    def validate_group_name(self, group_name):
        user = Group.query.filter_by(group_name=group_name.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

class ApplicationForm(FlaskForm):
    typeform_id = StringField("Typeform Form ID", validators=[DataRequired()])
    num_apps = IntegerField("Number of Applications", validators=[DataRequired(), NumberRange(min=0, max=10000, message='Number of Applications is out of range')])
    reviews_per_app = IntegerField("Reviews per Application", validators=[DataRequired()])
    num_per_user = IntegerField("Applications per Reviewer", validators=[DataRequired()])
    semester = StringField("Semester", validators=[DataRequired()])
    submit = SubmitField("Create App")
    

