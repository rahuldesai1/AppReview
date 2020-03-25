from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import Administrator

class AdminLoginForm(FlaskForm):
    group_name = StringField("Group Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Sign in")

class AdminRegistrationForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_group_name(self, group_name):
        user = Administrator.query.filter_by(group_name=group_name.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class ApplicationForm(FlaskForm):
    typeform_link = StringField("Link to TypeForm", validators=[DataRequired()])
    reviews_per_app = IntegerField("Reviews per Application", validators=[DataRequired()])
    semester = StringField("Semester", validators=[DataRequired()])
    submit = SubmitField("Create App")
    

